# Response 7: Why the Librarian-MCP Uses venv Instead of Docker

## Summary

The librarian-mcp project chose to use Python virtual environments (venv) instead of Docker containers for deployment. This decision was made after careful consideration of the project's specific requirements and deployment goals.

## Key Reasons for Using venv

Based on the architecture documentation, the following factors influenced this decision:

### 1. Simplicity
- **No Docker complexity**: There is no learning curve associated with Docker
- **Standard Python deployment**: Uses familiar Python tooling that developers expect
- **Easier to understand and modify**: The codebase is more transparent and easier to customize

[Source: ARCHITECTURE.md]

### 2. Close Coupling and Integration
- **Direct Python access to Chonkie and ChromaDB**: The application has tight coupling with these Python libraries, making container boundaries unnecessary
- **Shared memory space**: Components share memory for efficient data passing without container isolation
- **No container boundaries**: Direct access to data structures simplifies integration

[Source: ARCHITECTURE.md]

### 3. Performance Benefits
- **stdio transport**: Uses the Model Context Protocol's stdio transport, eliminating HTTP overhead
- **No container overhead**: Avoids CPU and memory costs associated with containerization
- **Faster startup and shutdown**: No need to start/stop containers for each operation
- **Lower resource usage**: Minimal memory footprint with no duplicate Python installations

[Source: ARCHITECTURE.md]

### 4. Developer Experience
- **Direct debugging access**: Python debugger can attach directly to the running process
- **Easy log inspection**: Logs are readily accessible without container shell complexities
- **Simpler CI/CD pipelines**: Integration with other Python tools is more straightforward

[Source: ARCHITECTURE.md]

### 5. Resource Efficiency
- **Lower memory footprint**: No need for a full container runtime
- **No duplicate Python installations**: Uses the system Python with a virtual environment
- **Shared system libraries**: Leverages existing system libraries instead of duplicating them

[Source: ARCHITECTURE.md]

## When Docker Might Be Appropriate

The architecture documentation notes that Docker would be more suitable for:
- Multi-user deployment requiring isolation
- Running on non-Python systems
- Complex dependency conflicts
- Enterprise deployment requirements

## Target Use Case

The librarian-mcp is designed for **single-user local deployment**, where venv is superior. Docker would be over-engineered for this use case.

[Source: ARCHITECTURE.md]

## Summary

The venv approach provides a simpler, more performant, and easier-to-debug solution for the librarian-mcp's target use case of single-user local deployment. The close coupling with Python-specific libraries (Chonkie, ChromaDB) and the stdio-based MCP protocol make Docker unnecessary complexity.

---
**Primary Source**: `/home/peter/development/librarian-mcp/ARCHITECTURE.md`
**Section**: "Why venv Instead of Docker?"