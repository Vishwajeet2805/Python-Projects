import tkinter as tk
from tkinter import messagebox, simpledialog


# =========================
# MODEL — Game Logic
# =========================
class HanoiModel:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.pegs = {"A": list(range(num_disks, 0, -1)), "B": [], "C": []}
        self.move_count = 0
        self.ideal_moves = 2 ** num_disks - 1

    def is_valid_move(self, from_peg, to_peg):
        if not self.pegs[from_peg]:
            return False
        moving_disk = self.pegs[from_peg][-1]
        if not self.pegs[to_peg]:
            return True
        return moving_disk < self.pegs[to_peg][-1]

    def move_disk(self, from_peg, to_peg):
        if self.is_valid_move(from_peg, to_peg):
            disk = self.pegs[from_peg].pop()
            self.pegs[to_peg].append(disk)
            self.move_count += 1
            return True
        return False

    def is_game_won(self):
        return len(self.pegs["C"]) == self.num_disks


# =========================
# VIEW — GUI Display
# =========================
class HanoiView:
    def __init__(self, root, num_disks, presenter):
        self.root = root
        self.presenter = presenter
        self.num_disks = num_disks

        # Create canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg="lightblue")
        self.canvas.pack()

        # Peg positions and dimensions
        self.pegs_x = {"A": 150, "B": 300, "C": 450}
        self.peg_width = 10
        self.peg_height = 180
        self.base_y = 350
        self.disk_height = 20

        self.disk_objects = {}
        self.selected_disk = None
        self.drag_data = {"x": 0, "y": 0, "peg": None}

        # Draw initial pegs and disks
        self.draw_pegs()
        self.draw_disks(self.presenter.model.pegs)

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Frame for move counters
        self.stats_frame = tk.Frame(root)
        self.stats_frame.pack(pady=5)

        # Move count labels
        self.user_move_label = tk.Label(self.stats_frame, text="Your Moves: 0", font=("Arial", 12))
        self.user_move_label.pack(side=tk.LEFT, padx=10)

        self.ideal_move_label = tk.Label(self.stats_frame, text=f"Ideal Moves: {self.presenter.model.ideal_moves}",
                                         font=("Arial", 12))
        self.ideal_move_label.pack(side=tk.LEFT, padx=10)

        self.efficiency_label = tk.Label(self.stats_frame, text="Efficiency: 0%", font=("Arial", 12))
        self.efficiency_label.pack(side=tk.LEFT, padx=10)

    def draw_pegs(self):
        """Draws three pegs"""
        for peg, x in self.pegs_x.items():
            self.canvas.create_rectangle(
                x - self.peg_width / 2,
                self.base_y,
                x + self.peg_width / 2,
                self.base_y - self.peg_height,
                fill="brown"
            )
        # Base platform
        self.canvas.create_rectangle(50, self.base_y, 550, self.base_y + 10, fill="brown")

    def draw_disks(self, pegs):
        """Draw all disks based on peg data (largest at bottom)"""
        self.canvas.delete("disk")
        self.disk_objects.clear()
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]

        for peg, disks in pegs.items():
            x_center = self.pegs_x[peg]
            # Draw from bottom to top - no need to reverse the list
            for level, disk in enumerate(disks):
                y_bottom = self.base_y - level * self.disk_height
                y_top = y_bottom - self.disk_height
                width = 40 + disk * 20
                color = colors[(disk - 1) % len(colors)]
                obj = self.canvas.create_rectangle(
                    x_center - width // 2,
                    y_top,
                    x_center + width // 2,
                    y_bottom,
                    fill=color,
                    tags="disk"
                )
                self.disk_objects[obj] = (peg, disk)

    def on_click(self, event):
        """When user clicks a disk"""
        clicked = self.canvas.find_closest(event.x, event.y)
        if clicked and clicked[0] in self.disk_objects:
            peg, disk = self.disk_objects[clicked[0]]
            if self.presenter.is_top_disk(peg, disk):
                self.selected_disk = clicked[0]
                self.drag_data = {"x": event.x, "y": event.y, "peg": peg}

    def on_drag(self, event):
        """Drag disk"""
        if self.selected_disk:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(self.selected_disk, dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_release(self, event):
        """When mouse is released — attempt to drop"""
        if self.selected_disk:
            target_peg = self.get_nearest_peg(event.x)
            from_peg = self.drag_data["peg"]
            self.presenter.handle_move(from_peg, target_peg)
            # Snap disks visually to correct stack
            self.presenter.refresh_view()
            self.selected_disk = None
            self.drag_data = {"x": 0, "y": 0, "peg": None}

    def get_nearest_peg(self, x):
        """Find which peg is nearest to drop"""
        distances = {peg: abs(self.pegs_x[peg] - x) for peg in self.pegs_x}
        return min(distances, key=distances.get)

    def update_display(self, pegs, move_count):
        self.draw_disks(pegs)
        self.user_move_label.config(text=f"Your Moves: {move_count}")

        # Calculate and update efficiency
        efficiency = 0
        if move_count > 0:
            efficiency = min(100, int((self.presenter.model.ideal_moves / move_count) * 100))
        self.efficiency_label.config(text=f"Efficiency: {efficiency}%")

    def show_message(self, msg):
        messagebox.showinfo("Tower of Hanoi", msg)


# =========================
# PRESENTER — Logic Controller
# =========================
class HanoiPresenter:
    def __init__(self, root, num_disks):
        self.model = HanoiModel(num_disks)
        self.view = HanoiView(root, num_disks, self)

    def is_top_disk(self, peg, disk):
        return self.model.pegs[peg] and self.model.pegs[peg][-1] == disk

    def handle_move(self, from_peg, to_peg):
        if from_peg == to_peg:
            return False
        moved = self.model.move_disk(from_peg, to_peg)
        self.refresh_view()
        if self.model.is_game_won():
            efficiency = min(100, int((self.model.ideal_moves / self.model.move_count) * 100))
            message = f" You Won!\n\n"
            message += f"Your Moves: {self.model.move_count}\n"
            message += f"Ideal Minimum: {self.model.ideal_moves}\n"
            message += f"Efficiency: {efficiency}%\n\n"

            if self.model.move_count == self.model.ideal_moves:
                message += "Perfect! You solved it in the minimum number of moves! "
            elif self.model.move_count <= self.model.ideal_moves * 1.2:
                message += "Excellent! Very close to the ideal solution! "
            elif self.model.move_count <= self.model.ideal_moves * 1.5:
                message += "Good job! You solved it efficiently! "
            else:
                message += "You solved it! Try to use fewer moves next time. "

            self.view.show_message(message)
        return moved

    def refresh_view(self):
        self.view.update_display(self.model.pegs, self.model.move_count)


# =========================
# MAIN APP
# =========================
def main():
    # Create hidden root for single popup
    hidden_root = tk.Tk()
    hidden_root.withdraw()  # Hide main window during input
    num_disks = simpledialog.askinteger("Tower of Hanoi", "Enter number of disks (3-8):",
                                        minvalue=3, maxvalue=8, initialvalue=0)
    hidden_root.destroy()

    if not num_disks:
        return

    # Now create visible game window
    root = tk.Tk()
    root.title("Tower of Hanoi (Drag & Drop GUI)")
    root.resizable(False, False)
    HanoiPresenter(root, num_disks)
    root.mainloop()


if __name__ == "__main__":
    main()