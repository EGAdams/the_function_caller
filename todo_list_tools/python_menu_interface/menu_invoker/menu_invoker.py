class MenuInvoker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MenuInvoker, cls).__new__(cls)
            cls._instance.commands = {}
        return cls._instance

    def register(self, option, command):
        self.commands[option] = command

    def display_menu(self):
        while True:
            print( "Todo Command Menu"   )
            print( "1. Add Todo"         )
            print( "2. Add Todo Subtask" )
            print( "3. Show Todo List"   )
            print( "x. Exit"             )
            choice = input("Choose an option:\n")
            if ( choice == "x" ):
                exit( 0 )
            command = self.commands.get(choice)
            if command:
                command.execute()
            else:
                print("Invalid choice. Try again.")
