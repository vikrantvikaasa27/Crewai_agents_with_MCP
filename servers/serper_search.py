from mcp.server.fastmcp import FastMCP
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("serper_search")

url = "https://google.serper.dev/search"

@mcp.tool(name="serper_search", description="Search the web for information")
def search(query: str) -> str:

    payload = json.dumps({
        "q": query,
        "num":20
    })
    headers = {
    'X-API-KEY': os.getenv("SERPER_API_KEY"),
    'Content-Type': 'application/json'
    }
    
    #make the request
    response = requests.request("POST", url, headers=headers, data=payload)
    
    #parse the response
    data = response.json()
    return data

if __name__ == "__main__":
    mcp.run(transport="stdio")