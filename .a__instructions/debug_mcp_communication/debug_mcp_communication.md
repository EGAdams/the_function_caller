I am having a communication issue with the MCP server.
Here is what I have in one terminal:
```bash
adamsl@DESKTOP-SHDBATI:~$ npx -y @modelcontextprotocol/server-memory --port 8006
Knowledge Graph MCP Server running on stdio
```
And here is what I have in another terminal:
```bash
adamsl@DESKTOP-SHDBATI:~$ curl -X POST http://localhost:8006/list_tools
curl: (7) Failed to connect to localhost port 8006 after 0 ms: Connection refused
adamsl@DESKTOP-SHDBATI:~$
```

How can I debug this issue?
