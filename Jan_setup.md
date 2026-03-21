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

---

## Tips and Best Practices

- **Always restart after**: Library rebuilds, System_prompt changes, major documentation updates
- **New chat per session**: Start a fresh chat after restarting MCP server
- **Verify count**: Ask "How many documents are in the library?" to confirm fresh data loaded

---

*Documentation in progress - full Jan interface walkthrough coming tomorrow*
