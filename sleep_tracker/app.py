import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import calendar
from datetime import datetime, date, time, timedelta
import json
import os
import random
import math
import csv
import platform
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = os.path.join(os.path.expanduser("~"), "sleep_tracker_data.json")
GOAL_HOURS = 8.0

QUOTES = [
    "Sleep is the best meditation. - Dalai Lama",
    "A good laugh and a long sleep are the best cures. - Irish Proverb",
    "Your future depends on your dreams, so go to sleep. - Mesut Barazany",
    "Sleep is the golden chain that ties health and our bodies together. - Thomas Dekker",
    "The best bridge between despair and hope is a good night's sleep. - E. Joseph Cossman",
    "Sleep is the most powerful recovery tool available. - Matthew Walker",
    "A well-spent day brings happy sleep. - Leonardo da Vinci",
    "Tired minds don't plan well. Sleep first, plan later. - Walter Reisch",
    "Good sleep is a superpower. Use it.",
    "Consistency builds habit — sleep regular hours.",
    "Protect your sleep like it's a valuable resource.",
    "Sleep well, live well, be well."
]

REMEDIES = [
    "Avoid screens 1 hour before bed — read or listen to soft music.",
    "Warm milk or chamomile tea in the evening.",
    "Practice 5–10 minutes of deep breathing before bed.",
    "Keep your bedroom cool, dark, and quiet.",
    "Avoid heavy meals and caffeine 4–6 hours before bedtime.",
    "Maintain a consistent sleep and wake time.",
    "Light stretching or yoga to release tension.",
    "Use lavender essential oil on pillow or diffuser.",
    "Limit naps to 20-30 minutes earlier in the day.",
    "Dim lights in the evening to support melatonin production.",
    "Use white noise or earplugs if noise is a problem.",
    "Keep electronic devices out of the bedroom."
]

DIET_TIPS = [
    "Eat a small handful of almonds before bed for magnesium.",
    "Have a banana in the evening — provides potassium and magnesium.",
    "Drink chamomile tea 30-60 minutes before bed.",
    "Include kiwi in your evening snack — improves sleep.",
    "Avoid spicy or heavy meals late at night.",
    "Include oats or a small bowl of warm cereal as a light bedtime snack.",
    "Incorporate fatty fish and nuts during the day for better sleep cycles.",
    "Use foods rich in magnesium and calcium throughout the day.",
    "Avoid large amounts of sugar in the evening.",
    "Stay hydrated during the day but limit liquids right before bed.",
    "Reduce alcohol close to bedtime — it fragments sleep.",
    "Try tart cherry juice earlier in the evening for melatonin support."
]

def minutes_to_hm(minutes):
    try:
        minutes = int(minutes)
    except Exception:
        minutes = 0
    h = minutes // 60
    m = minutes % 60
    return f"{int(h)}:{int(m):02d}"

def hm_to_minutes(h, m):
    return int(h) * 60 + int(m)

def parse_time_string(s):
    s = s.strip()
    fmts = ["%H:%M", "%I:%M %p", "%I:%M%p", "%H.%M"]
    for f in fmts:
        try:
            return datetime.strptime(s, f).time()
        except Exception:
            continue
    raise ValueError(f"Time not recognized: {s}")

class Tooltip:
    def __init__(self, widget, text="", delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.id = None
        self.tipwindow = None
        self.widget.bind("<Enter>", self.schedule)
        self.widget.bind("<Leave>", self.hide)
        self.widget.bind("<ButtonPress>", self.hide)
    def schedule(self, event=None):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)
    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)
    def show(self):
        if self.tipwindow:
            return
        x, y, cx, cy = self.widget.bbox("insert") if self.widget.winfo_viewable() else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=4, ipady=2)
    def hide(self, event=None):
        self.unschedule()
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class SleepDataManager:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self.data = {}
        self.load()
    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as fh:
                    self.data = json.load(fh)
            except Exception:
                self.data = {}
        else:
            self.data = {}
            try:
                with open(self.path, "w") as fh:
                    json.dump(self.data, fh)
            except Exception:
                pass
    def save(self):
        try:
            with open(self.path, "w") as fh:
                json.dump(self.data, fh, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Unable to save data: {e}")
    def get(self, iso):
        return self.data.get(iso)
    def ensure(self, iso):
        if iso not in self.data:
            self.data[iso] = {"periods": [], "total_min": 0}
            self.save()
    def add_period(self, iso, start_obj, end_obj, duration_min=None):
        self.ensure(iso)
        if duration_min is None:
            start_dt = datetime.combine(date.fromisoformat(iso), start_obj)
            end_dt = datetime.combine(date.fromisoformat(iso), end_obj)
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
            duration_min = int((end_dt - start_dt).total_seconds() // 60)
        self.data[iso].setdefault("periods", []).append({
            "start": start_obj.strftime("%H:%M") if start_obj else None,
            "end": end_obj.strftime("%H:%M") if end_obj else None,
            "duration_min": int(duration_min)
        })
        self.data[iso]["total_min"] = sum(p.get("duration_min", 0) for p in self.data[iso].get("periods", []))
        self.save()
    def set_total(self, iso, total_min):
        self.ensure(iso)
        self.data[iso].setdefault("periods", []).append({"start": None, "end": None, "duration_min": int(total_min)})
        self.data[iso]["total_min"] = sum(p.get("duration_min", 0) for p in self.data[iso].get("periods", []))
        self.save()
    def set_meta(self, iso, meta):
        self.ensure(iso)
        self.data[iso].update(meta)
        if "total_min" not in self.data[iso]:
            self.data[iso]["total_min"] = sum(p.get("duration_min", 0) for p in self.data[iso].get("periods", []))
        self.save()
    def delete(self, iso):
        if iso in self.data:
            del self.data[iso]
            self.save()
    def entries_range(self, start_date, end_date):
        cur = start_date
        out = {}
        while cur <= end_date:
            iso = cur.isoformat()
            out[iso] = self.data.get(iso, {}).get("total_min", 0)
            cur += timedelta(days=1)
        return out

class SleepTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sleep Tracker — Friendly Edition")
        self.root.geometry("1200x820")
        self.root.minsize(1000, 700)
        self.dm = SleepDataManager()
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        self.selected_iso = now.date().isoformat()
        self.goal = GOAL_HOURS
        self.theme = "light"
        self._make_styles()
        self._build_ui()
        self._draw_calendar()
        self._update_summary()
        self._daily_quote()
        self._apply_startup_animation()

    def _make_styles(self):
        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"))
        self.style.configure("Info.TLabel", font=("Helvetica", 10))
        self.style.configure("Calendar.TButton", font=("Helvetica", 9), padding=6)
        self.style.configure("Bad.TButton", background="#ffdad6")
        self.style.configure("Good.TButton", background="#dff0d8")
        self.style.configure("Primary.TButton", font=("Helvetica", 10, "bold"))
        self.style.configure("Small.TLabel", font=("Helvetica", 9))

    def _build_ui(self):
        self.top_frame = ttk.Frame(self.root, padding=10)
        self.top_frame.pack(fill="x", padx=12, pady=(12, 4))

        title = ttk.Label(self.top_frame, text="Sleep Tracker — Friendly Edition", style="Title.TLabel")
        title.pack(side="left", anchor="w")

        right_controls = ttk.Frame(self.top_frame)
        right_controls.pack(side="right", anchor="e")

        self.theme_btn = ttk.Button(right_controls, text="Switch Theme", command=self._toggle_theme)
        self.theme_btn.pack(side="right", padx=6)
        Tooltip(self.theme_btn, "Toggle light/dark theme")

        export_btn = ttk.Button(right_controls, text="Export JSON", command=self._export_json)
        export_btn.pack(side="right", padx=6)
        Tooltip(export_btn, "Export your sleep data to a JSON file")

        import_btn = ttk.Button(right_controls, text="Import JSON", command=self._import_json)
        import_btn.pack(side="right", padx=6)
        Tooltip(import_btn, "Import sleep data from a JSON file")

        self.quote_frame = ttk.Frame(self.root, padding=(10, 6))
        self.quote_frame.pack(fill="x", padx=12)

        self.quote_label = ttk.Label(self.quote_frame, text="", wraplength=1000, style="Info.TLabel", justify="center")
        self.quote_label.pack(fill="x")

        self.controls_frame = ttk.Frame(self.root, padding=(10, 6))
        self.controls_frame.pack(fill="x", padx=12, pady=(4, 10))

        self.avg_label = ttk.Label(self.controls_frame, text="Avg this month: —", style="Info.TLabel")
        self.avg_label.pack(side="left", padx=(0, 10))

        self.avg_score_label = ttk.Label(self.controls_frame, text="Avg score: —", style="Info.TLabel")
        self.avg_score_label.pack(side="left", padx=(0, 10))

        ttk.Label(self.controls_frame, text=f"Goal: {self.goal} hrs", style="Info.TLabel").pack(side="left", padx=(0, 10))

        nav_frame = ttk.Frame(self.controls_frame)
        nav_frame.pack(side="right", anchor="e")

        prev_btn = ttk.Button(nav_frame, text="◀ Prev", command=self._prev_month)
        prev_btn.grid(row=0, column=0, padx=4)
        Tooltip(prev_btn, "Show previous month")

        self.month_label = ttk.Label(nav_frame, text="", font=("Helvetica", 12, "bold"))
        self.month_label.grid(row=0, column=1, padx=8)

        next_btn = ttk.Button(nav_frame, text="Next ▶", command=self._next_month)
        next_btn.grid(row=0, column=2, padx=4)
        Tooltip(next_btn, "Show next month")

        today_btn = ttk.Button(nav_frame, text="Today", command=self._go_today)
        today_btn.grid(row=0, column=3, padx=4)
        Tooltip(today_btn, "Jump to current month and select today")

        body = ttk.Frame(self.root, padding=(10, 6))
        body.pack(fill="both", expand=True, padx=12)

        left = ttk.Frame(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        cal_header = ttk.Frame(left)
        cal_header.pack(fill="x", pady=(0, 8))

        ttk.Label(cal_header, text="Calendar", font=("Helvetica", 12, "bold")).pack(side="left", anchor="w")

        cal_action_frame = ttk.Frame(cal_header)
        cal_action_frame.pack(side="right")

        add_btn = ttk.Button(cal_action_frame, text="Add Record", command=self._add_record)
        add_btn.pack(side="left", padx=6)
        Tooltip(add_btn, "Add a sleep record for the selected date or today")

        quick_btn = ttk.Button(cal_action_frame, text="Quick Add", command=self._quick_add)
        quick_btn.pack(side="left", padx=6)
        Tooltip(quick_btn, "Quick add total minutes for selected date or today")

        graph_btn = ttk.Button(cal_action_frame, text="Graphs", command=self._graph_options)
        graph_btn.pack(side="left", padx=6)
        Tooltip(graph_btn, "Open graph and analysis options")

        help_btn = ttk.Button(cal_action_frame, text="Help", command=self._show_help)
        help_btn.pack(side="left", padx=6)
        Tooltip(help_btn, "Open help and usage tips")

        calendar_frame = ttk.Frame(left, relief="flat")
        calendar_frame.pack(fill="both", expand=True)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        header = ttk.Frame(calendar_frame)
        header.pack(fill="x")
        for i, d in enumerate(days):
            lbl = ttk.Label(header, text=d, width=12, anchor="center")
            lbl.grid(row=0, column=i, padx=2, pady=2)

        self.calendar_grid = ttk.Frame(calendar_frame)
        self.calendar_grid.pack(fill="both", expand=True)

        self.day_buttons = []
        for r in range(6):
            row = []
            for c in range(7):
                b = ttk.Button(self.calendar_grid, text="", command=lambda rr=r, cc=c: self._on_day_click(rr, cc))
                b.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                row.append(b)
            self.day_buttons.append(row)
        for i in range(6):
            self.calendar_grid.rowconfigure(i, weight=1)
        for i in range(7):
            self.calendar_grid.columnconfigure(i, weight=1)

        right = ttk.Frame(body, width=360)
        right.pack(side="right", fill="y")

        stats_frame = ttk.Frame(right, padding=(6, 6))
        stats_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(stats_frame, text="This Month Stats", font=("Helvetica", 11, "bold")).pack(anchor="w")
        self.total_days_label = ttk.Label(stats_frame, text="Days recorded: 0", style="Info.TLabel")
        self.total_days_label.pack(anchor="w", pady=(4, 0))
        self.best_label = ttk.Label(stats_frame, text="Best sleep: —", style="Info.TLabel")
        self.best_label.pack(anchor="w", pady=(4, 0))
        self.worst_label = ttk.Label(stats_frame, text="Worst sleep: —", style="Info.TLabel")
        self.worst_label.pack(anchor="w", pady=(4, 0))

        streak_frame = ttk.Frame(right, padding=(6, 6))
        streak_frame.pack(fill="x", pady=(8, 8))
        ttk.Label(streak_frame, text="Streak & Badges", font=("Helvetica", 11, "bold")).pack(anchor="w")
        self.streak_label = ttk.Label(streak_frame, text="Current streak: 0 days", style="Info.TLabel")
        self.streak_label.pack(anchor="w", pady=(6, 0))
        self.badge_label = ttk.Label(streak_frame, text="Badge: —", style="Info.TLabel")
        self.badge_label.pack(anchor="w", pady=(6, 0))

        action_frame = ttk.Frame(right, padding=(6, 6))
        action_frame.pack(fill="x", pady=(8, 0))

        export_csv_btn = ttk.Button(action_frame, text="Export CSV", command=self._export_csv)
        export_csv_btn.pack(fill="x", pady=4)
        Tooltip(export_csv_btn, "Export CSV of sleep records")

        import_csv_btn = ttk.Button(action_frame, text="Import CSV", command=self._import_csv)
        import_csv_btn.pack(fill="x", pady=4)
        Tooltip(import_csv_btn, "Import sleep records from a CSV (date,H:M or minutes)")

        spacer = ttk.Frame(right)
        spacer.pack(fill="both", expand=True)

        self.status_bar = ttk.Label(self.root, text="Ready", relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def _apply_startup_animation(self):
        self.status("Welcome! Click 'Add Record' to start tracking sleep.")
        self.root.after(1200, lambda: self.status("Remember: Consistency beats intensity."))

    def status(self, txt):
        try:
            self.status_bar.config(text=txt)
        except Exception:
            pass

    def _toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.root.configure(bg="#222831")
            self.status("Switched to dark theme")
        else:
            self.theme = "light"
            self.root.configure(bg="#f8f9fa")
            self.status("Switched to light theme")

    def _daily_quote(self):
        q = random.choice(QUOTES)
        try:
            self.quote_label.config(text=q)
        except Exception:
            pass
        self.root.after(60_000 * 60 * 12, self._daily_quote)

    def _draw_calendar(self):
        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        today = date.today()
        for r in range(6):
            for c in range(7):
                btn = self.day_buttons[r][c]
                try:
                    d = cal[r][c]
                except Exception:
                    d = 0
                if d == 0:
                    btn.config(text="", state="disabled")
                else:
                    day_date = date(self.current_year, self.current_month, d)
                    iso = day_date.isoformat()
                    entry = self.dm.get(iso)
                    if entry:
                        total_min = entry.get("total_min", 0)
                        hours_val = total_min / 60.0
                        score = entry.get("score", entry.get("quality", 0))
                        display = f"{d}\n{hours_val:.1f}h\n{score}/10"
                        btn.config(text=display, state="normal")
                        if hours_val < self.goal:
                            try:
                                btn.config(style="Bad.TButton")
                            except Exception:
                                btn.config(background="#ffdad6")
                        else:
                            try:
                                btn.config(style="Good.TButton")
                            except Exception:
                                btn.config(background="#dff0d8")
                    else:
                        btn.config(text=str(d), state="normal", style="")
                    if day_date > today:
                        btn.config(state="disabled")
                    if day_date == today:
                        current = btn.cget("text")
                        if "Today" not in current:
                            btn.config(text=current + "\nToday")

    def _on_day_click(self, row, col):
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        try:
            day = cal[row][col]
        except Exception:
            return
        if day == 0:
            return
        selected = date(self.current_year, self.current_month, day)
        if selected > date.today():
            messagebox.showwarning("Future", "Cannot add records for future dates.")
            return
        self.selected_iso = selected.isoformat()
        if self.dm.get(self.selected_iso):
            self._view_entry(self.selected_iso)
        else:
            self._open_entry(self.selected_iso)

    def _add_record(self):
        if not self.selected_iso:
            self.selected_iso = date.today().isoformat()
        if date.fromisoformat(self.selected_iso) > date.today():
            self.selected_iso = date.today().isoformat()
        self._open_entry(self.selected_iso)

    def _open_entry(self, iso_date):
        win = tk.Toplevel(self.root)
        win.title(f"Add / Edit - {iso_date}")
        win.geometry("520x620")
        win.transient(self.root)
        win.grab_set()

        container = ttk.Frame(win, padding=12)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text=f"Sleep record for {iso_date}", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0,8))

        mode = tk.StringVar(value="range")
        rb1 = ttk.Radiobutton(container, text="Use time range (start -> end)", variable=mode, value="range")
        rb1.pack(anchor="w", pady=(4,2))
        times = ttk.Frame(container)
        times.pack(fill="x", pady=4)
        ttk.Label(times, text="Start (HH:MM)").grid(row=0, column=0, padx=6, pady=2)
        start_var = tk.StringVar(value="23:00")
        start_entry = ttk.Entry(times, textvariable=start_var, width=12)
        start_entry.grid(row=0, column=1, padx=6, pady=2)
        ttk.Label(times, text="End (HH:MM)").grid(row=1, column=0, padx=6, pady=2)
        end_var = tk.StringVar(value="07:00")
        end_entry = ttk.Entry(times, textvariable=end_var, width=12)
        end_entry.grid(row=1, column=1, padx=6, pady=2)

        rb2 = ttk.Radiobutton(container, text="Enter duration directly (hours and minutes)", variable=mode, value="duration")
        rb2.pack(anchor="w", pady=(8,2))
        dur_frame = ttk.Frame(container)
        dur_frame.pack(fill="x", pady=4)
        ttk.Label(dur_frame, text="Hours").grid(row=0, column=0, padx=6)
        dur_h = tk.StringVar(value="7")
        spin_h = ttk.Spinbox(dur_frame, from_=0, to=24, width=6, textvariable=dur_h)
        spin_h.grid(row=0, column=1, padx=6)
        ttk.Label(dur_frame, text="Minutes").grid(row=0, column=2, padx=6)
        dur_m = tk.StringVar(value="30")
        spin_m = ttk.Spinbox(dur_frame, from_=0, to=59, width=6, textvariable=dur_m)
        spin_m.grid(row=0, column=3, padx=6)

        ttk.Label(container, text="Sleep quality (1-10)").pack(anchor="w", pady=(10,0))
        quality = tk.IntVar(value=7)
        qscale = ttk.Scale(container, from_=1, to=10, orient="horizontal", variable=quality)
        qscale.pack(fill="x", pady=4)
        qlabel = ttk.Label(container, text=f"{quality.get()}/10")
        qlabel.pack(anchor="w")
        def qtrace(*args):
            qlabel.config(text=f"{int(round(quality.get()))}/10")
        quality.trace_add("write", qtrace)

        ttk.Label(container, text="Number of naps").pack(anchor="w", pady=(10,0))
        naps = tk.IntVar(value=0)
        naps_spin = ttk.Spinbox(container, from_=0, to=10, width=6, textvariable=naps)
        naps_spin.pack(anchor="w", pady=4)

        ttk.Label(container, text="Notes").pack(anchor="w", pady=(10,0))
        notes = tk.Text(container, height=6, width=60)
        notes.pack(fill="x", pady=4)

        existing = self.dm.get(iso_date)
        if existing:
            tm = existing.get("total_min", 0)
            if tm and existing.get("periods"):
                p0 = existing.get("periods")[0]
                if p0.get("start") and p0.get("end"):
                    start_var.set(p0.get("start"))
                    end_var.set(p0.get("end"))
                else:
                    h = tm // 60
                    m = tm % 60
                    dur_h.set(str(h))
                    dur_m.set(str(m))
            meta_q = existing.get("quality")
            if meta_q is not None:
                quality.set(meta_q)
            naps.set(existing.get("naps", 0))
            if existing.get("notes"):
                notes.insert("1.0", existing.get("notes"))

        action_frame = ttk.Frame(container)
        action_frame.pack(fill="x", pady=(8,0))
        def save():
            try:
                if mode.get() == "range":
                    s_txt = start_var.get().strip()
                    e_txt = end_var.get().strip()
                    s_t = parse_time_string(s_txt)
                    e_t = parse_time_string(e_txt)
                    s_dt = datetime.combine(date.fromisoformat(iso_date), s_t)
                    e_dt = datetime.combine(date.fromisoformat(iso_date), e_t)
                    if e_dt <= s_dt:
                        e_dt += timedelta(days=1)
                    total_min = int((e_dt - s_dt).total_seconds() // 60)
                    self.dm.add_period(iso_date, s_t, e_t, duration_min=total_min)
                else:
                    h = int(dur_h.get())
                    m = int(dur_m.get())
                    if h < 0 or m < 0 or m > 59:
                        raise ValueError
                    total_min = h * 60 + m
                    self.dm.set_total(iso_date, total_min)
                qv = int(round(quality.get()))
                naps_v = int(naps.get())
                notes_txt = notes.get("1.0", "end").strip()
                duration_score = min(10, (total_min / (GOAL_HOURS * 60)) * 10) if GOAL_HOURS>0 else 0
                final_score = int(round((duration_score * 0.5) + (qv * 0.5)))
                self.dm.set_meta(iso_date, {"quality": qv, "naps": naps_v, "notes": notes_txt, "score": final_score})
                self._draw_calendar()
                self._update_summary()
                win.destroy()
                if final_score < 6 or (total_min/60.0) < self.goal:
                    remedy = random.choice(REMEDIES)
                    diet = random.choice(DIET_TIPS)
                    messagebox.showinfo("Suggestions", f"Sleep < {self.goal} hrs.\n\nRemedy: {remedy}\n\nDiet tip: {diet}")
                else:
                    messagebox.showinfo("Saved", f"Saved {minutes_to_hm(total_min)} ({final_score}/10) for {iso_date}")
            except ValueError:
                messagebox.showerror("Invalid", "Please enter valid numbers or times.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save: {e}")
        save_btn = ttk.Button(action_frame, text="Save", command=save, style="Primary.TButton")
        save_btn.pack(side="left", padx=6)
        Tooltip(save_btn, "Save record and close")
        ttk.Button(action_frame, text="Cancel", command=win.destroy).pack(side="left", padx=6)

    def _view_entry(self, iso_date):
        ent = self.dm.get(iso_date)
        if not ent:
            self._open_entry(iso_date)
            return
        win = tk.Toplevel(self.root)
        win.title(f"Details - {iso_date}")
        win.geometry("520x420")
        win.transient(self.root)
        win.grab_set()
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text=f"Details for {iso_date}", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0,8))
        txt = ""
        tm = ent.get("total_min", 0)
        txt += f"Total: {minutes_to_hm(tm)}\n"
        sc = ent.get("score", ent.get("quality", 0))
        txt += f"Score: {sc}/10\n"
        txt += f"Quality: {ent.get('quality', '-')}/10\n"
        txt += f"Naps: {ent.get('naps', 0)}\n\n"
        if ent.get("notes"):
            txt += "Notes:\n" + ent.get("notes") + "\n\n"
        if ent.get("periods"):
            txt += "Periods:\n"
            for p in ent.get("periods"):
                st = p.get("start") or "--"
                en = p.get("end") or "--"
                dmin = p.get("duration_min", 0)
                txt += f"{st} -> {en} : {minutes_to_hm(dmin)}\n"
        ttk.Label(frm, text=txt, justify="left").pack(anchor="w")
        bfr = ttk.Frame(frm)
        bfr.pack(fill="x", pady=(10,0))
        ttk.Button(bfr, text="Edit", command=lambda:[win.destroy(), self._open_entry(iso_date)]).pack(side="left", padx=6)
        ttk.Button(bfr, text="Delete", command=lambda:[self.dm.delete(iso_date), self._draw_calendar(), self._update_summary(), win.destroy()]).pack(side="left", padx=6)
        ttk.Button(bfr, text="Close", command=win.destroy).pack(side="right", padx=6)

    def _quick_add(self):
        mins = simpledialog.askinteger("Quick Add", "Enter total sleep minutes for selected date (or today if none):", minvalue=1)
        if mins is None:
            return
        target = self.selected_iso if self.selected_iso else date.today().isoformat()
        if date.fromisoformat(target) > date.today():
            messagebox.showwarning("Future", "Cannot add to future date.")
            return
        self.dm.set_total(target, mins)
        score = min(10, int((mins / (GOAL_HOURS * 60)) * 10)) if GOAL_HOURS>0 else 0
        self.dm.set_meta(target, {"score": int(score)})
        self._draw_calendar()
        self._update_summary()
        messagebox.showinfo("Saved", f"Saved {minutes_to_hm(mins)} for {target}")
        if (mins/60.0) < self.goal:
            remedy = random.choice(REMEDIES)
            diet = random.choice(DIET_TIPS)
            messagebox.showinfo("Suggestion", f"Sleep < {self.goal} hrs\nRemedy: {remedy}\nDiet Tip: {diet}")

    def _prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self._draw_calendar()
        self._update_summary()

    def _next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self._draw_calendar()
        self._update_summary()

    def _go_today(self):
        t = date.today()
        self.current_year = t.year
        self.current_month = t.month
        self.selected_iso = t.isoformat()
        self._draw_calendar()
        self._update_summary()

    def _update_summary(self):
        prefix = f"{self.current_year}-{self.current_month:02d}-"
        total_min = 0
        total_score = 0
        count = 0
        best = (0, "")
        worst = (9999, "")
        streak = 0
        max_streak = 0
        sorted_dates = sorted(self.dm.data.keys())
        for d in sorted_dates:
            v = self.dm.data[d]
            if d.startswith(prefix):
                tm = v.get("total_min", 0)
                total_min += tm
                total_score += v.get("score", v.get("quality", 0))
                count += 1
                if tm > best[0]:
                    best = (tm, d)
                if tm < worst[0]:
                    worst = (tm, d)
        # compute streak (consecutive days >= GOAL_HOURS) ending today
        sorted_local = sorted(self.dm.data.keys())
        streak = 0
        max_streak = 0
        prev_day = None
        for d in sorted_local:
            tm = self.dm.data[d].get("total_min", 0)
            if tm/60.0 >= self.goal:
                if prev_day:
                    dt_prev = date.fromisoformat(prev_day)
                    dt_cur = date.fromisoformat(d)
                    if (dt_cur - dt_prev).days == 1:
                        streak += 1
                    else:
                        streak = 1
                else:
                    streak = 1
                max_streak = max(max_streak, streak)
                prev_day = d
            else:
                prev_day = None
                streak = 0
        if count:
            avg_min = total_min / count
            ah = int(avg_min // 60)
            am = int(avg_min % 60)
            avg_score = round(total_score / count, 1)
            self.avg_label.config(text=f"Avg: {ah}h {am}m")
            self.avg_score_label.config(text=f"Avg score: {avg_score}/10")
            self.total_days_label.config(text=f"Days recorded: {count}")
            if best[1]:
                self.best_label.config(text=f"Best sleep: {minutes_to_hm(best[0])} on {best[1]}")
            else:
                self.best_label.config(text="Best sleep: —")
            if worst[1] and worst[0] < 9999:
                self.worst_label.config(text=f"Worst sleep: {minutes_to_hm(worst[0])} on {worst[1]}")
            else:
                self.worst_label.config(text="Worst sleep: —")
        else:
            self.avg_label.config(text="Avg: No data")
            self.avg_score_label.config(text="Avg score: No data")
            self.total_days_label.config(text="Days recorded: 0")
            self.best_label.config(text="Best sleep: —")
            self.worst_label.config(text="Worst sleep: —")
        # badges
        badge = "No badge"
        if max_streak >= 30:
            badge = "Legendary Sleeper"
        elif max_streak >= 14:
            badge = "Pro Sleeper"
        elif max_streak >= 7:
            badge = "Consistent Sleeper"
        elif max_streak >= 3:
            badge = "On a streak"
        else:
            badge = "Keep going"
        self.streak_label.config(text=f"Best streak: {max_streak} days")
        self.badge_label.config(text=f"Badge: {badge}")

    def _graph_options(self):
        win = tk.Toplevel(self.root)
        win.title("Graph Options")
        win.geometry("320x220")
        win.transient(self.root)
        win.grab_set()
        f = ttk.Frame(win, padding=12)
        f.pack(fill="both", expand=True)
        ttk.Label(f, text="Select graph:", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(0,8))
        ttk.Button(f, text="Weekly (past 7 days)", command=lambda:[win.destroy(), self._weekly_graph()]).pack(fill="x", pady=6)
        ttk.Button(f, text="Monthly (current month)", command=lambda:[win.destroy(), self._monthly_graph()]).pack(fill="x", pady=6)
        ttk.Button(f, text="Score Distribution", command=lambda:[win.destroy(), self._score_distribution()]).pack(fill="x", pady=6)

    def _weekly_graph(self):
        today = date.today()
        start = today - timedelta(days=6)
        days = []
        hours = []
        scores = []
        for i in range(7):
            d = start + timedelta(days=i)
            iso = d.isoformat()
            days.append(d.strftime("%a"))
            ent = self.dm.get(iso)
            if ent:
                hours.append(ent.get("total_min", 0)/60.0)
                scores.append(ent.get("score", ent.get("quality", 0)))
            else:
                hours.append(0)
                scores.append(0)
        fig = Figure(figsize=(9,5))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()
        bars = ax1.bar(days, hours, color="#5DA5FF", alpha=0.8)
        ax2.plot(days, scores, 'o-', color="#24B38F", linewidth=2)
        ax1.set_ylabel("Hours")
        ax2.set_ylabel("Score (0-10)")
        ax1.set_ylim(0, max(12, max(hours)+1))
        ax2.set_ylim(0, 10)
        ax1.set_title("Weekly Sleep (Hours & Scores)")
        for b in bars:
            h = b.get_height()
            if h > 0:
                ax1.text(b.get_x()+b.get_width()/2, h+0.05, f"{h:.1f}", ha="center", va="bottom", fontsize=8)
        win = tk.Toplevel(self.root)
        win.title("Weekly Graph")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _monthly_graph(self):
        days = []
        hours = []
        scores = []
        num_days = calendar.monthrange(self.current_year, self.current_month)[1]
        for d in range(1, num_days+1):
            dd = date(self.current_year, self.current_month, d)
            iso = dd.isoformat()
            days.append(d)
            ent = self.dm.get(iso)
            if ent:
                hours.append(ent.get("total_min", 0)/60.0)
                scores.append(ent.get("score", ent.get("quality", 0)))
            else:
                hours.append(0)
                scores.append(0)
        fig = Figure(figsize=(11,5))
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()
        ax1.plot(days, hours, 'o-', color="#5DA5FF", label="Hours")
        ax2.plot(days, scores, 's-', color="#24B38F", label="Score")
        ax1.set_xlabel("Day")
        ax1.set_ylabel("Hours")
        ax2.set_ylabel("Score")
        ax1.set_ylim(0, max(12, max(hours)+1))
        ax2.set_ylim(0, 10)
        ax1.set_title(f"Monthly Sleep for {calendar.month_name[self.current_month]} {self.current_year}")
        win = tk.Toplevel(self.root)
        win.title("Monthly Graph")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _score_distribution(self):
        counts = {i: 0 for i in range(1, 11)}
        for v in self.dm.data.values():
            s = v.get("score", v.get("quality", 0))
            if isinstance(s, int) and 1 <= s <= 10:
                counts[s] += 1
        labels = [str(k) for k in counts.keys()]
        sizes = [counts[k] for k in counts.keys()]
        fig = Figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Sleep Score Distribution")
        win = tk.Toplevel(self.root)
        win.title("Score Distribution")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _analysis(self):
        total_days = len(self.dm.data)
        if total_days == 0:
            messagebox.showinfo("No Data", "No sleep records to analyze.")
            return
        total_min = 0
        total_score = 0
        best = (-1, "")
        worst = (9999, "")
        for k, v in self.dm.data.items():
            tm = v.get("total_min", 0)
            total_min += tm
            sc = v.get("score", v.get("quality", 0))
            total_score += sc
            if sc > best[0]:
                best = (sc, k)
            if sc < worst[0]:
                worst = (sc, k)
        avg_min = total_min // total_days
        ah = avg_min // 60
        am = avg_min % 60
        avg_score = round(total_score / total_days, 1)
        text = f"Total days: {total_days}\nAverage sleep: {ah}h {am}m\nAverage score: {avg_score}/10\n\nBest: {best[0]}/10 on {best[1]}\nWorst: {worst[0]}/10 on {worst[1]}"
        win = tk.Toplevel(self.root)
        win.title("Analysis")
        win.geometry("480x320")
        ttk.Label(win, text="Sleep Analysis", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        ttk.Label(win, text=text, justify="left").pack(anchor="w", padx=10, pady=10)
        ttk.Button(win, text="Close", command=win.destroy).pack(anchor="e", padx=10, pady=10)

    def _export_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if not path:
            return
        try:
            with open(path, "w") as f:
                json.dump(self.dm.data, f, indent=2)
            messagebox.showinfo("Exported", f"Data exported to {path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def _import_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if not path:
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            if isinstance(data, dict):
                self.dm.data = data
                self.dm.save()
                self._draw_calendar()
                self._update_summary()
                messagebox.showinfo("Imported", "Data imported successfully.")
            else:
                messagebox.showerror("Invalid", "File does not contain valid data.")
        except Exception as e:
            messagebox.showerror("Import Failed", str(e))

    def _export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="") as fh:
                writer = csv.writer(fh)
                writer.writerow(["date", "total_min", "score", "quality", "naps", "notes"])
                for k, v in sorted(self.dm.data.items()):
                    writer.writerow([k, v.get("total_min", 0), v.get("score", ""), v.get("quality", ""), v.get("naps", ""), v.get("notes", "")])
            messagebox.showinfo("Export CSV", f"CSV exported to {path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def _import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if not path:
            return
        try:
            with open(path, "r", newline="") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    iso = row.get("date")
                    if not iso:
                        continue
                    try:
                        total_min = int(row.get("total_min", 0))
                    except Exception:
                        total_min = 0
                    self.dm.set_total(iso, total_min)
                    meta = {}
                    if row.get("score"):
                        try:
                            meta["score"] = int(float(row.get("score")))
                        except Exception:
                            pass
                    if row.get("quality"):
                        try:
                            meta["quality"] = int(float(row.get("quality")))
                        except Exception:
                            pass
                    if row.get("naps"):
                        try:
                            meta["naps"] = int(float(row.get("naps")))
                        except Exception:
                            pass
                    if row.get("notes"):
                        meta["notes"] = row.get("notes")
                    if meta:
                        self.dm.set_meta(iso, meta)
            self._draw_calendar()
            self._update_summary()
            messagebox.showinfo("Imported", "CSV imported successfully.")
        except Exception as e:
            messagebox.showerror("Import Failed", str(e))

    def _show_help(self):
        win = tk.Toplevel(self.root)
        win.title("Help & Tips")
        win.geometry("640x420")
        txt = ("How to use Sleep Tracker — Friendly Edition\n\n"
               "• Click any date on the calendar to add or view sleep records.\n"
               "• You can enter sleep as a time range (e.g. 23:00 - 07:30) or direct duration.\n"
               "• Days with total sleep < goal (8 hrs) are highlighted.\n"
               "• Use Quick Add to enter minutes fast.\n"
               "• Graphs provide weekly/monthly trend and score distribution.\n"
               "• Export/Import available for backup and sharing.\n\n"
               "Tips:\n"
               "• Keep a consistent sleep schedule.\n"
               "• Avoid screens 30-60 minutes before bed.\n"
               "• Try warm herbal tea and light stretching.")
        ttk.Label(win, text=txt, justify="left", wraplength=600).pack(padx=12, pady=12)
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=8)

if __name__ == "__main__":
    root = tk.Tk()
    app = SleepTrackerApp(root)
    root.mainloop()
