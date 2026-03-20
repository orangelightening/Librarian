# Query 7: Deployment Architecture

**Status**: success
**Tokens Used**: 359
**Timestamp**: 2026-03-18T19:21:41.487064
**Tool Calls**: 1

---

I'll search the library for information about why the librarian-mcp uses venv instead of Docker for deployment.


Based on the library, here's why the librarian-mcp uses venv instead of Docker for deployment:

**[Source: architecture.md]**
The primary reasons are **simplicity**, **performance**, and **developer experience**:

1. **Simplicity** - No container complexity or learning curve; standard Python deployment that's easier to understand and modify

2. **Performance & Coupling** - Enables close coupling between Chonkie and ChromaDB with direct data access, no container boundaries

3. **Better Performance** - Uses stdio transport for MCP communication (no HTTP overhead), lower resource usage without container overhead

4. **Developer Experience** - Direct debugging access, easier log inspection, simpler CI/CD workflows

5. **Deployment Model** - Optimized for single-user or local deployments where Docker's complexity isn't justified

**[Source: features.md]**
The venv approach is specifically recommended because it provides "close Chonkie-ChromaDB coupling" with direct Python access, making the system faster and easier to debug compared to containerized solutions.

**[Source: deployment.md]**
For multi-user or enterprise deployments, Docker may make sense, but for the librarian-mcp's intended use case (local/single-user), venv is the preferred approach due to its simplicity and performance characteristics.

Would you like me to read any of these documents in full to get more details about the deployment setup?