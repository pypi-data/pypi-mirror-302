import json
from json import JSONDecodeError
from datetime import date
from typing import List, Dict, Union, Optional, Literal, Tuple
import os
class TaskManager():
    """
    TaskManager provides functionality for managing tasks, including adding, removing, marking tasks as done, 
    saving/loading task states from a JSON file, and generating task reports. Tasks can be assigned priorities 
    (either strings or integers), and the task list can be customized or sorted based on these priorities.

    Attributes:
        to_do (dict): Dictionary of tasks yet to be completed, with task names as keys and their priorities as values.
        done (dict): Dictionary of tasks that have been completed, with task names as keys and their priorities as values.
        daily_added_tasks (dict): Dictionary of tasks added during the current day, used for reporting.
        daily_completed_tasks (dict): Dictionary of tasks completed during the current day, used for reporting.
        priority_levels (list): List of acceptable priority levels, either strings or integers.
        default_priority (str or int): The default priority level for new tasks.
        priorities_type (str or int): Defines the type of priorities used (string or integer).
    """

    def __init__(self, priority_levels: List[Union[str, int]] = ['high', 'medium', 'low'], default_priority: Union[str, int] = 'medium', priorities_type: Literal[str, int] = str) -> None: 
        """
            Initializes a new TaskManager instance with optional customizable priority levels.

            Args:
                priority_levels (list): A list of acceptable priority levels (string or integer). Defaults to ['high', 'medium', 'low'].
                default_priority (str or int): The default priority assigned to tasks if not specified. Defaults to 'medium'.
                priorities_type (str or int): Defines the type of priorities (either 'str' for string or 'int' for integer). Defaults to str.

            Attributes:
                to_do (dict): Tasks yet to be completed, with task names as keys and priorities as values.
                done (dict): Completed tasks, with task names as keys and priorities as values.
                daily_added_tasks (dict): Tasks added during the current day.
                daily_completed_tasks (dict): Tasks completed during the current day.
                priority_levels (list): A list of valid priority levels.
                default_priority (str or int): Default priority level assigned to new tasks.
                priorities_type (str or int): Defines the type of priority (either string or integer).
        """
        self.daily_added_tasks: Dict[str, Union[str, int]] = {}
        self.daily_completed_tasks: Dict[str, Union[str, int]] = {}
        self.to_do: Dict[str, Union[str, int]] = {}
        self.done: Dict[str, Union[str, int]] = {}
        self.priority_levels: List[Union[str, int]] = priority_levels
        self.default_priority: Union[str, int] = default_priority
        self.priorities_type: Literal[str, int] = priorities_type
    @property
    def data(self) -> Dict[str, Dict[str, Dict[str, Union[str, int]]]]:
        return {
            'to_do': self.to_do,
            'done': self.done,
            'daily added tasks': self.daily_added_tasks,
            'daily completed tasks': self.daily_completed_tasks
        }
    def save_current_state(self,data_file_path: str = './data.json') -> str:        
        """
        Saves the current state of the task manager to a JSON file.

        The current state includes tasks in the to-do, done, and reporting lists. The data is serialized
        and saved as a JSON file in the specified directory.

        Args:
            data_file_path (str): The file path where the task state will be saved. Defaults to './data.json'.

        Returns:
            str: A message indicating whether the data was successfully saved, or if an error occurred.
        """

        if not data_file_path:
            return f"{data_file_path} is invalid as a data file path to save to."   

        with open(data_file_path, 'w') as data_safe:
            json.dump(self.data, data_safe, indent=2)
        return f"Data written succesfully at \"{data_file_path}\" ."
    
    def load_state(self,data_file_path: Optional[str] = './data.json') -> str:
        """
        Loads a task manager state from a JSON file.

        This method retrieves and loads the saved task state from the specified JSON file. If the file 
        does not exist or contains invalid data, the state will be reset and a fresh start initiated.

        Args:
            data_file_path (str, optional): The file path from which to load the state. Defaults to './data.json'.

        Returns:
            str: A message indicating whether the data was successfully loaded or if an error occurred.
        """

        if not os.path.exists(data_file_path):
            self.clear()
            return f"\"{data_file_path}\" Doesn't exist. Starting fresh."

        try:
            with open(data_file_path, 'r') as data_safe:
                data = json.load(data_safe)
            self.to_do = data.get('to_do', {})
            self.done = data.get('done', {})
            self.daily_added_tasks = data.get('daily added tasks', {})
            self.daily_completed_tasks = data.get('daily completed tasks', {})

            return "Data loaded succesfully, ready to go!"
        except FileNotFoundError:
            self.clear()
            return 'No saved data found starting fresh.'  
        except JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            self.clear()
            return "Error loading data. Starting fresh."       

    def add_task(self, *tasks_priorities: Union[str, Tuple[str, Union[str, int]]]) -> str:  
        """
        Adds one or more tasks to the to-do list if they are not already present.

        Args:
            *tasks_priorities: The tasks to be added to the to-do list. Can be a string (task name) or a tuple (task name, priority).

        Returns:
            str: A message indicating which tasks were added or already exist in the list.
        """
        added_tasks = []
        not_added = []
        not_added_existence = []
        not_added_priority = []
        for tasks in tasks_priorities:
            if isinstance(tasks, tuple) and len(tasks) == 2:
                task, priority = tasks
            elif isinstance(tasks, str):
                task, priority = tasks, self.default_priority
            else:
                print(f"{tasks} can't be added.")
                continue
            if self.priorities_type == str:
                if task.lower() not in [task.lower() for task in self.to_do] and priority.lower() in [p.lower() for p in self.priority_levels]:
                    self.to_do[task] = priority
                    self.daily_added_tasks[task] = priority
                    added_tasks.append(f"{task} (Priority: {priority})") 
                elif task.lower() in [task.lower() for task in self.to_do] and priority.lower() not in [p.lower() for p in self.priority_levels]:
                    not_added.append(task)
                elif task.lower() in [task.lower() for task in self.to_do]:
                    not_added_existence.append(task)
                elif priority.lower() not in [p.lower() for p in self.priority_levels]:
                    not_added_priority.append(f'{task} (Priority: {priority})')
            elif self.priorities_type == int:
                if task.lower() not in [task.lower() for task in self.to_do] and priority in self.priority_levels:
                    self.to_do[task] = priority
                    self.daily_added_tasks[task] = priority
                    added_tasks.append(f"{task} (Priority: {priority})") 
                elif task.lower() in [task.lower() for task in self.to_do] and priority not in self.priority_levels:
                    not_added.append(task)
                elif task.lower() in [task.lower() for task in self.to_do]:
                    not_added_existence.append(task)
                elif priority not in self.priority_levels:
                    not_added_priority.append(f'{task} (Priority: {priority})')

        response = []
        if added_tasks:
            if len(added_tasks) == 1:
                response.append(f"{', '.join(added_tasks)} added successfully.")
            else:
                response.append(f"{', '.join(added_tasks)} added successfully.")
        if not_added:
            if len(not_added) == 1:
                response.append(f"{', '.join(not_added)} wasn't added to the To-Do list.\n ")
            else:
                response.append(f"{', '.join(not_added)} weren't added to the To-Do list.\n ")
        if not_added_existence:
            if len(not_added_existence) == 1:
                response.append(f"{', '.join(not_added_existence)} is already in the To-Do list:\n {self.current_state('to-do')}")
            else:
                response.append(f"{', '.join(not_added_existence)} are already in the To-Do list:\n {self.current_state('to-do')}")
        if not_added_priority:
            if len(not_added_priority) == 1:
                response.append(f"{', '.join(not_added_priority)} has an invalid priority. Available priorities are:\n{self.priority_levels} ")
            else:
                response.append(f"{', '.join(not_added_priority)} have an invalid priority. Available priorities are:\n{self.priority_levels} ")

        return " ".join(response)
    def remove_task(self,*tasks: str) -> str:
        """
        Removes one or more tasks from the to-do list.

        Args:
            *tasks: One or more tasks to remove from the to-do list.

        Returns:
            A message indicating whether the tasks were removed successfully.
        """
        removed_tasks = []
        not_found_tasks = []
        task_keys = {task.lower(): task for task in self.to_do.keys()}
        for task in tasks:
            if task.lower() in task_keys:
                og_task = task_keys[task.lower()]
                self.to_do.pop(og_task)
                self.daily_added_tasks.pop(og_task)
                removed_tasks.append(og_task)
            else:
                not_found_tasks.append(task)

        if removed_tasks and not_found_tasks:
            return f"{', '.join(removed_tasks)} removed successfully. However, {', '.join(not_found_tasks)} not found in the to-do list."
        elif removed_tasks:
            return f"{', '.join(removed_tasks)} removed successfully."
        elif not_found_tasks:
            return f"{', '.join(not_found_tasks)} not found in the to-do list."

    def task_done(self, *tasks: str) -> str:
        """
        Marks one or more tasks as done by moving them from the to-do list to the done list.

        Tasks are moved from the to-do list to the done list. If a task is already in the done list, it will 
        not be marked again.

        Args:
            *tasks (str): The task names to be marked as done.

        Returns:
            str: A message indicating which tasks were successfully marked as done, already completed, or not found.
        """

        done_tasks = []
        already_done_tasks = []
        absent_tasks = []
        task_keys = {task.lower(): task for task in self.to_do.keys()}
        for task in tasks:
            if task.lower() in task_keys:  
                original_task = task_keys[task.lower()]  
                if original_task not in self.done:  
                    self.done[original_task] = self.to_do[original_task]  
                    self.daily_completed_tasks[original_task] = self.to_do[original_task]  
                    self.to_do.pop(original_task)  
                    done_tasks.append(original_task)  
                else:
                    already_done_tasks.append(original_task) 
            else:
                absent_tasks.append(task)  
        response = []
        if done_tasks:
            response.append(f"{', '.join(done_tasks)} marked as done.")
        if already_done_tasks:
            response.append(f"{', '.join(already_done_tasks)} already done.")
        if absent_tasks:
            response.append(f"{', '.join(absent_tasks)} not in to-do list.")
        return " ".join(response)

    def _format_task_list(self, tasks: Dict[str, Union[str, int]], which_one: str) -> str :
        """
        Formats a dictionary of tasks for display, numbering them and displaying their priority levels.

        The tasks are sorted by their priority levels and formatted into a numbered list for easier reading.

        Args:
            tasks (dict): Dictionary of tasks with task names as keys and priorities as values.
            which_one (str): Specifies whether the tasks are 'to-do' or 'done' for labeling purposes.

        Returns:
            str: A formatted string of tasks, including numbering and priority levels.
        """

        if not tasks:
            return f"No {which_one} tasks."
        if self.priorities_type == int:
            sorted_tasks = sorted(tasks.items(), key=lambda x: self.priority_levels.index(x[1]))
        elif self.priorities_type == str:
            sorted_tasks = sorted(tasks.items(), key=lambda x: self.priority_levels.index(x[1].lower()))
        max_task_length = max(len(task) for task in tasks.keys()) + 2
        header = f"{'ID':<4} {'Task':<{max_task_length}} Priority\n{'-'*4} {'-'*max_task_length} {'-'*8}\n"
        formatted_list = f"{which_one.capitalize()} Tasks:\n"
        formatted_list += header

        if self.priorities_type == str:
            for idx, (task,priority) in enumerate(sorted_tasks, 1):
                formatted_list += f"{idx:<5}{task:<{max_task_length+1}}{priority.capitalize()}\n"
            return formatted_list
        elif self.priorities_type == int:
            for idx, (task,priority) in enumerate(sorted_tasks, 1):
                formatted_list += f"{idx:<5}{task:<{max_task_length+1}}{priority}\n"
            return formatted_list  

    def report(self, file_path: str = './', report_name: str = f"{date.today()}_tasks.txt",report_content: Literal['all', 'todo', 'done'] = 'all') :
        """
        Generates and saves a report of the day's to-do and completed tasks to a text file.

        The report can include either to-do tasks, done tasks, or both. It is saved to the specified file path.

        Args:
            file_path (str, optional): The directory where the report will be saved. Defaults to './' (The cwd).
            report_name (str, optional): The name of the file where the report will be saved. Defaults to a file named with the current date.
            report_content (str, optional): Specifies which tasks to include in the report ('todo', 'done', or 'all'). Defaults to 'all'.

        Returns:
            str: A message confirming the report was saved, or an error message if no tasks were found.
        """

        if not self.daily_added_tasks and not self.daily_completed_tasks:
            return "Both lists are empty, are you willing to save nothing? Do somrthing, you Panda."
        else:
            todo_final = self._format_task_list(self.daily_added_tasks, 'To-Do')
            done_final = self._format_task_list(self.daily_completed_tasks, 'Done')
            if report_content.lower() == 'todo': 
                report = f'''{date.today()} Tasks were:

{todo_final}        
            '''
                file_name = os.path.join(file_path, report_name)
                with open(file_name, 'w') as report_file:
                    report_file.write(report)
                return f"Report wrote succesfuly. And saved at the current directory with the following name:\n\"{file_name}\""
            elif report_content == 'done':
                report = f'''{date.today()} Tasks were:

{done_final}        
            '''
                file_name = os.path.join(file_path, report_name)
                with open(file_name, 'w') as report_file:
                    report_file.write(report)
                return f"Report wrote succesfuly. And saved at the current directory with the following name:\n\"{file_name}\""
            else:
                report = f'''{date.today()} Tasks were:

{todo_final}

{done_final}
            '''
                file_name = os.path.join(file_path, report_name)
                with open(file_name, 'w') as report_file:
                    report_file.write(report)
                return f"Report wrote succesfuly. And saved at the current directory with the following name:\n\"{file_name}\""
    def current_state(self, option: Literal['both', 'to-do', 'done'] = 'both') -> str:
        """ 
        Displays the current state of the task manager, showing either the to-do, done, or both lists.

        Args:
            option (str, optional): The task list(s) to display ('to-do', 'done', or 'both'). Defaults to 'both'.

        Returns:
            str: A formatted string representing the requested task list(s).
        """
        if option == 'both':
            return f"{self._format_task_list(self.to_do, 'to-do')}\n\n{self._format_task_list(self.done, 'done')}"
        elif option == 'to-do':
            return self._format_task_list(self.to_do, 'to-do')
        elif option == 'done':
            return self._format_task_list(self.done, 'done')
        else:
            return "Invalid option."

    def clear(self,which_one:  Literal['both','todo','done'] = 'both') -> str:
        """
        Resets todo list or done list or both lists.

        Returns:
            str: A message indicating whether specified list was cleared successfully.
        """
        if which_one.lower() == 'todo': 
            if self.to_do:
                self.to_do.clear()
                self.daily_added_tasks.clear()
                return " To-do list is cleared succesfully."
            else:
                return "To-do list is empty."
        elif which_one.lower() == 'done': 
            if self.done:
                self.done.clear()
                self.daily_completed_tasks.clear()
                return "Done list is cleared succesfully."
            else:
                return "Done list is empty."
        elif which_one.lower() == 'all': 
            if self.to_do:
                self.to_do.clear()
                self.daily_added_tasks.clear()
                self.done.clear()
                self.daily_completed_tasks.clear()
                return "Both lists are cleared succesfully."
            else:
                return "Both lists are empty."
        else:
            return "Invalid option."