# Query 7: Deployment Architecture

**Status**: success
**Tokens Used**: 403
**Timestamp**: 2026-03-18T21:01:50.574917
**Tool Calls**: 1

---

I'll search the library for information about why the librarian-mcp uses venv instead of Docker for deployment.


Based on the library, here's why the librarian-mcp uses venv instead of Docker for deployment:

## Key Reasons for Choosing venv Over Docker

**[Source: /home/peter/development/librarian-mcp]**

### 1. **Simplicity**
- No Docker complexity or learning curve
- Standard Python deployment approach
- Easier to understand and modify
- More straightforward setup process

### 2. **Close Coupling Between Components**
- Direct integration between Chonkie (chunking library) and ChromaDB (vector database)
- No container boundaries - direct data access
- Tighter coupling enables better performance optimization

### 3. **Better Performance**
- Uses stdio transport for MCP communication (no HTTP overhead)
- Lower resource usage compared to container overhead
- Faster inter-process communication between Chonkie and ChromaDB

### 4. **Easier Development & Debugging**
- Direct debugging access to Python code
- Simpler log inspection
- Easier CI/CD integration for single-user deployments

### 5. **Lower Resource Usage**
- No container runtime overhead
- More efficient memory and CPU utilization

## When Docker Might Make Sense

The documentation notes that **"For multi-user or enterprise deployments, Docker may make sense"** - suggesting venv is optimized for the current use case (single-user/local deployment), while Docker could be better suited for more complex, distributed environments.

---

Would you like me to search for more details about the specific technical implementation of stdio transport, or explore how the Chonkie-ChromaDB coupling works in practice?