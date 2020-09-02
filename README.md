# task-maneger

Overview

This is a task management system which helps in creating and monitoring of different tasks assigning to multiple users. Admin of the application can create a task board that contains number of task and their respective deadlines, he can also invite different users to see and interact on the created boards.

1	INTRODUCTION
1.1	Purpose and Scope
The purpose of this application is to create an application model that describes the created task boards in the form of different tasks and users.

1.2	Project Requirements
1.	Python 2.7
2.	Google app engine
3.	Git Repository

2	SYSTEM ARCHITECTURE
1.	JINJA ENVIRONMENT:
Jinja helps in defining of global objects as a central object in the template environment. Instances used here are further used to configure and store of the global variables, which are further used to load templates from other locations. It also helps to locate the root directory for google app engine. 
We define count_tasks as a global variable which stores the information of completed task by their time and date. 
It also helps in initialization of user request login with there user mail id and the task they created.
2.	CLASS MAIN HANDLER
Def get(): Here we only initialize the request pulls out form global variable and checks if the user is logged in with their email id and passes the specific parameters for verifying it. 
3.	CLASS NEW BOARD HANDLER
Def post(): Here after login and pulling out the main page we can create a new task board with particular name. The task board created has the unique ID and only the creator of task board can append or delete it as its associated with member key.
4.	CLASS TASK BOARD HANDLER
Def get(): When user clicks on the create task board the information is pulled out where parameters are user id associated with task board id for current user.
5.	CLASS INVITE MEMBER HANDLER
Def get(): It pulls out the form with the help of which user can invite other user to assign tasks to them.
Def post(): After the details form pulls out, user can invite other members to the task board with the help of there email id. If email id of the user exists, then it pulled out and the invitation was success. If the user invited is not exists, then it returns the value and redirected to the same page.
6.	CLASS ADDT ASK HANDLER

Function	Get(), Post()
Parameters	Name, date

Def get(): Initially it checks weather the user is logged in or not as these functions is depend on ndb key values. If the ndb values are true, then the desired function is called for creating a new task.
Def post(): After the information is pulled user can create a new task to the task board and add it. The task created with name and date when the task is finished. Task name work as the key value which help in assigning of task to different users.
7.	CLASS DEADLINE TASK HANDLER
Def get(): This function helps to check the user with their ndb values if its not true than redirected to the home page.
Def post(): Here user can define and edit the deadline of the task with the help of there deadline task id. It also holds the information and format of the date time.
8.	CLASS ASSIGN TASK HANDLER
Def get(): Checks weather the user is logged in or not. This function also depends on the ndb.key value of the current user logged in. This pulls out the form for assigning tasks.
Def post(): After the information is pulled out and the task is assigned to a member. Each task is defined by there own task id which helps in to identify them.
9.	CLASS COMPLETE TASK HANDLER
Def get(): Check for the user logged in.
Def post(): Pulls out the form which stores the information of the task and checks weather the task is competed on time defined or not and update it on the task board manager.
10.	CLASS DELETE TASK HANDLER
Def get(): This function does the same to identify user logged in.
Def post(): This pulls out the information about the task with the help of the ndb key value, which helps in identifying the owner who is the only one can delete the task. 
11.	CLASS RENAME BOARD HANDLER
Def get(): Checks weather the user is logged in with his email id. And check for task board associated than pulls out the related information.
Def post(): This checks the information about the task id and the task board associated. It also checks weather the task is completed, assigned or append . Only the owner of the with ndb key value can rename the task board handler and then the update it.


12.	CLASS REMOVE MEMBER HANDLER

Def get(): It pulls out the information of the user with the help of his email id. And checks if user is authorized for the function to execute or not.

Def post(): Owner of the task board can remove the member assigned and change it with the member key. The user member can only be removed if its not associated with any task in the task board.

13.	CLASS DELETE BOARD HANDLER
Def get(): It checks for the ndb key value of the user logged in.
Def post(): After the request is pulled out and the user logged in as an owner of the task board than he is authorized to delete the entire task board. After deleting the task board all the other members associated will also remove.
14.	Webapp2.WSGIApplication
For defining the route access for the user who have specific access to that function. By default, it doesn’t know which page user wants to access therefore, we must define the expected route through routing table in python.

3. DATASTRUCTURE USED (NOSQL) 
This application works on google app engine which supports NoSQL database to store information and don’t rely on traditional database structures and stored more flexible data models. NoSQL database is schema free can handle variety of data even in huge amount, it also helps in replication of data to avoid the single point failure. The data can be store by their key values in the database, all other parameters were stored in wide column structure. This will help us to store huge amount of data with speed development and increased horizontal scalability. 
This data structure is used by google app engine to fully managed the cloud service, which helps replication and handles shredding to ensure the consistent working of the database.

4. DATAMODEL (NDB) 
	This model depicts the structure of the entities stored in the database. Model classes define in the application to indicate the desired entities and their structure. The model is inherited by the given class model can be directly or indirectly inherited from main model. 
NDB model is also used to describe the definition of class declared straightforward used to declare the model class structure. The definition of property helps the system to identify the names and types of field stored in the cloud storage. We used two property of ndb in our application:
1.	String property: is used to store the name of the task boards and tasks created.

2.	Date property: it helps the user to store the date in chronological order when the task is created.

3.	Boolean property: it helps the user to store the information when the task is completed and can used for filtering and sorting.
4.	Date time property it is used for storing information of date time values according to different time zones.

5.	Key property: it defines and store the task and user information with their key values which help in identifying them at the time of assigning.
5. DOCUMENTATION OF USER INTERFACE:
1.	Simple interface is created for end user to operate the application.
2.	Old school but powerful interface to full fill the needs of the user.
3.	Background is clear white with bold black words and text boxes for entering desired entry.
4.	Buttons are clearly visible with there use. All the buttons are perfectly arranged according to their use.
5.	On the screen user can see his email id with which user logged in.
6.	All  the Headings and subheadings are arranged according to the working of application.
7.	Name of the task board and the status of all the task are clearly screen so user can easily identify the status of the tasks. 
8.	The tasks are shown with their deadline so user can change deadline in case of emergency.
9.	Working of the task board is clear and eye catching with simple format and working.
10.	User can User can rename the task board created according to the need.
11.	The user can connect to other members and assign them task by adding them.
12.	All the check boxes and textboxes are showing their purpose and what user has to fill with correct way in writing.
13.	Two colors are used to differentiate the assigned and non-assigned task.
14.	If the task is not assigned by the owner, it shows red and when assigned by the owner to another member shows green.
15.	The visibility shown itself clear how many tasks they assign and how many are left.
16.	Completed task are shown in the up middle of the page so user can clearly see how many tasks are completed , active and left for completion.
17.	At last home and logout buttons placed with one another and clearly visible to the user.


Liscence ©yadavpuneet
