var newTask=document.getElementById("new-task");//Add a new task.
var addTaskButton=document.getElementsByTagName("button")[0];//first button
var incompleteTasks=document.getElementById("incomplete-tasks");//ul of #incomplete-tasks
var completedTasks=document.getElementById("completed-tasks");//completed-tasks

//New task list item
function createNewTask(task) {

	var Task=document.createElement("li");

	//input (checkbox)
    var checkBox=document.createElement("input");
    
	//label
    var label=document.createElement("label");
    
	//input (text)
    var editTextField=document.createElement("input");
    
	//button.edit
	var editButton=document.createElement("button");

	//button.delete
	var deleteButton=document.createElement("button");

	label.innerText=task;

	checkBox.type="checkbox";
	editTextField.type="text";

	editButton.innerText="Edit";
	editButton.className="edit";
	deleteButton.innerText="Delete";
	deleteButton.className="delete";

	Task.appendChild(checkBox);
	Task.appendChild(label);
	Task.appendChild(editTextField);
	Task.appendChild(editButton);
	Task.appendChild(deleteButton);
	return Task;
}

function addTask() {
	//Create a new task item with the text from the #new-task:

    //Append listItem to incompleteTaskHolder
    if (newTask.value != "") {
        var listItem=createNewTask(newTask.value);

        incompleteTasks.appendChild(listItem);
        bindTaskEvents(listItem, taskComplete);
    
        newTask.value="";
    }
}

//Edit an existing task.
function editTask() {
    var task=this.parentNode;
    
    var editInput=task.querySelector('input[type=text]');
    var label=task.querySelector("label");
    var containsClass=task.classList.contains("editMode");
            //If class of the parent is .editmode
            if(containsClass){
    
            //switch to .editmode
            //label becomes the inputs value.
                label.innerText=editInput.value;
            }else{
                editInput.value=label.innerText;
            }
    
            //toggle .editmode on the parent.
            task.classList.toggle("editMode");
    }

//Delete task.
function deleteTask() {

    var task=this.parentNode;
    var ul=task.parentNode;
    //Remove the parent list item from the ul.
    ul.removeChild(task);
}

//Mark task completed
function taskComplete() {
    //Append the task list item to the #completed-tasks
    var task=this.parentNode;
    completedTasks.appendChild(task);
    bindTaskEvents(task, taskIncomplete);
}

function taskIncomplete() {
    //Mark task as incomplete.
    //When the checkbox is unchecked
    //Append the task list item to the #incomplete-tasks.
    var task=this.parentNode;
    incompleteTasks.appendChild(task);
    bindTaskEvents(task,taskComplete);
}

//Set the click handler to the addTask function.
addTaskButton.onclick=addTask;

function bindTaskEvents(taskListItem,checkBoxEventHandler){
    //select ListItems children
	var checkBox=taskListItem.querySelector("input[type=checkbox]");
	var editButton=taskListItem.querySelector("button.edit");
	var deleteButton=taskListItem.querySelector("button.delete");

	//Bind editTask to edit button.
	editButton.onclick=editTask;
	//Bind deleteTask to delete button.
	deleteButton.onclick=deleteTask;
	//Bind taskCompleted to checkBoxEventHandler.
	checkBox.onchange=checkBoxEventHandler;
}

//cycle over incompleteTaskHolder ul list items
//for each list item
for (var i=0; i<incompleteTasks.children.length;i++) {
    //bind events to list items chldren(tasksCompleted)
	bindTaskEvents(incompleteTasks.children[i],taskComplete);
}

//cycle over completedTasksHolder ul list items
for (var i=0; i<completedTasks.children.length;i++) {
	//bind events to list items chldren(tasksIncompleted)
	bindTaskEvents(completedTasks.children[i],taskIncomplete);
	}