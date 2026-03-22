# Jan AI MCP Setup Guide

**Created**: 2026-03-20
**Status**: In Progress

---

## Important: MCP Server Restart Requirement

**Critical**: When you rebuild the library index or make changes to the Librarian's data, you **must restart the MCP server in Jan** to pick up the fresh data.

### How to Restart the Librarian MCP in Jan

1. **Open Jan Settings**
   - Click Settings icon (gear) or use Ctrl+,

2. **Navigate to MCP Servers**
   - Settings → MCP Servers

3. **Find the Librarian MCP**
   - Locate "librarian-mcp" in your server list

4. **Restart the Server**
   - Toggle the server OFF
   - Wait 2-3 seconds
   - Toggle the server back ON

5. **Verify Fresh Data**
   - Start a new chat
   - Ask: "How many documents are in the library?"
   - The count should match your latest rebuild

### Why This Is Necessary

Jan maintains the MCP server connection in memory. When you rebuild the library:
- Old index remains in Jan's memory
- New index not loaded until server restarts
- Queries return stale data until restart

**This is a common source of confusion** - you rebuild the index, but Jan still shows old results because the MCP server wasn't restarted.

---

## Installation

*(To be documented tomorrow - full Jan interface walkthrough)*

---

## Configuration

*(To be documented tomorrow)*

---

## Multi-MCP Configuration

### ⚠️ Important: Filesystem MCP Compatibility

**Current Status**: Filesystem MCP should be **disabled** when using Librarian MCP.

#### The Problem

When both Librarian MCP and Filesystem MCP are enabled simultaneously:

1. **Tool Confusion**: Models may hybridize tools from both MCPs unpredictably
   - Use `read_document()` (librarian) when they should use `Read` (filesystem)
   - Get confused about sandbox boundaries (LIBRARIAN_SAFE_DIR vs unrestricted access)
   - Mix semantic search with filesystem search inappropriately

2. **Permission Reset Issue**: **Jan resets MCP permissions when switching models**
   - You configure Filesystem MCP as **read-only**
   - Switch to a different model in Jan
   - **Permissions reset to default (read + write) automatically**
   - This creates unintended write access risks

3. **Directory Overlap**: Both MCPs configured to same directory
   - Librarian MCP: `/home/peter/development/librarian-mcp`
   - Filesystem MCP: Same directory (when enabled)
   - Models may not understand which MCP to use for which operation

#### Recommended Configuration

**For Single-MCP Setup (Recommended)**:
- ✅ **Enable**: Librarian MCP only
- ❌ **Disable**: Filesystem MCP completely
- **Rationale**: Librarian provides all necessary file access within its secure sandbox

**If You Must Use Both MCPs**:
1. **Verify permissions after every model switch**
   - Settings → MCP Servers → Filesystem
   - Ensure "Read" access only, NO "Write" access
   - Re-verify after changing models

2. **Use different allowed directories**
   - Librarian MCP: `/home/peter/development/librarian-mcp`
   - Filesystem MCP: Different directory (e.g., `/home/peter/` for broader access)

3. **Monitor model behavior closely**
   - Watch for inappropriate tool usage
   - Check if model respects sandbox boundaries
   - Be prepared to disable Filesystem MCP if confusion occurs

#### Future Improvements

Needed: Add explicit tool selection guidelines to System_prompt.md to help models understand:
- When to use Librarian MCP tools (semantic search, sandboxed access)
- When to use Filesystem MCP tools (unrestricted read access)
- How to handle overlapping functionality

**For now: Keep Filesystem MCP disabled to avoid confusion.**

---

## Troubleshooting

### Issue: "Library has X documents" but rebuild script says Y documents

**Cause**: MCP server not restarted after rebuild

**Solution**:
1. Rebuild library: `./scripts/clear_and_rebuild.sh`
2. Restart MCP server in Jan (Settings → MCP Servers → Toggle Librarian OFF then ON)
3. Start new chat in Jan
4. Ask: "How many documents are indexed?"
5. Count should now match

### Issue: Model gives outdated information

**Cause**: Old System_prompt cached in Jan's MCP connection

**Solution**: Restart MCP server to pick up updated System_prompt.md

### Issue: Model confused about which file access tool to use

**Cause**: Both Librarian MCP and Filesystem MCP enabled simultaneously

**Symptoms**:
- Model tries to read files outside LIBRARIAN_SAFE_DIR using `read_document()`
- Model uses `Read` (filesystem) when it should use semantic search
- Inconsistent tool usage patterns

**Solution**:
1. **Disable Filesystem MCP** (recommended)
   - Settings → MCP Servers → Filesystem → Toggle OFF
   - Use Librarian MCP exclusively for file access

2. **If both MCPs required**:
   - Settings → MCP Servers → Filesystem → Permissions → **Read only**
   - **Re-verify permissions after every model switch** (Jan resets them!)
   - Use different allowed directories for each MCP

3. **Restart MCP server** after making changes

---

## Tips and Best Practices

- **Always restart after**: Library rebuilds, System_prompt changes, major documentation updates
- **New chat per session**: Start a fresh chat after restarting MCP server
- **Verify count**: Ask "How many documents are in the library?" to confirm fresh data loaded
- **Keep Filesystem MCP disabled**: Avoids tool confusion and permission reset issues
- **Re-verify permissions after model changes**: Jan resets MCP permissions when switching models

---

*Documentation in progress - full Jan interface walkthrough coming tomorrow*
