```mermaid
classDiagram
    class FileHandlerFactory {
        <<interface>>
        +createReadHandler(): FunctionHandler
        +createWriteHandler(): FunctionHandler
    }
    class LocalFileHandlerFactory {
        +createReadHandler(): FunctionHandler
        +createWriteHandler(): FunctionHandler
    }
    class RemoteFileHandlerFactory {
        +createReadHandler(): FunctionHandler
        +createWriteHandler(): FunctionHandler
    }
    class FunctionHandler {
        <<interface>>
        +execute(parameters: dict): str
    }
    class ReadFileHandler {
        +execute(parameters: dict): str
    }
    class WriteFileHandler {
        +execute(parameters: dict): str
    }
    class FileReader {
        +read(filename: str): str
    }
    class FileWriter {
        +write(filename: str, content: str): str
    }
    LocalFileHandlerFactory --|> FileHandlerFactory
    RemoteFileHandlerFactory --|> FileHandlerFactory
    ReadFileHandler --> FileReader : uses
    WriteFileHandler --> FileWriter : uses
    WriteFileHandler --|> FunctionHandler
    ReadFileHandler --|> FunctionHandler
    LocalFileHandlerFactory --> ReadFileHandler : creates
    LocalFileHandlerFactory --> WriteFileHandler : creates
    RemoteFileHandlerFactory --> ReadFileHandler : creates
    RemoteFileHandlerFactory --> WriteFileHandler : creates
```


Act as an expert user of the Gang of Four Design Patterns.  You are crazy about enforcing the Single Responsibility Principle.  Do you think that we could abstract out this widget factory example any more?

# The widget example
```mermaid
classDiagram
    class WidgetFactory {
        <<interface>>
        +createButton(): Button
        +createScrollbar(): Scrollbar
    }
    class MacOSWidgetFactory {
        +createButton(): Button
        +createScrollbar(): Scrollbar
    }
    class WindowsWidgetFactory {
        +createButton(): Button
        +createScrollbar(): Scrollbar
    }
    class Button {
        +render()
    }
    class Scrollbar {
        +render()
    }
    MacOSWidgetFactory --|> WidgetFactory
    WindowsWidgetFactory --|> WidgetFactory
    MacOSWidgetFactory --> Button : creates
    MacOSWidgetFactory --> Scrollbar : creates
    WindowsWidgetFactory --> Button : creates
    WindowsWidgetFactory --> Scrollbar : creates
```

# Theres more!
```mermaid
classDiagram
    class WidgetFactory {
        <<interface>>
    }
    class ButtonFactory {
        <<interface>>
        +createButton(): Button
    }
    class ScrollbarFactory {
        <<interface>>
        +createScrollbar(): Scrollbar
    }
    class MacOSButtonFactory {
        +createButton(): Button
    }
    class MacOSScrollbarFactory {
        +createScrollbar(): Scrollbar
    }
    class WindowsButtonFactory {
        +createButton(): Button
    }
    class WindowsScrollbarFactory {
        +createScrollbar(): Scrollbar
    }
    class Button {
        +render()
    }
    class Scrollbar {
        +render()
    }
    MacOSButtonFactory --|> ButtonFactory
    MacOSScrollbarFactory --|> ScrollbarFactory
    WindowsButtonFactory --|> ButtonFactory
    WindowsScrollbarFactory --|> ScrollbarFactory
    MacOSButtonFactory --> Button : creates
    MacOSScrollbarFactory --> Scrollbar : creates
    WindowsButtonFactory --> Button : creates
    WindowsScrollbarFactory --> Scrollbar : creates
```


Act as an expert user of the Gang of Four Design Patterns.  You are crazy about enforcing the Single Responsibility Principle.  Do you think that we could abstract out this widget factory example any more?

# The widget example
```mermaid
classDiagram
    class WidgetFactory {
        <<interface>>
    }
    class ButtonFactory {
        <<interface>>
        +createButton(): Button
    }
    class ScrollbarFactory {
        <<interface>>
        +createScrollbar(): Scrollbar
    }
    class MacOSButtonFactory {
        +createButton(): Button
    }
    class MacOSScrollbarFactory {
        +createScrollbar(): Scrollbar
    }
    class WindowsButtonFactory {
        +createButton(): Button
    }
    class WindowsScrollbarFactory {
        +createScrollbar(): Scrollbar
    }
    class Button {
        +render()
    }
    class Scrollbar {
        +render()
    }
    MacOSButtonFactory --|> ButtonFactory
    MacOSScrollbarFactory --|> ScrollbarFactory
    WindowsButtonFactory --|> ButtonFactory
    WindowsScrollbarFactory --|> ScrollbarFactory
    MacOSButtonFactory --> Button : creates
    MacOSScrollbarFactory --> Scrollbar : creates
    WindowsButtonFactory --> Button : creates
    WindowsScrollbarFactory --> Scrollbar : creates
```


# Another one even more abstract?
```mermaid
classDiagram
    class AbstractFactory {
        <<interface>>
        +createButton(): Button
        +createScrollbar(): Scrollbar
    }
    class MacOSFactory {
        +createButton(): Button
        +createScrollbar(): Scrollbar
    }
    class WindowsFactory {
        +createButton(): Button
        +createScrollbar(): Scrollbar
    }
    MacOSFactory --|> AbstractFactory
    WindowsFactory --|> AbstractFactory
    MacOSFactory --> Button : creates
    MacOSFactory --> Scrollbar : creates
    WindowsFactory --> Button : creates
    WindowsFactory --> Scrollbar : creates
```
