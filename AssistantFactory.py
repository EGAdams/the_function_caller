#
#
#
from openai import OpenAI 
GPT_MODEL = "gpt-3.5-turbo-0125"
from ToolManager import ToolManager

client = OpenAI()
class AssistantFactory:
    
    def __init__(self):
        self.tool_manager = ToolManager()

    def createAssistant( self, nameArg, modelArg=GPT_MODEL ):
        new_assistant = client.beta.assistants.create(
            name         = nameArg,
            model        = modelArg,
            instructions = "You are a helpful assistant.",
            tools        = [ self.tool_manager.get_tools() ])

        return new_assistant
    
    def getExistingAssistant( self, assistant_id ):
        existing_assistant = client.beta.assistants.retrieve( assistant_id )
        
        return existing_assistant
    
