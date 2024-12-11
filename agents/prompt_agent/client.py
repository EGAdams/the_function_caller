import asyncio
from mcp import ClientSession, SseServerParameters
from mcp.client.sse import sse_client

async def main():
    # Connect to the SSE server at localhost:8080
    server_params = SseServerParameters(url="http://localhost:8080/")
    
    # This opens a session with the SSE MCP server
    async with sse_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Now you can call MCP methods like list_prompts()
            prompts = await session.list_prompts()
            print("Prompts:", prompts)

            # Get a specific prompt
            prompt = await session.get_prompt("greeting-prompt", arguments={})
            print("Prompt:", prompt)

            # If you created a pseudo-tool named "process_user_message", you can call it:
            # Example: Passing a user message to the agent
            result = await session.call_tool("process_user_message", {"text": "Hi there"})
            # 'result' will contain the assistant's response
            for content in result:
                if content.type == "text":
                    print("Assistant Response:", content.text)

asyncio.run(main())
