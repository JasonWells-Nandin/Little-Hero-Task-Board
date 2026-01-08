# Little Hero Task Board（Task Adventure Manager）

This is a desktop task management application built with Python and Tkinter, designed for personal daily task management (to-do list), incorporating gamification elements. It helps you track tasks, earn coins, and improve productivity.
The result is shown below:

![image-20260108155621037](C:\Users\signal\AppData\Roaming\Typora\typora-user-images\image-20260108155621037.png)

## Features

- **Task Management:** Create, edit, delete, and complete tasks
- **Gamification:** Earn coins based on task difficulty levels
- **Task Levels:** Easy, Normal, Hard, Epic (different coin rewards)
- **Task Types:** One-time, daily, and weekly recurring tasks
- **Filtering and Sorting:** Filter by level, type, and tags, and sort by various criteria
- **Statistics Dashboard:** View total coins, number of tasks, and completion progress
- **Data Persistence:** All data is automatically saved to a JSON file

## Installation

### Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python task_manager.py
```

### Building an Executable

To build a standalone executable:

```bash
# Option 1: Using the batch file (recommended)
build.bat

# Option 2: Running the Python script directly
python build_exe.py
```

The executable will be generated in the `dist` directory. ## Task System

### Task Levels

- **Easy** (Lv.1): Reward 10 gold coins
- **Normal** (Lv.2): Reward 25 gold coins
- **Hard** (Lv.3): Reward 50 gold coins
- **Epic** (Lv.4): Reward 100 gold coins

### Task Types

- **One-time Task:** Removed after completion
- **Daily Task:** Can be completed once per day
- **Weekly Task:** Can be completed once per week

## Keyboard Shortcuts

- `Ctrl+N`: Create a new task
- `Ctrl+F`: Focus the search box
- `F5`: Refresh the task list
- `Esc`: Clear selection

## Project Structure

```
├── task_manager.py      # Main application
├── requirements.txt     # Python dependencies
├── build_exe.py        # Executable build script
├── build.bat           # Windows batch build script
└── dist/               # Build output (automatically generated)
```

## License

Free for personal use and can be freely modified; commercial use is prohibited.