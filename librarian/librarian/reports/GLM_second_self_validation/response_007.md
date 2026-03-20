# Validation Query 7: Deployment Architecture

**Query:**
"Why does the librarian-mcp use venv instead of Docker for deployment?"

---

## Response

The librarian-mcp uses **venv** (Python virtual environment) instead of Docker for deployment based on a deliberate design decision focused on simplicity, performance, and developer experience for its target use case.

### Key Reasons for Using venv

#### 1. Simplicity
- **No Docker complexity or learning curve** required [Source: librarian-mcp]
- Follows **standard Python deployment** approach that most developers are familiar with [Source: librarian-mcp]
- **Easier to understand and modify** for maintenance and troubleshooting [Source: librarian-mcp]

#### 2. Performance
- **Close coupling** between Chonkie (chunking) and ChromaDB (vector storage) is maintained without container boundaries [Source: librarian-mcp]
- Uses **stdio transport** (no HTTP overhead) for faster communication [Source: librarian-mcp]
- **Lower resource usage** compared to running a full containerized environment [Source: librarian-mcp]

#### 3. Developer Experience
- **Direct debugging access** to Python code without needing to debug inside containers [Source: librarian-mcp]
- **Easy log inspection** through standard file-based logging [Source: librarian-mcp]
- **Simpler CI/CD workflows** without container orchestration complexity [Source: librarian-mcp]

### Target Use Case Considerations

The deployment choice is specifically optimized for:
- **Single-user local deployment** - venv is superior for this scenario [Source: librarian-mcp]
- Personal development setups and individual researcher workflows [Source: librarian-mcp]

### When Docker Might Make Sense

The documentation acknowledges that **Docker would be more appropriate** for different scenarios [Source: librarian-mcp]:
- **Multi-user deployments** where isolation between users is important
- **Enterprise environments** with standardized container orchestration
- Production deployments requiring stricter reproducibility and scalability

### Summary

The librarian-mcp prioritizes **simplicity and developer experience** for its primary use case (single-user local deployment) by choosing venv over Docker. This decision trades the isolation and reproducibility benefits of containers for easier setup, better performance (no container overhead), and a more familiar development workflow for Python developers. The design recognizes that Docker becomes valuable when scaling to multi-user or enterprise contexts, but these are not the target use cases for the current implementation.
