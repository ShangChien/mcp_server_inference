import asyncio
from fastmcp import Client, FastMCP
from  config import config

# In-memory server (ideal for testing)
server = FastMCP("TestServer")
client = Client(config)

class Example:
    smiles = "Cc1ccccc1CC#CC(O)c1ccccc1C"
    h_shifts = [2.16, 2.29, 2.29, 2.29, 2.41, 2.41, 2.41, 3.58, 3.58, 5.63, 7.17, 7.17, 7.17, 7.17, 7.17, 7.17, 7.39, 7.64]
    c_shifts = [19.1, 19.4, 23.5, 62.7, 82.1, 84.5, 126.27, 126.3, 126.5, 127, 128.36, 128.41, 130.2, 130.8, 134.8, 135.98, 136.02, 138.9]
    allowed_elements = ['C', 'H', 'O', 'N']
    formula = "C18H18O"
    topk = 5

example = Example()


async def main():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # Description of tools
        tools = await client.list_tools()
        for tool in tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            if tool.inputSchema:
                print(f"Parameters: {tool.inputSchema}")

        # resources = await client.list_resources()
        # for resource in resources:
        #     print(f"Resource URI: {resource.uri}")
        #     print(f"Name: {resource.name}")
        #     print(f"Description: {resource.description}")
        #     print(f"MIME Type: {resource.mimeType}")

        
        # forward prediction
        result = await client.call_tool(
            "NMR_predict",
            {'data': {
                "smiles_list": [example.smiles],
                "H_shifts": example.h_shifts,
                "C_shifts": example.c_shifts
                }
            }
        )
        print(result)
        
        # # database search
        # result = await client.call_tool(
        #     "NMR_search",
        #     {'data': {
        #         "H_shifts": example.h_shifts,
        #         "C_shifts": example.c_shifts,
        #         "allowed_elements": example.allowed_elements,
        #         "topk": example.topk
        #         }
        #     }
        # )
        # print(result)
        
        # # reverse prediction
        # result = await client.call_tool(
        #     "NMR_reverse_predict",
        #     {'data': {
        #         "H_shifts": example.h_shifts,
        #         "C_shifts": example.c_shifts,
        #         "allowed_elements": example.allowed_elements,
        #         "formula": example.formula,
        #         "topk": example.topk
        #         }
        #     }
        # )
        # print(result)

asyncio.run(main())