# Test Agent built originally for the coder agent. 010925
import os, sys

home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
from agents.base_agent.base_agent import BaseAgent, ICommand
from agents.base_agent.base_agent import RPCCommunicationStrategyFactory
from agents.base_agent.base_agent import ConsoleLogger

class EchoCommand(ICommand):
    def execute(self, message: dict) -> dict:
        """
        Simple command to echo the received message back for testing.
        """
        response = message.get('response', '')
        # return { "status": "success", "response": response }
        print(f"TestAgent received message: { response }")

class TestAgent(BaseAgent):
    def __init__(self, agent_id: str, port: int, logger=None):
        strategy_factory = RPCCommunicationStrategyFactory(port=port, logger=logger)
        super().__init__(agent_id, strategy_factory, logger or ConsoleLogger())
        # Register commands
        self.register_command( "process_message", EchoCommand())

    def receive_message(self, message: dict) -> dict:
        """
        Handle incoming messages from other agents.
        """
        print(f"TestAgent received message: {message}")
        return self.process_message(message)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the TestAgent.")
    parser.add_argument("--port", type=int, default=8004, help="Port for the TestAgent.")
    args = parser.parse_args()

    agent_id = "test_agent"
    port = 8004  # Port for the TestAgent
    logger = ConsoleLogger()
    test_agent = TestAgent(agent_id=agent_id, port=args.port, logger=logger)
    test_agent.logger.info(f"TestAgent is running on port {args.port}...")
    test_agent.run()
