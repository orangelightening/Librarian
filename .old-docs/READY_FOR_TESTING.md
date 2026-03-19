# Jan Validation Pipeline - Ready for Testing

While you were investigating Jan's GitHub repo, I've prepared the complete validation pipeline for Jan with comprehensive logging on our side.

## What's Ready

### 1. Enhanced MCP Server with Logging
**File**: `librarian_mcp_with_logging.py`

This server logs ALL tool calls, arguments, and results from our side to compensate for Jan's inadequate client-side logging.

**Launch with**: `./run_jan_with_logging.sh`

**Logs to**: `librarian_mcp_debug.log` (comprehensive tool execution data)

### 2. Quick Test Script
**File**: `scripts/test_jan_quick.py`

Single-query test to verify Jan API + MCP integration is working.

**Run**: `python scripts/test_jan_quick.py`

**What it tests**:
- Jan API connection
- MCP tool access
- System prompt delivery
- Tool call detection

### 3. Full Batch Validation
**File**: `scripts/run_jan_validation.py`

Complete validation pipeline adapted from LM Studio version.

**Run**: `python scripts/run_jan_validation.py`

**Features**:
- Runs all 16 validation queries from `library_validation.md`
- Captures tool calls and token usage
- Generates detailed debug log: `jan_validation_debug.log`
- Saves results: `jan_validation_results.json`
- Shows summary with success/error counts and tool call analysis

## Key Differences from LM Studio Version

### API Format
**LM Studio**:
```json
{
  "model": "...",
  "input": "...",
  "system_prompt": "...",
  "integrations": [{"type": "plugin", "id": "mcp/librarian"}]
}
```

**Jan** (OpenAI-compatible):
```json
{
  "model": "...",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "tools_enabled": true
}
```

### Response Format
**Jan returns OpenAI-style structure**:
```json
{
  "choices": [{
    "message": {
      "content": "...",
      "tool_calls": [...]
    }
  }],
  "usage": {
    "total_tokens": 1234
  }
}
```

## Testing Strategy

### Step 1: Verify Jan API Access
```bash
# First, make sure Jan is running with API server enabled
# Then test the quick script:
python scripts/test_jan_quick.py
```

**What to look for**:
- ✓ Request successful
- 📞 Tool calls detected (should show for "list indexed documents")
- 📊 Token usage

### Step 2: Start Logging-Enhanced MCP Server
```bash
# In a separate terminal, start our server with logging:
./run_jan_with_logging.sh
```

**What to look for in logs**:
- Tool calls being received
- Arguments being parsed
- Results being returned

### Step 3: Run Full Validation
```bash
# In another terminal:
python scripts/run_jan_validation.py
```

**What to check**:
- All 16 queries complete successfully
- Tool calls are being made (check counts)
- `librarian_mcp_debug.log` shows actual tool execution
- `jan_validation_debug.log` shows API communication

## What We're Testing

### From Our Side (librarian-mcp)
- ✓ Tool registration with FastMCP
- ✓ Tool invocation by Jan
- ✓ Argument parsing and validation
- ✓ Result formatting and return

### From Jan's Side
- ✓ MCP client connection
- ✓ Tool calling capability
- ✓ Message passing to our server
- ✓ Response handling

### Quality Checks
- Proper tool usage (not just "I would use tool X")
- Citations included when using library content
- No hallucinations when no data found
- Proper error handling

## Log Files to Review

### 1. `librarian_mcp_debug.log`
Our comprehensive server-side logging showing:
- Every tool call received
- Full arguments for each call
- Results returned
- Any errors that occur

### 2. `jan_validation_debug.log`
API communication log showing:
- Request payloads
- Response structures
- Tool calls in responses
- Token usage

### 3. Jan's own logs
In the Jan UI (though currently limited):
- HTTP requests
- Connection status
- Basic proxying info

## Next Steps When You Return

1. **Share findings from Jan GitHub repo** - Any solutions for better logging?
2. **Test quick script first** - Verify basic connectivity
3. **Start logging server** - Capture tool execution from our side
4. **Run full validation** - Compare results to chat window quality
5. **Analyze logs** - See if tools are actually executing or just being called

## Comparison Points

### Chat Window vs API
When testing, compare:
- Tool usage frequency (chat vs API)
- Response quality and detail
- Citation accuracy
- Hallucination occurrences

### Temperature Settings
- Chat: 0.5 (working well)
- API: 0.5 (set to match)
- Both using Qwen3_5-4B-UD-Q8_K_XL

## Files Created/Modified

1. `librarian_mcp_with_logging.py` - Enhanced server with comprehensive logging
2. `scripts/run_jan_validation.py` - Jan-specific batch validation
3. `scripts/test_jan_quick.py` - Quick connectivity test
4. `run_jan_with_logging.sh` - Server launch script
5. `READY_FOR_TESTING.md` - This document

All ready for your return from the GitHub repo investigation!
