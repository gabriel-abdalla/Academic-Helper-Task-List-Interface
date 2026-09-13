"""
Task Interface
UI Program involving tasks
ICS4U
Gabriel Abdalla
History:
    January 13, 2026 - Program Creation
    March 25, 2026 - Program Completion
    April 14. 2026 - JSON UPDATE
"""

from taskclass import Task_List, Task
import tkinter as tk
from tkinter import messagebox
import random, json
from tkextrafont import Font

# ----- Constants -----
WIDTH = 500
HEIGHT = 400


# ----- Classes -----
class AppState:
    """
    Class for the app state
    Attributes:
        + current_screen (str)
        + current_message (bool)
        + edited_value (bool)
        + current_task (bool)
        + specific_task (bool)
    """
    def __init__(self):
        self.current_screen = "menu"
        self.current_message = None
        self.edited_value = None
        self.current_task = None
        self.specific_task = None
        
state = AppState()

# ----- Intialization -----

root = tk.Tk()
root.title("Task Window")
root_img = tk.PhotoImage(file = 'assets/lockedin_mascot.png')
root.wm_iconphoto(False, root_img)
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False) 

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# THIS SETS THE FONT
font = Font(file="fonts/sniglet.ttf", family="Sniglet")
root.option_add("*Font", "Sniglet 10")

# Colour display changes
root.option_add('*Button.Background', "#6c96cf")
root.option_add('*Button.Foreground', 'white')
root.option_add('*Entry.background', '#6c96cf')
root.option_add('*Entry.foreground', 'white')
root.option_add('*Label.background', '#6c96cf')
root.option_add('*Label.foreground', 'white')
root.option_add('*Frame.background', '#6c96cf')
root.option_add('*Canvas.background', '#6c96cf')


main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(0, weight=1)

bg = tk.PhotoImage(file = "assets/g_task_list.png")
bg_label = tk.Label(main_frame, image = bg)
bg_label.place(x = 0, y = 0)

# Top Label
label = tk.Label(main_frame, text="TASKS", font=("Sniglet", 24))
label.grid(row=0, column=0, pady=20)

# Debug Label (Commented out for final)
screen_debug = tk.Label(main_frame, text=f"Current screen: {state.current_screen}", font=("Sniglet", 10))
#screen_debug.grid(row=4, column=0)

# Frames
menu_frame = tk.Frame(main_frame)
task_list_scroll_frame = tk.Frame(main_frame)
task_list_options_frame = tk.Frame(main_frame) 
within_a_task_active_frame = tk.Frame(main_frame) 
editing_menu_frame = tk.Frame(main_frame) 
enter_a_value_frame = tk.Frame(main_frame) 
within_a_task_completed_frame = tk.Frame(main_frame) 

menu_frame.grid(row=2, column=0, pady=10)

for frame in (menu_frame, task_list_scroll_frame, task_list_options_frame):
    frame.columnconfigure(0, weight=1)

# Canvas intialization for scrolling

canvas = tk.Canvas(task_list_scroll_frame, highlightthickness=0, height=150)
scrollbar = tk.Scrollbar(task_list_scroll_frame, orient="vertical", command=canvas.yview)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

task_list_scroll_frame.columnconfigure(0, weight=1)

scrollable_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scrollregion)

def resize_frame(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", resize_frame)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

my_value = tk.StringVar()

# Load data from json file.
Task_List.load_from_json()

# ----- Functions -----

def on_closing():
    """
    Saves data to JSON and closes the application.
    """
    try:
        # Save the data to json
        Task_List.save_to_json() 
        print("Data saved successfully.")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save tasks: {e}")
    
    root.destroy()


def generate_number_string():
    """
    Generates a random number string of 10 numbers.
    
    Returns:
        new_id(str):   random 10 digits as a string
    """
    all_tasks = Task_List.task_list + Task_List.completed_task_list
    ids = {task.task_idd for task in all_tasks}

    while True:
        new_id = ''.join(str(random.randint(0, 9)) for _ in range(10))
        if new_id not in ids:
            return new_id

def set_screen(state, name):
    """
    Switches the screen state.
    Args:
        state (AppState) - Stores the current application state and values.
        name (str) - Name of the new state.
    Returns:
        None
    """
    state.current_screen = name
    screen_debug.config(text=f"Current screen: {name}")
    print("SCREEN ->", name)

def on_enter(state, event):
    """
    Function called when the user presses Enter in the input box.

    Args:
        state (AppState) - Stores the current application state and values.
        event (tk.Event) - The Tkinter event object triggered by pressing a key (specifically the Return/Enter key).

    Returns:
        None
    """
    # If in the message entering screen, save the message.
    if state.current_screen == "entering_a_value" and state.edited_value == "message":
        state.current_task.task_message = my_value.get()
    
    # If in the deadline entering screen, save the deadline.
    elif state.current_screen == "entering_a_value" and state.edited_value == "deadline":
        try:
            state.current_task.deadline = my_value.get()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter the date using the MM/DD/YYYY format.")
            return
            
    # If in the add_task entering screen, save the message.
    elif state.current_screen == "add_task" and state.edited_value == "message":
        state.current_message = my_value.get()
        options_for_changing_values(state, "deadline") # Switch to enter a deadline for a new task.
    
    # If in the task entering screen, save the deadline
    elif state.current_screen == "add_task" and state.edited_value == "deadline":
        try:
            t = Task_List.create_task(state.current_message, generate_number_string(), my_value.get()) # Create a task with the information.
            state.current_message = None
            exit_button_choices(state)
            handle_menu(state, "main_button")
            handle_menu(state, "main_button")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter the date using the MM/DD/YYYY format.")
            return

    inputbox.delete(0, tk.END)

    if state.current_screen == "entering_a_value":
        for i in range(3):
            exit_button_choices(state)

def handle_menu(state, button):
    """
    Function to handle the screen menu.

    Args:
        state (AppState) - Stores the current application state and values.
        button (str) - The string representing which button intiated the function.

    Returns:
        None
    """
    if button == "main_button": # If the button is the "main button"

        if state.current_screen == "menu": # Moves the screen to the task list menu
            menu_frame.grid_remove()
            task_list_options_frame.grid(row=2, column=0, pady=10)
            exit_button.config(text="back to menu", font=("Sniglet", 12))
            set_screen(state, "task_list")
            menu_button.config(text="View Active Tasks", font=("Sniglet", 18))

        elif state.current_screen == "task_list": # Moves the screen to the active task list
            render_tasklist("main_button")
            task_list_options_frame.grid_remove()
            task_list_scroll_frame.grid(row=2, column=0, pady=10)
            set_screen(state, "active_task_list")
            menu_button.grid_remove()
            completed_task_list_button.grid_remove()
            task_listlabel.grid(row=1, column=0, pady=5)

    elif button == "add_button": # If the button is the Add Task button
    
        if state.current_screen == "menu": # Moves the screen to the add task screen
            set_screen(state, "add_task")
            menu_button.grid_remove()
            options_for_changing_values(state, "message")
            exit_button.config(text="Back to the menu", font=("Sniglet", 12))

    elif button == "Task_button": # If the button is the completed task button
        
        if state.current_screen == "task_list": # Moves the screen to the completed task list
            render_tasklist("Task_button")
            task_list_options_frame.grid_remove()
            task_list_scroll_frame.grid(row=2, column=0, pady=10)
            set_screen(state, "completed_task_list")
            menu_button.grid_remove()
            completed_task_list_button.grid_remove()
            task_listlabel.grid(row=1, column=0, pady=5)

def task_interface(state, task):
    """
    Function to handle the task UI.

    Args:
        state (AppState) - Stores the current application state and values.
        task (Task) - The task the user selected on within the canvas list.

    Returns:
        None
    """
    if state.current_screen not in ("active_task_list", "completed_task_list"):
        return

    state.specific_task = task
    task_list_scroll_frame.grid_remove()
    task_listlabel.grid_remove()

    if state.current_screen == "active_task_list": # If the list was the active list, show a label with a deadline.
        frame = within_a_task_active_frame
        label = task_info_label
        screen_name = "within_a_task(active)"
        text = (
            f"Task ID: {task.task_idd}\n"
            f"Message: {task.task_message}\n"
            f"Created on: {task.date_of_creation}\n"
            f"Deadline: {task.deadline}"
        )
    else: # If the list was the completed list, show a label with a deadline.
        frame = within_a_task_completed_frame
        label = task_info_label2
        screen_name = "within_a_task(completed)"
        text = (
            f"Task ID: {task.task_idd}\n"
            f"Message: {task.task_message}\n"
            f"Created on: {task.date_of_creation}\n"
            f"Completed: {task.date_of_completion}"
        )

    frame.grid(row=2, column=0, pady=10)
    set_screen(state, screen_name)
    label.config(text=text)
        
def render_tasklist(button):
    """
    Function to render the completed or active task list.

    Args:
        button (str) - The string representing which button intiated the function.

    Returns:
        None
    """
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
        
    if button == "main_button": # If the active button is clicked, display active tasks.
        if not Task_List.task_list:
            tk.Label(scrollable_frame, text="You have no tasks.", font=("Sniglet", 8)).pack(pady=5)
        else:
            for i in Task_List.task_list:
                task = i
                g = f"Task: {i.task_message}, created on {i.date_of_creation}.. Due:{i.deadline}."
                tk.Button(scrollable_frame, text=g, font=("Sniglet", 8),
                          command=lambda t=task: task_interface(state, t)).pack(pady=5)
    elif button == "Task_button": # If the completed button is clicked, display completed tasks.
        if not Task_List.completed_task_list:
            tk.Label(scrollable_frame, text="You have no completed tasks.", font=("Sniglet", 8)).pack(pady=5)
        else:
            for i in Task_List.completed_task_list:
                task = i
                g = f"Task: {i.task_message}, created on {i.date_of_creation}, Completed:{i.date_of_completion}."
                tk.Button(scrollable_frame, text=g, font=("Sniglet", 8),
                          command=lambda t=task: task_interface(state, t)).pack(pady=5)

def exit_button_choices(state):
    """
    Function to handle the exit button logic.

    Args:
        state (AppState) - Stores the current application state and values.

    Returns:
        None
    """
    
    if state.current_screen == "task_list": # If the current screen is the task list menu, take the user back to the menu.
        task_list_options_frame.grid_remove()
        menu_frame.grid(row=2, column=0, pady=10)
        set_screen(state, "menu")
        exit_button.config(text="EXIT", font=("Sniglet", 24))
        menu_button.grid(row=1, column=0, pady=10)
        menu_button.config(text="View Tasks", font=("Sniglet", 18))

    elif state.current_screen in ("active_task_list", "completed_task_list"): # If the current screen is the completed/active task lists, take the user back to the task list menu.
        task_list_scroll_frame.grid_remove()
        task_list_options_frame.grid(row=2, column=0, pady=10)
        set_screen(state, "task_list")
        exit_button.config(text="back outside the menu", font=("Sniglet", 12))
        completed_task_list_button.grid(row=1, column=0, pady=5)
        menu_button.grid(row=1, column=0, pady=10)
        task_listlabel.grid_remove()
        instructions_msg.grid_remove()

    elif state.current_screen == "within_a_task(active)": # If the current screen is the menu inside an active task, take the user back to the active list.
        render_tasklist("main_button")
        within_a_task_active_frame.grid_remove()
        task_list_scroll_frame.grid(row=2, column=0, pady=10)
        set_screen(state, "active_task_list")
        task_listlabel.grid(row=1, column=0, pady=5)

    elif state.current_screen == "within_a_task(completed)": # If the current screen is the menu inside an completed task, take the user back to the completed list.

        render_tasklist("Task_button")
        within_a_task_completed_frame.grid_remove()
        task_list_scroll_frame.grid(row=2, column=0, pady=10)
        set_screen(state, "completed_task_list")
        task_listlabel.grid(row=1, column=0)

    elif state.current_screen == "editing_a_task": # If the current screen is the edit menu, take the user back to the options for that active task.
        editing_menu_frame.grid_remove()
        within_a_task_active_frame.grid(row=2, column=0, pady=10)
        set_screen(state, "within_a_task(active)")

    elif state.current_screen == "entering_a_value": # If the current screen is the input box for either the deadline or message, take the user back to the edit menu.
        enter_a_value_frame.grid_remove()
        editing_menu_frame.grid(row=2, column=0, pady=10)
        set_screen(state, "editing_a_task")

    elif state.current_screen == "add_task": # If the user is in any menu relating to adding a task (entering values), take them back to the menu.
        enter_a_value_frame.grid_remove()
        menu_frame.grid(row=2, column=0, pady=10)
        exit_button.config(text="back to menu", font=("Sniglet", 12))
        menu_button.grid(row=1, column=0, pady=10)
        set_screen(state, "menu")

    else:
        on_closing()

def task_options_for_interface(option, state):
    """
    Function to execute the user's wish in relation to a specific task.

    Args:
        state (AppState) - Stores the current application state and values.
        option (str) - The user's selected action for the task.

    Returns:
        None
    """
    if option == "delete": # Deletes the task
        Task_List.remove_task(state.specific_task)
        exit_button_choices(state)
    elif option == "edit": # Moves the task to another attribute to be edited.
        set_screen(state, "editing_a_task")
        within_a_task_active_frame.grid_remove()
        editing_menu_frame.grid(row=2, column=0, pady=10)
        state.current_task = state.specific_task
    elif option == "check": # Checks the task and moves it to the completed list.
        Task_List.complete_task(state.specific_task)
        exit_button_choices(state)
    elif option == "uncheck": # Unchecks the task and moves it to the active list.
        Task_List.uncomplete_task(state.specific_task)
        exit_button_choices(state)
        

def options_for_changing_values(state, option):
    """
    Function to set up the input box frames with instructions to guide the user.

    Args:
        state (AppState) - Stores the current application state and values.
        option (str) - The user's selected action for the task.

    Returns:
        None
    """
    instructions_msg.grid_remove()

    if state.current_screen != "add_task": # Sets up inputing menu for the add_task feature
        set_screen(state, "entering_a_value")

    enter_a_value_frame.grid(row=2, column=0, pady=10)
    editing_menu_frame.grid_remove()

    if option == "deadline": # Extra instructions for inputing a deadline
        instructions_msg.config(text=f"Enter the date as month/day/year for deadline -> e.g (Today) {Task_List.date_conversion()}")
    else: # Extra instructions for inputing a message
        instructions_msg.config(text="Enter any message for this task")

    instructions_msg.grid(row=1, column=0)
    state.edited_value = option

# =========================
# --- UI SETUP ---
# =========================

# --- FRAME CONFIG ---
within_a_task_active_frame.columnconfigure(0, weight=0)
within_a_task_active_frame.columnconfigure(1, weight=0)
within_a_task_active_frame.columnconfigure(2, weight=0)


# =========================
# --- BUTTONS ---
# =========================

# Main / Navigation
add_button = tk.Button(
    menu_frame, text="Add Task", font=("Sniglet", 18),
    command=lambda: handle_menu(state, "add_button")
)

menu_button = tk.Button(
    main_frame, text="View Tasks", font=("Sniglet", 18),
    command=lambda: handle_menu(state, "main_button")
)

completed_task_list_button = tk.Button(
    task_list_options_frame, text="View Completed Tasks", font=("Sniglet", 15),
    command=lambda: handle_menu(state, "Task_button")
)

exit_button = tk.Button(
    main_frame, text="EXIT", font=("Sniglet", 24),
    bg="red", command=lambda: exit_button_choices(state)
)


# Task Actions
edit_button = tk.Button(
    within_a_task_active_frame, text="Edit Task", font=("Sniglet", 18),
    command=lambda: task_options_for_interface("edit", state)
)

check_button = tk.Button(
    within_a_task_active_frame, text="Check Task", font=("Sniglet", 18), bg="green",
    command=lambda: task_options_for_interface("check", state)
)

delete_button = tk.Button(
    within_a_task_active_frame, text="Delete Task", font=("Sniglet", 18), bg="red",
    command=lambda: task_options_for_interface("delete", state)
)

uncheck_button = tk.Button(
    within_a_task_completed_frame, text="Uncheck Task", font=("Sniglet", 18),
    command=lambda: task_options_for_interface("uncheck", state)
)


# Edit Options
deadline_button = tk.Button(
    editing_menu_frame, text="Edit deadline", font=("Sniglet", 18),
    command=lambda: options_for_changing_values(state, "deadline")
)

message_button = tk.Button(
    editing_menu_frame, text="Edit message", font=("Sniglet", 18),
    command=lambda: options_for_changing_values(state, "message")
)


# =========================
# --- LABELS ---
# =========================

task_info_label = tk.Label(
    within_a_task_active_frame, text="", font=("Sniglet", 9),
    justify="left", wraplength=400
)

task_info_label2 = tk.Label(
    within_a_task_completed_frame, text="", font=("Sniglet", 9),
    justify="left", wraplength=400
)

task_listlabel = tk.Label(
    task_list_scroll_frame, text="Click on a task to see options"
)

instructions_msg = tk.Label(
    enter_a_value_frame, text="Enter the date as month/day/year", font=("Sniglet", 8)
)


# =========================
# --- INPUT ---
# =========================

inputbox = tk.Entry(
    enter_a_value_frame, font=("Sniglet", 14),
    textvariable=my_value
)

inputbox.bind('<Return>', lambda event: on_enter(state, event))

# =========================
# --- LAYOUT (GRID) ---
# =========================

# Main
add_button.grid(row=0, column=0, pady=5, sticky="ew")
menu_button.grid(row=1, column=0, pady=10)
exit_button.grid(row=3, column=0, pady=20)

# Task Actions (within_a_task_active_frame)
task_info_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

edit_button.grid(row=1, column=0, pady=5, padx=5)
check_button.grid(row=1, column=1, pady=5, padx=5)
delete_button.grid(row=1, column=2, pady=5, padx=5)

# Uncheck (separate frame)
task_info_label2.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")
uncheck_button.grid(row=1, column=1, pady=5, padx=5)

# Edit Options (editing_menu_frame)
deadline_button.grid(row=0, column=0, pady=5, sticky="ew")
message_button.grid(row=1, column=0, pady=5, sticky="ew")

# Input area
inputbox.grid(row=2, column=0, pady=10, sticky="ew")
instructions_msg.grid(row=1, column=0, pady=5)

# Task list area
completed_task_list_button.grid(row=1, column=0, pady=5)

# Function to activate when the user clicks x.
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
