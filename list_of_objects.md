## Initialize the main process
- choose a model, temperature, assistant, etc...

## Assistant Factory
- get an existing assistant

## Thread Factory
- create a new thread

## Message Manager
- add a message to a thread

## Run Factory
- create a run for the thread

## Extract the function calls
- get the function calls from the run that is given

## 

## Map strings to live functions 
* populate the json map object used to construct the `StringToFunction object`
for example
```python
json_map = {
    "read_file": read_file,
    "write_file": write_file,
} # read_file and write_file are live function pointers
```

## Check the run status ( TODO: )

## Main Loop
- get user input
- fire off a new run
- sit and wait for the run to complete
- show messages

## File Operations
- write content to a file
- read content from a file

these are the live function pointers that the strings map to above.

## Pull the information about the function
- get the function name from the tool call
- get the arguments from the tool call ( `JSONArgumentParser` )

## Create the function given the function name string
uses the ( `StringToFunction` ) class that was constructed with a dictionary that maps strings to live function objects. 

## Execute Function
hmm... this might be useful in other projects
- execute the function using the function name and arguments ( `FunctionExecutor` )

The `FunctionExecutor` uses the `StringToFunction` to avoid violating the single responsibility principle.  the `StringToFunction` object is responsible for mapping the string to the live function object.  The `FunctionExecutor` is responsible for executing the live function object with the arguments that where passed to it.


## Send LLM Message
- use the current messages array, tools list schemas created by our ToolManager, the gpt model and the desired tool to use to keep the model from using a ridiculous tool.


## Send the output of the function to the caller
- Yes we would need the caller id for this which in this case would be the run id, thread id and the tool call associated with the output
