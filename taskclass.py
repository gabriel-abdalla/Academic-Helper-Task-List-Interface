"""
Task Class
UI Program involving tasks
ICS4U
Gabriel Abdalla
History:
    January 13, 2026 - Program Creation
    March 25, 2026 - Program Completion
    April 14. 2026 - JSON UPDATE
"""

from datetime import date
import json

class Task_List():
    """
    Class for different tasks.
    Attributes (class):
        + task_list (list)
        + completed_task_list (list)
    Methods:
        + date_conversion(): str
        + remove_task(task): void
        + complete_task(task): void
        + uncomplete_task(task): void
        + create_task(msg, idd, deadline): Task
        + to_a_dictionary(): dict
        + load_from_json(filename): void
        + save_to_json(): void
        + from_a_dictionary(data, type): Task
    """
    
    # Class Attributes
    task_list = []
    completed_task_list = []
    
    @staticmethod
    def date_conversion():
        """
        Returns the current day
        Returns:
            formatted_date (str)
        """
        today = date.today()
        
        # Format as 'MM/DD/YYYY'
        formatted_date = today.strftime("%m/%d/%Y")
        return formatted_date
    
    @staticmethod    
    def remove_task(task):
        """
        Removes a task from the active task list.
        Args:
            task (Task)
        """
        Task_List.task_list.remove(task)
    
    @staticmethod            
    def complete_task(task):
        """
        Sends a task to the completed task list.
        Args:
            task (Task)
        """
        task.date_of_completion = Task_List.date_conversion() 
        Task_List.completed_task_list.append(task)
        Task_List.task_list.remove(task)
                
    @staticmethod            
    def uncomplete_task(task):
        """
        Sends a completed task back to the active list.
        Args:
            task (str)
        """
        task.date_of_completion = None
        Task_List.task_list.append(task)
        Task_List.completed_task_list.remove(task)
    
    @staticmethod            
    def create_task(msg, idd, deadline):
        """
        Creates a task based on collected data
        Args:
            msg (str)
            idd (str)
            deadline(str)
        Return:
            (Task)
        """
        return Task(msg, idd, deadline)

    @staticmethod
    def to_a_dictionary():
        """
        Converts the two task list's tasks into dictionaries for use in json
        Args:
            (dict)
        """
        return {
            "task_list": [task.to_a_dictionary() for task in Task_List.task_list],
            "completed_task_list": [task.to_a_dictionary() for task in Task_List.completed_task_list]
        }
    
    @staticmethod
    def load_from_json(filename="task_saveddata.json"):
        """
        Loads the dictionaries from json and converts them back into tasks, restoring data from previous use.
        Args:
            filename (str) - The json file itself

        Returns:
            None
        """
        try:
            with open(filename, "r") as f:
                # This will fail if the file is empty or doesn't exist
                data = json.load(f)
                
            # Rebuilds the tasks for the active task list.
            for task_data in data.get("task_list", []):
                t = Task_List.from_a_dictionary(task_data, "active")

            # Rebuilds the tasks for the completed task list.
            for task_data in data.get("completed_task_list", []):
                ct = Task_List.from_a_dictionary(task_data, "completed")

        # Error checking to handle files with error or corruption. 
        except (FileNotFoundError, json.JSONDecodeError):
            print("File cleared. File was missing or empty.")
            Task_List.task_list = []
            Task_List.completed_task_list = []

    @staticmethod
    def save_to_json():
        """
        Saves the tasks in both lists as dictionaries and exports them to the json file.
        """
        data = Task_List.to_a_dictionary()
        print(f"Data being saved is: {data}") 
        with open("task_saveddata.json", "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def from_a_dictionary(data, type):
        """
        Extracts the data from the JSON file, returning the dictionaries as tasks in their respective lists.
        Args:
            data (dict) - dictionary with all JSON data for a task
            type (str)  - determines whether it's a completed task or an incomplete task

        Returns:
            task (Task)
        """
        task = Task_List.create_task(data["task_message"], data["task_idd"], data["deadline"])
        task.date_of_creation = data["date_of_creation"]

        if type == "completed":
            task.date_of_completion = data["date_of_completion"]
            Task_List.completed_task_list.append(task)
            Task_List.task_list.remove(task)


        return task
                
        
class Task():
    """
    Class for different tasks.
    Attributes (instance):
        + task_message (str)
        - task_idd (str)
        - date_of_completion (str)
        - date_of_creation (str)
        - deadline (str)
    Methods:
        + __init__(task_message, task_idd, deadline): void
        - task_idd(self): str
        - task_idd(self, idd_newval): void
        - date_of_completion(self): str
        - date_of_completion(self, val): void
        - date_of_creation(self): str
        - date_of_creation(self, val): void
        - deadline(self): str
        - deadline(self, val): void
        + date_verification(val): bool
        + __repr__(self): str
        + to_a_dictionary(self): dict
    """
    def __init__(self, task_message, task_idd, deadline):
        """
        Initializes a new task object
        Args:
            task_message (str)
            task_idd (str)
            deadline (str)
        """
        self.task_message = task_message
        self.task_idd = task_idd
        self.date_of_completion = None
        current_date = Task_List.date_conversion()
        self.date_of_creation = current_date
        self.deadline = deadline
        Task_List.task_list.append(self)

    @property
    def task_idd(self):
        """Returns the book's tasks idd."""
        return self._task_idd

    @task_idd.setter
    def task_idd(self, val):
        """
        Set a valid task ID (10-digit numeric string) and ensure it's unique.
    
        Args:
            val (str): Proposed task ID
    
        Raises:
            ValueError: If ID is not 10 digits or already exists.
        """
        # Ensures it is a string of exactly 10 digits
        if not isinstance(val, str) or len(val) != 10 or not val.isdigit():
            raise ValueError("Task ID must be exactly 10 digits.")
    
        # Checks uniqueness in the task list, excluding self if already in list
        for task in Task_List.task_list:
            if task is not self and task.task_idd == val:
                raise ValueError("This Task ID already exists!")
    
        self._task_idd = val
            
    @property
    def date_of_completion(self):
        """Returns the list with the three important dates."""
        return self._date_of_completion
        
    @date_of_completion.setter
    def date_of_completion(self, val):
        """
        Method to set a valid date, if not valid, raise an error
        Args:
            val (str)
        Raises:
            ValueError: If the input is not in correct date format or a None then it raises an error.
        """
        if val == None:
            self._date_of_completion = val
        else:
            if Task.date_verification(val):
                self._date_of_completion = val
            else:
                raise ValueError("Invalid date format")
            
    @property
    def date_of_creation(self):
        """Returns the list with the three important dates."""
        return self._date_of_creation
        
        
    @date_of_creation.setter
    def date_of_creation(self, val):
        """
        Method to set a valid date, if not valid, raise an error
        Args:
            val (str)
        Raises:
            ValueError: If the input is not in correct date format then it raises an error.
        """
        if Task.date_verification(val):
            self._date_of_creation = val
        else:
            raise ValueError("Invalid date format")
        
    @property
    def deadline(self):
        """Returns the list with the three important dates."""
        return self._deadline
        
    @deadline.setter
    def deadline(self, val):
        """
        Method to set a valid date, if not valid, raise an error
        Args:
            val (str)
        Raises:
            ValueError: If the input is not in correct date format then it raises an error.
        """
        if Task.date_verification(val):
            self._deadline = val
        else:
            raise ValueError("Invalid date format")
        
    @staticmethod    
    def date_verification(val):
        """
        Utility function to verify if the date is provided in the correct format.
        Args:
            val (str)
        Returns
            returned_val (bool)
        """
        returned_val = True
        # Checks is the string is 10 characters long.
        if len(val) != 10:
            returned_val = False
        
        # Checks if the slashes are in the right places
        if val[2] != "/" or val[5] != "/":
            returned_val = False
    
        month, day, year = val.split("/")
        
        # Checks if the month, days, and years are numbers.
        if not (month.isdigit() and day.isdigit() and year.isdigit()):
            returned_val = False
    
        month = int(month)
        day = int(day)
        
        # Checks if the month is between 1 and 12.
        if month < 1 or month > 12:
            returned_val = False
        # Checks if the day is between 1 and 31.
        if day < 1 or day > 31:
            returned_val = False
    
        return returned_val
        

    def __repr__(self):
        """
        Returns developer string for class use.
        Args:
            None
        Returns:
            (str)
        """
        return (
            f"Task(message={self.task_message!r}, "
            f"idd={self.task_idd!r}, "
            f"completion={self.date_of_completion!r}, "
            f"creation={self.date_of_creation!r}, "
            f"deadline={self.deadline!r}" 
        )
    
    def to_a_dictionary(self):
        """
        Turns a task into a dictionary for json use.
        Args:
            None
        Returns:
            (dict)
        """
        return {
            "task_message": self.task_message,
            "task_idd": self.task_idd,
            "date_of_completion": self.date_of_completion,
            "date_of_creation": self.date_of_creation,
            "deadline": self.deadline
        }