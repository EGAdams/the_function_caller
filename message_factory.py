#
# MessageFactory class
#
class MessageFactory:
    
    def __init__(self):
        pass
    
    def create_initial_messages_object( self ):
        """Create the initial messages object. """
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user",   "content": "What is your purpose?"        }
        ]
        return messages
        

    def create_message( self, role, content ):
        """Create a message object. """
        message = {
            "role": role,
            "content": content
        }
    
        return message
