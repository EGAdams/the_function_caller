from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python", # Executable
    args=["server.py"], # Optional command line arguments
    env=None # Optional environment variables
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            try:
                # List available prompts
                prompts = await session.list_prompts()
                print("\nAvailable prompts:")
                
                # Debug print to see what we're getting
                print(f"Type of prompts: {type(prompts)}")
                print(f"Content of prompts: {prompts}")
                
                # Safely access prompt attributes
                for prompt in prompts:
                    try:
                        print(f"\nPrompt details:")
                        print(f"Name: {getattr(prompt, 'name', 'N/A')}")
                        print(f"Description: {getattr(prompt, 'description', 'N/A')}")
                        print("Arguments:")
                        for arg in getattr(prompt, 'arguments', []):
                            print(f"  - {arg.name}: {arg.description} (Required: {arg.required})")
                    except Exception as e:
                        print(f"Error processing prompt: {e}")
                        print(f"Prompt data: {prompt}")

            except Exception as e:
                print(f"Error: {e}")
                raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
