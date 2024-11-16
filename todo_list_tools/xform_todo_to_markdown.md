
I need a Python script that takes the following input and produces a markdown output:
```bash
 └───[26] sleep
     ├───[27] get tired
     ├───[45] read
     │    ├───[50] find something to read
     │    │    ├───[52] pick the subject
     │    │    │    └───[54] list the subjects
     │    │    │        └───[55] find the subject lister
     │    │    └───[56] find the dam glasses
     │    └───[51] put some dam glasses on
     └───[46] count sheep
         ├───[47] smoke something
         ├───[48] find something to smoke
         └───[49] determine the amount of sheep to count
             └───[53] think about what color the sheep are
```

Here is the markdown output that should be produced:
```markdown
* [26] sleep
  * [27] get tired
  * [45] read
    * [50] find something to read
      * [52] pick the subject
        * [54] list the subjects
          * [55] find the subject lister
      * [56] find the dam glasses
    * [51] put some dam glasses on
  * [46] count sheep
    * [47] smoke something
    * [48] find something to smoke
    * [49] determine the amount of sheep to count
      * [53] think about what color the sheep are
```
