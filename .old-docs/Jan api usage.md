# Local API Server

Jan provides a built-in, OpenAI-compatible API server that runs entirely on your computer, powered by `llama.cpp`. Use it as a drop-in replacement for cloud APIs to build private, offline-capable AI applications.

![Jan's Local API Server Settings UI](https://www.jan.ai/_next/static/media/local-api-server.c85bad91.png)

## Quick Start[](https://www.jan.ai/docs/desktop/api-server#quick-start)

### Start the Server[](https://www.jan.ai/docs/desktop/api-server#start-the-server)

1. Navigate to **Settings** > **Local API Server**.
2. Click **Start Server**.

The server is ready when the logs show `JAN API listening at http://127.0.0.1:1337`.

### Test with cURL[](https://www.jan.ai/docs/desktop/api-server#test-with-curl)

Open a terminal and make a request. Replace `YOUR_MODEL_ID` with the ID of an available model in Jan.

`   curl http://127.0.0.1:1337/v1/chat/completions \    -H "Content-Type: application/json" \    -H "Authorization: Bearer secret-key-123" \    -d '{    "model": "YOUR_MODEL_ID",    "messages": [{"role": "user", "content": "Tell me a joke."}]    }'            `

## Server Configuration[](https://www.jan.ai/docs/desktop/api-server#server-configuration)

These settings control the network accessibility and basic behavior of your local server. Access them via the **Configuration** button in the top right.

![Server Configuration](https://www.jan.ai/_next/static/media/server-configuration.1abea2c3.png)

### Server Host[](https://www.jan.ai/docs/desktop/api-server#server-host)

The network address the server listens on.

- **`127.0.0.1`** (Default): The server is only accessible from your own computer. This is the most secure option for personal use.
- **`0.0.0.0`**: The server is accessible from other devices on your local network (e.g., your phone or another computer). Use this with caution.

### Server Port[](https://www.jan.ai/docs/desktop/api-server#server-port)

The port number for the API server.

- **`1337`** (Default): A common alternative port.
- You can change this to any available port number (e.g., `8000`).

### API Prefix[](https://www.jan.ai/docs/desktop/api-server#api-prefix)

The base path for all API endpoints.

- **`/v1`** (Default): Follows OpenAI's convention. The chat completions endpoint would be `http://127.0.0.1:1337/v1/chat/completions`.
- You can change this or leave it empty if desired.

### API Key[](https://www.jan.ai/docs/desktop/api-server#api-key)

A mandatory secret key to authenticate requests.

- You must set a key. It can be any string (e.g., `a-secure-password`).
- All API requests must include this key in the `Authorization: Bearer YOUR_API_KEY` header.

### Trusted Hosts[](https://www.jan.ai/docs/desktop/api-server#trusted-hosts)

A comma-separated list of hostnames allowed to access the server. This provides an additional layer of security when the server is exposed on your network.

## Advanced Settings[](https://www.jan.ai/docs/desktop/api-server#advanced-settings)

### Cross-Origin Resource Sharing (CORS)[](https://www.jan.ai/docs/desktop/api-server#cross-origin-resource-sharing-cors)

- **(Enabled by default)** Allows web applications (like a custom web UI you are building) running on different domains to make requests to the API server.
- **Disable this** if your API will only be accessed by non-browser-based applications (e.g., scripts, command-line tools) for slightly improved security.

### Verbose Server Logs[](https://www.jan.ai/docs/desktop/api-server#verbose-server-logs)

- **(Enabled by default)** Provides detailed, real-time logs of all incoming requests, responses, and server activity.
- This is extremely useful for debugging application behavior and understanding exactly what is being sent to the models.

## Troubleshooting[](https://www.jan.ai/docs/desktop/api-server#troubleshooting)

Ensure **Verbose Server Logs** are enabled to get detailed error messages in the "Server Logs" view.

- **Connection Refused:** The server is not running, or your application is pointing to the wrong host or port.
- **401 Unauthorized:** Your API Key is missing from the `Authorization` header or is incorrect.
- **404 Not Found:**
    - The `model` ID in your request body does not match an available model in Jan.
    - Your request URL is incorrect (check the API Prefix).
- **CORS Error (in a web browser):** Ensure the CORS toggle is enabled in Jan's settings.

Last updated on March 18, 2026

# API Reference

Jan's local API server exposes an OpenAI-compatible REST API at `http://127.0.0.1:1337`. Use it as a drop-in replacement for cloud APIs in any application that supports OpenAI-compatible endpoints.

## Supported Endpoints[](https://www.jan.ai/docs/desktop/api-preference#supported-endpoints)

### `GET /v1/models`[](https://www.jan.ai/docs/desktop/api-preference#get-v1models)

Returns a list of all models currently loaded or available in Jan.

`   curl http://127.0.0.1:1337/v1/models \    -H "Authorization: Bearer YOUR_API_KEY"            `

`   {    "object": "list",    "data": [    { "id": "jan-v3-4b-base-instruct", "object": "model" }    ]    }            `

---

### `POST /v1/chat/completions`[](https://www.jan.ai/docs/desktop/api-preference#post-v1chatcompletions)

OpenAI-compatible chat completions endpoint. Supports streaming, tool calling, and multi-turn conversations.

`   curl http://127.0.0.1:1337/v1/chat/completions \    -H "Content-Type: application/json" \    -H "Authorization: Bearer YOUR_API_KEY" \    -d '{    "model": "jan-v3-4b-base-instruct",    "messages": [{"role": "user", "content": "Hello!"}],    "stream": false    }'            `

---

### `POST /v1/messages`[](https://www.jan.ai/docs/desktop/api-preference#post-v1messages)

Anthropic-compatible messages endpoint. Jan automatically translates requests to the internal format, so you can use Anthropic SDK clients pointed at your local server.

`   curl http://127.0.0.1:1337/v1/messages \    -H "Content-Type: application/json" \    -H "x-api-key: YOUR_API_KEY" \    -d '{    "model": "jan-v3-4b-base-instruct",    "max_tokens": 1024,    "messages": [{"role": "user", "content": "Hello!"}]    }'            `

---

**OpenAI Responses API** (`/v1/responses`) support is coming soon.

## Use With Agents & Integrations[](https://www.jan.ai/docs/desktop/api-preference#use-with-agents--integrations)

Jan's local API is designed to wire directly into AI agents and coding tools — no cloud account needed.

[

Claude Code

Point Claude Code at Jan's local server to run Opus, Sonnet, and Haiku tiers on your own hardware.

](https://www.jan.ai/docs/desktop/integrations/claude-code)[

OpenClaw

Wire OpenClaw to Jan's local API for a fully private autonomous agent — no cloud, no usage fees.

](https://www.jan.ai/docs/desktop/integrations/openclaw)

## Using with OpenAI SDK[](https://www.jan.ai/docs/desktop/api-preference#using-with-openai-sdk)

Point the OpenAI SDK at your local server by setting the base URL and API key:

`   from openai import OpenAI        client = OpenAI(    base_url="http://127.0.0.1:1337/v1",    api_key="YOUR_API_KEY"    )        response = client.chat.completions.create(    model="jan-v3-4b-base-instruct",    messages=[{"role": "user", "content": "Hello!"}]    )            `

`   import OpenAI from "openai";        const client = new OpenAI({    baseURL: "http://127.0.0.1:1337/v1",    apiKey: "YOUR_API_KEY",    });            `

Last updated on March 18, 2026

## System prompt for API session

To set a system prompt for a session using the **Jan API**, you need to include the system prompt within the `initialPrompts` array when creating a new session, with the `role` set to `"system"`. 

The system prompt must be placed at the **0th position** in the `initialPrompts` array, as placing it elsewhere will result in a `TypeError`. 

### Example:

```
const session = await LanguageModel.create({
  initialPrompts: [
    {
      role: "system",
      content: "You are a helpful assistant that provides concise, accurate answers."
    },
    {
      role: "user",
      content: "What is the capital of France?"
    }
  ]
});
```

This setup ensures the model's behavior is defined from the start of the session and persists throughout, even if the context window overflows. The `initialPrompts` option also supports **N-shot prompting** by including example user/assistant interactions, which helps guide the model’s responses. 

Can the model used in the api session use the mcp tools in Jan

Finished

Yes, models used in **Jan API sessions can use MCP (Model Context Protocol) tools**, but only if the **model supports tool calling** and **tools are explicitly enabled**. 

### Key Requirements:

- **MCP Support**: Jan acts as an MCP client, connecting models to external tools via standardized servers. 
    
- **Model Compatibility**: Not all models support tool calling. Recommended models include:
    
    - **Cloud models**: GPT-4, Claude 3.5+, Gemini Pro
        
    - **Local models**: Qwen3, Gemma3, or other function-calling variants
        
- **Enable Tools**: In the Jan UI, go to _Model Providers_ and enable **tool calling** for your selected model. 
    
- **Runtime Dependencies**: Install **Node.js** and/or **Python** as needed by the MCP server. 
    
- **Permissions**: Toggle _Allow All MCP Tool Permission_ in Settings > MCP Servers. 
    

### Example MCP Tools Available:

- **Web & Search**: Serper (Google search), Browserbase (browser automation)
    
- **Code & Analysis**: Jupyter (code execution, data analysis)
    
- **Productivity**: Notion, Todoist, Calendar integrations
    
- **Creative**: Canva (design generation) 
    

### Configuration Example:

```
{
  "initialPrompts": [
    {
      "role": "system",
      "content": "You can use tools like web search, code execution, and browser automation."
    }
  ],
  "model": "claude-3-5-sonnet",
  "tools_enabled": true
}
```

> **Note**: Tool availability depends on proper MCP server setup (e.g., Docker for Jupyter, API keys for Serper). Local models may struggle with complex tool workflows due to context or performance limits. 




