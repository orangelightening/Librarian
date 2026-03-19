These are from openai not lmstudio

# Developer quickstart

Take your first steps with the OpenAI API.

The OpenAI API provides a simple interface to state-of-the-art AI [models](https://developers.openai.com/api/docs/models) for text generation, natural language processing, computer vision, and more. Get started by creating an API Key and running your first API call. Discover how to generate text, analyze images, build agents, and more.

## Create and export an API key

[](https://platform.openai.com/api-keys)

Before you begin, create an API key in the dashboard, which you’ll use to securely [access the API](https://developers.openai.com/api/docs/api-reference/authentication). Store the key in a safe location, like a [`.zshrc` file](https://www.freecodecamp.org/news/how-do-zsh-configuration-files-work/) or another text file on your computer. Once you’ve generated an API key, export it as an [environment variable](https://en.wikipedia.org/wiki/Environment_variable) in your terminal.

macOS / LinuxWindows

Export an environment variable on macOS or Linux systems

```
export OPENAI_API_KEY="your_api_key_here"
```

OpenAI SDKs are configured to automatically read your API key from the system environment.

## Install the OpenAI SDK and Run an API Call

JavaScriptPython.NETJavaGo

To use the OpenAI API in Python, you can use the official [OpenAI SDK for Python](https://github.com/openai/openai-python). Get started by installing the SDK using [pip](https://pypi.org/project/pip/):

Install the OpenAI SDK with pip

```
pip install openai
```

With the OpenAI SDK installed, create a file called `example.py` and copy the example code into it:

Test a basic API request

```
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```

Execute the code with `python example.py`. In a few moments, you should see the output of your API request.

[

Learn more on GitHub

Discover more SDK capabilities and options on the library’s GitHub README.







](https://github.com/openai/openai-python)

[

Responses starter app

Start building with the Responses API.







](https://github.com/openai/openai-responses-starter-app)[

Text generation and prompting

Learn more about prompting, message roles, and building conversational apps.







](https://developers.openai.com/api/docs/guides/text)

## Add credits to keep building

[](https://platform.openai.com/account/billing/overview)

Congrats on running a free test API request! Start building real applications with higher limits and use [our models](https://developers.openai.com/api/docs/models) to generate text, audio, images, videos and more.

Access dashboard features designed to help you ship faster:

[

Chat Playground

Build & test conversational prompts and embed them in your app.







](https://platform.openai.com/chat)[

Agent Builder

Build, deploy, and optimize agent workflows.







](https://platform.openai.com/agent-builder)

## Analyze images and files

Send image URLs, uploaded files, or PDF documents directly to the model to extract text, classify content, or detect visual elements.

Image URLFile URLUpload file

Analyze the content of an image

```
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    input: [
        {
            role: "user",
            content: [
                {
                    type: "input_text",
                    text: "What is in this image?",
                },
                {
                    type: "input_image",
                    image_url: "https://openai-documentation.vercel.app/images/cat_and_otter.png",
                },
            ],
        },
    ],
});

console.log(response.output_text);
```

[

Image inputs guide

Learn to use image inputs to the model and extract meaning from images.







](https://developers.openai.com/api/docs/guides/images) [

File inputs guide

Learn to use file inputs to the model and extract meaning from documents.







](https://developers.openai.com/api/docs/guides/file-inputs)

## Extend the model with tools

Give the model access to external data and functions by attaching [tools](https://developers.openai.com/api/docs/guides/tools). Use built-in tools like web search or file search, or define your own for calling APIs, running code, or integrating with third-party systems.

Web searchFile searchFunction callingRemote MCP

Use web search in a response

```
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    tools: [
        { type: "web_search" },
    ],
    input: "What was a positive news story from today?",
});

console.log(response.output_text);
```

[

Use built-in tools

Learn about powerful built-in tools like web search and file search.







](https://developers.openai.com/api/docs/guides/tools) [

Function calling guide

Learn to enable the model to call your own custom code.







](https://developers.openai.com/api/docs/guides/function-calling)

## Stream responses and build realtime apps

Use server‑sent [streaming events](https://developers.openai.com/api/docs/guides/streaming-responses) to show results as they’re generated, or the [Realtime API](https://developers.openai.com/api/docs/guides/realtime) for interactive voice and multimodal apps.

Stream server-sent events from the API

```
import { OpenAI } from "openai";
const client = new OpenAI();

const stream = await client.responses.create({
    model: "gpt-5",
    input: [
        {
            role: "user",
            content: "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream: true,
});

for await (const event of stream) {
    console.log(event);
}
```

[

Use streaming events

Use server-sent events to stream model responses to users fast.







](https://developers.openai.com/api/docs/guides/streaming-responses) [

Get started with the Realtime API

Use WebRTC or WebSockets for super fast speech-to-speech AI apps.







](https://developers.openai.com/api/docs/guides/realtime)

## Build agents

Use the OpenAI platform to build [agents](https://developers.openai.com/api/docs/guides/agents) capable of taking action—like [controlling computers](https://developers.openai.com/api/docs/guides/tools-computer-use)—on behalf of your users. Use the Agents SDK for [Python](https://openai.github.io/openai-agents-python) or [TypeScript](https://openai.github.io/openai-agents-js) to create orchestration logic on the backend.

Build a language triage agent

```
import { Agent, run } from '@openai/agents';

const spanishAgent = new Agent({
    name: 'Spanish agent',
    instructions: 'You only speak Spanish.',
});

const englishAgent = new Agent({
    name: 'English agent',
    instructions: 'You only speak English',
});

const triageAgent = new Agent({
    name: 'Triage agent',
    instructions:
        'Handoff to the appropriate agent based on the language of the request.',
    handoffs: [spanishAgent, englishAgent],
});

const result = await run(triageAgent, 'Hola, ¿cómo estás?');
console.log(result.finalOutput);
```

[

Build agents that can take action

Learn how to use the OpenAI platform to build powerful, capable AI agents.







](https://developers.openai.com/api/docs/guides/agents)