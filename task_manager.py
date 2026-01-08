
from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Iterable

import tkinter as tk
from tkinter import ttk, messagebox





class TaskLevel(Enum):

    SIMPLE = ("Simple", 1, 10)
    NORMAL = ("Normal", 2, 25)
    HARD = ("Hard", 3, 50)
    EPIC = ("Epic", 4, 100)

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def order(self) -> int:
        return self.value[1]

    @property
    def reward(self) -> int:
        return self.value[2]


class TaskType(Enum):

    ONCE = "One-time"
    DAILY = "Daily"
    WEEKLY = "Weekly"


@dataclass
class Task:

    id: str
    name: str
    description: str = ""
    level: TaskLevel = TaskLevel.NORMAL
    task_type: TaskType = TaskType.ONCE
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed: bool = False
    completed_at: Optional[str] = None
    last_completed: Optional[str] = None



    @property
    def is_once(self) -> bool:
        return self.task_type == TaskType.ONCE

    @property
    def can_complete(self) -> bool:
        now = datetime.now()

        if self.task_type == TaskType.ONCE:
            return not self.completed

        if not self.last_completed:

            return True

        last_dt = datetime.fromisoformat(self.last_completed)
        if self.task_type == TaskType.DAILY:

            return now.date() > last_dt.date()

        if self.task_type == TaskType.WEEKLY:

            return now.date() >= (last_dt.date() + timedelta(days=7))

        return False

    @property
    def display_status(self) -> str:
        if self.is_once:
            return "Completed" if self.completed else "In Progress"

        if self.can_complete:
            return "Available"
        if self.last_completed:
            return "Cooldown"
        return "In Progress"



    def mark_completed(self) -> bool:
        if not self.can_complete:
            return False

        now_str = datetime.now().isoformat()

        if self.is_once:
            self.completed = True
            self.completed_at = now_str
        else:
            self.last_completed = now_str

        return True



    def to_dict(self) -> Dict:
        data = asdict(self)
        data["level"] = self.level.name
        data["task_type"] = self.task_type.name
        return data

    @classmethod
    def from_dict(cls, data: Dict) -> "Task":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            level=TaskLevel[data["level"]],
            task_type=TaskType[data["task_type"]],
            tags=data.get("tags", []),
            created_at=data.get("created_at", datetime.now().isoformat()),
            completed=data.get("completed", False),
            completed_at=data.get("completed_at"),
            last_completed=data.get("last_completed"),
        )


class DataManager:

    def __init__(self, data_file: str = "task_data.json") -> None:
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.total_coins: int = 0
        self.coin_history: List[Dict] = []
        self.load()



    def load(self) -> None:
        if not os.path.exists(self.data_file):
            self.tasks = []
            self.total_coins = 0
            self.coin_history = []
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as exc:  # noqa: BLE001
            print(f"[DataManager] Failed to load data: {exc}")
            self.tasks = []
            self.total_coins = 0
            self.coin_history = []
            return

        self.tasks = [Task.from_dict(t) for t in raw.get("tasks", [])]
        self.total_coins = raw.get("total_coins", 0)
        self.coin_history = raw.get("coin_history", [])

    def save(self) -> None:
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "total_coins": self.total_coins,
            "coin_history": self.coin_history,
        }
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as exc:  # noqa: BLE001
            print(f"[DataManager] Failed to save data: {exc}")



    def _new_id(self) -> str:
        return f"task_{datetime.now().timestamp()}"

    def create_task(
        self,
        name: str,
        description: str,
        level: TaskLevel,
        task_type: TaskType,
        tags: Optional[Iterable[str]] = None,
    ) -> Task:
        task = Task(
            id=self._new_id(),
            name=name,
            description=description,
            level=level,
            task_type=task_type,
            tags=list(tags or []),
        )
        self.tasks.append(task)
        self.save()
        return task

    def update_task(self, task: Task) -> None:
        for idx, t in enumerate(self.tasks):
            if t.id == task.id:
                self.tasks[idx] = task
                self.save()
                return

    def delete_task(self, task_id: str) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save()



    def complete_task(self, task_id: str) -> int:
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            return 0

        if not task.mark_completed():
            return 0

        coins = task.level.reward
        self.total_coins += coins
        self.coin_history.append(
            {
                "task_id": task.id,
                "task_name": task.name,
                "coins": coins,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.save()
        return coins



    def iter_tasks(self) -> Iterable[Task]:
        return list(self.tasks)

    def count_all(self) -> int:
        return len(self.tasks)

    def count_completed_for_progress(self) -> int:
        count = 0
        for t in self.tasks:
            if t.is_once and t.completed:
                count += 1
            elif not t.is_once and t.last_completed:
                count += 1
        return count





class TaskManagerApp:

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.data = DataManager()


        self.search_var = tk.StringVar()
        self.filter_level_var = tk.StringVar(value="All")
        self.filter_type_var = tk.StringVar(value="All")
        self.filter_tag_var = tk.StringVar()
        self.sort_field_var = tk.StringVar(value="Default")
        self.sort_order_var = tk.StringVar(value="Desc")

        self.current_page = 1
        self.page_size = 6
        self.filtered_tasks: List[Task] = []


        self.task_list_frame: tk.Frame
        self.task_list_canvas: tk.Canvas
        self.task_list_canvas_window: int
        self.detail_text: tk.Text
        self.coin_label: tk.Label
        self.total_task_label: tk.Label
        self.completed_label: tk.Label
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_label: tk.Label
        self.complete_btn: tk.Button
        self.page_info_label: tk.Label
        self.prev_btn: tk.Button
        self.next_btn: tk.Button

        self.selected_task_id: Optional[str] = None

        self._build_ui()
        self.refresh_task_list()
        self.update_stats()



    def _build_ui(self) -> None:
        self.root.title("🌿 Task Adventure")
        self.root.geometry("1200x780")
        self.root.configure(bg="#f5e6d3")


        self.root.bind("<Control-n>", lambda _e: self.show_task_editor())
        self.root.bind("<Control-f>", lambda _e: self.focus_search())
        self.root.bind("<F5>", lambda _e: self.refresh_task_list())
        self.root.bind("<Escape>", lambda _e: self.clear_selection())

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Adventure.Horizontal.TProgressbar",
            troughcolor="#e8d5b7",
            background="#6b8e23",
            bordercolor="#e8d5b7",
            lightcolor="#7aa93a",
            darkcolor="#5b7a1b",
            thickness=18,
        )

        colors = self._colors


        main = tk.Frame(self.root, bg=colors["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)


        title_frame = tk.Frame(main, bg=colors["bg"])
        title_frame.pack(fill=tk.X, pady=(0, 15))


        title_row = tk.Frame(title_frame, bg=colors["bg"])
        title_row.pack()


        tk.Label(
            title_row,
            text="🐕",
            font=("Microsoft YaHei", 20),
            bg=colors["bg"],
            fg=colors["fg"],
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(
            title_row,
            text="Task Adventure",
            font=("Microsoft YaHei", 24, "bold"),
            bg=colors["bg"],
            fg=colors["fg"],
        ).pack(side=tk.LEFT)


        tk.Label(
            title_row,
            text="🐕",
            font=("Microsoft YaHei", 20),
            bg=colors["bg"],
            fg=colors["fg"],
        ).pack(side=tk.LEFT, padx=(8, 0))


        subtitle_frame = tk.Frame(title_frame, bg=colors["bg"])
        subtitle_frame.pack(pady=(6, 0))
        tk.Label(
            subtitle_frame,
            text="🐶 ",
            font=("Microsoft YaHei", 12),
            bg=colors["bg"],
            fg=colors["fg_light"],
        ).pack(side=tk.LEFT)
        tk.Label(
            subtitle_frame,
            text="Complete tasks, collect coins, start your adventure!",
            font=("Microsoft YaHei", 12, "bold"),
            bg=colors["bg"],
            fg=colors["fg_light"],
        ).pack(side=tk.LEFT)


        self._build_stats_bar(main)


        middle = tk.Frame(main, bg=colors["bg"])
        middle.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self._build_task_list_panel(middle)
        self._build_detail_panel(middle)

    @property
    def _colors(self) -> Dict[str, str]:
        return {
            "bg": "#f5e6d3",
            "bg_light": "#faf5ed",
            "bg_panel": "#e8d5b7",
            "panel": "#c4d5a0",
            "panel_dark": "#a8c97f",
            "card": "#d4e4b5",
            "fg": "#3d2817",
            "fg_light": "#5a3d2e",
            "fg_white": "#ffffff",
            "button": "#8fb573",
            "button_hover": "#7aa35f",
            "button_secondary": "#d4a574",
            "button_secondary_hover": "#c9a961",
            "accent": "#d4a574",
            "accent_dark": "#b8935a",
            "success": "#6b8e23",
            "danger": "#cd5c5c",
            "shadow": "#d4c4b0",
        }

    def _build_stats_bar(self, parent: tk.Frame) -> None:
        c = self._colors

        outer = tk.Frame(parent, bg=c["bg_panel"], bd=0, relief=tk.FLAT)
        outer.pack(fill=tk.X, pady=(0, 10))
        bar = tk.Frame(outer, bg=c["panel"], bd=0, relief=tk.FLAT)
        bar.pack(fill=tk.X, padx=3, pady=3)


        coin_box = tk.Frame(bar, bg=c["panel"], bd=0)
        coin_box.pack(side=tk.LEFT, padx=20, pady=10)
        coin_inner = tk.Frame(coin_box, bg=c["accent"], bd=2, relief=tk.RIDGE)
        coin_inner.pack(padx=2, pady=2, fill=tk.BOTH)
        tk.Label(
            coin_inner,
            text="Total Coins",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["accent"],
            fg=c["fg_white"],
        ).pack(padx=20, pady=(10, 0))
        self.coin_label = tk.Label(
            coin_inner,
            text="0",
            font=("Consolas", 18, "bold"),
            bg=c["accent"],
            fg="#ffd700",
        )
        self.coin_label.pack(padx=20, pady=(5, 12))


        total_box = tk.Frame(bar, bg=c["panel"], bd=0)
        total_box.pack(side=tk.LEFT, padx=20, pady=10)
        total_inner = tk.Frame(total_box, bg=c["panel_dark"], bd=2, relief=tk.RIDGE)
        total_inner.pack(padx=2, pady=2)
        tk.Label(
            total_inner,
            text="Total Tasks",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        ).pack(padx=20, pady=(10, 0))
        self.total_task_label = tk.Label(
            total_inner,
            text="0",
            font=("Consolas", 18, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        )
        self.total_task_label.pack(padx=20, pady=(5, 12))


        done_box = tk.Frame(bar, bg=c["panel"], bd=0)
        done_box.pack(side=tk.LEFT, padx=20, pady=10)
        done_inner = tk.Frame(done_box, bg=c["success"], bd=2, relief=tk.RIDGE)
        done_inner.pack(padx=2, pady=2)
        tk.Label(
            done_inner,
            text="Completed",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["success"],
            fg=c["fg_white"],
        ).pack(padx=20, pady=(10, 0))
        self.completed_label = tk.Label(
            done_inner,
            text="0",
            font=("Consolas", 18, "bold"),
            bg=c["success"],
            fg=c["fg_white"],
        )
        self.completed_label.pack(padx=20, pady=(5, 12))


        prog_box = tk.Frame(bar, bg=c["panel"], bd=0)
        prog_box.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.X, expand=True)
        tk.Label(
            prog_box,
            text="Progress",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(anchor="w")

        pb = ttk.Progressbar(
            prog_box,
            style="Adventure.Horizontal.TProgressbar",
            variable=self.progress_var,
            maximum=100,
        )
        pb.pack(fill=tk.X, pady=(4, 2))
        self.progress_label = tk.Label(
            prog_box,
            text="0.0%",
            font=("Consolas", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        )
        self.progress_label.pack(anchor="e")


        btn_box = tk.Frame(bar, bg=c["panel"], bd=0)
        btn_box.pack(side=tk.RIGHT, padx=20, pady=10)

        add_btn = tk.Button(
            btn_box,
            text="＋ Add Task",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["button"],
            fg=c["fg_white"],
            activebackground=c["button_hover"],
            activeforeground=c["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.show_task_editor,
        )
        add_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        refresh_btn = tk.Button(
            btn_box,
            text="🔄 Refresh",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.refresh_task_list,
        )
        refresh_btn.pack(side=tk.TOP, fill=tk.X)

    def _build_task_list_panel(self, parent: tk.Frame) -> None:
        c = self._colors

        outer = tk.Frame(parent, bg=c["bg_panel"], bd=0, relief=tk.FLAT)
        outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        panel = tk.Frame(outer, bg=c["panel"], bd=0, relief=tk.FLAT)
        panel.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)


        title_bar = tk.Frame(panel, bg=c["panel_dark"], bd=0, relief=tk.FLAT)
        title_bar.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(
            title_bar,
            text="🐕 📝 Task List",
            font=("Microsoft YaHei", 16, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        ).pack(side=tk.LEFT, padx=10, pady=8)


        search_bar = tk.Frame(title_bar, bg=c["panel_dark"])
        search_bar.pack(side=tk.RIGHT, padx=10)
        tk.Label(
            search_bar,
            text="🔍",
            font=("Microsoft YaHei", 11),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        ).pack(side=tk.LEFT, padx=(0, 4))
        entry = tk.Entry(
            search_bar,
            textvariable=self.search_var,
            font=("Microsoft YaHei", 11),
            width=20,
            bg=c["bg_light"],
            fg=c["fg"],
            relief=tk.RAISED,
            bd=2,
        )
        entry.pack(side=tk.LEFT)
        entry.bind("<KeyRelease>", lambda _e: self.filter_tasks())


        filter_row = tk.Frame(panel, bg=c["panel"])
        filter_row.pack(fill=tk.X, padx=8, pady=(0, 6))

        tk.Label(
            filter_row,
            text="Filter:",
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(side=tk.LEFT, padx=(0, 4))

        level_menu = ttk.Combobox(
            filter_row,
            textvariable=self.filter_level_var,
            values=["All", "Simple", "Normal", "Hard", "Epic"],
            width=6,
            state="readonly",
        )
        level_menu.pack(side=tk.LEFT, padx=4)
        level_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())

        type_menu = ttk.Combobox(
            filter_row,
            textvariable=self.filter_type_var,
            values=["All", "One-time", "Daily", "Weekly"],
            width=10,
            state="readonly",
        )
        type_menu.pack(side=tk.LEFT, padx=4)
        type_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())

        tk.Label(
            filter_row,
            text="Tags:",
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(side=tk.LEFT, padx=(10, 4))

        tag_entry = tk.Entry(
            filter_row,
            textvariable=self.filter_tag_var,
            font=("Microsoft YaHei", 10),
            width=12,
            bg=c["bg_light"],
            fg=c["fg"],
            relief=tk.RAISED,
            bd=2,
        )
        tag_entry.pack(side=tk.LEFT, padx=4)
        tag_entry.bind("<KeyRelease>", lambda _e: self.filter_tasks())

        tk.Label(
            filter_row,
            text="Sort:",
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(side=tk.LEFT, padx=(12, 4))

        sort_menu = ttk.Combobox(
            filter_row,
            textvariable=self.sort_field_var,
            values=["Default", "Level", "Name", "Created"],
            width=8,
            state="readonly",
        )
        sort_menu.pack(side=tk.LEFT, padx=4)
        sort_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())

        order_menu = ttk.Combobox(
            filter_row,
            textvariable=self.sort_order_var,
            values=["Asc", "Desc"],
            width=6,
            state="readonly",
        )
        order_menu.pack(side=tk.LEFT, padx=4)
        order_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())


        list_container = tk.Frame(panel, bg=c["panel"])
        list_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        canvas = tk.Canvas(
            list_container,
            bg=c["card"],
            highlightthickness=0,
            bd=0,
            relief=tk.FLAT,
        )
        scrollbar = ttk.Scrollbar(
            list_container,
            orient="vertical",
            command=canvas.yview,
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        inner = tk.Frame(canvas, bg=c["card"])
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")

        def update_canvas_scrollregion() -> None:
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:
                canvas.itemconfig(canvas_window, width=canvas_width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_inner_configure(_e: tk.Event) -> None:  # type: ignore[override]
            update_canvas_scrollregion()

        def _on_canvas_configure(_e: tk.Event) -> None:  # type: ignore[override]
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:
                canvas.itemconfig(canvas_window, width=canvas_width)
            update_canvas_scrollregion()

        inner.bind("<Configure>", _on_inner_configure)
        canvas.bind("<Configure>", _on_canvas_configure)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_list_canvas = canvas
        self.task_list_canvas_window = canvas_window
        self.task_list_frame = inner


        pager = tk.Frame(panel, bg=c["panel"])
        pager.pack(fill=tk.X, padx=10, pady=(2, 6))
        self.page_info_label = tk.Label(
            pager,
            text="Page 1/1",
            font=("Microsoft YaHei", 9),
            bg=c["panel"],
            fg=c["fg"],
        )
        self.page_info_label.pack(side=tk.LEFT)

        nav = tk.Frame(pager, bg=c["panel"])
        nav.pack(side=tk.RIGHT)

        self.prev_btn = tk.Button(
            nav,
            text="⬅ Prev",
            font=("Microsoft YaHei", 9),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=lambda: self.change_page(-1),
        )
        self.prev_btn.pack(side=tk.LEFT, padx=4)

        self.next_btn = tk.Button(
            nav,
            text="Next ➡",
            font=("Microsoft YaHei", 9),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=lambda: self.change_page(1),
        )
        self.next_btn.pack(side=tk.LEFT, padx=4)

    def _build_detail_panel(self, parent: tk.Frame) -> None:
        c = self._colors

        outer = tk.Frame(parent, bg=c["bg_panel"], bd=0, relief=tk.FLAT, width=320)
        outer.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(8, 0))
        outer.pack_propagate(False)

        panel = tk.Frame(outer, bg=c["panel"], bd=0, relief=tk.FLAT)
        panel.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        title = tk.Frame(panel, bg=c["panel_dark"], bd=0, relief=tk.FLAT)
        title.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(
            title,
            text="🐶 📄 Task Details",
            font=("Microsoft YaHei", 16, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        ).pack(pady=8)

        text_wrap = tk.Frame(panel, bg=c["card"], bd=0, relief=tk.FLAT)
        text_wrap.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self.detail_text = tk.Text(
            text_wrap,
            bg=c["bg_light"],
            fg=c["fg"],
            font=("Microsoft YaHei", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED,
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        self._set_detail_text("Please select a task to view details...")


        btns = tk.Frame(panel, bg=c["panel"])
        btns.pack(fill=tk.X, padx=8, pady=(0, 8))

        self.complete_btn = tk.Button(
            btns,
            text="✅ Complete",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["success"],
            fg=c["fg_white"],
            activebackground="#5a7a1a",
            activeforeground=c["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.complete_selected_task,
        )
        self.complete_btn.pack(fill=tk.X, pady=3)

        edit_btn = tk.Button(
            btns,
            text="✏ Edit",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["button"],
            fg=c["fg_white"],
            activebackground=c["button_hover"],
            activeforeground=c["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=lambda: self.show_task_editor(edit=True),
        )
        edit_btn.pack(fill=tk.X, pady=3)

        delete_btn = tk.Button(
            btns,
            text="🗑 Delete",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["danger"],
            fg=c["fg_white"],
            activebackground="#b84a4a",
            activeforeground=c["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.delete_selected_task,
        )
        delete_btn.pack(fill=tk.X, pady=3)



    def focus_search(self) -> None:
        self.search_var.set("")

        self.refresh_task_list()

    def clear_selection(self) -> None:
        self.selected_task_id = None
        self._set_detail_text("Please select a task to view details...")
        self.complete_btn.config(state=tk.DISABLED, text="✅ Complete")

    def change_page(self, delta: int) -> None:
        self.current_page = max(1, self.current_page + delta)
        self.refresh_task_list()

    def filter_tasks(self) -> None:
        self.current_page = 1
        self.refresh_task_list()

    def refresh_task_list(self) -> None:

        for w in self.task_list_frame.winfo_children():
            w.destroy()

        tasks = list(self.data.iter_tasks())


        keyword = self.search_var.get().strip().lower()
        if keyword:
            tasks = [
                t
                for t in tasks
                if keyword in t.name.lower()
                or keyword in t.description.lower()
            ]


        lv = self.filter_level_var.get()
        level_map = {
            "Simple": TaskLevel.SIMPLE,
            "Normal": TaskLevel.NORMAL,
            "Hard": TaskLevel.HARD,
            "Epic": TaskLevel.EPIC,
        }
        if lv in level_map:
            tasks = [t for t in tasks if t.level == level_map[lv]]


        tp = self.filter_type_var.get()
        type_map = {
            "One-time": TaskType.ONCE,
            "Daily": TaskType.DAILY,
            "Weekly": TaskType.WEEKLY,
        }
        if tp in type_map:
            tasks = [t for t in tasks if t.task_type == type_map[tp]]


        tag_text = self.filter_tag_var.get().strip().lower()
        if tag_text:
            wanted = [s.strip() for s in tag_text.split(",") if s.strip()]
            if wanted:
                tasks = [
                    t
                    for t in tasks
                    if all(
                        any(tag.lower() == w for tag in t.tags)
                        for w in wanted
                    )
                ]


        reverse = self.sort_order_var.get() == "Desc"
        field = self.sort_field_var.get()
        if field == "Level":
            tasks.sort(key=lambda t: t.level.order, reverse=reverse)
        elif field == "Name":
            tasks.sort(key=lambda t: t.name, reverse=reverse)
        elif field == "Created":
            tasks.sort(key=lambda t: t.created_at, reverse=reverse)

        self.filtered_tasks = tasks

        total = len(tasks)
        total_pages = max(1, (total + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))

        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_tasks = tasks[start:end]

        if not page_tasks:
            tk.Label(
                self.task_list_frame,
                text="No tasks\nClick 'Add Task' to start! ✨",
                font=("Microsoft YaHei", 12),
                bg=self._colors["card"],
                fg=self._colors["fg_light"],
                justify=tk.CENTER,
            ).pack(pady=40)
        else:
            for t in page_tasks:
                self._render_task_card(t)


        self.page_info_label.config(
            text=f"Page {self.current_page}/{total_pages} (Total {total} items)"
        )
        self.prev_btn.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_btn.config(
            state=tk.NORMAL if self.current_page < total_pages else tk.DISABLED
        )


        self.task_list_canvas.update_idletasks()
        canvas_width = self.task_list_canvas.winfo_width()
        if canvas_width > 1:
            self.task_list_canvas.itemconfig(self.task_list_canvas_window, width=canvas_width)
        self.task_list_canvas.configure(scrollregion=self.task_list_canvas.bbox("all"))

        self.update_stats()

    def _render_task_card(self, task: Task) -> None:
        c = self._colors


        shadow = tk.Frame(self.task_list_frame, bg=c["shadow"], bd=0, relief=tk.FLAT)
        shadow.pack(fill=tk.X, padx=8, pady=5)


        level_colors = {
            TaskLevel.SIMPLE: ("#a8d5a0", "#8fb573"),
            TaskLevel.NORMAL: ("#8fb573", "#7aa35f"),
            TaskLevel.HARD: ("#d4a574", "#c9a961"),
            TaskLevel.EPIC: ("#c9a961", "#b8935a"),
        }
        bg_color, border_color = level_colors.get(
            task.level, (c["card"], c["accent_dark"])
        )


        frame = tk.Frame(
            shadow,
            bg=bg_color,
            bd=2,
            relief=tk.RAISED,
            height=140,
        )
        frame.pack(fill=tk.X, padx=2, pady=2)
        frame.pack_propagate(False)


        inner = tk.Frame(frame, bg=bg_color)
        inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)


        top = tk.Frame(inner, bg=bg_color)
        top.pack(fill=tk.X)

        name_label = tk.Label(
            top,
            text=f"🐕 {task.name}",
            font=("Microsoft YaHei", 12, "bold"),
            bg=bg_color,
            fg="#2b1a10",
            anchor="w",
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)


        state_text = task.display_status
        state_bg = c["accent_dark"] if "Completed" in state_text else c["panel_dark"]
        state_badge = tk.Label(
            top,
            text=state_text,
            font=("Microsoft YaHei", 9, "bold"),
            bg=state_bg,
            fg=c["fg_white"],
            padx=6,
            pady=2,
        )
        state_badge.pack(side=tk.RIGHT, padx=(4, 0))


        level_badge = tk.Label(
            top,
            text=f"Lv.{task.level.order}",
            font=("Microsoft YaHei", 9, "bold"),
            bg=border_color,
            fg=c["fg_white"],
            padx=7,
            pady=2,
        )
        level_badge.pack(side=tk.RIGHT, padx=(6, 0))


        mid = tk.Frame(inner, bg=bg_color)
        mid.pack(fill=tk.X, pady=(5, 3))

        type_icon = (
            "🔄" if task.task_type == TaskType.DAILY else
            "📅" if task.task_type == TaskType.WEEKLY else
            "📌"
        )
        tk.Label(
            mid,
            text=f"{type_icon} {task.task_type.value}",
            font=("Microsoft YaHei", 10, "bold"),
            bg=bg_color,
            fg=c["fg"],
        ).pack(side=tk.LEFT)

        reward_label = tk.Label(
            mid,
            text=f"💰 +{task.level.reward}",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#ffd700",
            fg="#2b1a10",
            bd=1,
            relief=tk.RIDGE,
            padx=7,
            pady=2,
        )
        reward_label.pack(side=tk.RIGHT)


        if task.tags:
            tag_row = tk.Frame(inner, bg=bg_color)
            tag_row.pack(fill=tk.X, pady=(3, 0))
            for tag in task.tags[:3]:
                tk.Label(
                    tag_row,
                    text=f"🏷 {tag}",
                    font=("Microsoft YaHei", 9),
                    bg=c["bg_light"],
                    fg=c["fg"],
                    bd=1,
                    relief=tk.RIDGE,
                    padx=5,
                    pady=1,
                ).pack(side=tk.LEFT, padx=2, pady=1)


        tk.Label(
            inner,
            text=f"Created: {datetime.fromisoformat(task.created_at).strftime('%m-%d %H:%M')}",
            font=("Microsoft YaHei", 8),
            bg=bg_color,
            fg=c["fg"],
            anchor="w",
        ).pack(fill=tk.X, pady=(3, 0))


        def on_click(_e: tk.Event) -> None:  # type: ignore[override]
            self.select_task(task.id)

        def on_enter(_e: tk.Event) -> None:  # type: ignore[override]
            frame.config(relief=tk.SUNKEN)

        def on_leave(_e: tk.Event) -> None:  # type: ignore[override]
            frame.config(relief=tk.RAISED)

        for w in (frame, inner, top, mid):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)



    def _set_detail_text(self, text: str) -> None:
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert("1.0", text)
        self.detail_text.config(state=tk.DISABLED)

    def select_task(self, task_id: str) -> None:
        self.selected_task_id = task_id
        task = next((t for t in self.data.iter_tasks() if t.id == task_id), None)
        if not task:
            return

        tags = ", ".join(task.tags) if task.tags else "None"

        info = [
            f"📝 Task Name:{task.name}",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "📄 Description:",
            task.description or "(No description)",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            f"⭐ Level:{task.level.label} (Lv.{task.level.order})",
            f"🔄 Type:{task.task_type.value}",
            f"🏷 Tags: {tags}",
            f"💰 Reward: {task.level.reward} coins",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            f"📅 Created:{datetime.fromisoformat(task.created_at).strftime('%Y-%m-%d %H:%M')}",
        ]

        if task.last_completed:
            info.append(
                f"✅ Last Completed:{datetime.fromisoformat(task.last_completed).strftime('%Y-%m-%d %H:%M')}"
            )
        if task.completed_at:
            info.append(
                f"✅ Completed:{datetime.fromisoformat(task.completed_at).strftime('%Y-%m-%d %H:%M')}"
            )

        info.append("")
        info.append(f"{'✅' if task.can_complete else '⏳'} Status:{task.display_status}")

        self._set_detail_text("\n".join(info))


        if task.can_complete:
            self.complete_btn.config(state=tk.NORMAL, text="✅ Complete")
        else:
            self.complete_btn.config(state=tk.DISABLED, text="⏳ Not Available")



    def show_task_editor(self, edit: bool = False) -> None:
        is_edit = edit
        current: Optional[Task] = None
        if is_edit:
            if not self.selected_task_id:
                messagebox.showwarning("Notice", "Please select a task to edit first.")
                return
            current = next(
                (t for t in self.data.iter_tasks() if t.id == self.selected_task_id),
                None,
            )
            if not current:
                messagebox.showwarning("Notice", "Task not found.")
                return

        win = tk.Toplevel(self.root)
        win.title("Edit" if is_edit else "Add Task")
        win.geometry("560x520")
        win.transient(self.root)
        win.grab_set()

        c = self._colors

        outer = tk.Frame(win, bg=c["bg_panel"])
        outer.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        panel = tk.Frame(outer, bg=c["panel"], bd=3, relief=tk.RIDGE)
        panel.pack(fill=tk.BOTH, expand=True)


        title = tk.Frame(panel, bg=c["panel_dark"])
        title.pack(fill=tk.X, padx=4, pady=4)
        tk.Label(
            title,
            text="✏ Edit" if is_edit else "✨ Create New Task",
            font=("Microsoft YaHei", 14, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        ).pack(pady=6)

        body = tk.Frame(panel, bg=c["panel"])
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)


        tk.Label(
            body,
            text="📝 Task Name:",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(anchor="w")
        name_var = tk.StringVar(value=current.name if current else "")
        name_entry = tk.Entry(
            body,
            textvariable=name_var,
            font=("Microsoft YaHei", 11),
            bg=c["bg_light"],
            fg=c["fg"],
            bd=2,
            relief=tk.RAISED,
        )
        name_entry.pack(fill=tk.X, pady=(2, 8))


        tk.Label(
            body,
            text="📄 Description:",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(anchor="w", pady=(4, 0))
        desc_text = tk.Text(
            body,
            font=("Microsoft YaHei", 10),
            bg=c["bg_light"],
            fg=c["fg"],
            height=5,
            wrap=tk.WORD,
            bd=2,
            relief=tk.RAISED,
        )
        if current and current.description:
            desc_text.insert("1.0", current.description)
        desc_text.pack(fill=tk.BOTH, pady=(2, 8))


        tk.Label(
            body,
            text="🏷 Tags (comma-separated):",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(anchor="w", pady=(4, 0))
        tags_var = tk.StringVar(
            value=", ".join(current.tags) if current and current.tags else ""
        )
        tags_entry = tk.Entry(
            body,
            textvariable=tags_var,
            font=("Microsoft YaHei", 10),
            bg=c["bg_light"],
            fg=c["fg"],
            bd=2,
            relief=tk.RAISED,
        )
        tags_entry.pack(fill=tk.X, pady=(2, 8))


        tk.Label(
            body,
            text="⭐ Level:",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(anchor="w", pady=(4, 0))
        level_var = tk.StringVar(
            value=(current.level.name if current else TaskLevel.NORMAL.name)
        )
        level_row = tk.Frame(body, bg=c["panel"])
        level_row.pack(fill=tk.X, pady=(2, 4))
        for lv in TaskLevel:
            ttk.Radiobutton(
                level_row,
                text=f"{lv.label} (+{lv.reward}💰)",
                value=lv.name,
                variable=level_var,
            ).pack(side=tk.LEFT, padx=4)


        tk.Label(
            body,
            text="🔄 Type:",
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        ).pack(anchor="w", pady=(4, 0))
        type_var = tk.StringVar(
            value=(current.task_type.name if current else TaskType.ONCE.name)
        )
        type_row = tk.Frame(body, bg=c["panel"])
        type_row.pack(fill=tk.X, pady=(2, 4))
        for tp in TaskType:
            ttk.Radiobutton(
                type_row,
                text=tp.value,
                value=tp.name,
                variable=type_var,
            ).pack(side=tk.LEFT, padx=4)


        foot = tk.Frame(panel, bg=c["panel"])
        foot.pack(pady=12)

        def on_save() -> None:
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Notice", "Task name cannot be empty.")
                return

            description = desc_text.get("1.0", tk.END).strip()
            level = TaskLevel[level_var.get()]
            ttype = TaskType[type_var.get()]
            tags = [s.strip() for s in tags_var.get().split(",") if s.strip()]

            if is_edit and current:
                current.name = name
                current.description = description
                current.level = level
                current.task_type = ttype
                current.tags = tags
                self.data.update_task(current)
                self.select_task(current.id)
            else:
                task = self.data.create_task(name, description, level, ttype, tags)
                self.selected_task_id = task.id

            self.refresh_task_list()
            win.destroy()

        tk.Button(
            foot,
            text="💾 Save",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self._colors["success"],
            fg=self._colors["fg_white"],
            activebackground="#5a7a1a",
            activeforeground=self._colors["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=on_save,
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            foot,
            text="Cancel",
            font=("Microsoft YaHei", 11, "bold"),
            bg=self._colors["button_secondary"],
            fg=self._colors["fg_white"],
            activebackground=self._colors["button_secondary_hover"],
            activeforeground=self._colors["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=win.destroy,
        ).pack(side=tk.LEFT, padx=10)

        name_entry.focus_set()
        win.bind("<Return>", lambda _e: on_save())

    def delete_selected_task(self) -> None:
        if not self.selected_task_id:
            messagebox.showwarning("Notice", "Please select a task first.")
            return
        task = next(
            (t for t in self.data.iter_tasks() if t.id == self.selected_task_id), None
        )
        if not task:
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task \"{task.name}\"?"):
            return
        self.data.delete_task(task.id)
        self.selected_task_id = None
        self.refresh_task_list()
        self._set_detail_text("Task deleted.")

    def complete_selected_task(self) -> None:
        if not self.selected_task_id:
            messagebox.showwarning("Notice", "Please select a task first.")
            return
        coins = self.data.complete_task(self.selected_task_id)
        if coins <= 0:
            messagebox.showinfo("Notice", "Task cannot be completed (may be completed or on cooldown).")
            self.refresh_task_list()
            return
        messagebox.showinfo("Success", f"Task completed! Earned {coins}  coins.")
        self.refresh_task_list()
        self.select_task(self.selected_task_id)



    def update_stats(self) -> None:
        total = self.data.count_all()
        completed_for_progress = self.data.count_completed_for_progress()

        self.coin_label.config(text=str(self.data.total_coins))
        self.total_task_label.config(text=str(total))
        self.completed_label.config(text=str(completed_for_progress))

        if total:
            pct = completed_for_progress * 100.0 / total
        else:
            pct = 0.0
        self.progress_var.set(pct)
        self.progress_label.config(text=f"{pct:.1f}%")





def main() -> None:
    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()



