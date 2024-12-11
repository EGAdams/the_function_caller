import asyncio
import json
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types

from openai import OpenAI

server = Server("prompt-agent-server")
GPT_MODEL = "gpt-3.5-turbo-0125"

class PromptAgent:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []
        self.tools = []
        # Initialize self.tools if you have any tools.

    def process_message(self, new_message: dict) -> dict:
        self.messages.append(new_message)
        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto"
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            self.messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_response = self.execute_function(function_name, function_args)
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
            second_response = self.client.chat.completions.create(
                model=GPT_MODEL,
                messages=self.messages,
            )
            return second_response.choices[0].message
        else:
            self.messages.append(response_message)
            return response_message

    def execute_function(self, function_name: str, function_args: dict) -> str:
        # Implement function execution logic
        return f"Executed {function_name} with args {function_args}"

prompt_agent = PromptAgent()

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="greeting-prompt",
            description="A simple greeting prompt",
            arguments=[]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str]|None) -> types.GetPromptResult:
    if name == "greeting-prompt":
        return types.GetPromptResult(
            description="A greeting prompt",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(type="text", text="Hello, how can I help you?")
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="process_user_message",
            description="Process a user message through the agent",
            inputSchema={"type": "object", "properties": {"text": {"type": "string"}}},
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "process_user_message":
        user_input = arguments.get("text", "")
        user_message = {"role": "user", "content": user_input}
        final_response = prompt_agent.process_message(user_message)
        content_text = final_response["content"]
        return [types.TextContent(type="text", text=content_text)]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="prompt-agent",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
