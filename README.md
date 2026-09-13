# Academic Helper — Task List & Interface

A Tkinter-based task manager built as the task list and interface module of a larger team academic helper application. Tasks persist between sessions via JSON.

## Files in this repo

| File | What it does |
|---|---|
| `task_interface.py` | Main entry point. Builds the Tkinter UI, manages screen state, and wires up all the buttons/menus. Run this file. |
| `taskclass.py` | Defines the `Task` and `Task_List` classes — task data, validation (10-digit unique IDs, MM/DD/YYYY date checks), and the JSON save/load logic. |
| `task_saveddata.json` | The data file tasks are saved to and loaded from. Starts empty (`{"task_list": [], "completed_task_list": []}`); the app overwrites it as you use it. |
| `assets/lockedin_mascot.png` | Window icon. |
| `assets/g_task_list.png` | Background image for the main window. |
| `fonts/sniglet.ttf` | Custom UI font (Sniglet), loaded via `tkextrafont`. |

All of these need to be in the repo, in the same relative layout, for the app to run — `task_interface.py` alone won't work.

## Features

- Add, view, edit, complete, uncomplete, and delete tasks
- Separate scrollable views for active and completed tasks
- Each task tracks a message, creation date, deadline, and (once completed) a completion date
- Guided single-field input flow for entering task messages and deadlines, with date-format validation
- Automatic unique 10-digit task ID generation, checked for collisions against existing tasks
- Saves to and loads from `task_saveddata.json` automatically on close/open
- Custom app icon, background image, and font

## Requirements

- Python 3
- `tkextrafont` (`pip install tkextrafont`)

## Running it

```bash
pip install tkextrafont
python task_interface.py
```

Make sure `taskclass.py`, `task_saveddata.json`, the `assets/` folder, and the `fonts/` folder are all in the same directory as `task_interface.py` before running.

## Notes

This was my portion of a larger team project — I designed and built both the task list/interface layer (`task_interface.py`: screen state management, task rendering, and the add/edit/complete/delete flows) and the underlying task data model (`taskclass.py`: the `Task` and `Task_List` classes, validation, and JSON persistence).
