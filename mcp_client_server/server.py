# /// script
# dependencies = [
#   "mcp"
# ]
# ///
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Create a server instance
server = Server("server")

# Add prompt capabilities
@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="code-review",
            description="A prompt template for code review",
            arguments=[
                types.PromptArgument(
                    name="language",
                    description="Programming language of the code",
                    required=True
                ),
                types.PromptArgument(
                    name="code_snippet",
                    description="Code to review",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str,
    arguments: dict[str, str] | None
) -> types.GetPromptResult:
    prompts = {
        "code-review": {
            "description": "Code Review Assistant",
            "template": f"Please review this {arguments.get('language')} code:\n\n\n{arguments.get('code_snippet')}\n\n\nProvide feedback on:",
        },
        "bug-analysis": {
            "description": "Bug Analysis Helper",
            "template": f"Error Message:\n{arguments.get('error_message')}\n\nContext:\n{arguments.get('context', 'No additional context provided')}\n\nAnalyze this error and suggest solutions."
        }
    }

    if name not in prompts:
        raise ValueError(f"Unknown prompt: {name}")

    return types.GetPromptResult(
        description=prompts[name]["description"],
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=prompts[name]["template"]
                )
            )
        ]
    )
async def run():
    # Run the server as STDIO
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())