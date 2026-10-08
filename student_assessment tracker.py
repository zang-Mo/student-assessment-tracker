import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class StudentAssessmentTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Assessment Tracker")
        self.root.geometry("1250x760")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#f5f7fb")

        self.selected_task_id = None

        self.create_database()
        self.create_variables()
        self.create_styles()
        self.create_interface()

        self.load_tasks()
        self.update_dashboard()

    def create_database(self):
        self.connection = sqlite3.connect(
            "student_assessment_tracker.db"
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                date_added TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def create_variables(self):
        self.task_name_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")
        self.search_var = tk.StringVar()

    def create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#25324a",
            rowheight=42,
            fieldbackground="white",
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#f1f4fb",
            foreground="#405070",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#e8eaff")],
            foreground=[("selected", "#24325a")]
        )

    def create_interface(self):

        self.create_sidebar()

        self.main_area = tk.Frame(
            self.root,
            bg="#f5f7fb"
        )

        self.main_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_top_bar()
        self.create_summary_cards()
        self.create_dashboard_content()

    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            width=225,
            bg="white"
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        logo_area = tk.Frame(
            sidebar,
            bg="white",
            height=100
        )

        logo_area.pack(fill="x")
        logo_area.pack_propagate(False)

        tk.Label(
            logo_area,
            text="▣",
            font=("Segoe UI", 30, "bold"),
            fg="#5b5bd6",
            bg="white"
        ).place(
            x=22,
            y=18
        )

        tk.Label(
            logo_area,
            text="Student\nAssessment Tracker",
            font=("Segoe UI", 13, "bold"),
            fg="#263451",
            bg="white",
            justify="left"
        ).place(
            x=65,
            y=20
        )

        tk.Frame(
            sidebar,
            height=1,
            bg="#e9edf5"
        ).pack(
            fill="x",
            padx=18
        )

        profile = tk.Frame(
            sidebar,
            bg="white",
            height=105
        )

        profile.pack(fill="x")
        profile.pack_propagate(False)

        tk.Label(
            profile,
            text="S",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#8d8de8",
            width=3,
            height=1
        ).place(
            x=20,
            y=23
        )

        tk.Label(
            profile,
            text="Student",
            font=("Segoe UI", 11, "bold"),
            fg="#263451",
            bg="white"
        ).place(
            x=75,
            y=25
        )

        tk.Label(
            profile,
            text="Manage Your Tasks",
            font=("Segoe UI", 8),
            fg="#8a94a8",
            bg="white"
        ).place(
            x=75,
            y=48
        )

        self.create_nav_button(
            sidebar,
            "▦",
            "Dashboard",
            self.show_dashboard,
            True
        )

        self.create_nav_button(
            sidebar,
            "+",
            "Add Task",
            self.open_add_task
        )

        self.create_nav_button(
            sidebar,
            "☷",
            "View Tasks",
            self.show_tasks
        )

        self.create_nav_button(
            sidebar,
            "✎",
            "Update Task",
            self.update_selected_from_sidebar
        )

        self.create_nav_button(
            sidebar,
            "▣",
            "Delete Task",
            self.delete_selected_from_sidebar
        )

        self.create_nav_button(
            sidebar,
            "✓",
            "Mark Complete",
            self.mark_complete
        )

        self.create_nav_button(
            sidebar,
            "☑",
            "Completed Tasks",
            self.show_completed_tasks
        )

        tk.Frame(
            sidebar,
            height=1,
            bg="#e9edf5"
        ).pack(
            fill="x",
            padx=18,
            pady=15
        )

        self.create_nav_button(
            sidebar,
            "⚙",
            "Settings",
            self.show_settings
        )

        self.create_nav_button(
            sidebar,
            "↪",
            "Exit",
            self.close_application
        )

        bottom_box = tk.Frame(
            sidebar,
            bg="#f0efff",
            height=80
        )

        bottom_box.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )

        bottom_box.pack_propagate(False)

        tk.Label(
            bottom_box,
            text="◷",
            font=("Segoe UI", 22),
            fg="#6666d9",
            bg="#f0efff"
        ).place(
            x=18,
            y=20
        )

        tk.Label(
            bottom_box,
            text="Stay Organized\nAchieve More",
            font=("Segoe UI", 9, "bold"),
            fg="#626aa0",
            bg="#f0efff",
            justify="left"
        ).place(
            x=55,
            y=18
        )

    def create_nav_button(
        self,
        parent,
        icon,
        text,
        command,
        active=False
    ):

        bg_color = "#e9e8ff" if active else "white"
        fg_color = "#5b5bd6" if active else "#52627f"

        frame = tk.Frame(
            parent,
            bg=bg_color,
            height=42
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=2
        )

        frame.pack_propagate(False)

        button = tk.Button(
            frame,
            text=f"{icon}    {text}",
            command=command,
            font=(
                "Segoe UI",
                10,
                "bold" if active else "normal"
            ),
            anchor="w",
            bg=bg_color,
            fg=fg_color,
            activebackground="#e9e8ff",
            activeforeground="#5b5bd6",
            bd=0,
            relief="flat",
            cursor="hand2"
        )

        button.pack(
            fill="both",
            expand=True,
            padx=8
        )

    def create_top_bar(self):

        top = tk.Frame(
            self.main_area,
            bg="#f5f7fb",
            height=80
        )

        top.pack(
            fill="x",
            padx=28
        )

        top.pack_propagate(False)

        title_frame = tk.Frame(
            top,
            bg="#f5f7fb"
        )

        title_frame.pack(
            side="left",
            pady=15
        )

        tk.Label(
            title_frame,
            text="▦",
            font=("Segoe UI", 25, "bold"),
            fg="#5b5bd6",
            bg="#f5f7fb"
        ).pack(
            side="left",
            padx=(0, 12)
        )

        title_text = tk.Frame(
            title_frame,
            bg="#f5f7fb"
        )

        title_text.pack(side="left")

        tk.Label(
            title_text,
            text="Dashboard",
            font=("Segoe UI", 22, "bold"),
            fg="#263451",
            bg="#f5f7fb"
        ).pack(anchor="w")

        tk.Label(
            title_text,
            text="Track your assessment tasks at a glance",
            font=("Segoe UI", 9),
            fg="#8791a6",
            bg="#f5f7fb"
        ).pack(anchor="w")

        date_label = tk.Label(
            top,
            text=datetime.now().strftime("%d/%m/%Y"),
            font=("Segoe UI", 9, "bold"),
            fg="#56627b",
            bg="white",
            padx=15,
            pady=9
        )

        date_label.pack(
            side="right",
            padx=(12, 0),
            pady=20
        )

        search_frame = tk.Frame(
            top,
            bg="white",
            highlightbackground="#e2e6f0",
            highlightthickness=1
        )

        search_frame.pack(
            side="right",
            pady=20
        )

        tk.Label(
            search_frame,
            text="⌕",
            font=("Segoe UI", 17),
            fg="#7c879d",
            bg="white"
        ).pack(
            side="left",
            padx=(10, 4)
        )

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 9),
            width=27,
            bd=0,
            relief="flat"
        )

        search_entry.pack(
            side="left",
            ipady=8,
            padx=(0, 10)
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_tasks()
        )

    def create_summary_cards(self):

        cards_frame = tk.Frame(
            self.main_area,
            bg="#f5f7fb"
        )

        cards_frame.pack(
            fill="x",
            padx=28,
            pady=(0, 20)
        )

        self.total_card = self.create_summary_card(
            cards_frame,
            "TOTAL TASKS",
            "0",
            "All assessment tasks",
            "#4b8de8",
            "▣"
        )

        self.pending_card = self.create_summary_card(
            cards_frame,
            "PENDING",
            "0",
            "Tasks not completed",
            "#e7a22c",
            "◷"
        )

        self.completed_card = self.create_summary_card(
            cards_frame,
            "COMPLETED",
            "0",
            "Finished tasks",
            "#3db68a",
            "✓"
        )

        self.high_card = self.create_summary_card(
            cards_frame,
            "HIGH PRIORITY",
            "0",
            "High priority tasks",
            "#e75c65",
            "!"
        )

    def create_summary_card(
        self,
        parent,
        title,
        value,
        subtitle,
        color,
        icon
    ):

        card = tk.Frame(
            parent,
            bg="white",
            height=120,
            highlightbackground="#e4e8f0",
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 19, "bold"),
            fg=color,
            bg="#f1f3ff",
            width=3
        ).place(
            x=15,
            y=25
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#68748c",
            bg="white"
        ).place(
            x=75,
            y=18
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 22, "bold"),
            fg="#263451",
            bg="white"
        )

        value_label.place(
            x=75,
            y=40
        )

        tk.Label(
            card,
            text=subtitle,
            font=("Segoe UI", 8),
            fg="#98a1b2",
            bg="white"
        ).place(
            x=75,
            y=77
        )

        return value_label

    def create_dashboard_content(self):

        content = tk.Frame(
            self.main_area,
            bg="#f5f7fb"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 20)
        )

        top_content = tk.Frame(
            content,
            bg="#f5f7fb",
            height=270
        )

        top_content.pack(
            fill="x"
        )

        top_content.pack_propagate(False)

        priority_card = tk.Frame(
            top_content,
            bg="white",
            highlightbackground="#e4e8f0",
            highlightthickness=1
        )

        priority_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            priority_card,
            text="▥  Tasks by Priority",
            font=("Segoe UI", 12, "bold"),
            fg="#263451",
            bg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        self.priority_canvas = tk.Canvas(
            priority_card,
            bg="white",
            highlightthickness=0
        )

        self.priority_canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        status_card = tk.Frame(
            top_content,
            bg="white",
            width=360,
            highlightbackground="#e4e8f0",
            highlightthickness=1
        )

        status_card.pack(
            side="right",
            fill="y",
            padx=(8, 0)
        )

        status_card.pack_propagate(False)

        tk.Label(
            status_card,
            text="◔  Task Status",
            font=("Segoe UI", 12, "bold"),
            fg="#263451",
            bg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
        )

        self.status_canvas = tk.Canvas(
            status_card,
            bg="white",
            highlightthickness=0
        )

        self.status_canvas.pack(
            fill="both",
            expand=True
        )

        recent_card = tk.Frame(
            content,
            bg="white",
            highlightbackground="#e4e8f0",
            highlightthickness=1
        )

        recent_card.pack(
            fill="both",
            expand=True,
            pady=(15, 0)
        )

        recent_header = tk.Frame(
            recent_card,
            bg="white",
            height=55
        )

        recent_header.pack(
            fill="x"
        )

        recent_header.pack_propagate(False)

        tk.Label(
            recent_header,
            text="▤  Recent Assessment Tasks",
            font=("Segoe UI", 12, "bold"),
            fg="#263451",
            bg="white"
        ).pack(
            side="left",
            padx=20,
            pady=17
        )

        tk.Button(
            recent_header,
            text="View All →",
            command=self.show_tasks,
            font=("Segoe UI", 8, "bold"),
            fg="#6565d7",
            bg="white",
            bd=0,
            cursor="hand2"
        ).pack(
            side="right",
            padx=20
        )

        table_frame = tk.Frame(
            recent_card,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columns = (
            "ID",
            "Task Name",
            "Priority",
            "Status",
            "Date Added",
            "Actions"
        )

        self.task_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "ID": "ID",
            "Task Name": "Task Name",
            "Priority": "Priority",
            "Status": "Status",
            "Date Added": "Date Added",
            "Actions": "Actions"
        }

        for column in columns:
            self.task_tree.heading(
                column,
                text=headings[column]
            )

        self.task_tree.column(
            "ID",
            width=45,
            anchor="center"
        )

        self.task_tree.column(
            "Task Name",
            width=330,
            anchor="w"
        )

        self.task_tree.column(
            "Priority",
            width=110,
            anchor="center"
        )

        self.task_tree.column(
            "Status",
            width=120,
            anchor="center"
        )

        self.task_tree.column(
            "Date Added",
            width=120,
            anchor="center"
        )

        self.task_tree.column(
            "Actions",
            width=120,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.task_tree.yview
        )

        self.task_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.task_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.task_tree.bind(
            "<Double-1>",
            self.select_task
        )

    def update_priority_chart(self):

        canvas = self.priority_canvas
        canvas.delete("all")

        width = max(
            canvas.winfo_width(),
            500
        )

        height = max(
            canvas.winfo_height(),
            180
        )

        self.cursor.execute("""
            SELECT priority, COUNT(*)
            FROM tasks
            GROUP BY priority
        """)

        data = dict(
            self.cursor.fetchall()
        )

        values = [
            (
                "High",
                data.get("High", 0),
                "#e75c65"
            ),
            (
                "Medium",
                data.get("Medium", 0),
                "#e7a22c"
            ),
            (
                "Low",
                data.get("Low", 0),
                "#3db68a"
            )
        ]

        maximum = max(
            [item[1] for item in values] + [1]
        )

        left = 55
        bottom = height - 35
        chart_height = height - 75
        bar_width = 65

        for i in range(4):

            value = int(
                maximum * i / 3
            )

            y = bottom - (
                chart_height * i / 3
            )

            canvas.create_line(
                left,
                y,
                width - 20,
                y,
                fill="#edf0f6"
            )

            canvas.create_text(
                left - 15,
                y,
                text=str(value),
                fill="#8a94a8",
                font=("Segoe UI", 8)
            )

        positions = [
            left + 70,
            left + 200,
            left + 330
        ]

        for index, item in enumerate(values):

            name, value, color = item

            bar_height = (
                value / maximum
            ) * chart_height

            x = positions[index]

            canvas.create_rectangle(
                x,
                bottom - bar_height,
                x + bar_width,
                bottom,
                fill=color,
                outline=""
            )

            canvas.create_text(
                x + bar_width / 2,
                bottom - bar_height - 10,
                text=str(value),
                fill="#44516d",
                font=("Segoe UI", 9, "bold")
            )

            canvas.create_text(
                x + bar_width / 2,
                bottom + 15,
                text=name,
                fill="#7d879c",
                font=("Segoe UI", 8)
            )

    def update_status_chart(self):

        canvas = self.status_canvas
        canvas.delete("all")

        width = max(
            canvas.winfo_width(),
            350
        )

        height = max(
            canvas.winfo_height(),
            180
        )

        self.cursor.execute("""
            SELECT status, COUNT(*)
            FROM tasks
            GROUP BY status
        """)

        data = dict(
            self.cursor.fetchall()
        )

        completed = data.get(
            "Completed",
            0
        )

        pending = data.get(
            "Pending",
            0
        )

        total = completed + pending

        if total == 0:

            completed_percent = 0
            pending_percent = 0

        else:

            completed_percent = (
                completed / total
            )

            pending_percent = (
                pending / total
            )

        center_x = 105
        center_y = 105
        radius = 60

        canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="#edf0f6",
            outline=""
        )

        if total > 0:

            completed_angle = (
                -360 * completed_percent
            )

            canvas.create_arc(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                start=90,
                extent=completed_angle,
                fill="#3db68a",
                outline=""
            )

            canvas.create_arc(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                start=90 + completed_angle,
                extent=-360 * pending_percent,
                fill="#e7a22c",
                outline=""
            )

        inner_radius = 38

        canvas.create_oval(
            center_x - inner_radius,
            center_y - inner_radius,
            center_x + inner_radius,
            center_y + inner_radius,
            fill="white",
            outline=""
        )

        canvas.create_text(
            center_x,
            center_y - 4,
            text=str(total),
            font=("Segoe UI", 17, "bold"),
            fill="#263451"
        )

        canvas.create_text(
            center_x,
            center_y + 15,
            text="Total",
            font=("Segoe UI", 7),
            fill="#8a94a8"
        )

        legend_x = 195

        canvas.create_oval(
            legend_x,
            65,
            legend_x + 12,
            77,
            fill="#3db68a",
            outline=""
        )

        canvas.create_text(
            legend_x + 20,
            71,
            text=f"Completed   {completed}",
            anchor="w",
            font=("Segoe UI", 9),
            fill="#536078"
        )

        canvas.create_oval(
            legend_x,
            105,
            legend_x + 12,
            117,
            fill="#e7a22c",
            outline=""
        )

        canvas.create_text(
            legend_x + 20,
            111,
            text=f"Pending      {pending}",
            anchor="w",
            font=("Segoe UI", 9),
            fill="#536078"
        )

        canvas.create_text(
            legend_x,
            155,
            text=f"Completion: {completed_percent * 100:.0f}%",
            anchor="w",
            font=("Segoe UI", 9, "bold"),
            fill="#3d9c7a"
        )

    def load_tasks(self):

        if not hasattr(self, "task_tree"):
            return

        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        search = self.search_var.get().strip().lower()

        if search:

            self.cursor.execute("""
                SELECT task_id,
                       task_name,
                       priority,
                       status,
                       date_added
                FROM tasks
                WHERE LOWER(task_name) LIKE ?
                ORDER BY task_id DESC
            """, (
                "%" + search + "%",
            ))

        else:

            self.cursor.execute("""
                SELECT task_id,
                       task_name,
                       priority,
                       status,
                       date_added
                FROM tasks
                ORDER BY task_id DESC
            """)

        tasks = self.cursor.fetchall()

        for task in tasks:

            self.task_tree.insert(
                "",
                "end",
                values=(
                    task[0],
                    task[1],
                    task[2],
                    task[3],
                    task[4],
                    "Edit   ✓   Delete"
                )
            )

        self.update_priority_chart()
        self.update_status_chart()

    def update_dashboard(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM tasks
        """)

        total = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM tasks
            WHERE status = 'Pending'
        """)

        pending = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM tasks
            WHERE status = 'Completed'
        """)

        completed = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM tasks
            WHERE priority = 'High'
        """)

        high = self.cursor.fetchone()[0]

        self.total_card.config(
            text=str(total)
        )

        self.pending_card.config(
            text=str(pending)
        )

        self.completed_card.config(
            text=str(completed)
        )

        self.high_card.config(
            text=str(high)
        )

        self.update_priority_chart()
        self.update_status_chart()

    def add_task(self):

        task_window = tk.Toplevel(
            self.root
        )

        task_window.title(
            "Add Assessment Task"
        )

        task_window.geometry(
            "450x330"
        )

        task_window.configure(
            bg="white"
        )

        task_window.resizable(
            False,
            False
        )

        tk.Label(
            task_window,
            text="Add Assessment Task",
            font=("Segoe UI", 18, "bold"),
            fg="#263451",
            bg="white"
        ).pack(
            pady=(25, 20)
        )

        tk.Label(
            task_window,
            text="Task Name",
            font=("Segoe UI", 10, "bold"),
            fg="#52627f",
            bg="white"
        ).pack(
            anchor="w",
            padx=40
        )

        task_entry = tk.Entry(
            task_window,
            font=("Segoe UI", 11),
            width=38,
            bd=1,
            relief="solid"
        )

        task_entry.pack(
            padx=40,
            pady=(5, 18),
            ipady=8
        )

        tk.Label(
            task_window,
            text="Priority",
            font=("Segoe UI", 10, "bold"),
            fg="#52627f",
            bg="white"
        ).pack(
            anchor="w",
            padx=40
        )

        priority_combo = ttk.Combobox(
            task_window,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            state="readonly",
            font=("Segoe UI", 10),
            width=35
        )

        priority_combo.set("Medium")

        priority_combo.pack(
            padx=40,
            pady=(5, 20),
            ipady=5
        )

        def save():

            task_name = task_entry.get().strip()
            priority = priority_combo.get()

            if not task_name:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter the assessment task name.",
                    parent=task_window
                )

                return

            date_added = datetime.now().strftime(
                "%d/%m/%Y"
            )

            self.cursor.execute("""
                INSERT INTO tasks
                (task_name, priority, status, date_added)
                VALUES (?, ?, ?, ?)
            """, (
                task_name,
                priority,
                "Pending",
                date_added
            ))

            self.connection.commit()

            task_window.destroy()

            self.load_tasks()
            self.update_dashboard()

            messagebox.showinfo(
                "Task Added",
                "Assessment task added successfully."
            )

        tk.Button(
            task_window,
            text="Save Task",
            command=save,
            font=("Segoe UI", 10, "bold"),
            bg="#5b5bd6",
            fg="white",
            activebackground="#4848bc",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack()

        task_entry.focus()

    def open_add_task(self):
        self.add_task()

    def select_task(self, event=None):

        selected = self.task_tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Task Selected",
                "Please select a task first."
            )

            return None

        values = self.task_tree.item(
            selected[0]
        )["values"]

        self.selected_task_id = values[0]

        return values

    def update_selected_from_sidebar(self):

        values = self.select_task()

        if values:
            self.update_task(values)

    def update_task(self, values=None):

        if values is None:
            values = self.select_task()

        if not values:
            return

        task_id = values[0]

        task_window = tk.Toplevel(
            self.root
        )

        task_window.title(
            "Update Assessment Task"
        )

        task_window.geometry(
            "450x330"
        )

        task_window.configure(
            bg="white"
        )

        task_window.resizable(
            False,
            False
        )

        tk.Label(
            task_window,
            text="Update Assessment Task",
            font=("Segoe UI", 18, "bold"),
            fg="#263451",
            bg="white"
        ).pack(
            pady=(25, 20)
        )

        tk.Label(
            task_window,
            text="Task Name",
            font=("Segoe UI", 10, "bold"),
            fg="#52627f",
            bg="white"
        ).pack(
            anchor="w",
            padx=40
        )

        task_entry = tk.Entry(
            task_window,
            font=("Segoe UI", 11),
            width=38,
            bd=1,
            relief="solid"
        )

        task_entry.insert(
            0,
            values[1]
        )

        task_entry.pack(
            padx=40,
            pady=(5, 18),
            ipady=8
        )

        tk.Label(
            task_window,
            text="Priority",
            font=("Segoe UI", 10, "bold"),
            fg="#52627f",
            bg="white"
        ).pack(
            anchor="w",
            padx=40
        )

        priority_combo = ttk.Combobox(
            task_window,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            state="readonly",
            font=("Segoe UI", 10),
            width=35
        )

        priority_combo.set(
            values[2]
        )

        priority_combo.pack(
            padx=40,
            pady=(5, 20),
            ipady=5
        )

        def save_update():

            new_name = task_entry.get().strip()
            new_priority = priority_combo.get()

            if not new_name:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter a task name.",
                    parent=task_window
                )

                return

            self.cursor.execute("""
                UPDATE tasks
                SET task_name = ?,
                    priority = ?
                WHERE task_id = ?
            """, (
                new_name,
                new_priority,
                task_id
            ))

            self.connection.commit()

            task_window.destroy()

            self.load_tasks()
            self.update_dashboard()

            messagebox.showinfo(
                "Task Updated",
                "Assessment task updated successfully."
            )

        tk.Button(
            task_window,
            text="Save Changes",
            command=save_update,
            font=("Segoe UI", 10, "bold"),
            bg="#e0a02c",
            fg="white",
            activebackground="#c8881c",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack()

    def delete_task(self):

        values = self.select_task()

        if not values:
            return

        task_id = values[0]
        task_name = values[1]

        confirm = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete\n\n"
            f"'{task_name}'?"
        )

        if not confirm:
            return

        self.cursor.execute("""
            DELETE FROM tasks
            WHERE task_id = ?
        """, (
            task_id,
        ))

        self.connection.commit()

        self.selected_task_id = None

        self.load_tasks()
        self.update_dashboard()

        messagebox.showinfo(
            "Task Deleted",
            "Assessment task deleted successfully."
        )

    def delete_selected_from_sidebar(self):
        self.delete_task()

    def mark_complete(self):

        values = self.select_task()

        if not values:
            return

        task_id = values[0]
        status = values[3]

        if status == "Completed":

            messagebox.showinfo(
                "Already Completed",
                "This task is already completed."
            )

            return

        self.cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE task_id = ?
        """, (
            "Completed",
            task_id
        ))

        self.connection.commit()

        self.load_tasks()
        self.update_dashboard()

        messagebox.showinfo(
            "Task Completed",
            "Task marked as completed."
        )

    def show_dashboard(self):

        self.search_var.set("")

        self.load_tasks()
        self.update_dashboard()

    def show_tasks(self):

        self.search_var.set("")

        self.load_tasks()

        messagebox.showinfo(
            "View Tasks",
            "All assessment tasks are displayed in the dashboard."
        )

    def show_completed_tasks(self):

        self.search_var.set("")

        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        self.cursor.execute("""
            SELECT task_id,
                   task_name,
                   priority,
                   status,
                   date_added
            FROM tasks
            WHERE status = 'Completed'
            ORDER BY task_id DESC
        """)

        tasks = self.cursor.fetchall()

        for task in tasks:

            self.task_tree.insert(
                "",
                "end",
                values=(
                    task[0],
                    task[1],
                    task[2],
                    task[3],
                    task[4],
                    "Edit   ✓   Delete"
                )
            )

        self.update_priority_chart()
        self.update_status_chart()

    def show_settings(self):

        messagebox.showinfo(
            "Settings",
            "STUDENT ASSESSMENT TRACKER\n\n"
            "Python Tkinter GUI\n"
            "SQLite Database\n\n"
            "The system is designed to help users "
            "organize, prioritize and track "
            "assessment-related tasks."
        )

    def search_tasks(self):

        self.load_tasks()

    def close_application(self):

        confirm = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )

        if confirm:

            self.connection.close()
            self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    application = StudentAssessmentTracker(
        root
    )

    root.mainloop()