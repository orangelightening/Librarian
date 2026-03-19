
LM Studio offers a powerful REST API with first-class support for local inference and model management. In addition to our native API, we provide OpenAI-compatible endpoints ([learn more](/docs/developer/openai-compat)) and Anthropic-compatible endpoints ([learn more](/docs/developer/anthropic-compat)).

## What's new
Previously, there was a [v0 REST API](/docs/developer/rest/endpoints). With LM Studio 0.4.0, we have officially released our native v1 REST API at `/api/v1/*` endpoints and recommend using it.

The v1 REST API includes enhanced features such as:
- [MCP via API](/docs/developer/core/mcp)
- [Stateful chats](/docs/developer/rest/stateful-chats)
- [Authentication](/docs/developer/core/authentication) configuration with API tokens
- Model [download](/docs/developer/rest/download), [load](/docs/developer/rest/load) and [unload](/docs/developer/rest/unload) endpoints

## Supported endpoints
The following endpoints are available in LM Studio's v1 REST API.
<table class="flexible-cols">
  <thead>
    <tr>
      <th>Endpoint</th>
      <th>Method</th>
      <th>Docs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>/api/v1/chat</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/rest/chat">Chat</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models</code></td>
      <td><apimethod method="GET" /></td>
      <td><a href="/docs/developer/rest/list">List Models</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models/load</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/rest/load">Load</a></td>
    </tr>
    <tr>
        <td><code>/api/v1/models/unload</code></td>
        <td><apimethod method="POST" /></td>
        <td><a href="/docs/developer/rest/unload">Unload</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models/download</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/rest/download">Download</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models/download/status</code></td>
      <td><apimethod method="GET" /></td>
      <td><a href="/docs/developer/rest/download-status">Download Status</a></td>
    </tr>
  </tbody>
</table>

## Inference endpoint comparison
The table below compares the features of LM Studio's `/api/v1/chat` endpoint with OpenAI-compatible and Anthropic-compatible inference endpoints.
<table class="flexible-cols">
  <thead>
    <tr>
      <th>Feature</th>
      <th><a href="/docs/developer/rest/chat"><code>/api/v1/chat</code></a></th>
      <th><a href="/docs/developer/openai-compat/responses"><code>/v1/responses</code></a></th>
      <th><a href="/docs/developer/openai-compat/chat-completions"><code>/v1/chat/completions</code></a></th>
      <th><a href="/docs/developer/anthropic-compat/messages"><code>/v1/messages</code></a></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Streaming</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Stateful chat</td>
      <td>✅</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Remote MCPs</td>
      <td>✅</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>MCPs you have in LM Studio</td>
      <td>✅</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Custom tools</td>
      <td>❌</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Include assistant messages in the request</td>
      <td>❌</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Model load streaming events</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Prompt processing streaming events</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>Specify context length in the request</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
  </tbody>
</table>

---

Please report bugs by opening an issue on [Github](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues).

## Start the server

[Install](/download) and launch LM Studio.

Then ensure the server is running through the toggle at the top left of the Developer page, or through [lms](/docs/cli) in the terminal:

```bash
lms server start
```

By default, the server is available at `http://localhost:1234`.

If you don't have a model downloaded yet, you can download the model:

```bash
lms get ibm/granite-4-micro
```


## API Authentication

By default, the LM Studio API server does **not** require authentication. You can configure the server to require authentication by API token in the [server settings](/docs/developer/core/server/settings) for added security.

To authenticate API requests, generate an API token from the Developer page in LM Studio, and include it in the `Authorization` header of your requests as follows: `Authorization: Bearer $LM_API_TOKEN`. Read more about authentication [here](/docs/developer/core/authentication).


## Chat with a model

Use the chat endpoint to send a message to a model. By default, the model will be automatically loaded if it is not already.

The `/api/v1/chat` endpoint is stateful, which means you do not need to pass the full history in every request. Read more about it [here](/docs/developer/rest/stateful-chats).

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Write a short haiku about sunrise."
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={
          "model": "ibm/granite-4-micro",
          "input": "Write a short haiku about sunrise."
        }
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "ibm/granite-4-micro",
          input: "Write a short haiku about sunrise."
        })
      });
      const data = await response.json();
      console.log(data);
```

See the full [chat](/docs/developer/rest/chat) docs for more details.

## Use MCP servers via API


Enable the model interact with ephemeral Model Context Protocol (MCP) servers in `/api/v1/chat` by specifying servers in the `integrations` field.

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "What is the top trending model on hugging face?",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"]
            }
          ],
          "context_length": 8000
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={
          "model": "ibm/granite-4-micro",
          "input": "What is the top trending model on hugging face?",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"]
            }
          ],
          "context_length": 8000
        }
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "ibm/granite-4-micro",
          input: "What is the top trending model on hugging face?",
          integrations: [
            {
              type: "ephemeral_mcp",
              server_label: "huggingface",
              server_url: "https://huggingface.co/mcp",
              allowed_tools: ["model_search"]
            }
          ],
          context_length: 8000
        })
      const data = await response.json();
      console.log(data);
```

You can also use locally configured MCP plugins (from your `mcp.json`) via the `integrations` field. Using locally run MCP plugins requires authentication via an API token passed through the `Authorization` header. Read more about authentication [here](/docs/developer/core/authentication).

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Open lmstudio.ai",
          "integrations": [
            {
              "type": "plugin",
              "id": "mcp/playwright",
              "allowed_tools": ["browser_navigate"]
            }
          ],
          "context_length": 8000
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={
          "model": "ibm/granite-4-micro",
          "input": "Open lmstudio.ai",
          "integrations": [
            {
              "type": "plugin",
              "id": "mcp/playwright",
              "allowed_tools": ["browser_navigate"]
            }
          ],
          "context_length": 8000
        }
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "ibm/granite-4-micro",
          input: "Open lmstudio.ai",
          integrations: [
            {
              type: "plugin",
              id: "mcp/playwright",
              allowed_tools: ["browser_navigate"]
            }
          ],
          context_length: 8000
        })
      });
      const data = await response.json();
      console.log(data);
```

See the full [chat](/docs/developer/rest/chat) docs for more details.

## Download a model

Use the download endpoint to download models by identifier from the [LM Studio model catalog](https://lmstudio.ai/models), or by Hugging Face model URL.

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/download \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro"
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/models/download",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={"model": "ibm/granite-4-micro"}
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/models/download", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "ibm/granite-4-micro"
        })
      });
      const data = await response.json();
      console.log(data);
```

The response will return a `job_id` that you can use to track download progress.

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl -H "Authorization: Bearer $LM_API_TOKEN" \
        http://localhost:1234/api/v1/models/download/status/{job_id}
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      job_id = "your-job-id"
      response = requests.get(
        f"http://localhost:1234/api/v1/models/download/status/{job_id}",
        headers={"Authorization": f"Bearer {os.environ['LM_API_TOKEN']}"}
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const jobId = "your-job-id";
      const response = await fetch(
        `http://localhost:1234/api/v1/models/download/status/${jobId}`,
        {
          headers: {
            "Authorization": `Bearer ${process.env.LM_API_TOKEN}`
          }
        }
      );
      const data = await response.json();
      console.log(data);
```

See the [download](/docs/developer/rest/download) and [download status](/docs/developer/rest/download-status) docs for more details.

The `/api/v1/chat` endpoint is stateful by default. This means you don't need to pass the full conversation history in every request — LM Studio automatically stores and manages the context for you.

## How it works

When you send a chat request, LM Studio stores the conversation in a chat thread and returns a `response_id` in the response. Use this `response_id` in subsequent requests to continue the conversation.

```lms_code_snippet
title: Start a new conversation
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "My favorite color is blue."
        }'
```

The response includes a `response_id`:

```lms_info
Every response includes an unique `response_id` that you can use to reference that specific point in the conversation for future requests. This allows you to branch conversations.
```

```lms_code_snippet
title: Response
variants:
  response:
    language: json
    code: |
      {
        "model_instance_id": "ibm/granite-4-micro",
        "output": [
          {
            "type": "message",
            "content": "That's great! Blue is a beautiful color..."
          }
        ],
        "response_id": "resp_abc123xyz..."
      }
```

## Continue a conversation

Pass the `previous_response_id` in your next request to continue the conversation. The model will remember the previous context.



```lms_code_snippet
title: Continue the conversation
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "What color did I just mention?",
          "previous_response_id": "resp_abc123xyz..."
        }'
```

The model can reference the previous message without you needing to resend it and will return a new `response_id` for further continuation.

## Disable stateful storage

If you don't want to store the conversation, set `store` to `false`. The response will not include a `response_id`.

```lms_code_snippet
title: Stateless chat
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Tell me a joke.",
          "store": false
        }'
```

This is useful for one-off requests where you don't need to maintain context.

Streaming events let you render chat responses incrementally over Server‑Sent Events (SSE). When you call `POST /api/v1/chat` with `stream: true`, the server emits a series of named events that you can consume. These events arrive in order and may include multiple deltas (for reasoning and message content), tool call boundaries and payloads, and any errors encountered. The stream always begins with `chat.start` and concludes with `chat.end`, which contains the aggregated result equivalent to a non‑streaming response.

List of event types that can be sent in an `/api/v1/chat` response stream:
- `chat.start`
- `model_load.start`
- `model_load.progress`
- `model_load.end`
- `prompt_processing.start`
- `prompt_processing.progress`
- `prompt_processing.end`
- `reasoning.start`
- `reasoning.delta`
- `reasoning.end`
- `tool_call.start`
- `tool_call.arguments`
- `tool_call.success`
- `tool_call.failure`
- `message.start`
- `message.delta`
- `message.end`
- `error`
- `chat.end`

Events will be streamed out in the following raw format:
```bash
event: <event type>
data: <JSON event data>
```

### `chat.start`
````lms_hstack
An event that is emitted at the start of a chat response stream.
```lms_params
- name: model_instance_id
  type: string
  description: Unique identifier for the loaded model instance that will generate the response.
- name: type
  type: '"chat.start"'
  description: The type of the event. Always `chat.start`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "chat.start",
        "model_instance_id": "openai/gpt-oss-20b"
      }
```
````

### `model_load.start`
````lms_hstack
Signals the start of a model being loaded to fulfill the chat request. Will not be emitted if the requested model is already loaded.
```lms_params
- name: model_instance_id
  type: string
  description: Unique identifier for the model instance being loaded.
- name: type
  type: '"model_load.start"'
  description: The type of the event. Always `model_load.start`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "model_load.start",
        "model_instance_id": "openai/gpt-oss-20b"
      }
```
````

### `model_load.progress`
````lms_hstack
Progress of the model load.
```lms_params
- name: model_instance_id
  type: string
  description: Unique identifier for the model instance being loaded.
- name: progress
  type: number
  description: Progress of the model load as a float between `0` and `1`.
- name: type
  type: '"model_load.progress"'
  description: The type of the event. Always `model_load.progress`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "model_load.progress",
        "model_instance_id": "openai/gpt-oss-20b",
        "progress": 0.65
      }
```
````

### `model_load.end`
````lms_hstack
Signals a successfully completed model load.
```lms_params
- name: model_instance_id
  type: string
  description: Unique identifier for the model instance that was loaded.
- name: load_time_seconds
  type: number
  description: Time taken to load the model in seconds.
- name: type
  type: '"model_load.end"'
  description: The type of the event. Always `model_load.end`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "model_load.end",
        "model_instance_id": "openai/gpt-oss-20b",
        "load_time_seconds": 12.34
      }
```
````

### `prompt_processing.start`
````lms_hstack
Signals the start of the model processing a prompt.
```lms_params
- name: type
  type: '"prompt_processing.start"'
  description: The type of the event. Always `prompt_processing.start`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "prompt_processing.start"
      }
```
````

### `prompt_processing.progress`
````lms_hstack
Progress of the model processing a prompt.
```lms_params
- name: progress
  type: number
  description: Progress of the prompt processing as a float between `0` and `1`.
- name: type
  type: '"prompt_processing.progress"'
  description: The type of the event. Always `prompt_processing.progress`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "prompt_processing.progress",
        "progress": 0.5
      }
```
````

### `prompt_processing.end`
````lms_hstack
Signals the end of the model processing a prompt.
```lms_params
- name: type
  type: '"prompt_processing.end"'
  description: The type of the event. Always `prompt_processing.end`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "prompt_processing.end"
      }
```
````

### `reasoning.start`
````lms_hstack
Signals the model is starting to stream reasoning content.
```lms_params
- name: type
  type: '"reasoning.start"'
  description: The type of the event. Always `reasoning.start`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "reasoning.start"
      }
```
````

### `reasoning.delta`
````lms_hstack
A chunk of reasoning content. Multiple deltas may arrive.
```lms_params
- name: content
  type: string
  description: Reasoning text fragment.
- name: type
  type: '"reasoning.delta"'
  description: The type of the event. Always `reasoning.delta`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "reasoning.delta",
        "content": "Need to"
      }
```
````

### `reasoning.end`
````lms_hstack
Signals the end of the reasoning stream.
```lms_params
- name: type
  type: '"reasoning.end"'
  description: The type of the event. Always `reasoning.end`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "reasoning.end"
      }
```
````

### `tool_call.start`
````lms_hstack
Emitted when the model starts a tool call.
```lms_params
- name: tool
  type: string
  description: Name of the tool being called.
- name: provider_info
  type: object
  description: Information about the tool provider. Discriminated union upon possible provider types.
  children:
    - name: Plugin provider info
      type: object
      description: Present when the tool is provided by a plugin.
      children:
        - name: type
          type: '"plugin"'
          description: Provider type.
        - name: plugin_id
          type: string
          description: Identifier of the plugin.
    - name: Ephemeral MCP provider info
      type: object
      description: Present when the tool is provided by a ephemeral MCP server.
      children:
        - name: type
          type: '"ephemeral_mcp"'
          description: Provider type.
        - name: server_label
          type: string
          description: Label of the MCP server.
- name: type
  type: '"tool_call.start"'
  description: The type of the event. Always `tool_call.start`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.start",
        "tool": "model_search",
        "provider_info": {
          "type": "ephemeral_mcp",
          "server_label": "huggingface"
        }
      }
```
````

### `tool_call.arguments`
````lms_hstack
Arguments streamed for the current tool call.
```lms_params
- name: tool
  type: string
  description: Name of the tool being called.
- name: arguments
  type: object
  description: Arguments passed to the tool. Can have any keys/values depending on the tool definition.
- name: provider_info
  type: object
  description: Information about the tool provider. Discriminated union upon possible provider types.
  children:
    - name: Plugin provider info
      type: object
      description: Present when the tool is provided by a plugin.
      children:
        - name: type
          type: '"plugin"'
          description: Provider type.
        - name: plugin_id
          type: string
          description: Identifier of the plugin.
    - name: Ephemeral MCP provider info
      type: object
      description: Present when the tool is provided by a ephemeral MCP server.
      children:
        - name: type
          type: '"ephemeral_mcp"'
          description: Provider type.
        - name: server_label
          type: string
          description: Label of the MCP server.
- name: type
  type: '"tool_call.arguments"'
  description: The type of the event. Always `tool_call.arguments`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.arguments",
        "tool": "model_search",
        "arguments": {
          "sort": "trendingScore",
          "limit": 1
        },
        "provider_info": {
          "type": "ephemeral_mcp",
          "server_label": "huggingface"
        }
      }
```
````

### `tool_call.success`
````lms_hstack
Result of the tool call, along with the arguments used.
```lms_params
- name: tool
  type: string
  description: Name of the tool that was called.
- name: arguments
  type: object
  description: Arguments that were passed to the tool.
- name: output
  type: string
  description: Raw tool output string.
- name: provider_info
  type: object
  description: Information about the tool provider. Discriminated union upon possible provider types.
  children:
    - name: Plugin provider info
      type: object
      description: Present when the tool is provided by a plugin.
      children:
        - name: type
          type: '"plugin"'
          description: Provider type.
        - name: plugin_id
          type: string
          description: Identifier of the plugin.
    - name: Ephemeral MCP provider info
      type: object
      description: Present when the tool is provided by a ephemeral MCP server.
      children:
        - name: type
          type: '"ephemeral_mcp"'
          description: Provider type.
        - name: server_label
          type: string
          description: Label of the MCP server.
- name: type
  type: '"tool_call.success"'
  description: The type of the event. Always `tool_call.success`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.success",
        "tool": "model_search",
        "arguments": {
          "sort": "trendingScore",
          "limit": 1
        },
        "output": "[{\"type\":\"text\",\"text\":\"Showing first 1 models...\"}]",
        "provider_info": {
          "type": "ephemeral_mcp",
          "server_label": "huggingface"
        }
      }
```
````


### `tool_call.failure`
````lms_hstack
Indicates that the tool call failed.
```lms_params
- name: reason
  type: string
  description: Reason for the tool call failure.
- name: metadata
  type: object
  description: Metadata about the invalid tool call.
  children:
    - name: type
      type: '"invalid_name" | "invalid_arguments"'
      description: Type of error that occurred.
    - name: tool_name
      type: string
      description: Name of the tool that was attempted to be called.
    - name: arguments
      type: object
      optional: true
      description: Arguments that were passed to the tool (only present for `invalid_arguments` errors).
    - name: provider_info
      type: object
      optional: true
      description: Information about the tool provider (only present for `invalid_arguments` errors).
      children:
        - name: type
          type: '"plugin" | "ephemeral_mcp"'
          description: Provider type.
        - name: plugin_id
          type: string
          optional: true
          description: Identifier of the plugin (when `type` is `"plugin"`).
        - name: server_label
          type: string
          optional: true
          description: Label of the MCP server (when `type` is `"ephemeral_mcp"`).
- name: type
  type: '"tool_call.failure"'
  description: The type of the event. Always `tool_call.failure`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.failure",
        "reason": "Cannot find tool with name open_browser.",
        "metadata": {
          "type": "invalid_name",
          "tool_name": "open_browser"
        }
      }
```
````

### `message.start`
````lms_hstack
Signals the model is about to stream a message.
```lms_params
- name: type
  type: '"message.start"'
  description: The type of the event. Always `message.start`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "message.start"
      }
```
````

### `message.delta`
````lms_hstack
A chunk of message content. Multiple deltas may arrive.
```lms_params
- name: content
  type: string
  description: Message text fragment.
- name: type
  type: '"message.delta"'
  description: The type of the event. Always `message.delta`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "message.delta",
        "content": "The current"
      }
```
````

### `message.end`
````lms_hstack
Signals the end of the message stream.
```lms_params
- name: type
  type: '"message.end"'
  description: The type of the event. Always `message.end`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "message.end"
      }
```
````

### `error`
````lms_hstack
An error occurred during streaming. The final payload will still be sent in `chat.end` with whatever was generated.
```lms_params
- name: error
  type: object
  description: Error information.
  children:
    - name: type
      type: '"invalid_request" | "unknown" | "mcp_connection_error" | "plugin_connection_error" | "not_implemented" | "model_not_found" | "job_not_found" | "internal_error"'
      description: High-level error type.
    - name: message
      type: string
      description: Human-readable error message.
    - name: code
      type: string
      optional: true
      description: More detailed error code (e.g., validation issue code).
    - name: param
      type: string
      optional: true
      description: Parameter associated with the error, if applicable.
- name: type
  type: '"error"'
  description: The type of the event. Always `error`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "error",
        "error": {
          "type": "invalid_request",
          "message": "\"model\" is required",
          "code": "missing_required_parameter",
          "param": "model"
        }
      }
```
````

### `chat.end`
````lms_hstack
Final event containing the full aggregated response, equivalent to the non-streaming `POST /api/v1/chat` response body.
```lms_params
- name: result
  type: object
  description: Final response with `model_instance_id`, `output`, `stats`, and optional `response_id`. See [non-streaming chat docs](/docs/developer/rest/chat) for more details.
- name: type
  type: '"chat.end"'
  description: The type of the event. Always `chat.end`.
```
:::split:::
```lms_code_snippet
title: Example Event Data
variants:
  json:
    language: json
    code: |
      {
        "type": "chat.end",
        "result": {
          "model_instance_id": "openai/gpt-oss-20b",
          "output": [
            { "type": "reasoning", "content": "Need to call function." },
            {
              "type": "tool_call",
              "tool": "model_search",
              "arguments": { "sort": "trendingScore", "limit": 1 },
              "output": "[{\"type\":\"text\",\"text\":\"Showing first 1 models...\"}]",
              "provider_info": { "type": "ephemeral_mcp", "server_label": "huggingface" }
            },
            { "type": "message", "content": "The current top‑trending model is..." }
          ],
          "stats": {
            "input_tokens": 329,
            "total_output_tokens": 268,
            "reasoning_output_tokens": 5,
            "tokens_per_second": 43.73,
            "time_to_first_token_seconds": 0.781
          },
          "response_id": "resp_02b2017dbc06c12bfc353a2ed6c2b802f8cc682884bb5716"
        }
      }
```
````

````lms_hstack
`POST /api/v1/chat`

**Request body**
```lms_params
- name: model
  type: string
  optional: false
  description: Unique identifier for the model to use.
- name: input
  type: string | array<object>
  optional: false
  description: Message to send to the model.
  children:
    - name: Input text
      unstyledName: true
      type: string
      description: Text content of the message.
    - name: Input object
      unstyledName: true
      type: object
      description: Object representing a message with additional metadata.
      children:
        - name: Text Input
          type: object
          optional: true
          description: Text input to provide user messages
          children:
            - name: type
              type: '"message"'
              optional: false
              description: Type of input item.
            - name: content
              type: string
              description: Text content of the message.
              optional: false
        - name: Image Input
          type: object
          optional: true
          description: Image input to provide user messages
          children:
            - name: type
              type: '"image"'
              optional: false
              description: Type of input item.
            - name: data_url
              type: string
              description: Image data as a base64-encoded data URL.
              optional: false
- name: system_prompt
  type: string
  optional: true
  description: System message that sets model behavior or instructions.
- name: integrations
  type: array<string | object>
  optional: true
  description: List of integrations (plugins, ephemeral MCP servers, etc...) to enable for this request.
  children:
    - name: Plugin id
      unstyledName: true
      type: string
      description: Unique identifier of a plugin to use. Plugins contain `mcp.json` installed MCP servers (id `mcp/<server_label>`). Shorthand for plugin object with no custom configuration.
    - name: Plugin
      unstyledName: true
      type: object
      description: Specification of a plugin to use. Plugins contain `mcp.json` installed MCP servers (id `mcp/<server_label>`).
      children:
        - name: type
          type: '"plugin"'
          optional: false
          description: Type of integration.
        - name: id
          type: string
          optional: false
          description: Unique identifier of the plugin.
        - name: allowed_tools
          type: array<string>
          optional: true
          description: List of tool names the model can call from this plugin. If not provided, all tools from the plugin are allowed.
    - name: Ephemeral MCP server specification
      unstyledName: true
      type: object
      description: Specification of an ephemeral MCP server. Allows defining MCP servers on-the-fly without needing to pre-configure them in your `mcp.json`.
      children:
        - name: type
          type: '"ephemeral_mcp"'
          optional: false
          description: Type of integration.
        - name: server_label
          type: string
          optional: false
          description: Label to identify the MCP server.
        - name: server_url
          type: string
          optional: false
          description: URL of the MCP server.
        - name: allowed_tools
          type: array<string>
          optional: true
          description: List of tool names the model can call from this server. If not provided, all tools from the server are allowed.
        - name: headers
          type: object
          optional: true
          description: Custom HTTP headers to send with requests to the server.
- name: stream
  type: boolean
  optional: true
  description: Whether to stream partial outputs via SSE. Default `false`. See [streaming events](/docs/developer/rest/streaming-events) for more information.
- name: temperature
  type: number
  optional: true
  description: Randomness in token selection. 0 is deterministic, higher values increase creativity [0,1].
- name: top_p
  type: number
  optional: true
  description: Minimum cumulative probability for the possible next tokens [0,1].
- name: top_k
  type: integer
  optional: true
  description: Limits next token selection to top-k most probable tokens.
- name: min_p
  type: number
  optional: true
  description: Minimum base probability for a token to be selected for output [0,1].
- name: repeat_penalty
  type: number
  optional: true
  description: Penalty for repeating token sequences. 1 is no penalty, higher values discourage repetition.
- name: max_output_tokens
  type: integer
  optional: true
  description: Maximum number of tokens to generate.
- name: reasoning
  type: '"off" | "low" | "medium" | "high" | "on"'
  optional: true
  description: Reasoning setting. Will error if the model being used does not support the reasoning setting using. Defaults to the automatically chosen setting for the model.
- name: context_length
  type: integer
  optional: true
  description: Number of tokens to consider as context. Higher values recommended for MCP usage.
- name: store
  type: boolean
  optional: true
  description: Whether to store the chat. If set, response will return a `"response_id"` field. Default `true`.
- name: previous_response_id
  type: string
  optional: true
  description: Identifier of existing response to append to. Must start with `"resp_"`.
```
:::split:::
```lms_code_snippet
variants:
  Request with MCP:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Tell me the top trending model on hugging face and navigate to https://lmstudio.ai",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": [
                "model_search"
              ]
            },
            {
              "type": "plugin",
              "id": "mcp/playwright",
              "allowed_tools": [
                "browser_navigate"
              ]
            }
          ],
          "context_length": 8000,
          "temperature": 0
        }'
  Request with Images:
    language: bash
    code: |
      # Image is a small red square encoded as a base64 data URL
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "qwen/qwen3-vl-4b",
          "input": [
            {
              "type": "text",
              "content": "Describe this image in two sentences"
            },
            {
              "type": "image",
              "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8z8BQz0AEYBxVSF+FABJADveWkH6oAAAAAElFTkSuQmCC"
            }
          ],
          "context_length": 2048,
          "temperature": 0
        }'
```
````

---

````lms_hstack
**Response fields**
```lms_params
- name: model_instance_id
  type: string
  description: Unique identifier for the loaded model instance that generated the response.
- name: output
  type: array<object>
  description: Array of output items generated. Each item can be one of three types.
  children:
    - name: Message
      unstyledName: true
      type: object
      description: A text message from the model.
      children:
        - name: type
          type: '"message"'
          description: Type of output item.
        - name: content
          type: string
          description: Text content of the message.
    - name: Tool call
      unstyledName: true
      type: object
      description: A tool call made by the model.
      children:
        - name: type
          type: '"tool_call"'
          description: Type of output item.
        - name: tool
          type: string
          description: Name of the tool called.
        - name: arguments
          type: object
          description: Arguments passed to the tool. Can have any keys/values depending on the tool definition.
        - name: output
          type: string
          description: Result returned from the tool.
        - name: provider_info
          type: object
          description: Information about the tool provider.
          children:
            - name: type
              type: '"plugin" | "ephemeral_mcp"'
              description: Provider type.
            - name: plugin_id
              type: string
              optional: true
              description: Identifier of the plugin (when `type` is `"plugin"`).
            - name: server_label
              type: string
              optional: true
              description: Label of the MCP server (when `type` is `"ephemeral_mcp"`).
    - name: Reasoning
      unstyledName: true
      type: object
      description: Reasoning content from the model.
      children:
        - name: type
          type: '"reasoning"'
          description: Type of output item.
        - name: content
          type: string
          description: Text content of the reasoning.
    - name: Invalid tool call
      unstyledName: true
      type: object
      description: An invalid tool call made by the model - due to invalid tool name or tool arguments.
      children:
        - name: type
          type: '"invalid_tool_call"'
          description: Type of output item.
        - name: reason
          type: string
          description: Reason why the tool call was invalid.
        - name: metadata
          type: object
          description: Metadata about the invalid tool call.
          children:
            - name: type
              type: '"invalid_name" | "invalid_arguments"'
              description: Type of error that occurred.
            - name: tool_name
              type: string
              description: Name of the tool that was attempted to be called.
            - name: arguments
              type: object
              optional: true
              description: Arguments that were passed to the tool (only present for `invalid_arguments` errors).
            - name: provider_info
              type: object
              optional: true
              description: Information about the tool provider (only present for `invalid_arguments` errors).
              children:
                - name: type
                  type: '"plugin" | "ephemeral_mcp"'
                  description: Provider type.
                - name: plugin_id
                  type: string
                  optional: true
                  description: Identifier of the plugin (when `type` is `"plugin"`).
                - name: server_label
                  type: string
                  optional: true
                  description: Label of the MCP server (when `type` is `"ephemeral_mcp"`).
- name: stats
  type: object
  description: Token usage and performance metrics.
  children:
    - name: input_tokens
      type: number
      description: Number of input tokens. Includes formatting, tool definitions, and prior messages in the chat.
    - name: total_output_tokens
      type: number
      description: Total number of output tokens generated.
    - name: reasoning_output_tokens
      type: number
      description: Number of tokens used for reasoning.
    - name: tokens_per_second
      type: number
      description: Generation speed in tokens per second.
    - name: time_to_first_token_seconds
      type: number
      description: Time in seconds to generate the first token.
    - name: model_load_time_seconds
      type: number
      optional: true
      description: Time taken to load the model for this request in seconds. Present only if the model was not already loaded.
- name: response_id
  type: string
  optional: true
  description: Identifier of the response for subsequent requests. Starts with `"resp_"`. Present when `store` is `true`.
```
:::split:::
```lms_code_snippet
variants:
  Request with MCP:
    language: json
    code: |
      {
        "model_instance_id": "ibm/granite-4-micro",
        "output": [
          {
            "type": "tool_call",
            "tool": "model_search",
            "arguments": {
              "sort": "trendingScore",
              "query": "",
              "limit": 1
            },
            "output": "...",
            "provider_info": {
              "server_label": "huggingface",
              "type": "ephemeral_mcp"
            }
          },
          {
            "type": "message",
            "content": "..."
          },
          {
            "type": "tool_call",
            "tool": "browser_navigate",
            "arguments": {
              "url": "https://lmstudio.ai"
            },
            "output": "...",
            "provider_info": {
              "plugin_id": "mcp/playwright",
              "type": "plugin"
            }
          },
          {
            "type": "message",
            "content": "**Top Trending Model on Hugging Face** ... Below is a quick snapshot of what’s on the landing page ... more details on the model or LM Studio itself!"
          }
        ],
        "stats": {
          "input_tokens": 646,
          "total_output_tokens": 586,
          "reasoning_output_tokens": 0,
          "tokens_per_second": 29.753900615398926,
          "time_to_first_token_seconds": 1.088,
          "model_load_time_seconds": 2.656
        },
        "response_id": "resp_4ef013eba0def1ed23f19dde72b67974c579113f544086de"
      }
  Request with Images:
    language: json
    code: |
      {
        "model_instance_id": "qwen/qwen3-vl-4b",
        "output": [
          {
            "type": "message",
            "content": "This image is a solid, vibrant red square that fills the entire frame, with no discernible texture, pattern, or other elements. It presents a minimalist, uniform visual field of pure red, evoking a sense of boldness or urgency."
          }
        ],
        "stats": {
          "input_tokens": 17,
          "total_output_tokens": 50,
          "reasoning_output_tokens": 0,
          "tokens_per_second": 51.03762685242662,
          "time_to_first_token_seconds": 0.814
        },
        "response_id": "resp_0182bd7c479d7451f9a35471f9c26b34de87a7255856b9a4"
      }
```
````

````lms_hstack
`GET /api/v1/models`

This endpoint has no request parameters.
:::split:::
```lms_code_snippet
title: Example Request
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models \
        -H "Authorization: Bearer $LM_API_TOKEN"
```
````

---

````lms_hstack
**Response fields**
```lms_params
- name: models
  type: array
  description: List of available models (both LLMs and embedding models).
  children:
    - name: type
      type: '"llm" | "embedding"'
      description: Type of model.
    - name: publisher
      type: string
      description: Model publisher name.
    - name: key
      type: string
      description: Unique identifier for the model.
    - name: display_name
      type: string
      description: Human-readable model name.
    - name: architecture
      type: string | null
      optional: true
      description: Model architecture (e.g., "llama", "mistral"). Absent for embedding models.
    - name: quantization
      type: object | null
      description: Quantization information for the model.
      children:
        - name: name
          type: string | null
          description: Quantization method name.
        - name: bits_per_weight
          type: number | null
          description: Bits per weight for the quantization.
    - name: size_bytes
      type: number
      description: Size of the model in bytes.
    - name: params_string
      type: string | null
      description: Human-readable parameter count (e.g., "7B", "13B").
    - name: loaded_instances
      type: array
      description: List of currently loaded instances of this model.
      children:
        - name: id
          type: string
          description: Unique identifier for the loaded model instance.
        - name: config
          type: object
          description: Configuration for the loaded instance.
          children:
            - name: context_length
              type: number
              description: The maximum context length for the model in number of tokens.
            - name: eval_batch_size
              type: number
              optional: true
              description: Number of input tokens to process together in a single batch during evaluation. Absent for embedding models.
            - name: flash_attention
              type: boolean
              optional: true
              description: Whether Flash Attention is enabled for optimized attention computation. Absent for embedding models.
            - name: num_experts
              type: number
              optional: true
              description: Number of experts for MoE (Mixture of Experts) models. Absent for embedding models.
            - name: offload_kv_cache_to_gpu
              type: boolean
              optional: true
              description: Whether KV cache is offloaded to GPU memory. Absent for embedding models.
    - name: max_context_length
      type: number
      description: Maximum context length supported by the model in number of tokens.
    - name: format
      type: '"gguf" | "mlx" | null'
      description: Model file format.
    - name: capabilities
      type: object
      optional: true
      description: Model capabilities. Absent for embedding models.
      children:
        - name: vision
          type: boolean
          description: Whether the model supports vision/image inputs.
        - name: trained_for_tool_use
          type: boolean
          description: Whether the model was trained for tool/function calling.
    - name: description
      type: string | null
      optional: true
      description: Model description. Absent for embedding models.
```
:::split:::
```lms_code_snippet
title: Response
variants:
  json:
    language: json
    code: |
      {
        "models": [
          {
            "type": "llm",
            "publisher": "lmstudio-community",
            "key": "gemma-3-270m-it-qat",
            "display_name": "Gemma 3 270m Instruct Qat",
            "architecture": "gemma3",
            "quantization": {
              "name": "Q4_0",
              "bits_per_weight": 4
            },
            "size_bytes": 241410208,
            "params_string": "270M",
            "loaded_instances": [
              {
                "id": "gemma-3-270m-it-qat",
                "config": {
                  "context_length": 4096,
                  "eval_batch_size": 512,
                  "flash_attention": false,
                  "num_experts": 0,
                  "offload_kv_cache_to_gpu": true
                }
              }
            ],
            "max_context_length": 32768,
            "format": "gguf",
            "capabilities": {
              "vision": false,
              "trained_for_tool_use": false
            },
            "description": null
          },
          {
            "type": "embedding",
            "publisher": "gaianet",
            "key": "text-embedding-nomic-embed-text-v1.5-embedding",
            "display_name": "Nomic Embed Text v1.5",
            "quantization": {
              "name": "F16",
              "bits_per_weight": 16
            },
            "size_bytes": 274290560,
            "params_string": null,
            "loaded_instances": [],
            "max_context_length": 2048,
            "format": "gguf"
          }
        ]
      }
```
````
````lms_hstack
`POST /api/v1/models/load`

**Request body**
```lms_params
- name: model
  type: string
  optional: false
  description: Unique identifier for the model to load. Can be an LLM or embedding model.
- name: context_length
  type: number
  optional: true
  description: Maximum number of tokens that the model will consider.
- name: eval_batch_size
  type: number
  optional: true
  description: Number of input tokens to process together in a single batch during evaluation. Will only have an effect on LLMs loaded by LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
- name: flash_attention
  type: boolean
  optional: true
  description: Whether to optimize attention computation. Can decrease memory usage and improved generation speed. Will only have an effect on LLMs loaded by LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
- name: num_experts
  type: number
  optional: true
  description: Number of expert to use during inference for MoE (Mixture of Experts) models. Will only have an effect on MoE LLMs loaded by LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
- name: offload_kv_cache_to_gpu
  type: boolean
  optional: true
  description: Whether KV cache is offloaded to GPU memory. If false, KV cache is stored in CPU memory/RAM. Will only have an effect on LLMs loaded by LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
- name: echo_load_config
  type: boolean
  optional: true
  description: If true, echoes the final load configuration in the response under `"load_config"`. Default `false`.
```
:::split:::
```lms_code_snippet
title: Example Request
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/load \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "openai/gpt-oss-20b",
          "context_length": 16384,
          "flash_attention": true,
          "echo_load_config": true
        }'
```
````

---

````lms_hstack
**Response fields**
```lms_params
- name: type
  type: '"llm" | "embedding"'
  description: Type of the loaded model.
- name: instance_id
  type: string
  description: Unique identifier for the loaded model instance.
- name: load_time_seconds
  type: number
  description: Time taken to load the model in seconds.
- name: status
  type: '"loaded"'
  description: Load status.
- name: load_config
  type: object
  optional: true
  description: The final configuration applied to the loaded model. This may include settings that were not specified in the request. Included only when `"echo_load_config"` is `true` in the request.
  children:
    - name: LLM load config
      unstyledName: true
      type: object
      description: Configuration parameters specific to LLM models. `load_config` will be this type when `"type"` is `"llm"`. Only parameters that applied to the load will be present.
      children:
        - name: context_length
          type: number
          optional: false
          description: Maximum number of tokens that the model will consider.
        - name: eval_batch_size
          type: number
          optional: true
          description: Number of input tokens to process together in a single batch during evaluation. Only present for models loaded with LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
        - name: flash_attention
          type: boolean
          optional: true
          description: Whether Flash Attention is enabled for optimized attention computation. Only present for models loaded with LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
        - name: num_experts
          type: number
          optional: true
          description: Number of experts for MoE (Mixture of Experts) models. Only present for MoE models loaded with LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
        - name: offload_kv_cache_to_gpu
          type: boolean
          optional: true
          description: Whether KV cache is offloaded to GPU memory. Only present for models loaded with LM Studio's [llama.cpp](https://github.com/ggml-org/llama.cpp)-based engine.
    - name: Embedding model load config
      unstyledName: true
      type: object
      description: Configuration parameters specific to embedding models. `load_config` will be this type when `"type"` is `"embedding"`. Only parameters that applied to the load will be present.
      children:
        - name: context_length
          type: number
          optional: false
          description: Maximum number of tokens that the model will consider.
```
:::split:::
```lms_code_snippet
title: Response
variants:
  json:
    language: json
    code: |
      {
        "type": "llm",
        "instance_id": "openai/gpt-oss-20b",
        "load_time_seconds": 9.099,
        "status": "loaded",
        "load_config": {
          "context_length": 16384,
          "eval_batch_size": 512,
          "flash_attention": true,
          "offload_kv_cache_to_gpu": true,
          "num_experts": 4
        }
      }
```
````

````lms_hstack
`POST /api/v1/models/download`

**Request body**
```lms_params
- name: model
  type: string
  optional: false
  description: The model to download. Accepts [model catalog](https://lmstudio.ai/models) identifiers (e.g., `openai/gpt-oss-20b`) and exact Hugging Face links (e.g., `https://huggingface.co/lmstudio-community/gpt-oss-20b-GGUF`)
- name: quantization
  type: string
  optional: true
  description: Quantization level of the model to download (e.g., `Q4_K_M`). Only supported for Hugging Face links.
```
:::split:::
```lms_code_snippet
title: Example Request
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/download \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro"
        }'
```
````

````lms_hstack
**Response fields**

Returns a download job status object. The response varies based on the download status.

```lms_params
- name: job_id
  type: string
  optional: true
  description: Unique identifier for the download job. Absent when `status` is `already_downloaded`.
- name: status
  type: '"downloading" | "paused" | "completed" | "failed" | "already_downloaded"'
  description: Current status of the download.
- name: completed_at
  type: string
  optional: true
  description: Download completion time in ISO 8601 format. Present when `status` is `completed`.
- name: total_size_bytes
  type: number
  optional: true
  description: Total size of the download in bytes. Absent when `status` is `already_downloaded`.
- name: started_at
  type: string
  optional: true
  description: Download start time in ISO 8601 format. Absent when `status` is `already_downloaded`.
```
:::split:::
```lms_code_snippet
title: Response
variants:
  json:
    language: json
    code: |
      {
        "job_id": "job_493c7c9ded",
        "status": "downloading",
        "total_size_bytes": 2279145003,
        "started_at": "2025-10-03T15:33:23.496Z"
      }
```
````
````lms_hstack
`POST /api/v1/models/unload`

**Request body**
```lms_params
- name: instance_id
  type: string
  optional: false
  description: Unique identifier of the model instance to unload.
```
:::split:::
```lms_code_snippet
title: Example Request
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/unload \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "instance_id": "openai/gpt-oss-20b"
        }'
```
````

---

````lms_hstack
**Response fields**
```lms_params
- name: instance_id
  type: string
  description: Unique identifier for the unloaded model instance.
```
:::split:::
```lms_code_snippet
title: Response
variants:
  json:
    language: json
    code: |
      {
        "instance_id": "openai/gpt-oss-20b"
      }
```
````
````lms_hstack
`POST /api/v1/models/unload`

**Request body**
```lms_params
- name: instance_id
  type: string
  optional: false
  description: Unique identifier of the model instance to unload.
```
:::split:::
```lms_code_snippet
title: Example Request
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/unload \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "instance_id": "openai/gpt-oss-20b"
        }'
```
````

---

````lms_hstack
**Response fields**
```lms_params
- name: instance_id
  type: string
  description: Unique identifier for the unloaded model instance.
```
:::split:::
```lms_code_snippet
title: Response
variants:
  json:
    language: json
    code: |
      {
        "instance_id": "openai/gpt-oss-20b"
      }
```
````

```lms_warning
LM Studio now has a [v1 REST API](/docs/developer/rest)! We recommend using the v1 API for new projects!
```

##### Requires [LM Studio 0.3.6](/download) or newer.

LM Studio now has its own REST API, in addition to OpenAI-compatible endpoints ([learn more](/docs/developer/openai-compat)) and Anthropic-compatible endpoints ([learn more](/docs/developer/anthropic-compat)).

The REST API includes enhanced stats such as Token / Second and Time To First Token (TTFT), as well as rich information about models such as loaded vs unloaded, max context, quantization, and more.

#### Supported API Endpoints

- [`GET /api/v0/models`](#get-apiv0models) - List available models
- [`GET /api/v0/models/{model}`](#get-apiv0modelsmodel) - Get info about a specific model
- [`POST /api/v0/chat/completions`](#post-apiv0chatcompletions) - Chat Completions (messages -> assistant response)
- [`POST /api/v0/completions`](#post-apiv0completions) - Text Completions (prompt -> completion)
- [`POST /api/v0/embeddings`](#post-apiv0embeddings) - Text Embeddings (text -> embedding)

---

### Start the REST API server

To start the server, run the following command:

```bash
lms server start
```

```lms_protip
You can run LM Studio as a service and get the server to auto-start on boot without launching the GUI. [Learn about Headless Mode](/docs/developer/core/headless).
```

## Endpoints

### `GET /api/v0/models`

List all loaded and downloaded models

**Example request**

```bash
curl -H "Authorization: Bearer $LM_API_TOKEN" http://localhost:1234/api/v0/models
```

**Response format**

```json
{
  "object": "list",
  "data": [
    {
      "id": "qwen2-vl-7b-instruct",
      "object": "model",
      "type": "vlm",
      "publisher": "mlx-community",
      "arch": "qwen2_vl",
      "compatibility_type": "mlx",
      "quantization": "4bit",
      "state": "not-loaded",
      "max_context_length": 32768
    },
    {
      "id": "meta-llama-3.1-8b-instruct",
      "object": "model",
      "type": "llm",
      "publisher": "lmstudio-community",
      "arch": "llama",
      "compatibility_type": "gguf",
      "quantization": "Q4_K_M",
      "state": "not-loaded",
      "max_context_length": 131072
    },
    {
      "id": "text-embedding-nomic-embed-text-v1.5",
      "object": "model",
      "type": "embeddings",
      "publisher": "nomic-ai",
      "arch": "nomic-bert",
      "compatibility_type": "gguf",
      "quantization": "Q4_0",
      "state": "not-loaded",
      "max_context_length": 2048
    }
  ]
}
```

---

### `GET /api/v0/models/{model}`

Get info about one specific model

**Example request**

```bash
curl -H "Authorization: Bearer $LM_API_TOKEN" http://localhost:1234/api/v0/models/qwen2-vl-7b-instruct
```

**Response format**

```json
{
  "id": "qwen2-vl-7b-instruct",
  "object": "model",
  "type": "vlm",
  "publisher": "mlx-community",
  "arch": "qwen2_vl",
  "compatibility_type": "mlx",
  "quantization": "4bit",
  "state": "not-loaded",
  "max_context_length": 32768
}
```

---

### `POST /api/v0/chat/completions`

Chat Completions API. You provide a messages array and receive the next assistant response in the chat.

**Example request**

```bash
curl http://localhost:1234/api/v0/chat/completions \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "granite-3.0-2b-instruct",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes." },
      { "role": "user", "content": "Introduce yourself." }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
  }'
```

**Response format**

```json
{
  "id": "chatcmpl-i3gkjwthhw96whukek9tz",
  "object": "chat.completion",
  "created": 1731990317,
  "model": "granite-3.0-2b-instruct",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "Greetings, I'm a helpful AI, here to assist,\nIn providing answers, with no distress.\nI'll keep it short and sweet, in rhyme you'll find,\nA friendly companion, all day long you'll bind."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 24,
    "completion_tokens": 53,
    "total_tokens": 77
  },
  "stats": {
    "tokens_per_second": 51.43709529007664,
    "time_to_first_token": 0.111,
    "generation_time": 0.954,
    "stop_reason": "eosFound"
  },
  "model_info": {
    "arch": "granite",
    "quant": "Q4_K_M",
    "format": "gguf",
    "context_length": 4096
  },
  "runtime": {
    "name": "llama.cpp-mac-arm64-apple-metal-advsimd",
    "version": "1.3.0",
    "supported_formats": ["gguf"]
  }
}
```

---

### `POST /api/v0/completions`

Text Completions API. You provide a prompt and receive a completion.

**Example request**

```bash
curl http://localhost:1234/api/v0/completions \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "granite-3.0-2b-instruct",
    "prompt": "the meaning of life is",
    "temperature": 0.7,
    "max_tokens": 10,
    "stream": false,
    "stop": "\n"
  }'
```

**Response format**

```json
{
  "id": "cmpl-p9rtxv6fky2v9k8jrd8cc",
  "object": "text_completion",
  "created": 1731990488,
  "model": "granite-3.0-2b-instruct",
  "choices": [
    {
      "index": 0,
      "text": " to find your purpose, and once you have",
      "logprobs": null,
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 9,
    "total_tokens": 14
  },
  "stats": {
    "tokens_per_second": 57.69230769230769,
    "time_to_first_token": 0.299,
    "generation_time": 0.156,
    "stop_reason": "maxPredictedTokensReached"
  },
  "model_info": {
    "arch": "granite",
    "quant": "Q4_K_M",
    "format": "gguf",
    "context_length": 4096
  },
  "runtime": {
    "name": "llama.cpp-mac-arm64-apple-metal-advsimd",
    "version": "1.3.0",
    "supported_formats": ["gguf"]
  }
}
```

---

### `POST /api/v0/embeddings`

Text Embeddings API. You provide a text and a representation of the text as an embedding vector is returned.

**Example request**

```bash
curl http://localhost:1234/api/v0/embeddings \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-nomic-embed-text-v1.5",
    "input": "Some text to embed"
  }
```

**Example response**

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        -0.016731496900320053,
        0.028460891917347908,
        -0.1407836228609085,
        ... (truncated for brevity) ...,
        0.02505224384367466,
        -0.0037634256295859814,
        -0.04341062530875206
      ],
      "index": 0
    }
  ],
  "model": "text-embedding-nomic-embed-text-v1.5@q4_k_m",
  "usage": {
    "prompt_tokens": 0,
    "total_tokens": 0
  }
}
```

---

Please report bugs by opening an issue on [Github](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues).
