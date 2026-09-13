# Academic-Helper-Task-List-Interface

A Tkinter-based task manager built as the task list and interface module of a larger team academic helper application. Tasks persist between sessions via JSON.

Features
Add, view, edit, complete, uncomplete, and delete tasks
Separate scrollable views for active and completed tasks
Each task tracks a message, creation date, deadline, and (once completed) a completion date
Guided single-field input flow for entering task messages and deadlines, with date-format validation
Automatic unique task ID generation
Saves to and loads from a JSON file automatically on close/open
Custom app icon and background image, custom font (Sniglet) loaded via tkextrafont
Requirements
Python 3
tkextrafont (pip install tkextrafont)
A taskclass.py module defining Task and Task_List (with create_task, remove_task, complete_task, uncomplete_task, save_to_json, load_from_json, and date_conversion)
Assets referenced by the script, placed relative to it:
assets/lockedin_mascot.png (window icon)
assets/g_task_list.png (background image)
fonts/sniglet.ttf (UI font)
task_saveddata.json — the data file Task_List.load_from_json() reads on startup and save_to_json() writes to on close. Include a starter version with empty lists so the app has something to load on first run:

json
  {
      "task_list": [],
      "completed_task_list": []
  }
  
Running it

bash
pip install tkextrafont
python task_interface.py

Make sure taskclass.py, the assets/ folder, and the fonts/ folder are in the same directory as the script before running.

Notes

This was my portion of a larger team project — I designed and built the task list and interface layer (screen state management, task rendering, and the add/edit/complete/delete flows). The underlying Task and Task_List data classes were part of the broader team codebase.
