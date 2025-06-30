#We use tkinter for this project
import tkinter as tk
from tkinter import messagebox, simpledialog

class TodoApp:

    #Initialize the application
    def __init__(self, root):
        self.root = root #Store the root window reference
        self.root.title("To-Do List Application") #Title
        self.root.geometry("500x500") #Set window size (wxh)
        self.root.resizable(False, False) #Make width and height non resizable
        
        self.tasks = [] #Initialize list to store tasks
        
        # Create GUI
        self.create_widgets()
        
        # Load tasks if any exist
        self.load_tasks()
    

    #Creates GUI widgets
    def create_widgets(self):

        #Create a frame to hold input widgets
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10) #Add padding around the frame
        
        # Entry widget
        self.task_entry = tk.Entry(input_frame, width=40, font=("Arial", 12)) #Create an entry widget for task input
        self.task_entry.pack(side=tk.LEFT, padx=5) #Pack the entry widget to the left with padding
        self.task_entry.bind("<Return>", lambda event: self.add_task()) #The enter key can trigger add_task
        
        # Add Task Button
        add_button = tk.Button(input_frame, #Parent window
                               text="Add Task", #Displayed text
                               command=self.add_task, #Function that is called when the button is clicked
                               bg="green", #Background colour
                               fg="white", #Text colour
                               font=("Arial", 10, "bold")) #Font style
        add_button.pack(side=tk.RIGHT, padx=5) #Pack the button to the right with padding
        
        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.root, #Parent window
                                       width=50, 
                                       height=15, 
                                      font=("Arial", 12), #Font for list items
                                      selectmode=tk.SINGLE) #Only one item can be selected at a time
        self.task_listbox.pack(pady=10) #Add 10px vertical padding
        
        # Frame for action buttons
        button_frame = tk.Frame(self.root) #self.root is the parent window
        button_frame.pack(pady=10) #Add 10px vertical padding when placing in window
        
        # Edit Button
        edit_button = tk.Button(button_frame, text="Edit Task", command=self.edit_task,
                               bg="blue", fg="white", font=("Arial", 10, "bold"))
        edit_button.pack(side=tk.LEFT, padx=5)
        
        # Delete Button
        delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task,
                                 bg="red", fg="white", font=("Arial", 10, "bold"))
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Complete Button
        complete_button = tk.Button(button_frame, text="Mark Complete", command=self.mark_complete,
                                   bg="purple", fg="white", font=("Arial", 10, "bold"))
        complete_button.pack(side=tk.LEFT, padx=5)
        
        # Clear All Button
        clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_all,
                                bg="orange", fg="white", font=("Arial", 10, "bold"))
        clear_button.pack(side=tk.LEFT, padx=5)
    

    #Adds new task
    def add_task(self): 
        task = self.task_entry.get().strip() #Gets the text from task_entry entry widget
        if task: #If entry is not empty
            self.tasks.append({"task": task, "completed": False}) #Add the task to the tasks list (with completed=False)
            self.update_listbox() #Updates listbox display
            self.task_entry.delete(0, tk.END) #Clears entry widget
            self.save_tasks() #Save the tasks to the file
        else:
            messagebox.showwarning("Retry", "Please enter a task.") #If nothing is typed in the entry widget, a messagebox appears
    

    #Edits a task
    def edit_task(self):
        selected_index = self.task_listbox.curselection() #Get the index of the selected task
        if selected_index: #Check if a task is selected
            selected_index = selected_index[0] #Get the first selected index 
            current_task = self.tasks[selected_index]["task"] #Get the current task text from the self.tasks list
            new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_task)  #Show dialogue to edit the task
            if new_task and new_task.strip(): #Checks if new task is not empty
                self.tasks[selected_index]["task"] = new_task.strip()  #Update the task in the list
                self.update_listbox()  #Update the listbox display
                self.save_tasks() #Save tasks to file
        else:
            messagebox.showwarning("Retry", "Please select a task to edit.") #Show warning if no task is selected
    

    #Deletes a task
    def delete_task(self):
        selected_index = self.task_listbox.curselection() #Get the index of the selected task
        if selected_index: #If selected_index exists
            selected_index = selected_index[0] #Get the first selected index
            self.tasks.pop(selected_index) #Remove the task from the list
            self.update_listbox() #Update the listbox display
            self.save_tasks() #Save tasks to file
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.") #Show warning if no task is selected
    

    #Toggles completion status
    def mark_complete(self):
        selected_index = self.task_listbox.curselection() ##Get the index of the selected task
        if selected_index: #If selected_index exists
            selected_index = selected_index[0] #Get the first selected index
            self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"] #Toggle the completed status
            self.update_listbox() #Update the listbox display
            self.save_tasks() #Save tasks to file
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as complete.") #Show warning if no task is selected
    

    #Clears all tasks
    def clear_all(self): 
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"): # Show confirmation dialogue
            self.tasks = [] #Clear the tasks list
            self.update_listbox() #Update the listbox display
            self.save_tasks() #Save tasks to file
    

    #Updates listbox with current tasks
    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)  #Clear all items from the listbox
        for task in self.tasks: #Loop through all tasks
            task_text = task["task"] #Get the task text
            if task["completed"]: #Check if task is completed
                task_text = f"✓ {task_text}" #Add checkmark prefix for completed tasks
                self.task_listbox.insert(tk.END, task_text) #Insert the task into the listbox
                self.task_listbox.itemconfig(tk.END, {'fg': 'green'}) #Set the text color to green
            else:
                self.task_listbox.insert(tk.END, task_text) #Insert the task without modification
    
    #Saves tasks to a file
    def save_tasks(self):
        with open("tasks.txt", "w") as f: #Open the tasks file in write mode
            for task in self.tasks: #Write each task to the file
                f.write(f"{task['task']}|{task['completed']}\n") #Format: task_text|completed_status
    
    #Loads tasks from a file
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f: #Open the tasks file in read mode
                for line in f.readlines(): #Read each line in the file
                    task, completed = line.strip().split("|") #Split the line into task and completed status
                    self.tasks.append({  #Add the task to the list
                        "task": task,
                        "completed": completed == "True"
                    })
            self.update_listbox() #Update the listbox display
        except FileNotFoundError: #If file doesn't exist, do nothing
            pass

#Main entry point
if __name__ == "__main__":
    root = tk.Tk() #Create the root window
    app = TodoApp(root) #Create an instance of the TodoApp
    root.mainloop() #Start the main event loop
