class MenuInvoker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MenuInvoker, cls).__new__(cls)
            cls._instance.commands = {}
        return cls._instance

    def register(self, option, command):
        self.commands[option] = command

    def display_menu(self, command_sequence=None):
        commands_iter = iter(command_sequence) if command_sequence else None
        while True:
            print("\nTodo Command Menu")
            print("1. Add Todo Subtask")
            print("2. Edit Todo Description")
            print("3. Show Todo List")
            print("4. Show Storage Handler Path")
            print("x. Exit")

            if commands_iter:
                try:
                    choice = next(commands_iter)
                    print(f"Automatically selected option: {choice}")
                except StopIteration:
                    print("No more commands in sequence. Exiting menu.")
                    break
            else:
                try:
                    choice = input("Choose an option: ")
                except EOFError:
                    print("\nNo interactive input available. Exiting menu.")
                    break

            if choice == 'x':
                print("Exiting menu.")
                break
            elif choice in self.commands:
                self.commands[choice].execute()
            else:
                print("Invalid option, please try again.")
