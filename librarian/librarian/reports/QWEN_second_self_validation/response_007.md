# Query 7: Deployment Architecture

## Why Does the Librarian-MCP Use venv Instead of Docker?

### Overview

The librarian-mcp system uses Python virtual environments (venv) rather than Docker containers for its deployment architecture. This choice was made specifically for single-user local deployment scenarios, where venv provides superior simplicity, performance, and developer experience.

### Key Advantages of venv Over Docker

| Aspect | venv | Docker | Why It Matters |
|--------|------|--------|----------------|
| **Complexity** | Minimal | High | No Docker learning curve or container management overhead |
| **Performance** | Direct stdio transport | HTTP-based communication | Closes the Chonkie-ChromaDB coupling gap; faster data exchange |
| **Resource Usage** | Lower | Higher | More efficient for local development and single-user scenarios |
| **Debugging** | Direct Python access | Container boundaries | Easier debugging, log inspection, and code modification |
| **CI/CD** | Simpler workflows | More complex | Easier to understand and modify deployment pipelines |

### Why Docker is Less Suitable for This Use Case

1. **Single-User Focus**: The current deployment is optimized for single-user local use, where Docker's complexity is unnecessary overhead

2. **Tight Coupling Requirements**: The close coupling between Chonkie (document chunking) and ChromaDB (vector database) benefits from direct, low-latency communication within a shared venv

3. **Development Workflow**: venv allows developers to directly access, debug, and modify Python code without container context switching

4. **Resource Efficiency**: For local development, venv uses fewer resources and provides faster startup times

### When Docker Would Be Appropriate

Docker becomes more suitable for:
- **Multi-user deployments**: Multiple users sharing a library across different machines
- **Enterprise environments**: Standardized deployment across heterogeneous infrastructure
- **Production scalability**: When containerization is required for orchestration (Kubernetes, etc.)

### Deployment Setup

```bash
# Create and activate virtual environment
cd /home/peter/development/librarian-mcp
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Conclusion

For the primary use case of single-user local deployment, venv is the superior choice. Docker would only be necessary for multi-user or enterprise deployments where containerization provides the required isolation and orchestration capabilities.

[Source: librarian-mcp]