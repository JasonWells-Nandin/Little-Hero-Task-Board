
from __future__ import annotations

import json
import os
import threading
import urllib.request
import urllib.parse
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta, date
from enum import Enum
from typing import List, Dict, Optional, Iterable
from calendar import monthcalendar, month_name

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog




class I18n:
    _translations = {
        "zh": {
            "app_title": "🌿 任务冒险手册",
            "subtitle": "完成任务，收集金币，开启你的冒险之旅！",
            "total_coins": "总金币",
            "total_tasks": "总任务数",
            "completed": "已完成",
            "progress": "完成进度",
            "add_task": "＋ 添加任务",
            "refresh": "🔄 刷新",
            "task_list": "🐕 📝 任务列表",
            "search": "🔍",
            "filter": "筛选:",
            "all": "全部",
            "level": "级别",
            "name": "名称",
            "create_time": "创建时间",
            "default": "默认",
            "asc": "升序",
            "desc": "降序",
            "tag": "标签:",
            "sort": "排序:",
            "task_detail": "🐶 📄 任务详情",
            "select_task": "请选择一个任务查看详情……",
            "complete_task": "✅ 完成任务",
            "edit_task": "✏ 编辑任务",
            "delete_task": "🗑 删除任务",
            "page": "第 {}/{} 页",
            "prev": "⬅ 上一页",
            "next": "下一页 ➡",
            "weather": "🌤 天气",
            "calendar": "📅 日历",
            "task_view": "📝 任务视图",
            "calendar_view": "📅 日历视图",
            "language": "语言",
            "auto_refresh": "自动刷新",
            "manual_refresh": "手动刷新",
            "location": "地区",
            "select_location": "选择地区",
            "temperature": "温度",
            "humidity": "湿度",
            "wind": "风速",
            "condition": "天气",
            "loading": "加载中...",
            "error": "错误",
            "no_weather": "无法获取天气信息",
            "daily_task_reset": "日常任务已刷新",
            "confirm_delete": "确认删除",
            "delete_confirm_msg": "确定要删除任务「{}」吗？",
            "task_completed": "任务完成！获得 {} 金币。",
            "cannot_complete": "当前任务暂不可完成（可能已完成或冷却中）。",
            "select_task_first": "请先在左侧选择一个任务。",
            "task_deleted": "任务已删除。",
            "warning": "提示",
            "congratulations": "恭喜",
            "task_name_empty": "任务名称不能为空。",
            "task_not_found": "未找到要编辑的任务。",
            "select_task_to_edit": "请先在左侧选择一个任务再编辑。",
            "total_items": "共{}条",
            "task_name": "任务名称",
            "task_description": "任务描述",
            "level_label": "等级",
            "type_label": "类型",
            "tags_label": "标签",
            "reward_label": "奖励",
            "created_at_label": "创建时间",
            "last_completed_label": "最近完成",
            "current_status_label": "当前状态",
            "no_description": "（暂无描述）",
            "no_tags": "无",
            "coins_unit": "金币",
            "one_time_completed": "一次性完成时间",
            "simple": "简单",
            "normal": "普通",
            "hard": "困难",
            "epic": "史诗",
            "once": "一次性任务",
            "daily": "日常任务",
            "weekly": "每周任务",
            "in_progress": "进行中",
            "completed": "已完成",
            "available": "可完成",
            "cooldown": "冷却中",
            "year": "年",
            "january": "一月",
            "february": "二月",
            "march": "三月",
            "april": "四月",
            "may": "五月",
            "june": "六月",
            "july": "七月",
            "august": "八月",
            "september": "九月",
            "october": "十月",
            "november": "十一月",
            "december": "十二月",
            "monday": "周一",
            "tuesday": "周二",
            "wednesday": "周三",
            "thursday": "周四",
            "friday": "周五",
            "saturday": "周六",
            "sunday": "周日",
            "today": "今天",
        },
        "en": {
            "app_title": "🌿 Task Adventure",
            "subtitle": "Complete tasks, collect coins, start your adventure!",
            "total_coins": "Total Coins",
            "total_tasks": "Total Tasks",
            "completed": "Completed",
            "progress": "Progress",
            "add_task": "＋ Add Task",
            "refresh": "🔄 Refresh",
            "task_list": "🐕 📝 Task List",
            "search": "🔍",
            "filter": "Filter:",
            "all": "All",
            "level": "Level",
            "name": "Name",
            "create_time": "Create Time",
            "default": "Default",
            "asc": "Asc",
            "desc": "Desc",
            "tag": "Tag:",
            "sort": "Sort:",
            "task_detail": "🐶 📄 Task Detail",
            "select_task": "Please select a task to view details...",
            "complete_task": "✅ Complete Task",
            "edit_task": "✏ Edit Task",
            "delete_task": "🗑 Delete Task",
            "page": "Page {}/{}",
            "prev": "⬅ Prev",
            "next": "Next ➡",
            "weather": "🌤 Weather",
            "calendar": "📅 Calendar",
            "task_view": "📝 Task View",
            "calendar_view": "📅 Calendar View",
            "language": "Language",
            "auto_refresh": "Auto Refresh",
            "manual_refresh": "Manual Refresh",
            "location": "Location",
            "select_location": "Select Location",
            "temperature": "Temperature",
            "humidity": "Humidity",
            "wind": "Wind",
            "condition": "Condition",
            "loading": "Loading...",
            "error": "Error",
            "no_weather": "Unable to fetch weather",
            "daily_task_reset": "Daily tasks refreshed",
            "confirm_delete": "Confirm Delete",
            "delete_confirm_msg": "Are you sure you want to delete task \"{}\"?",
            "task_completed": "Task completed! Earned {} coins.",
            "cannot_complete": "Task cannot be completed (may be completed or on cooldown).",
            "select_task_first": "Please select a task first.",
            "task_deleted": "Task deleted.",
            "warning": "Warning",
            "congratulations": "Congratulations",
            "task_name_empty": "Task name cannot be empty.",
            "task_not_found": "Task not found.",
            "select_task_to_edit": "Please select a task first to edit.",
            "total_items": "Total {} items",
            "task_name": "Task Name",
            "task_description": "Task Description",
            "level_label": "Level",
            "type_label": "Type",
            "tags_label": "Tags",
            "reward_label": "Reward",
            "created_at_label": "Created At",
            "last_completed_label": "Last Completed",
            "current_status_label": "Current Status",
            "no_description": "(No description)",
            "no_tags": "None",
            "coins_unit": "coins",
            "one_time_completed": "Completed At",
            "save": "💾 Save",
            "cancel": "Cancel",
            "create_new_task": "Create New Task",
            "edit_task_title": "Edit Task",
            "today": "Today",
            "monday": "Mon",
            "tuesday": "Tue",
            "wednesday": "Wed",
            "thursday": "Thu",
            "friday": "Fri",
            "saturday": "Sat",
            "sunday": "Sun",
            "january": "January",
            "february": "February",
            "march": "March",
            "april": "April",
            "may": "May",
            "june": "June",
            "july": "July",
            "august": "August",
            "september": "September",
            "october": "October",
            "november": "November",
            "december": "December",
            "year": "",
            "month": "",
            "simple": "Simple",
            "normal": "Normal",
            "hard": "Hard",
            "epic": "Epic",
            "once": "One-time",
            "daily": "Daily",
            "weekly": "Weekly",
            "in_progress": "In Progress",
            "completed": "Completed",
            "available": "Available",
            "cooldown": "Cooldown",
            "city_name": "City Name",
            "example": "Example",
        }
    }
    def __init__(self, lang: str = "zh"):
        self.lang = lang
        self._t = self._translations.get(lang, self._translations["zh"])
    def t(self, key: str, **kwargs) -> str:
        text = self._t.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except:
                return text
        return text
    def set_language(self, lang: str):
        self.lang = lang
        self._t = self._translations.get(lang, self._translations["zh"])




class TaskLevel(Enum):

    SIMPLE = ("简单", 1, 10)
    NORMAL = ("普通", 2, 25)
    HARD = ("困难", 3, 50)
    EPIC = ("史诗", 4, 100)

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

    ONCE = "一次性任务"
    DAILY = "日常任务"
    WEEKLY = "每周任务"


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
            return "已完成" if self.completed else "进行中"

        if self.can_complete:
            return "可完成"
        if self.last_completed:
            return "冷却中"
        return "进行中"


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


class WeatherManager:
    def __init__(self, initial_location: str = "Beijing"):
        self.location = initial_location
        self.weather_data: Optional[Dict] = None
        self.last_update: Optional[datetime] = None
        self.data_manager: Optional[DataManager] = None
    def set_data_manager(self, data_manager: DataManager) -> None:
        self.data_manager = data_manager
    def set_location(self, location: str):
        self.location = location
        self.weather_data = None
        if self.data_manager:
            self.data_manager.weather_location = location
            self.data_manager.save()
    def fetch_weather(self) -> Optional[Dict]:
        try:
            url = f"https://wttr.in/{urllib.parse.quote(self.location)}?format=j1"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                current = data.get("current_condition", [{}])[0]
                weather = {
                    "temp": current.get("temp_C", "N/A"),
                    "humidity": current.get("humidity", "N/A"),
                    "wind": current.get("windspeedKmph", "N/A"),
                    "condition": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
                    "icon": self._get_weather_icon(current.get("weatherCode", "113")),
                }
                self.weather_data = weather
                self.last_update = datetime.now()
                return weather
        except Exception as e:
            print(f"Weather fetch error: {e}")
            return None
    def _get_weather_icon(self, code: str) -> str:
        code_map = {
            "113": "☀️",
            "116": "⛅",
            "119": "☁️",
            "122": "☁️",
            "143": "🌫️",
            "176": "🌦️",
            "179": "🌨️",
            "182": "🌨️",
            "185": "🌧️",
            "200": "⛈️",
            "227": "🌨️",
            "230": "🌨️",
            "248": "🌫️",
            "260": "🌫️",
            "263": "🌦️",
            "266": "🌧️",
            "281": "🌧️",
            "284": "🌧️",
            "293": "🌦️",
            "296": "🌦️",
            "299": "🌧️",
            "302": "🌧️",
            "305": "🌧️",
            "308": "🌧️",
            "311": "🌧️",
            "314": "🌧️",
            "317": "🌧️",
            "320": "🌧️",
            "323": "🌨️",
            "326": "🌨️",
            "329": "🌨️",
            "332": "🌨️",
            "335": "🌨️",
            "338": "🌨️",
            "350": "🌨️",
            "353": "🌦️",
            "356": "🌧️",
            "359": "🌧️",
            "362": "🌨️",
            "365": "🌨️",
            "368": "🌨️",
            "371": "🌨️",
            "374": "🌨️",
            "377": "🌨️",
            "386": "⛈️",
            "389": "⛈️",
            "392": "⛈️",
            "395": "🌨️",
        }
        return code_map.get(str(code), "🌤️")


class DataManager:

    def __init__(self, data_file: str = "task_data.json") -> None:
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.total_coins: int = 0
        self.coin_history: List[Dict] = []
        self.auto_refresh_daily: bool = True
        self.weather_location: str = "Beijing"
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
        except Exception as exc:
            print(f"[DataManager] Load data failed: {exc}")
            self.tasks = []
            self.total_coins = 0
            self.coin_history = []
            return

        self.tasks = [Task.from_dict(t) for t in raw.get("tasks", [])]
        self.total_coins = raw.get("total_coins", 0)
        self.coin_history = raw.get("coin_history", [])
        self.auto_refresh_daily = raw.get("auto_refresh_daily", True)
        self.weather_location = raw.get("weather_location", "Beijing")

    def save(self) -> None:
        data = {
            "tasks": [t.to_dict() for t in self.tasks],
            "total_coins": self.total_coins,
            "coin_history": self.coin_history,
            "auto_refresh_daily": self.auto_refresh_daily,
            "weather_location": self.weather_location,
        }
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            print(f"[DataManager] Save data failed: {exc}")


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

    def refresh_daily_tasks(self) -> int:
        count = 0
        now = datetime.now()
        for task in self.tasks:
            if task.task_type == TaskType.DAILY and task.last_completed:
                last_dt = datetime.fromisoformat(task.last_completed)
                if now.date() > last_dt.date():
                    task.last_completed = None
                    count += 1
        if count > 0:
            self.save()
        return count

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
        self.weather = WeatherManager(initial_location=self.data.weather_location)
        self.weather.set_data_manager(self.data)
        self.i18n = I18n("en")
        self.current_view = "task"
        self.last_daily_refresh_date = date.today()
        self.calendar_year = datetime.now().year
        self.calendar_month = datetime.now().month

        self.search_var = tk.StringVar()
        self.filter_level_var = tk.StringVar(value=self.i18n.t("all"))
        self.filter_type_var = tk.StringVar(value=self.i18n.t("all"))
        self.filter_tag_var = tk.StringVar()
        self.sort_field_var = tk.StringVar(value=self.i18n.t("default"))
        self.sort_order_var = tk.StringVar(value=self.i18n.t("desc"))

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
        self.weather_label: tk.Label
        self.calendar_frame: tk.Frame
        self.view_toggle_btn: tk.Button

        self.selected_task_id: Optional[str] = None

        self._build_ui()
        self._check_daily_refresh()
        self.refresh_task_list()
        self.update_stats()
        self._update_weather()


    def _build_ui(self) -> None:
        self.root.title(self.i18n.t("app_title"))
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
        self.title_label = tk.Label(
            title_row,
            text=self.i18n.t("app_title").replace("🌿 ", ""),
            font=("Microsoft YaHei", 24, "bold"),
            bg=colors["bg"],
            fg=colors["fg"],
        )
        self.title_label.pack(side=tk.LEFT)
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
        self.subtitle_label = tk.Label(
            subtitle_frame,
            text=self.i18n.t("subtitle"),
            font=("Microsoft YaHei", 12, "bold"),
            bg=colors["bg"],
            fg=colors["fg_light"],
        )
        self.subtitle_label.pack(side=tk.LEFT)

        self._build_stats_bar(main)

        middle = tk.Frame(main, bg=colors["bg"])
        middle.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.task_list_panel = tk.Frame(middle, bg=colors["bg"])
        self.task_list_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        self._build_task_list_panel(self.task_list_panel)
        self.calendar_frame = tk.Frame(middle, bg=colors["bg"])
        self._build_detail_panel(middle)

    @property
    def _colors(self) -> Dict[str, str]:
        return {
            "bg": "#f8f4e6",
            "bg_light": "#fefcf5",
            "bg_panel": "#e8e0d0",
            "panel": "#d4c5a9",
            "panel_dark": "#c4b59a",
            "card": "#e8ddd0",
            "fg": "#2d2418",
            "fg_light": "#4a3d2e",
            "fg_white": "#ffffff",
            "button": "#9db882",
            "button_hover": "#8aa770",
            "button_secondary": "#c9a97a",
            "button_secondary_hover": "#b89a6a",
            "accent": "#b8a082",
            "accent_dark": "#a89072",
            "success": "#7ba05b",
            "danger": "#d67a7a",
            "shadow": "#d0c4b0",
            "weather_bg": "#a8c4d8",
            "weather_fg": "#1a3a4a",
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
        self.coin_title_label = tk.Label(
            coin_inner,
            text=self.i18n.t("total_coins"),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["accent"],
            fg=c["fg_white"],
        )
        self.coin_title_label.pack(padx=20, pady=(10, 0))
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
        self.total_task_title_label = tk.Label(
            total_inner,
            text=self.i18n.t("total_tasks"),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        )
        self.total_task_title_label.pack(padx=20, pady=(10, 0))
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
        self.completed_title_label = tk.Label(
            done_inner,
            text=self.i18n.t("completed"),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["success"],
            fg=c["fg_white"],
        )
        self.completed_title_label.pack(padx=20, pady=(10, 0))
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
        self.progress_title_label = tk.Label(
            prog_box,
            text=self.i18n.t("progress"),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        )
        self.progress_title_label.pack(anchor="w")

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

        weather_box = tk.Frame(bar, bg=c["panel"], bd=0)
        weather_box.pack(side=tk.RIGHT, padx=10, pady=10)
        weather_card = tk.Frame(weather_box, bg=c["weather_bg"], bd=3, relief=tk.RAISED)
        weather_card.pack(padx=2, pady=2)
        self.weather_header = tk.Frame(weather_card, bg=c["weather_bg"])
        self.weather_header.pack(fill=tk.X, padx=12, pady=(10, 4))
        tk.Label(
            self.weather_header,
            text="🌤️",
            font=("Microsoft YaHei", 16),
            bg=c["weather_bg"],
            fg=c["weather_fg"],
        ).pack(side=tk.LEFT, padx=(0, 6))
        self.weather_location_label = tk.Label(
            self.weather_header,
            text=self.weather.location,
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["weather_bg"],
            fg=c["weather_fg"],
            cursor="hand2",
        )
        self.weather_location_label.pack(side=tk.LEFT)
        self.weather_location_label.bind("<Button-1>", lambda _e: self._select_weather_location())
        self.weather_icon_label = tk.Label(
            weather_card,
            text="⏳",
            font=("Microsoft YaHei", 24),
            bg=c["weather_bg"],
            fg=c["weather_fg"],
        )
        self.weather_icon_label.pack(pady=(4, 2))
        self.weather_temp_label = tk.Label(
            weather_card,
            text="--°C",
            font=("Microsoft YaHei", 18, "bold"),
            bg=c["weather_bg"],
            fg=c["weather_fg"],
        )
        self.weather_temp_label.pack()
        self.weather_condition_label = tk.Label(
            weather_card,
            text=self.i18n.t("loading"),
            font=("Microsoft YaHei", 9),
            bg=c["weather_bg"],
            fg=c["weather_fg"],
        )
        self.weather_condition_label.pack(pady=(2, 10))
        btn_box = tk.Frame(bar, bg=c["panel"], bd=0)
        btn_box.pack(side=tk.RIGHT, padx=20, pady=10)

        self.add_btn = tk.Button(
            btn_box,
            text=self.i18n.t("add_task"),
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
        self.add_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        self.refresh_btn = tk.Button(
            btn_box,
            text=self.i18n.t("refresh"),
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
        self.refresh_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        self.view_toggle_btn = tk.Button(
            btn_box,
            text=self.i18n.t("calendar_view"),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=self._toggle_view,
        )
        self.view_toggle_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        lang_btn = tk.Button(
            btn_box,
            text="🌐 中/EN",
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self._toggle_language,
        )
        lang_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))
        self.daily_refresh_btn = tk.Button(
            btn_box,
            text="🔄 " + self.i18n.t("manual_refresh"),
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self._manual_refresh_daily,
        )
        self.daily_refresh_btn.pack(side=tk.TOP, fill=tk.X)

    def _build_task_list_panel(self, parent: tk.Frame) -> None:
        c = self._colors

        outer = tk.Frame(parent, bg=c["bg_panel"], bd=0, relief=tk.FLAT)
        outer.pack(fill=tk.BOTH, expand=True)
        panel = tk.Frame(outer, bg=c["panel"], bd=0, relief=tk.FLAT)
        panel.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        title_bar = tk.Frame(panel, bg=c["panel_dark"], bd=0, relief=tk.FLAT)
        title_bar.pack(fill=tk.X, padx=5, pady=5)
        self.task_list_title = tk.Label(
            title_bar,
            text=self.i18n.t("task_list"),
            font=("Microsoft YaHei", 16, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        )
        self.task_list_title.pack(side=tk.LEFT, padx=10, pady=8)

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

        self.filter_label = tk.Label(
            filter_row,
            text=self.i18n.t("filter"),
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        )
        self.filter_label.pack(side=tk.LEFT, padx=(0, 4))

        level_values = [
            self.i18n.t("all"),
            self.i18n.t("simple"),
            self.i18n.t("normal"),
            self.i18n.t("hard"),
            self.i18n.t("epic"),
        ]
        self.level_menu = ttk.Combobox(
            filter_row,
            textvariable=self.filter_level_var,
            values=level_values,
            width=6,
            state="readonly",
        )
        self.level_menu.pack(side=tk.LEFT, padx=4)
        self.level_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())

        type_values = [
            self.i18n.t("all"),
            self.i18n.t("once"),
            self.i18n.t("daily"),
            self.i18n.t("weekly"),
        ]
        self.type_menu = ttk.Combobox(
            filter_row,
            textvariable=self.filter_type_var,
            values=type_values,
            width=10,
            state="readonly",
        )
        self.type_menu.pack(side=tk.LEFT, padx=4)
        self.type_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())

        self.tag_label = tk.Label(
            filter_row,
            text=self.i18n.t("tag"),
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        )
        self.tag_label.pack(side=tk.LEFT, padx=(10, 4))

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

        self.sort_label = tk.Label(
            filter_row,
            text=self.i18n.t("sort"),
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["panel"],
            fg=c["fg"],
        )
        self.sort_label.pack(side=tk.LEFT, padx=(12, 4))

        sort_values = [
            self.i18n.t("default"),
            self.i18n.t("level"),
            self.i18n.t("name"),
            self.i18n.t("create_time"),
        ]
        self.sort_menu = ttk.Combobox(
            filter_row,
            textvariable=self.sort_field_var,
            values=sort_values,
            width=8,
            state="readonly",
        )
        self.sort_menu.pack(side=tk.LEFT, padx=4)
        self.sort_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())

        order_values = [
            self.i18n.t("asc"),
            self.i18n.t("desc"),
        ]
        self.order_menu = ttk.Combobox(
            filter_row,
            textvariable=self.sort_order_var,
            values=order_values,
            width=6,
            state="readonly",
        )
        self.order_menu.pack(side=tk.LEFT, padx=4)
        self.order_menu.bind("<<ComboboxSelected>>", lambda _e: self.filter_tasks())

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

        def _on_inner_configure(_e: tk.Event) -> None:
            update_canvas_scrollregion()

        def _on_canvas_configure(_e: tk.Event) -> None:
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
            text=self.i18n.t("page", page=1, total=1),
            font=("Microsoft YaHei", 9),
            bg=c["panel"],
            fg=c["fg"],
        )
        self.page_info_label.pack(side=tk.LEFT)

        nav = tk.Frame(pager, bg=c["panel"])
        nav.pack(side=tk.RIGHT)

        self.prev_btn = tk.Button(
            nav,
            text=self.i18n.t("prev"),
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
            text=self.i18n.t("next"),
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

        outer = tk.Frame(parent, bg=c["bg_panel"], bd=0, relief=tk.FLAT, width=360)
        outer.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(8, 0))
        outer.pack_propagate(False)

        panel = tk.Frame(outer, bg=c["panel"], bd=0, relief=tk.FLAT)
        panel.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        title = tk.Frame(panel, bg=c["panel_dark"], bd=0, relief=tk.FLAT)
        title.pack(fill=tk.X, padx=5, pady=5)
        self.task_detail_title = tk.Label(
            title,
            text=self.i18n.t("task_detail"),
            font=("Microsoft YaHei", 16, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        )
        self.task_detail_title.pack(pady=8)

        content_frame = tk.Frame(panel, bg=c["panel"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        text_wrap = tk.Frame(content_frame, bg=c["card"], bd=0, relief=tk.FLAT)
        text_wrap.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

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
            height=12,
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        self._set_detail_text(self.i18n.t("select_task"))

        btns = tk.Frame(content_frame, bg=c["panel"])
        btns.pack(fill=tk.X, pady=0)

        self.complete_btn = tk.Button(
            btns,
            text=self.i18n.t("complete_task"),
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

        self.edit_btn = tk.Button(
            btns,
            text=self.i18n.t("edit_task"),
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
        self.edit_btn.pack(fill=tk.X, pady=3)

        self.delete_btn = tk.Button(
            btns,
            text=self.i18n.t("delete_task"),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["danger"],
            fg=c["fg_white"],
            activebackground="#5a7a1a",
            activeforeground=c["fg_white"],
            bd=3,
            relief=tk.RAISED,
            cursor="hand2",
            command=self.delete_selected_task,
        )
        self.delete_btn.pack(fill=tk.X, pady=3)


    def focus_search(self) -> None:
        self.search_var.set("")
        self.refresh_task_list()

    def clear_selection(self) -> None:
        self.selected_task_id = None
        self._set_detail_text(self.i18n.t("select_task"))
        self.complete_btn.config(state=tk.DISABLED, text=self.i18n.t("complete_task"))

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
            self.i18n.t("simple"): TaskLevel.SIMPLE,
            self.i18n.t("normal"): TaskLevel.NORMAL,
            self.i18n.t("hard"): TaskLevel.HARD,
            self.i18n.t("epic"): TaskLevel.EPIC,
        }
        if lv in level_map:
            tasks = [t for t in tasks if t.level == level_map[lv]]

        tp = self.filter_type_var.get()
        type_map = {
            self.i18n.t("once"): TaskType.ONCE,
            self.i18n.t("daily"): TaskType.DAILY,
            self.i18n.t("weekly"): TaskType.WEEKLY,
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

        reverse = self.sort_order_var.get() == self.i18n.t("desc")
        field = self.sort_field_var.get()
        if field == self.i18n.t("level"):
            tasks.sort(key=lambda t: t.level.order, reverse=reverse)
        elif field == self.i18n.t("name"):
            tasks.sort(key=lambda t: t.name, reverse=reverse)
        elif field == self.i18n.t("create_time"):
            tasks.sort(key=lambda t: t.created_at, reverse=reverse)

        self.filtered_tasks = tasks

        total = len(tasks)
        total_pages = max(1, (total + self.page_size - 1) // self.page_size)
        self.current_page = max(1, min(self.current_page, total_pages))

        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_tasks = tasks[start:end]

        if not page_tasks:
            empty_text = f"{self.i18n.t('all')} {self.i18n.t('total_tasks')}\n{self.i18n.t('add_task')} ✨"
            tk.Label(
                self.task_list_frame,
                text=empty_text,
                font=("Microsoft YaHei", 12),
                bg=self._colors["card"],
                fg=self._colors["fg_light"],
                justify=tk.CENTER,
            ).pack(pady=40)
        else:
            for t in page_tasks:
                self._render_task_card(t)

        page_text = self.i18n.t("page", page=self.current_page, total=total_pages)
        total_text = self.i18n.t("total_items", total=total)
        self.page_info_label.config(
            text=f"{page_text} ({total_text})"
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
            TaskLevel.SIMPLE: ("#f0e68c", "#d4af37"),
            TaskLevel.NORMAL: ("#98fb98", "#6b8e23"),
            TaskLevel.HARD: ("#ffb347", "#d2691e"),
            TaskLevel.EPIC: ("#dda0dd", "#9370db"),
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

        state_text = self._get_task_status_text(task)
        state_bg = c["accent_dark"] if task.completed or (task.last_completed and not task.can_complete) else c["panel_dark"]
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
        type_text = self._get_task_type_text(task.task_type)
        tk.Label(
            mid,
            text=f"{type_icon} {type_text}",
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

        created_text = self.i18n.t("created_at_label").replace("：", "").replace(":", "")
        tk.Label(
            inner,
            text=f"{created_text}：{datetime.fromisoformat(task.created_at).strftime('%m-%d %H:%M')}",
            font=("Microsoft YaHei", 8),
            bg=bg_color,
            fg=c["fg"],
            anchor="w",
        ).pack(fill=tk.X, pady=(3, 0))

        def on_click(_e: tk.Event) -> None:
            self.select_task(task.id)

        def on_enter(_e: tk.Event) -> None:
            frame.config(relief=tk.SUNKEN)

        def on_leave(_e: tk.Event) -> None:
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

        tags = ", ".join(task.tags) if task.tags else self.i18n.t("no_tags")

        info = [
            f"📝 {self.i18n.t('task_name')}：{task.name}",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            f"📄 {self.i18n.t('task_description')}：",
            task.description or self.i18n.t("no_description"),
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            f"⭐ {self.i18n.t('level_label')}：{self._get_task_level_text(task.level)} (Lv.{task.level.order})",
            f"🔄 {self.i18n.t('type_label')}：{self._get_task_type_text(task.task_type)}",
            f"🏷 {self.i18n.t('tags_label')}：{tags}",
            f"💰 {self.i18n.t('reward_label')}：{task.level.reward} {self.i18n.t('coins_unit')}",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            f"📅 {self.i18n.t('created_at_label')}：{datetime.fromisoformat(task.created_at).strftime('%Y-%m-%d %H:%M')}",
        ]

        if task.last_completed:
            info.append(
                f"✅ {self.i18n.t('last_completed_label')}：{datetime.fromisoformat(task.last_completed).strftime('%Y-%m-%d %H:%M')}"
            )
        if task.completed_at:
            info.append(
                f"✅ {self.i18n.t('one_time_completed')}：{datetime.fromisoformat(task.completed_at).strftime('%Y-%m-%d %H:%M')}"
            )

        info.append("")
        status_text = self._get_task_status_text(task)
        info.append(f"{'✅' if task.can_complete else '⏳'} {self.i18n.t('current_status_label')}：{status_text}")

        self._set_detail_text("\n".join(info))

        if task.can_complete:
            self.complete_btn.config(state=tk.NORMAL, text=self.i18n.t("complete_task"))
        else:
            self.complete_btn.config(state=tk.DISABLED, text="⏳ " + self.i18n.t("cannot_complete"))


    def show_task_editor(self, edit: bool = False) -> None:
        is_edit = edit
        current: Optional[Task] = None
        if is_edit:
            if not self.selected_task_id:
                messagebox.showwarning(self.i18n.t("warning"), self.i18n.t("select_task_to_edit"))
                return
            current = next(
                (t for t in self.data.iter_tasks() if t.id == self.selected_task_id),
                None,
            )
            if not current:
                messagebox.showwarning(self.i18n.t("warning"), self.i18n.t("task_not_found"))
                return

        win = tk.Toplevel(self.root)
        win.title(self.i18n.t("edit_task") if is_edit else self.i18n.t("add_task"))
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
        title_text = "✏ " + self.i18n.t("edit_task") if is_edit else "✨ " + self.i18n.t("add_task").replace("＋ ", "")
        tk.Label(
            title,
            text=title_text,
            font=("Microsoft YaHei", 14, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        ).pack(pady=6)

        body = tk.Frame(panel, bg=c["panel"])
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        tk.Label(
            body,
            text=f"📝 {self.i18n.t('task_name')}：",
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
            text=f"📄 {self.i18n.t('task_description')}：",
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

        tags_label_text = self.i18n.t("tags_label").replace("：", "").replace(":", "")
        tk.Label(
            body,
            text=f"🏷 {tags_label_text}（{self.i18n.t('tag').replace(':', '')}）",
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

        level_label_text = self.i18n.t("level_label")
        tk.Label(
            body,
            text=f"⭐ {level_label_text}：",
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
            level_text = self._get_task_level_text(lv)
            ttk.Radiobutton(
                level_row,
                text=f"{level_text} (+{lv.reward}💰)",
                value=lv.name,
                variable=level_var,
            ).pack(side=tk.LEFT, padx=4)

        type_label_text = self.i18n.t("type_label")
        tk.Label(
            body,
            text=f"🔄 {type_label_text}：",
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
            type_text = self._get_task_type_text(tp)
            ttk.Radiobutton(
                type_row,
                text=type_text,
                value=tp.name,
                variable=type_var,
            ).pack(side=tk.LEFT, padx=4)

        foot = tk.Frame(panel, bg=c["panel"])
        foot.pack(pady=12)

        def on_save() -> None:
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning(self.i18n.t("warning"), self.i18n.t("task_name_empty"))
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
            text=self.i18n.t("save"),
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
            text=self.i18n.t("cancel"),
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
            messagebox.showwarning(self.i18n.t("warning"), self.i18n.t("select_task_first"))
            return
        task = next(
            (t for t in self.data.iter_tasks() if t.id == self.selected_task_id), None
        )
        if not task:
            return
        if not messagebox.askyesno(self.i18n.t("confirm_delete"), self.i18n.t("delete_confirm_msg", task_name=task.name)):
            return
        self.data.delete_task(task.id)
        self.selected_task_id = None
        self.refresh_task_list()
        self._set_detail_text(self.i18n.t("task_deleted"))

    def complete_selected_task(self) -> None:
        if not self.selected_task_id:
            messagebox.showwarning(self.i18n.t("warning"), self.i18n.t("select_task_first"))
            return
        coins = self.data.complete_task(self.selected_task_id)
        if coins <= 0:
            messagebox.showinfo(self.i18n.t("warning"), self.i18n.t("cannot_complete"))
            self.refresh_task_list()
            return
        messagebox.showinfo(self.i18n.t("congratulations"), self.i18n.t("task_completed", coins=coins))
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
    def _check_daily_refresh(self) -> None:
        today = date.today()
        if self.data.auto_refresh_daily and today > self.last_daily_refresh_date:
            count = self.data.refresh_daily_tasks()
            if count > 0:
                self.last_daily_refresh_date = today
                self.refresh_task_list()
    def _update_weather(self) -> None:
        def fetch():
            weather = self.weather.fetch_weather()
            if weather:
                self.root.after(0, lambda: self._display_weather(weather))
            else:
                self.root.after(0, lambda: self._display_weather_error())
        threading.Thread(target=fetch, daemon=True).start()
    def _display_weather(self, weather: Dict) -> None:
        if hasattr(self, 'weather_icon_label'):
            self.weather_icon_label.config(text=weather.get('icon', '🌤️'))
        if hasattr(self, 'weather_temp_label'):
            self.weather_temp_label.config(text=f"{weather.get('temp', '--')}°C")
        if hasattr(self, 'weather_condition_label'):
            condition = weather.get('condition', self.i18n.t("loading"))
            if len(condition) > 10:
                condition = condition[:10] + "..."
            self.weather_condition_label.config(text=condition)
        if hasattr(self, 'weather_location_label'):
            self.weather_location_label.config(text=self.weather.location)
    def _display_weather_error(self) -> None:
        if hasattr(self, 'weather_icon_label'):
            self.weather_icon_label.config(text="❌")
        if hasattr(self, 'weather_temp_label'):
            self.weather_temp_label.config(text="--°C")
        if hasattr(self, 'weather_condition_label'):
            self.weather_condition_label.config(text=self.i18n.t("no_weather"))
    def _toggle_language(self) -> None:
        new_lang = "en" if self.i18n.lang == "zh" else "zh"
        self.i18n.set_language(new_lang)
        self._refresh_ui_texts()
    def _get_task_level_text(self, level: TaskLevel) -> str:
        level_map = {
            TaskLevel.SIMPLE: self.i18n.t("simple"),
            TaskLevel.NORMAL: self.i18n.t("normal"),
            TaskLevel.HARD: self.i18n.t("hard"),
            TaskLevel.EPIC: self.i18n.t("epic"),
        }
        return level_map.get(level, level.label)
    def _get_task_type_text(self, task_type: TaskType) -> str:
        type_map = {
            TaskType.ONCE: self.i18n.t("once"),
            TaskType.DAILY: self.i18n.t("daily"),
            TaskType.WEEKLY: self.i18n.t("weekly"),
        }
        return type_map.get(task_type, task_type.value)
    def _get_task_status_text(self, task: Task) -> str:
        if task.is_once:
            return self.i18n.t("completed") if task.completed else self.i18n.t("in_progress")
        if task.can_complete:
            return self.i18n.t("available")
        if task.last_completed:
            return self.i18n.t("cooldown")
        return self.i18n.t("in_progress")
    def _refresh_ui_texts(self) -> None:
        self.root.title(self.i18n.t("app_title"))
        if hasattr(self, 'title_label'):
            self.title_label.config(text=self.i18n.t("app_title").replace("🌿 ", ""))
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.config(text=self.i18n.t("subtitle"))
        if hasattr(self, 'coin_title_label'):
            self.coin_title_label.config(text=self.i18n.t("total_coins"))
        if hasattr(self, 'total_task_title_label'):
            self.total_task_title_label.config(text=self.i18n.t("total_tasks"))
        if hasattr(self, 'completed_title_label'):
            self.completed_title_label.config(text=self.i18n.t("completed"))
        if hasattr(self, 'progress_title_label'):
            self.progress_title_label.config(text=self.i18n.t("progress"))
        if hasattr(self, 'add_btn'):
            self.add_btn.config(text=self.i18n.t("add_task"))
        if hasattr(self, 'refresh_btn'):
            self.refresh_btn.config(text=self.i18n.t("refresh"))
        if hasattr(self, 'daily_refresh_btn'):
            self.daily_refresh_btn.config(text="🔄 " + self.i18n.t("manual_refresh"))
        if hasattr(self, 'view_toggle_btn'):
            if self.current_view == "task":
                self.view_toggle_btn.config(text=self.i18n.t("calendar_view"))
            else:
                self.view_toggle_btn.config(text=self.i18n.t("task_view"))
        if hasattr(self, 'task_list_title'):
            self.task_list_title.config(text=self.i18n.t("task_list"))
        if hasattr(self, 'task_detail_title'):
            self.task_detail_title.config(text=self.i18n.t("task_detail"))
        if hasattr(self, 'filter_label'):
            self.filter_label.config(text=self.i18n.t("filter"))
        if hasattr(self, 'tag_label'):
            self.tag_label.config(text=self.i18n.t("tag"))
        if hasattr(self, 'sort_label'):
            self.sort_label.config(text=self.i18n.t("sort"))
        if hasattr(self, 'level_menu'):
            level_values = [
                self.i18n.t("all"),
                self.i18n.t("simple"),
                self.i18n.t("normal"),
                self.i18n.t("hard"),
                self.i18n.t("epic"),
            ]
            current_level = self.filter_level_var.get()
            self.level_menu.config(values=level_values)
            if current_level in ["简单", "普通", "困难", "史诗"]:
                level_map = {"简单": self.i18n.t("simple"), "普通": self.i18n.t("normal"), 
                           "困难": self.i18n.t("hard"), "史诗": self.i18n.t("epic")}
                self.filter_level_var.set(level_map.get(current_level, self.i18n.t("all")))
            elif current_level not in level_values:
                self.filter_level_var.set(self.i18n.t("all"))
        if hasattr(self, 'type_menu'):
            type_values = [
                self.i18n.t("all"),
                self.i18n.t("once"),
                self.i18n.t("daily"),
                self.i18n.t("weekly"),
            ]
            current_type = self.filter_type_var.get()
            self.type_menu.config(values=type_values)
            if current_type in ["一次性任务", "日常任务", "每周任务"]:
                type_map = {"一次性任务": self.i18n.t("once"), "日常任务": self.i18n.t("daily"), 
                          "每周任务": self.i18n.t("weekly")}
                self.filter_type_var.set(type_map.get(current_type, self.i18n.t("all")))
            elif current_type not in type_values:
                self.filter_type_var.set(self.i18n.t("all"))
        if hasattr(self, 'sort_menu'):
            sort_values = [
                self.i18n.t("default"),
                self.i18n.t("level"),
                self.i18n.t("name"),
                self.i18n.t("create_time"),
            ]
            current_sort = self.sort_field_var.get()
            self.sort_menu.config(values=sort_values)
            if current_sort not in sort_values:
                self.sort_field_var.set(self.i18n.t("default"))
        if hasattr(self, 'sort_order_menu'):
            order_values = [self.i18n.t("asc"), self.i18n.t("desc")]
            current_order = self.sort_order_var.get()
            self.sort_order_menu.config(values=order_values)
            if current_order not in order_values:
                self.sort_order_var.set(self.i18n.t("asc"))
        if hasattr(self, 'prev_btn'):
            self.prev_btn.config(text=self.i18n.t("prev"))
        if hasattr(self, 'next_btn'):
            self.next_btn.config(text=self.i18n.t("next"))
        if hasattr(self, 'complete_btn'):
            if self.selected_task_id:
                task = next((t for t in self.data.iter_tasks() if t.id == self.selected_task_id), None)
                if task:
                    if task.can_complete:
                        self.complete_btn.config(state=tk.NORMAL, text=self.i18n.t("complete_task"))
                    else:
                        self.complete_btn.config(state=tk.DISABLED, text="⏳ " + self.i18n.t("cannot_complete"))
                else:
                    self.complete_btn.config(state=tk.DISABLED, text=self.i18n.t("complete_task"))
            else:
                self.complete_btn.config(state=tk.DISABLED, text=self.i18n.t("complete_task"))
        if hasattr(self, 'edit_btn'):
            self.edit_btn.config(text=self.i18n.t("edit_task"))
        if hasattr(self, 'delete_btn'):
            self.delete_btn.config(text=self.i18n.t("delete_task"))
        if hasattr(self, 'weather_condition_label'):
            if not self.weather.weather_data:
                self.weather_condition_label.config(text=self.i18n.t("loading"))
        self.refresh_task_list()
        if self.current_view == "calendar":
            self._build_calendar()
        if self.selected_task_id:
            self.select_task(self.selected_task_id)
        else:
            self._set_detail_text(self.i18n.t("select_task"))
    def _toggle_view(self) -> None:
        if self.current_view == "task":
            self.current_view = "calendar"
            self._show_calendar_view()
        else:
            self.current_view = "task"
            self._show_task_view()
    def _show_calendar_view(self) -> None:
        if hasattr(self, 'task_list_panel'):
            self.task_list_panel.pack_forget()
        if hasattr(self, 'calendar_frame'):
            self.calendar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        if hasattr(self, 'view_toggle_btn'):
            self.view_toggle_btn.config(text=self.i18n.t("task_view"))
        self._build_calendar()
    def _show_task_view(self) -> None:
        if hasattr(self, 'calendar_frame'):
            self.calendar_frame.pack_forget()
        if hasattr(self, 'task_list_panel'):
            self.task_list_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        if hasattr(self, 'view_toggle_btn'):
            self.view_toggle_btn.config(text=self.i18n.t("calendar_view"))
    def _build_calendar(self) -> None:
        if not hasattr(self, 'calendar_frame'):
            return
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        c = self._colors
        year = self.calendar_year
        month = self.calendar_month
        title_frame = tk.Frame(self.calendar_frame, bg=c["panel_dark"])
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        prev_month_btn = tk.Button(
            title_frame,
            text="⬅",
            font=("Microsoft YaHei", 14, "bold"),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self._prev_month,
            width=3,
        )
        prev_month_btn.pack(side=tk.LEFT, padx=10, pady=8)
        month_names = [
            self.i18n.t("january"), self.i18n.t("february"), self.i18n.t("march"),
            self.i18n.t("april"), self.i18n.t("may"), self.i18n.t("june"),
            self.i18n.t("july"), self.i18n.t("august"), self.i18n.t("september"),
            self.i18n.t("october"), self.i18n.t("november"), self.i18n.t("december")
        ]
        year_text = self.i18n.t("year")
        month_text = self.i18n.t("month")
        if year_text and month_text and year_text != "year" and month_text != "month":
            title_text = f"{year}{year_text}{month_names[month-1]}{month_text}"
        else:
            title_text = f"{month_names[month-1]} {year}"
        self.calendar_title_label = tk.Label(
            title_frame,
            text=title_text,
            font=("Microsoft YaHei", 16, "bold"),
            bg=c["panel_dark"],
            fg=c["fg_white"],
        )
        self.calendar_title_label.pack(side=tk.LEFT, expand=True, pady=8)
        next_month_btn = tk.Button(
            title_frame,
            text="➡",
            font=("Microsoft YaHei", 14, "bold"),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self._next_month,
            width=3,
        )
        next_month_btn.pack(side=tk.RIGHT, padx=10, pady=8)
        today_btn = tk.Button(
            title_frame,
            text=self.i18n.t("today"),
            font=("Microsoft YaHei", 10, "bold"),
            bg=c["button"],
            fg=c["fg_white"],
            activebackground=c["button_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=self._go_to_today,
            width=4,
        )
        today_btn.pack(side=tk.RIGHT, padx=5, pady=8)
        week_frame = tk.Frame(self.calendar_frame, bg=c["panel"])
        week_frame.pack(fill=tk.X, padx=8, pady=(0, 4))
        weekdays = [
            self.i18n.t("monday"), self.i18n.t("tuesday"), self.i18n.t("wednesday"),
            self.i18n.t("thursday"), self.i18n.t("friday"), self.i18n.t("saturday"),
            self.i18n.t("sunday")
        ]
        for day in weekdays:
            tk.Label(
                week_frame,
                text=day,
                font=("Microsoft YaHei", 10, "bold"),
                bg=c["panel"],
                fg=c["fg"],
                width=10,
            ).pack(side=tk.LEFT, padx=2)
        cal = monthcalendar(year, month)
        for week in cal:
            week_frame = tk.Frame(self.calendar_frame, bg=c["panel"])
            week_frame.pack(fill=tk.X, padx=8, pady=2)
            for day in week:
                day_frame = tk.Frame(week_frame, bg=c["card"], bd=1, relief=tk.RIDGE, width=100, height=80)
                day_frame.pack(side=tk.LEFT, padx=2, fill=tk.BOTH, expand=True)
                day_frame.pack_propagate(False)
                if day == 0:
                    continue
                day_date = date(year, month, day)
                is_today = day_date == date.today()
                day_color = c["fg_white"] if is_today else c["fg"]
                day_bg = c["success"] if is_today else c["card"]
                day_label = tk.Label(
                    day_frame,
                    text=str(day),
                    font=("Microsoft YaHei", 12, "bold"),
                    bg=day_bg,
                    fg=day_color,
                )
                day_label.pack(anchor="nw", padx=4, pady=2)
                day_tasks = [
                    t for t in self.data.iter_tasks()
                    if t.task_type == TaskType.DAILY
                ]
                if day_tasks:
                    task_text = "\n".join([f"• {t.name[:8]}" for t in day_tasks[:3]])
                    if len(day_tasks) > 3:
                        task_text += f"\n+{len(day_tasks)-3}"
                    tk.Label(
                        day_frame,
                        text=task_text,
                        font=("Microsoft YaHei", 8),
                        bg=c["card"],
                        fg=c["fg"],
                        justify=tk.LEFT,
                        anchor="nw",
                    ).pack(anchor="nw", padx=4, pady=(0, 2))
    def _prev_month(self) -> None:
        self.calendar_month -= 1
        if self.calendar_month < 1:
            self.calendar_month = 12
            self.calendar_year -= 1
        self._build_calendar()
    def _next_month(self) -> None:
        self.calendar_month += 1
        if self.calendar_month > 12:
            self.calendar_month = 1
            self.calendar_year += 1
        self._build_calendar()
    def _go_to_today(self) -> None:
        now = datetime.now()
        self.calendar_year = now.year
        self.calendar_month = now.month
        self._build_calendar()
    def _select_weather_location(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title(self.i18n.t("select_location"))
        dialog.geometry("400x200")
        dialog.configure(bg=self._colors["bg"])
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        c = self._colors
        tk.Label(
            dialog,
            text=f"🌍 {self.i18n.t('select_location')}",
            font=("Microsoft YaHei", 14, "bold"),
            bg=c["bg"],
            fg=c["fg"],
        ).pack(pady=(20, 10))
        entry_frame = tk.Frame(dialog, bg=c["bg"])
        entry_frame.pack(pady=10, padx=30, fill=tk.X)
        tk.Label(
            entry_frame,
            text=f"{self.i18n.t('location')}:",
            font=("Microsoft YaHei", 11),
            bg=c["bg"],
            fg=c["fg"],
        ).pack(side=tk.LEFT, padx=(0, 10))
        location_var = tk.StringVar(value=self.weather.location)
        entry = tk.Entry(
            entry_frame,
            textvariable=location_var,
            font=("Microsoft YaHei", 11),
            bg=c["bg_light"],
            fg=c["fg"],
            relief=tk.RAISED,
            bd=2,
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        entry.focus_set()
        entry.select_range(0, tk.END)
        tk.Label(
            dialog,
            text=f"{self.i18n.t('example')}: Beijing, Shanghai, New York, Tokyo",
            font=("Microsoft YaHei", 9),
            bg=c["bg"],
            fg=c["fg_light"],
        ).pack(pady=(5, 15))
        btn_frame = tk.Frame(dialog, bg=c["bg"])
        btn_frame.pack(pady=10)
        def on_confirm():
            loc = location_var.get().strip()
            if loc:
                self.weather.set_location(loc)
                if hasattr(self, 'weather_location_label'):
                    self.weather_location_label.config(text=loc)
                self._update_weather()
                dialog.destroy()
        tk.Button(
            btn_frame,
            text=self.i18n.t("save").replace("💾 ", ""),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["button"],
            fg=c["fg_white"],
            activebackground=c["button_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=on_confirm,
            width=10,
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            btn_frame,
            text=self.i18n.t("cancel"),
            font=("Microsoft YaHei", 11, "bold"),
            bg=c["button_secondary"],
            fg=c["fg_white"],
            activebackground=c["button_secondary_hover"],
            activeforeground=c["fg_white"],
            bd=2,
            relief=tk.RAISED,
            cursor="hand2",
            command=dialog.destroy,
            width=10,
        ).pack(side=tk.LEFT, padx=5)
        entry.bind("<Return>", lambda _e: on_confirm())
        dialog.bind("<Escape>", lambda _e: dialog.destroy())
    def _manual_refresh_daily(self) -> None:
        count = self.data.refresh_daily_tasks()
        if count > 0:
            messagebox.showinfo(self.i18n.t("daily_task_reset"), f"{self.i18n.t('daily_task_reset')}: {count} tasks")
            self.refresh_task_list()
        else:
            messagebox.showinfo(self.i18n.t("refresh"), "No tasks to refresh")




def main() -> None:
    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()



