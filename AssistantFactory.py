GPT_MODEL = "gpt-3.5-turbo-0125"
from openai import OpenAI 
from ToolManager import ToolManager

class AssistantFactory:
    def __init__(self):
        self.tool_manager = ToolManager()
        self.client = OpenAI()

    def createAssistant( self, nameArg, modelArg=GPT_MODEL ):
        new_assistant = self.client.beta.assistants.create(
            name         = nameArg,
            model        = modelArg,
            instructions = "You are a helpful assistant.",
            tools        = [ self.tool_manager.get_tools() ])

        return new_assistant
    
    def getExistingAssistant( self, assistant_id ):
        existing_assistant = self.client.beta.assistants.retrieve( assistant_id )
        
        return existing_assistant
    
