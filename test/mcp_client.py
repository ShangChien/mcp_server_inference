import asyncio
from fastmcp import Client, FastMCP
from  config import config

# In-memory server (ideal for testing)
server = FastMCP("TestServer")
client = Client(config)

# # HTTP server
# client = Client("https://example.com/mcp")

# # Local Python script
# client = Client("my_mcp_server.py")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # # List available operations
        tools = await client.list_tools()
        for tool in tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            if tool.inputSchema:
                print(f"Parameters: {tool.inputSchema}")

        resources = await client.list_resources()
        for resource in resources:
            print(f"Resource URI: {resource.uri}")
            print(f"Name: {resource.name}")
            print(f"Description: {resource.description}")
            print(f"MIME Type: {resource.mimeType}")

            
        # prompts = await client.list_prompts()


        
        # Execute operations
        result = await client.call_tool(
            "NMR_predict",
            {'data': {"smiles_list": ["CN1C=NC2=C1C(=O)N(C(=O)N2C)C"]}}
        )
        print(result)

asyncio.run(main())