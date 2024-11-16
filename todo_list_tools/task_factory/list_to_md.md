Here is my TODO liust output in raw format:
```bash
└───[1] Create IMessageBus interface

 └───[2] Implement SimpleMessageBus class

 └───[3] Create IMessage interface

 └───[4] Implement SimpleMessage class

 └───[5] Create ISubscriber interface

 └───[6] Implement BaseSubscriber class

 └───[7] Create IHandler interface

 └───[8] Implement ThreadRetrievalHandler class

 └───[9] Implement ToolExecutionHandler class

 └───[10] Create IAgent interface

 └───[11] Implement UserInteractionManager class

 └───[12] Create IUserInteraction interface

 └───[13] Implement Thread class

 └───[14] Create IToolCall interface

 └───[15] Implement ToolCall class

 └───[16] Create IMessageOutput interface

 └───[17] Implement MessageOutput class

 └───[18] Create IErrorHandler interface

 └───[19] Implement ErrorHandler class

 └───[20] Implement ThreadFactory class

 └───[21] Implement ToolFactory class

 └───[44] Debug a segfault

 └───[23] Debug zero connection

 └───[24] finish beer

 └───[25] get out of here

 └───[26] sleep
     ├───[27] get tired
     ├───[45] read
     │    └───[50] find something to read
     └───[46] count sheep
         ├───[47] smoke something
         ├───[48] find something to smoke
         └───[49] determine the amount of sheep to count

```
Please create a Python script that will take this output and create a markdown file similar to the following structure:
```markdown
# TODO List
## Tasks
### [1] sleep
#### [27] get tired
#### [45] read
##### [50] find something to read
#### [46] count sheep
##### [47] smoke something
##### [48] find something to smoke
##### [49] determine the amount of sheep to count
...
```


