#
# Class PrettyPrint
#
from termcolor import colored 

class PrettyPrint:
    def __init__( self ):
        pass

    def execute( self, messages ):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "function": "magenta" }

        for message in messages:
            if message == None:
                continue
            if message.role == "system":
                print( colored( f"system: { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))
            elif message.role == "user":
                print( colored( f"user: { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))
            # elif message.role == "assistant" and message.get( "function_call" ):
            #     print( colored( f"assistant: {message['function_call']}\n", role_to_color[message.role]))
            elif message.role == "assistant": # and not message.get( "function_call" ):
                print( colored( f"assistant: { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))
            elif message.role == "function":
                print( colored( f"function ({ message[ 'name' ]}): { message.content[ 0 ].text.value }\n", role_to_color[ message.role ]))
