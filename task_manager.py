# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)
print(type(task_list))


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Function to add a new user
def reg_user():
    while True:
        new_username = input("New Username: ")
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        # If the usernale doesn't already exist and the passwords match, the user can be set up
        if new_password == confirm_password and new_username not in username_password.keys():
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
                break
        # If the username already exists then the user needs to select a different username
        elif new_username in username_password.keys():
            print("User already exists, please select a different username")        
        # If the password and confirmed password don't match the user will not be set up
        elif new_password != confirm_password:
            print("Passwords do not match")





    
# Function to add task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    # Try Except block to make sure the correct date time format is used
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date. 
    curr_date = date.today
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add the new task to the task list
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)    

# Function to view user's tasks
def view_mine():
    print("\n")
     
    for index, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str =  "\n" + f"\tTask: \t\t {t['title']}\n"
            disp_str += f"\tAssigned to: \t {t['username']}\n"
            disp_str += f"\tDate Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\tDue Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\tTask Description: \n {t['description']}\n"
            print("Task Number", str(index + 1), "=", disp_str)







while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    # Using the reg_user function 
    if menu == 'r':
        reg_user()

    # Using the add_task function
    elif menu == 'a':
        add_task()

    # Using the view_all function
    elif menu == 'va':
        view_all()

    # Using the view_mine function
    elif menu == 'vm':
        while True:
            view_mine()

            # Creating a menu in this option to select a specific task or exit to the main menu
            user_choice_vm_menu = int(input('''\nIf you would like to select a specific task, please enter the number of that task.
If you would like to exit the menu, please enter -1\nUser choice = '''))
            
            if user_choice_vm_menu == -1:
                break

            elif user_choice_vm_menu != -1:
                # Creating a third menu for the user to select to edit the chosen task or complete
                edit_or_complete = (input("\nWould you like to:\n\tA. edit the selected task or \n\tB. mark it as complete?\nPlease enter A or B:")).upper()
                
                # If statement to make sure only incomplete tasks can be edited
                if edit_or_complete == "A" and task_list[user_choice_vm_menu - 1]['completed'] == False:
                    print("\nYou can edit either the username that this task is assigned to or the due date")

                    edit_choice = (input("u = change username\ndd = change due date\n")).lower()

                    if edit_choice == "dd":
                        print(f"The current due date is: {task_list[user_choice_vm_menu - 1]['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                        while True:
                            try:
                                new_due_date = input("New due date of task (YYYY-MM-DD): ")
                                new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                task_list[user_choice_vm_menu - 1]['due_date'] = new_due_date_time
                                break
                            except ValueError:
                                print("Invalid datetime format. Please use the format specified")

                    elif edit_choice == "u":
                        print(f"The current user this task is assigned to is: {task_list[user_choice_vm_menu - 1]['username']}")
                        change_user = input("Please enter the username of the user that you wish to assign this task to:") 
                        if change_user not in username_password.keys():
                            print("User does not exist. Please enter a valid username")
                        elif change_user in username_password.keys():
                            task_list[user_choice_vm_menu - 1]['username'] = change_user

                elif edit_or_complete == "A" and task_list[user_choice_vm_menu - 1]['completed'] == True:
                    print("You cannot edit this task as it has already been completed")   
                     
                elif edit_or_complete == "B":
                    task_list[user_choice_vm_menu - 1]['completed'] = "Yes" 
                    print(f"\nTask {user_choice_vm_menu} has been marked as complete")
                    break
                else:
                    print("Sorry, you have not selected a valid option.")
            


    # Creating two new files to store the task and user data for the gr option of the program
    # This option is only available to admin
    elif menu == 'gr' and curr_user == 'admin':
        with open('task_overview.txt' , 'w') as task_overview_file:

            # Variables created to count number of tasks, complete tasks, incomplete tasks and those overdue
            curr_date = datetime.now()
            total = 0
            completed_total = 0
            incompleted_total = 0
            overdue_tasks = 0

            for t in task_list:
                total += 1
                if t['completed'] == True:
                    completed_total += 1
                elif t['completed'] == False:
                    incompleted_total += 1
                if t['due_date'] > curr_date:
                    overdue_tasks += 1

            # Dictionaries created to store counts (task number, incomplete, complete and overdue) 
            # for each individual user 
            number_of_users = 0
            user_task_counter = {}
            user_incompleted_tasks = {}
            user_completed_tasks = {}
            user_overdue_tasks = {}

            for u in username_password:
                user_assigned = 0
                number_of_users += 1           
                for t in task_list:
                    if t['username'] == u:
                        user_assigned += 1
                    user_task_counter[u] = user_assigned
            for uin in username_password:
                user_incompleted = 0
                for t in task_list:
                    if t['username'] == uin and t['completed'] == False:
                        user_incompleted += 1
                    user_incompleted_tasks[uin] = user_incompleted
            for ucom in username_password:
                user_completed = 0
                for t in task_list:
                    if t['username'] == ucom and t['completed'] == True:
                        user_completed += 1
                    user_completed_tasks[ucom] = user_completed
            for uodue in username_password:
                user_overdue = 0
                for t in task_list:
                    if t['username'] == uodue and t['due_date'] > curr_date:
                        user_overdue += 1
                    user_overdue_tasks[uodue] = user_overdue                

        
            percentage_of_incomplete_tasks = (incompleted_total/total)*100
            percentage_of_overdue_tasks = (overdue_tasks/total)*100


            # Writing to the task overiew file
            task_overview_file.write("The total number of tasks in the task manager is: " + str(total) + "\n")
            task_overview_file.write("The total number of completed tasks is: " + str(completed_total) + "\n")
            task_overview_file.write("The total number of uncompleted tasks is: " + str(incompleted_total)+ "\n")
            task_overview_file.write("The total number of overdue tasks is: " + str(overdue_tasks)+ "\n")
            task_overview_file.write("The percentage of incomplete tasks is: " + str(percentage_of_incomplete_tasks) + "%\n")
            task_overview_file.write("The percentage of overdue tasks is: " + str(percentage_of_overdue_tasks) + "%\n")



        with open('user_overview.txt' , 'w') as user_overview_file:
            # Writing to the user overiew file
            user_overview_file.write("\nThe total number of registered users is: " + str(number_of_users))
            user_overview_file.write("\nThe total number of tasks in the task manager is: " + str(total))
            user_overview_file.write("\n-----------------------------------\n") 

            # For loop used to write for each user
            for u in username_password: 
                user_overview_file.write(f"\nThe total number of tasks assigned to user " + u + " =  " + str(user_task_counter[u]) + "\n")
                if user_task_counter[u] > 0:
                    user_incomplete_percentage = (user_incompleted_tasks[u]/user_task_counter[u])*100
                    user_overview_file.write(f"Their percentage of incomplete tasks = " + str(user_incomplete_percentage) + "%\n")
                    user_complete_percentage = (user_completed_tasks[u]/user_task_counter[u])*100
                    user_overview_file.write(f"Their percentage of complete tasks = " + str(user_complete_percentage) + "%\n")
                    user_overdue_percentage = (user_overdue_tasks[u]/user_task_counter[u])*100
                    user_overview_file.write(f"Their percentage of overdue tasks = " + str(user_overdue_percentage) + "%\n")
                    user_overview_file.write("-----------------------------------\n")
                else:
                    continue
               
    # Menu option to display statistics which prints the information from the task overview and user overview files
    # This option is only available to the admin user
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)
      

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------") 

        with open('task_overview.txt' , 'r') as task_overview_file:
            task_overview_contents = ""
            for line in task_overview_file:
                task_overview_contents = task_overview_contents + line + "\n"
        print(task_overview_contents)
        print("-----------------------------------") 
        
        with open('user_overview.txt' , 'r') as user_overview_file:
            user_overview_contents = ""
            for line in user_overview_file:
                user_overview_contents = user_overview_contents + line + "\n"  
        print(user_overview_contents)
         


    # Option to end the program
    # At this point, all changes are written to tasks.txt so that they are saved for when the program is next used
    elif menu == 'e':
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))


        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")