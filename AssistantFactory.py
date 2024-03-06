#
#
#
from openai import OpenAI 
GPT_MODEL = "gpt-3.5-turbo-0125"

client = OpenAI()
class AssistantFactory:
    
    def __init__(self):
        pass

    def createAssistant( self, nameArg, modelArg=GPT_MODEL ):
        new_assistant = client.beta.assistants.create(
            name         = nameArg,
            model        = modelArg,
            instructions = "You are a helpful assistant.",
            tools        = [{ "type": "retrieval" }])

        return new_assistant
    
    def getExistingAssistant( self, assistant_id ):
        existing_assistant = client.beta.assistants.retrieve( assistant_id)
        
        return existing_assistant
    
