#!/usr/bin/env python
import sys
from crew import WebscraperCrew
import agentops
from agentops.enums import EndState
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the agentops library
session = agentops.init( api_key=os.getenv( 'AGENTOPS_API_KEY' ))


def run():
    """
    Run the crew.
    """
    inputs = {
    }
    WebscraperCrew().crew().kickoff( inputs=inputs )
    session.end_session( EndState.SUCCESS )

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
    }
    try:
        WebscraperCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        WebscraperCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
    }
    try:
        WebscraperCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == '__main__':
    run()