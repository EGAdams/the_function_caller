import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Replace 'node' and 'filesystem_server.js' with the actual command you use
    # to run the server if needed. If your server’s filename differs, use that.
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/home/eg1972/the_function_caller/mcp_client_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            print("Connected to MCP Filesystem Server.")
            print("Type 'list_tools' to see available tools, or 'quit' to exit.")
            
            while True:
                user_input = input("You> ")
                if user_input.strip().lower() == 'quit':
                    break

                # A simple command parser:
                # - "list_tools" -> call session.list_tools()
                # - "tool name {args}" -> call the tool with JSON args
                # Example: call a tool like: "tool read_file {\"path\": \"./somefile.txt\"}"

                if user_input.strip().lower() == 'list_tools':
                    tools = await session.list_tools()
                    print("Tools available:")
                    for name, description in tools:
                        print(f"- {name}: {description}")

                    continue
                
                if user_input.startswith("tool "):
                    # Format: tool toolname {json-args}
                    # Example: tool read_file {"path":"./file.txt"}
                    parts = user_input.split(" ", 2)
                    if len(parts) < 3:
                        print("Invalid tool command. Format: tool <name> <json-args>")
                        continue
                    tool_name = parts[1]
                    args_str = parts[2]

                    import json
                    try:
                        tool_args = json.loads(args_str)
                    except json.JSONDecodeError:
                        print("Invalid JSON for tool arguments.")
                        continue

                    # Call the tool
                    try:
                        
                        result = await session.call_tool(tool_name, tool_args)

                        # 'result' is a CallToolResult object, which has a 'content' attribute
                        for c in result.content:
                            # Each 'c' is a content item object with 'type' and 'text' attributes
                            if c.type == "text":
                                print(c.text)
                            else:
                                print(f"[{c.type}] {c.text}")


                    except Exception as e:
                        print(f"Error calling tool: {e}")
                    continue

                print("Unrecognized command. Type 'list_tools' or 'quit'.")

            print("Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())
