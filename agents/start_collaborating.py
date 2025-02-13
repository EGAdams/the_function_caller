#
#   start collaborating by sending 
#   a message to the collaborator agent
#
import os, sys
home_directory = os.path.expanduser( "~" )
sys.path.append( home_directory + '/the_function_caller' )
import xmlrpc.client
from colorama import Fore, Style
from send_message_tool.send_message_tool import SendMessageTool  # Add this import

def main():
    agents_urls = {
            "collaborator"  : "http://localhost:8001",
            "planner"       : "http://localhost:8002",
            "coder"         : "http://localhost:8003",
            "prompt"        : "http://localhost:8004" }
        
    send_message_tool = SendMessageTool( agents_urls )              # Create an instance of the send message tool just like we do
                                                                    # when we initialize the file system mapped functions.
    from colorama import init
    init( autoreset=True )  # Initialize colorama
    
    while True:
        message = input( "Enter your message for the agency: " )    # Get input from the user
        if message.lower() == "exit" or message.lower() == "quit" or message.lower() == "kk" or message.lower() == "x" or message.lower() == "q":
            print("Exiting chat client. Goodbye!")
            break

        try:                                                        # Send the message as a command to the collaborator
            send_message_tool.send_message( "collaborator", message )
        except Exception as e:
            print( f"{ Fore.RED }Failed to send message: { e }" )

if __name__ == "__main__":
    main()
