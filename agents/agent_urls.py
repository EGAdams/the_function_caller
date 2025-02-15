class AgentUrlProvider:
    @staticmethod
    def get_agent_urls():
        return {
            "collaborator": "http://localhost:8001",
            "planner": "http://localhost:8002", 
            "coder": "http://localhost:8003",
            "prompt": "http://localhost:8004"
        }