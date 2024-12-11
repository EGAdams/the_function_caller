import asyncio
import json
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.sse import sse_server
import mcp.types as types

from openai import OpenAI

server = Server("prompt-agent-server")
GPT_MODEL = "gpt-3.5-turbo-0125"

class PromptAgent:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []    # Stores the conversation messages
        self.tools = []       # Tool schemas if you have them
        # Initialize self.tools with your tool schemas as before.

    def process_message(self, new_message: dict) -> dict:
        """
        Process incoming user or tool messages.
        This replicates the logic you previously had:
        - Append to self.messages
        - Call OpenAI with self.messages and self.tools
        - If tool calls requested, execute them, then call OpenAI again
        - Return final assistant message as a dict
        """
        self.messages.append(new_message)

        # First OpenAI call
        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            # Model requested tool calls
            self.messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the tool function
                function_response = self.execute_function(function_name, function_args)

                # Append the tool response to messages
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

            # Second OpenAI call after tool responses
            second_response = self.client.chat.completions.create(
                model=GPT_MODEL,
                messages=self.messages,
            )
            return second_response.choices[0].message
        else:
            # No tool calls; just append assistant response
            self.messages.append(response_message)
            return response_message

    def execute_function(self, function_name: str, function_args: dict) -> str:
        # Implement function execution logic as before
        # This should match your function_executor logic from the old code
        return f"Executed {function_name} with args {function_args}"

prompt_agent = PromptAgent()

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    # Just an example. In reality, prompts might be dynamic.
    return [
        types.Prompt(
            name="greeting-prompt",
            description="A simple greeting prompt",
            arguments=[]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    if name == "greeting-prompt":
        # Return a fixed prompt. After the client receives this prompt,
        # they may send user input in another request (e.g., a custom handler)
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

# Example custom endpoint to handle user queries and run `process_message()`
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    # For example, let's say name="process_user_message" is a pseudo-tool to process user input
    if name == "process_user_message":
        user_input = arguments.get("text", "")
        user_message = {"role": "user", "content": user_input}
        final_response = prompt_agent.process_message(user_message)

        # final_response is a dict like {"role":"assistant","content":"..."} from OpenAI
        content_text = final_response["content"]
        return [types.TextContent(type="text", text=content_text)]
    else:
        raise ValueError(f"Unknown pseudo-tool: {name}")

async def main():
    async with sse_server(host="localhost", port=8080) as (read_stream, write_stream):
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
