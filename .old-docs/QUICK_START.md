# Quick Start: Jan Validation Testing

## When You Return - Run These in Order

### 1. Quick Connectivity Test
```bash
python3 scripts/test_jan_quick.py
```
**What it checks**: Jan API connection, MCP tool access, system prompt delivery
**Expected**: Tool calls detected for "list indexed documents"

### 2. Start Logging-Enhanced Server
```bash
# In a new terminal window
./run_jan_with_logging.sh
```
**What it does**: Starts librarian-mcp with comprehensive logging
**Logs to**: `librarian_mcp_debug.log`

### 3. Run Full Validation Batch
```bash
# In original terminal
python3 scripts/run_jan_validation.py
```
**What it does**: Runs all 16 validation queries
**Output**: `jan_validation_results.json`
**Logs**: `jan_validation_debug.log`

## Files to Review

### API Communication
- `jan_validation_debug.log` - Full request/response logging

### Tool Execution
- `librarian_mcp_debug.log` - Server-side tool call logging

### Results
- `jan_validation_results.json` - Structured results for analysis

## Success Criteria

✓ All 16 queries complete without errors
✓ Tool calls detected in responses
✓ Actual tool execution visible in logs
✓ Quality matches chat window
✓ Proper citations included

## Troubleshooting

**No tool calls detected**:
- Check Jan has MCP server configured
- Verify `tools_enabled: true` in payload
- Check Jan UI MCP Servers section

**Connection refused**:
- Verify Jan API server is running (Settings > Local API Server)
- Check URL: `http://127.0.0.1:1337/v1/chat/completions`
- Verify API key setting

**Quality degradation vs chat**:
- Compare system prompts (prompt_jan.md)
- Check temperature setting (0.5)
- Verify tools_enabled is true

## Key Differences from Chat

| Chat Window | API |
|-------------|-----|
| Direct UI interaction | HTTP requests |
| Built-in tool execution | Requires MCP connection |
| Visual tool feedback | Must parse tool_calls array |
| Immediate response | Network latency + ~300s timeout |

## Documentation

- `READY_FOR_TESTING.md` - Complete testing guide
- `STATUS.md` - Overall status and next steps
- `Jan api usage.md` - Jan API reference

---
**Everything ready for your return from Jan GitHub repo!**
