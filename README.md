# 🤖 Doclet: Private Technical Assistant

Doclet is a **local, privacy-focused RAG (Retrieval-Augmented Generation) assistant** that lets you chat with your documents using a small language model running entirely on your CPU. No cloud, no API keys, no data leaving your machine.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-latest-green.svg)

> **Demo Video**: [Watch on LinkedIn](https://www.linkedin.com/in/muhammad-saad-ar/) | [GitHub](https://github.com/Arman001/doclet)

---

## ✨ Features

- 🔒 **100% Local & Private** - All processing happens on your machine
- 📚 **Multi-Format Support** - Ingest Markdown, TXT, and PDF documents
- 🧠 **Smart Retrieval** - ChromaDB vector database with semantic search
- 💬 **Interactive Chat UI** - Clean Streamlit interface with chat history
- ⚡ **CPU-Optimized** - Runs on CPU using quantized Llama 3.2 1B model
- 🎯 **Selective Querying** - Choose which documents to include in your queries
- 📊 **Source Citations** - Every answer includes references with relevance scores
- 🔄 **Incremental Ingestion** - Only processes new or modified documents
- 💰 **Zero Cost** - No API subscriptions or cloud services needed

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- 4GB+ RAM recommended
- ~2GB disk space for model and dependencies
- No GPU required!
- **Note**: Close resource-intensive applications (video editors, screen recorders) for optimal performance

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Arman001/doclet.git
   cd doclet
   ```

2. **Set up the environment**
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Download the language model**
   ```bash
   python setup_models.py
   ```
   This downloads the Llama 3.2 1B model (~1.1GB)

### Running Doclet

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

### 1. Upload Documents

- Click **"Browse files"** in the sidebar
- Select your `.md`, `.txt`, or `.pdf` files
- Click **"Save & Process"** to ingest them

### 2. Load the Model

- Click **"Load Llama 3.2 (1B)"** in the main interface
- Wait for the model to initialize (~10-30 seconds)

### 3. Start Chatting

- Select which documents you want to query (or use all)
- Type your question in the chat input
- View answers with source citations and relevance scores

### 4. Manage Your Knowledge Base

- **Select Documents**: Choose specific documents from the sidebar
- **Reset Database**: Clear all indexed documents
- **Clear Chat**: Start a fresh conversation

## 🏗️ Project Structure

```
doclet/
├── app.py                  # Main Streamlit application
├── ingest.py              # Document ingestion pipeline
├── setup_models.py        # Model download script
├── setup_env.sh           # Environment setup script
├── requirements.txt       # Python dependencies
├── docs/                  # Your documents go here
├── models/                # Downloaded LLM models
├── chroma_db/            # Vector database storage
└── ingested_files.json   # Tracking file for incremental updates
```

## 🔧 Configuration

Key parameters can be adjusted in `app.py`:

```python
MODEL_PATH = "models/Llama-3.2-1B-Instruct-Q4_K_M.gguf"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RELEVANCE_THRESHOLD = 1.3      # Lower = stricter relevance
RETRIEVAL_K = 5                # Number of chunks to retrieve
MAX_CONTEXT_CHUNKS = 3         # Chunks sent to LLM
```

In `ingest.py`:

```python
chunk_size = 500              # Characters per chunk
chunk_overlap = 50            # Overlap between chunks
```

## 🧪 How It Works

1. **Document Ingestion**
   - Documents are loaded and split into chunks
   - Each chunk is embedded using `all-MiniLM-L6-v2`
   - Embeddings are stored in ChromaDB for fast retrieval

2. **Query Processing**
   - User question is embedded using the same model
   - Top K relevant chunks are retrieved via cosine similarity search
   - Chunks below relevance threshold are filtered out

3. **Answer Generation**
   - Top 3 most relevant chunks are formatted into a prompt
   - Llama 3.2 1B generates an answer based on the context
   - Response is cleaned to remove artifacts and hallucinations
   - Citations with relevance scores are displayed

## ⚡ Performance Expectations

### Typical Response Times (CPU-only):

| System Load | Query Complexity | Response Time |
|-------------|------------------|---------------|
| Light (just Doclet) | Simple | 10-15 seconds |
| Light | Complex | 15-20 seconds |
| Heavy (OBS, browsers, etc.) | Simple | 20-30 seconds |
| Heavy | Complex | 30-45 seconds |

**Factors affecting speed:**
- **CPU**: Modern CPUs (2020+) perform better
- **RAM availability**: 8GB+ recommended
- **System load**: Close unnecessary applications
- **Query complexity**: Longer questions take more time
- **Context size**: More retrieved documents = slower
- **Background processes**: Screen recording software (OBS) significantly impacts performance

**Performance Tips:**
1. Close OBS Studio and screen recorders before using Doclet
2. Close browser tabs you're not using
3. Reduce `MAX_CONTEXT_CHUNKS` to 2 for faster responses
4. Use shorter, more specific questions
5. Consider upgrading to the 3B model if you have 16GB+ RAM for better quality at similar speeds

## 🎯 Use Cases

- 📖 **Technical Documentation**: Query your project docs, API references, or manuals
- 🔬 **Research Notes**: Search through research papers and notes
- 🧠 **Knowledge Management**: Build a personal knowledge base
- 💻 **Code Documentation**: Understand large codebases through documentation
- 📚 **Learning**: Create study materials and quiz yourself
- 🏢 **Corporate Policies**: Query company handbooks and procedures privately

## ⚠️ Known Limitations

- **Hallucination**: Small models can occasionally generate plausible-sounding but incorrect information
- **Context Window**: Limited to ~2K tokens, which restricts complex multi-document reasoning
- **Language**: Optimized for English; other languages may have reduced accuracy
- **Complex Queries**: Best for straightforward factual questions rather than creative or abstract reasoning
- **Speed**: CPU inference takes 10-30 seconds per query depending on system load and complexity (faster without screen recording software running)
- **Resource Usage**: Performance degrades when running alongside resource-intensive applications (OBS, video editors, etc.)

## 🛠️ Troubleshooting

### Model doesn't load
- Ensure you ran `python setup_models.py`
- Check that `models/Llama-3.2-1B-Instruct-Q4_K_M.gguf` exists
- Verify you have enough RAM (4GB+ recommended)
- Try closing other applications to free memory

### Documents not being retrieved
- Check the relevance threshold (try increasing to 1.5-2.0 in `app.py`)
- Ensure documents are selected in the sidebar
- Verify documents were successfully ingested (check logs)
- Try shorter, more specific questions

### Slow performance
- Reduce `MAX_CONTEXT_CHUNKS` to 2
- Use smaller documents or split large ones
- Close other applications to free up RAM and CPU
- Consider using the GPU version if you have NVIDIA GPU

### Hallucinated answers
- Lower the `RELEVANCE_THRESHOLD` to be more strict
- Reduce `MAX_CONTEXT_CHUNKS` for more focused context
- Rephrase questions to be more specific
- Check if the information actually exists in your documents

## 🚀 Roadmap

- [ ] Add support for DOCX and HTML files
- [ ] Implement conversation memory across sessions
- [ ] Add GPU acceleration support
- [ ] Multi-language document support
- [ ] Export chat history
- [ ] Fine-tune model on specific domains
- [ ] Add web scraping for URL ingestion
- [ ] Implement advanced filtering and search

## 📦 Dependencies

- **LangChain**: RAG orchestration framework
- **llama-cpp-python**: CPU-optimized LLM inference
- **ChromaDB**: Vector database
- **Streamlit**: Web UI framework
- **sentence-transformers**: Embedding models
- **PyTorch**: ML framework (CPU-only)

See `requirements.txt` for the complete list.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Areas for Improvement
- Hallucination reduction techniques
- Better prompt engineering
- Performance optimizations
- Additional file format support
- UI/UX enhancements

### How to Contribute
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct.

## 🐛 Issues

Found a bug or have a feature request? Please [open an issue](https://github.com/Arman001/doclet/issues).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta AI** for Llama 3.2
- **LangChain** for the RAG framework
- **ChromaDB** for vector storage
- **Sentence Transformers** for embeddings
- **Streamlit** for the amazing UI framework

## 📧 Contact

- **GitHub Issues**: [Project Issues](https://github.com/Arman001/doclet/issues)
- **LinkedIn**: [Muhammad Saad](https://www.linkedin.com/in/muhammad-saad-ar/)
- **Email**: muhammad.saad.ar@gmail.com

## ⭐ Support

If you find this project useful, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with others who might benefit
- Contributing improvements
- Reporting bugs or suggesting features

---

**Built with ❤️ for privacy-conscious developers**

*Last updated: December 2025*
