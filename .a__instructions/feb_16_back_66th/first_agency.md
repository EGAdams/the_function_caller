# Coding Solution Agency
Created on February 16, 2025 at 06:26 AM 
#
# It is more important to make reusable code even though the responsibility is small.  We need smaller responsibilities.


Current Task:
Add memory capabilities to the Base Agent.  

## Agents Involved
### Collaborator Agent
#### Responsibilities
The Collaborator Agent collaborates communication between all of the Agents in this Agency.

#### Team members
* Prompt Agent
* Coder Agent


### Prompt Agent
#### Responsibilities
Builds the prompt for the next Coding task.

#### Steps to complete tasks
* List the objects needed to complete the task
* List the full path to the directories of each file that needs to be created for these objects.

#### Team members
* Collaborator Agent
* Coder Agent

### Coder Agent
#### Responsibilities
Write code and make sure that the directories to put the code in are in the correct places.

#### Steps to complete tasks
* checks for the location of all of the files involved.
* creates the necessary directories for the new code if they do not exist.
* we are going to start with Python, so it is going to make sure that all of the __init__
  files are created and placed in their correct directories.

#### Team Members
* Prompt Agent
* Collaborator Agent

