# Contributing to Doclet

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to Doclet. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Areas We Need Help](#areas-we-need-help)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. By participating, you are expected to uphold this commitment. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue list](https://github.com/Arman001/doclet/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

**Bug Report Template:**

```markdown
**Description**
A clear and concise description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Ubuntu 22.04, macOS 14.0, Windows 11]
- Python Version: [e.g., 3.11]
- Doclet Version/Commit: [e.g., main branch, commit abc123]
- RAM: [e.g., 8GB]

**Additional Context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

**Enhancement Template:**

```markdown
**Is your feature request related to a problem?**
A clear description of the problem. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Any other context, mockups, or examples.
```

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- **Good First Issue** - Issues labeled `good-first-issue` are great for newcomers
- **Help Wanted** - Issues labeled `help-wanted` need community support
- **Documentation** - Improvements to README, comments, or guides

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following our style guidelines
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Write clear commit messages**
6. **Submit a pull request**

**PR Guidelines:**

- Fill in the PR template completely
- Link relevant issues (e.g., "Fixes #123")
- Include screenshots for UI changes
- Keep PRs focused on a single feature/fix
- Update tests if adding new functionality

**PR Template:**

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## How Has This Been Tested?
Describe the tests you ran

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have tested this on my local machine

## Related Issues
Fixes #(issue number)
```

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/Arman001/doclet.git
   cd doclet
   ```

2. **Set up the development environment**
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   source venv/bin/activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install black flake8 pytest  # Optional: code formatting and testing
   ```

4. **Download the model**
   ```bash
   python setup_models.py
   ```

5. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable names

**Good:**
```python
def retrieve_relevant_documents(vector_store, query, threshold=1.3):
    """
    Retrieve documents based on similarity threshold.
    
    Args:
        vector_store: ChromaDB instance
        query: User's search query
        threshold: Maximum distance for relevance
    
    Returns:
        List of relevant documents
    """
    results = vector_store.similarity_search_with_score(query)
    return [doc for doc, score in results if score <= threshold]
```

**Bad:**
```python
def get_docs(vs,q,t=1.3):
    r=vs.search(q)
    return [d for d,s in r if s<=t]
```

### Code Formatting

We recommend using `black` for automatic code formatting:

```bash
black app.py ingest.py
```

### Documentation Style

- Use docstrings for all functions and classes
- Keep comments clear and concise
- Update README.md for user-facing changes
- Add inline comments for complex logic

### Commit Messages

Write clear, descriptive commit messages:

**Good:**
```
feat: Add PDF support to document ingestion
fix: Resolve hallucination with stricter relevance threshold
docs: Update README with troubleshooting section
refactor: Simplify prompt construction logic
```

**Bad:**
```
update stuff
fixed bug
changes
```

**Format:**
```
<type>: <subject>

<optional body>

<optional footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding tests
- `chore`: Maintenance tasks

## Project Structure

```
doclet/
├── app.py                 # Main Streamlit UI - handles user interactions
├── ingest.py             # Document processing - chunking and embedding
├── setup_models.py       # Model downloading and setup
├── setup_env.sh          # Environment configuration script
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── CONTRIBUTING.md      # This file
├── LICENSE              # MIT License
├── docs/                # User documents (gitignored)
├── models/              # LLM models (gitignored)
└── chroma_db/          # Vector database (gitignored)
```

### Key Files to Know

- **app.py**: Main application logic, UI, and chat handling
- **ingest.py**: Document loading, chunking, and embedding pipeline
- **requirements.txt**: All Python package dependencies

## Testing

Currently, Doclet uses manual testing. We welcome contributions to add automated tests!

**Manual Testing Checklist:**

- [ ] Upload different document types (MD, TXT, PDF)
- [ ] Test with various query types
- [ ] Verify relevance filtering works
- [ ] Check memory usage doesn't spike
- [ ] Test on different operating systems
- [ ] Verify chat history persists correctly
- [ ] Test document selection/deselection

**Future: Automated Testing**

We plan to add:
- Unit tests with pytest
- Integration tests for RAG pipeline
- Performance benchmarks
- CI/CD with GitHub Actions

## Areas We Need Help

### High Priority

1. **Hallucination Reduction**
   - Better prompt engineering
   - Improved post-processing
   - Context filtering techniques

2. **Performance Optimization**
   - Faster document chunking
   - Efficient embedding caching
   - Query optimization

3. **File Format Support**
   - DOCX support
   - HTML parsing
   - Code file highlighting
   - CSV/Excel data extraction

### Medium Priority

4. **User Experience**
   - Better error messages
   - Loading indicators
   - Mobile-responsive UI
   - Dark mode support

5. **Features**
   - Conversation history export
   - Multi-language support
   - Web URL ingestion
   - Document preview

### Documentation

6. **Guides and Tutorials**
   - Video walkthrough
   - Common use case examples
   - Performance tuning guide
   - Advanced configuration

## Questions?

Feel free to:
- Open an issue with the `question` label
- Reach out on LinkedIn: [Muhammad Saad](https://www.linkedin.com/in/muhammad-saad-ar/)
- Email: muhammad.saad.ar@gmail.com

## Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- GitHub contributors page
- Release notes for significant contributions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Doclet! 🚀

Every contribution, no matter how small, helps make this project better for everyone.