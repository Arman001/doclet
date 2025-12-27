import streamlit as st
import os
import shutil
import hashlib
from langchain_community.llms import LlamaCpp
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from ingest import ingest

# -----------------------------
# Configuration
# -----------------------------
MODEL_PATH = "models/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
DB_DIR = "chroma_db"
DOCS_DIR = "docs"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RELEVANCE_THRESHOLD = 1.3
RETRIEVAL_K = 5
MAX_CONTEXT_CHUNKS = 3  # Only use top 3 chunks for generation

st.set_page_config(
    page_title="Doclet AI",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# UI Styling
# -----------------------------
st.markdown("""
<style>
    .stChatMessage {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Cached Loaders
# -----------------------------
@st.cache_resource
def load_embeddings():
    """Load and cache embeddings once"""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

@st.cache_resource
def load_vector_store(_hash=None):
    """Load Chroma vector store with cache invalidation"""
    if not os.path.exists(DB_DIR):
        return None
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=load_embeddings()
    )

def get_ingestion_hash():
    """Get hash of ingested_files.json to detect changes"""
    hash_file = "ingested_files.json"
    if not os.path.exists(hash_file):
        return "empty"
    try:
        with open(hash_file, 'r') as f:
            return hashlib.md5(f.read().encode()).hexdigest()
    except:
        return "error"

@st.cache_resource
def load_llm():
    """Load Llama.cpp model"""
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model not found at {MODEL_PATH}")
        return None

    return LlamaCpp(
        model_path=MODEL_PATH,
        temperature=0.1,
        max_tokens=200,
        n_ctx=2048,
        n_gpu_layers=0,
        verbose=False,
        stop=["<|eot_id|>", "<|end_of_text|>", "\n\nQuestion:", "\n\nUser:", "\n\nHuman:"]
    )

# -----------------------------
# Utility Functions
# -----------------------------
def get_indexed_sources(vector_store):
    """Return unique document sources from vector DB"""
    if not vector_store:
        return []

    try:
        data = vector_store.get()
        if not data or not data.get("metadatas"):
            return []

        sources = {
            meta["source"]
            for meta in data["metadatas"]
            if meta and "source" in meta
        }
        return sorted(list(sources))
    except Exception as e:
        st.error(f"Error reading database: {e}")
        return []


def retrieve_relevant_documents(vector_store, query, selected_docs, k=5, threshold=1.3):
    """Retrieve documents and filter by relevance score"""
    if not vector_store or not selected_docs:
        return []
    
    try:
        results = vector_store.similarity_search_with_score(
            query,
            k=k,
            filter={"source": {"$in": selected_docs}}
        )
        
        relevant_docs = [
            (doc, score) for doc, score in results 
            if score <= threshold
        ]
        
        return relevant_docs
    except Exception as e:
        st.error(f"Error retrieving documents: {e}")
        return []


def create_prompt_with_context(question, docs, max_docs=3):
    """
    Create a well-formatted prompt with context for small models.
    This gives us full control over formatting.
    """
    # Build context from top N documents
    context_parts = []
    for i, doc in enumerate(docs[:max_docs], 1):
        # Clean and truncate document content
        content = doc.page_content.strip()
        # Limit each chunk to ~400 chars to prevent context overflow
        if len(content) > 400:
            content = content[:400] + "..."
        context_parts.append(f"[Source {i}]\n{content}")
    
    context = "\n\n".join(context_parts)
    
    # Build the complete prompt
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant. Answer questions using only the provided documents.

Documents:
{context}

Rules:
- Answer directly based on the documents
- Keep answers concise
- Don't repeat the question
- If information is not in documents, say "I don't have that information"
<|eot_id|><|start_header_id|>user<|end_header_id|>

{question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
    
    return prompt


def clean_response(response, original_question):
    """Clean up model response to remove artifacts"""
    import re
    
    answer = response.strip()
    
    # Remove question echo if it appears at start
    if original_question.lower() in answer.lower()[:150]:
        # Find where question ends and answer begins
        question_lower = original_question.lower()
        answer_lower = answer.lower()
        if question_lower in answer_lower:
            idx = answer_lower.find(question_lower)
            answer = answer[idx + len(original_question):].strip()
    
    # Remove common prefixes
    prefixes = [
        r'^(Answer|Response|Assistant|AI):\s*',
        r'^(According to|Based on) (the )?(documents?|context|information)[,:]?\s*',
    ]
    for pattern in prefixes:
        answer = re.sub(pattern, '', answer, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove duplicate lines
    lines = answer.split('\n')
    seen = set()
    unique_lines = []
    for line in lines:
        line_clean = line.strip().lower()
        if line_clean and line_clean not in seen and len(line_clean) > 3:
            seen.add(line_clean)
            unique_lines.append(line.strip())
    
    answer = '\n'.join(unique_lines).strip()
    
    # Fallback for very short or repeated answers
    if len(answer) < 15 or answer.lower() == original_question.lower():
        return None
    
    return answer


# -----------------------------
# Sidebar – Document Management
# -----------------------------
with st.sidebar:
    st.title("📂 Document Manager")

    uploaded_files = st.file_uploader(
        "Upload Documents (MD, TXT)",
        type=["md", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Save & Process"):
        os.makedirs(DOCS_DIR, exist_ok=True)

        for file in uploaded_files:
            with open(os.path.join(DOCS_DIR, file.name), "wb") as f:
                f.write(file.getbuffer())

        with st.spinner("Ingesting documents..."):
            status = ingest()
            st.success(status)
            st.cache_resource.clear()
            st.rerun()

    st.divider()
    st.subheader("📚 Indexed Knowledge Base")

    ingestion_hash = get_ingestion_hash()
    vector_store = load_vector_store(_hash=ingestion_hash)
    all_sources = get_indexed_sources(vector_store)

    if all_sources:
        if "selected_docs" not in st.session_state:
            st.session_state.selected_docs = all_sources

        selected = st.multiselect(
            "Select documents to chat with:",
            options=all_sources,
            format_func=os.path.basename,
            default=all_sources
        )

        st.session_state.selected_docs = selected
        st.caption(f"Indexed documents: {len(all_sources)}")

        if st.button("🗑️ Reset Knowledge Base", type="primary"):
            shutil.rmtree(DB_DIR, ignore_errors=True)
            st.cache_resource.clear()
            st.success("Knowledge base cleared.")
            st.rerun()
    else:
        st.info("Knowledge base is empty.")

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main Chat UI
# -----------------------------
st.title("🤖 Doclet: Private Technical Assistant")

if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False

if not st.session_state.model_loaded:
    st.info("Model is unloaded to save resources.")
    if st.button("Load Llama 3.2 (1B)"):
        with st.spinner("Loading model..."):
            if load_llm():
                st.session_state.model_loaded = True
                st.rerun()
else:
    st.caption("🟢 Model Loaded: Llama 3.2 1B")

    llm = load_llm()
    ingestion_hash = get_ingestion_hash()
    vector_store = load_vector_store(_hash=ingestion_hash)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander(f"📚 References ({len(msg['sources'])} chunks)"):
                    for idx, src in enumerate(msg["sources"], 1):
                        if "score" in src:
                            st.caption(f"**{idx}. {src['source']}** (Distance: {src['score']:.3f})")
                        else:
                            st.caption(f"**{idx}. {src['source']}**")
                        st.caption(f"{src['content'][:300]}...")
                        if idx < len(msg["sources"]):
                            st.divider()

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        if not vector_store:
            st.error("No vector database found. Please ingest documents.")
            st.stop()

        selected_docs = st.session_state.get("selected_docs", [])
        if not selected_docs:
            st.warning("No documents selected.")
            st.stop()

        # Retrieve relevant documents
        with st.spinner("Searching documents..."):
            relevant_docs_with_scores = retrieve_relevant_documents(
                vector_store, 
                prompt, 
                selected_docs,
                k=RETRIEVAL_K,
                threshold=RELEVANCE_THRESHOLD
            )

        if not relevant_docs_with_scores:
            with st.chat_message("assistant"):
                no_info_msg = "⚠️ I don't have relevant information about that in the provided documents."
                st.warning(no_info_msg)
                st.info("Your question might be outside the scope of the indexed knowledge base.")
                
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": no_info_msg,
                        "sources": []
                    }
                )
            st.stop()

        # Extract documents and scores
        relevant_docs = [doc for doc, score in relevant_docs_with_scores]
        doc_scores = {id(doc): score for doc, score in relevant_docs_with_scores}

        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                try:
                    # Create custom prompt with controlled context
                    full_prompt = create_prompt_with_context(
                        prompt, 
                        relevant_docs, 
                        max_docs=MAX_CONTEXT_CHUNKS
                    )
                    
                    # Direct LLM call (bypass LangChain chains for better control)
                    response = llm.invoke(full_prompt)
                    
                    # Clean the response
                    answer = clean_response(response, prompt)
                    
                    # Fallback if cleaning failed
                    if not answer:
                        answer = "I found relevant information but couldn't generate a clear answer. Please check the references below or try rephrasing your question."

                    # Prepare sources
                    sources = [
                        {
                            "source": os.path.basename(doc.metadata.get("source", "Unknown")),
                            "content": doc.page_content,
                            "score": doc_scores.get(id(doc), 0.0)
                        }
                        for doc in relevant_docs
                    ]

                    st.markdown(answer)
                    
                    # Display references
                    with st.expander(f"📚 References ({len(sources)} relevant chunks)"):
                        for idx, src in enumerate(sources, 1):
                            st.caption(f"**{idx}. {src['source']}** (Distance: {src['score']:.3f})")
                            st.caption(f"{src['content'][:300]}...")
                            if idx < len(sources):
                                st.divider()

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )
                    
                except Exception as e:
                    st.error(f"Error generating answer: {e}")
                    import traceback
                    st.code(traceback.format_exc())
                    st.stop()