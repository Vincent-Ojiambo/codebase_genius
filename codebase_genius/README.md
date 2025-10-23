# Codebase Genius - Agentic Code Documentation System

An AI-powered, multi-agent system that automatically generates high-quality documentation for software repositories. Built with Jac (JacLang) following the multi-agent architecture patterns.

## 🌟 Features

- **Multi-Agent Architecture**: Supervisor, Repo Mapper, Code Analyzer, and DocGenie agents
- **Comprehensive Analysis**: Functions, classes, dependencies, and relationships
- **Visual Documentation**: Mermaid diagrams for call graphs and inheritance
- **Multi-Language Support**: Python, Jac, JavaScript, Java, C/C++
- **REST API**: HTTP interface for programmatic access
- **Web Interface**: User-friendly frontend for easy interaction

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- JacLang (`pip install jaclang`)
- Git

### Installation & Setup
```bash
# Clone and setup
git clone <your-repo-url>
cd codebase_genius

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate environment
source venv/bin/activate

# Start the server
jac serve main.jac
```

### API Usage
```bash
# Generate documentation
curl -X POST http://localhost:8000/walker/api/generate_docs \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/example/repo"}'

# Check status
curl http://localhost:8000/walker/api/get_status

# List outputs
curl http://localhost:8000/walker/api/list_outputs
```

### Web Interface
```bash
# Serve web interface (separate terminal)
python3 -m http.server 3000
# Visit: http://localhost:3000
```

## 📁 Project Structure

```
codebase_genius/
├── main.jac              # Main Jac file with all agents
├── utils.py              # Python utilities (text processing, validation, diagrams)
├── config.json           # System configuration
├── requirements.txt      # Dependencies
├── setup.sh              # Setup script
├── deploy.sh             # Deployment script
├── index.html            # Web interface
├── test_*.py             # Test scripts
└── README.md             # This file

outputs/                  # Generated documentation
└── <repo_name>/
    └── README.md        # Generated docs
```

## 🧠 Architecture

### Agents
1. **Code Genius (Supervisor)**: Orchestrates workflow and manages state
2. **Repo Mapper**: Clones repos and builds file trees with README summaries
3. **Code Analyzer**: Parses code and constructs Code Context Graphs (CCG)
4. **DocGenie**: Generates comprehensive markdown documentation with diagrams

### Key Technologies
- **Jac Language**: Multi-agent framework with nodes, edges, and walkers
- **Python Integration**: PyModule for utility functions
- **Mermaid Diagrams**: Visual representation of code relationships
- **REST API**: HTTP interface for external integration

## 📊 Sample Output

Generated documentation includes:
- Project overview and structure
- Function and class analysis
- Dependency mapping
- Call graphs and inheritance diagrams
- API reference documentation

## 🧪 Testing

```bash
# Test with sample repository
python3 test_local.py

# Test full system
python3 test_system.py

# Test specific repository
curl -X POST http://localhost:8000/walker/api/generate_docs \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/sample/repo"}'
```

## ⚙️ Configuration

Edit `config.json` to customize:
- Processing limits and timeouts
- Supported file types
- Output formats
- Agent behavior settings

## 📖 Documentation

- **Implementation**: See `FINAL_README.md` for comprehensive technical details
- **Sample Repository**: Check `../sample_repo/` for testing example
- **API Reference**: Built into the generated documentation

## 🎯 Assignment Compliance

✅ **All Requirements Met:**
- Multi-agent Jac implementation
- Repository cloning and analysis
- Code Context Graph (CCG) construction
- Comprehensive documentation generation
- HTTP API interface
- Error handling and robustness
- Setup and run instructions
- Sample repository testing
- Visual diagram generation

## 🌐 Web Interface

The included HTML interface provides:
- Repository URL input
- Real-time status updates
- Documentation preview
- Example repository buttons
- Responsive design

## 🔧 Development

### Adding Language Support
1. Update `CodeAnalyzer` walker in `main.jac`
2. Add parsing logic for new language
3. Update file extension filters
4. Add test cases

### Extending Agents
1. Create new walker in `main.jac`
2. Register with supervisor agent
3. Add API endpoints in `api` walker
4. Update configuration

## 📄 License

MIT License - See repository for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

---

**Built with ❤️ using Jac Language and Multi-Agent Architecture**

For detailed implementation notes, see `FINAL_README.md`.
