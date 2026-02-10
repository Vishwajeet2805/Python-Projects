import pygame
import time
import random
from copy import deepcopy
import sys

# Initialize pygame
pygame.init()

# Get screen info for full screen
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Game Constants
GRID_SIZE = 9
FPS = 60

GRID_AREA_SIZE = min(SCREEN_HEIGHT * 0.6, SCREEN_WIDTH * 0.8)
CELL_SIZE = int(GRID_AREA_SIZE // GRID_SIZE)
GRID_WIDTH = CELL_SIZE * GRID_SIZE

GRID_X = (SCREEN_WIDTH - GRID_WIDTH) // 2

GRID_Y = 80

UI_AREA_Y = GRID_Y + GRID_WIDTH + 30
# Colors (Simplified)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (200, 200, 200)
COLOR_LIGHT_GRAY = (240, 240, 240)
COLOR_GREEN = (0, 180, 0)
COLOR_RED = (220, 0, 0)
COLOR_BLUE = (0, 100, 220)
COLOR_LIGHT_BLUE = (200, 230, 255)
COLOR_ORANGE = (255, 140, 0)
COLOR_PURPLE = (120, 0, 200)
COLOR_BUTTON = (60, 120, 200)
COLOR_BUTTON_HOVER = (80, 140, 220)


class SudokuSolver:
    """Pure Python Sudoku solving utilities"""

    @staticmethod
    def find_empty(board):
        """Find next empty cell (0) in the board"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    @staticmethod
    def is_valid(board, row, col, num):
        """Check if num can be placed at (row, col)"""
        # Check row
        for j in range(9):
            if board[row][j] == num and j != col:
                return False

        # Check column
        for i in range(9):
            if board[i][col] == num and i != row:
                return False

        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num and (box_row + i != row or box_col + j != col):
                    return False

        return True

    @staticmethod
    def solve(board, visualize=False, callback=None):
        """Solve Sudoku using backtracking"""
        empty = SudokuSolver.find_empty(board)
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if SudokuSolver.is_valid(board, row, col, num):
                board[row][col] = num

                if visualize and callback:
                    callback(board, row, col, num, True)

                if SudokuSolver.solve(board, visualize, callback):
                    return True

                board[row][col] = 0

                if visualize and callback:
                    callback(board, row, col, 0, False)

        return False

    @staticmethod
    def generate_full_board():
        """Generate a complete valid Sudoku board"""
        board = [[0 for _ in range(9)] for _ in range(9)]

        # Fill diagonal 3x3 boxes (they are independent)
        for box in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for i in range(3):
                for j in range(3):
                    board[box + i][box + j] = nums.pop()

        # Solve the rest
        SudokuSolver.solve(board)
        return board

    @staticmethod
    def remove_numbers(board, difficulty):
        """Remove numbers based on difficulty"""
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)

        # Define difficulties
        difficulties = {
            'easy': (38, 42),
            'medium': (30, 35),
            'hard': (25, 28)
        }

        cells_to_keep = random.randint(*difficulties.get(difficulty, (30, 35)))
        puzzle = deepcopy(board)

        # Set cells to 0 except for the ones we keep
        cells_to_remove = 81 - cells_to_keep
        for i in range(cells_to_remove):
            row, col = cells[i]
            puzzle[row][col] = 0

        return puzzle


class SudokuCell:
    """Represents a single cell in the Sudoku grid"""

    def __init__(self, row, col, value=0, is_original=False):
        self.row = row
        self.col = col
        self.value = value
        self.is_original = is_original
        self.is_selected = False
        self.is_correct = False
        self.is_incorrect = False
        self.is_hint = False
        self.rect = pygame.Rect(
            GRID_X + col * CELL_SIZE,
            GRID_Y + row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

    def draw(self, screen, font):
        """Draw the cell on screen"""
        # Cell background
        if self.is_selected:
            pygame.draw.rect(screen, COLOR_LIGHT_BLUE, self.rect)
        elif self.is_correct:
            pygame.draw.rect(screen, (220, 255, 220), self.rect)
        elif self.is_incorrect:
            pygame.draw.rect(screen, (255, 220, 220), self.rect)
        elif self.is_hint:
            pygame.draw.rect(screen, (255, 255, 200), self.rect)
        elif self.is_original:
            pygame.draw.rect(screen, COLOR_LIGHT_GRAY, self.rect)

        # Cell border
        border_color = COLOR_BLUE if self.is_selected else COLOR_BLACK
        border_width = 3 if self.is_selected else 1
        pygame.draw.rect(screen, border_color, self.rect, border_width)

        # Draw number if exists
        if self.value != 0:
            if self.is_original:
                color = COLOR_BLACK
                text_font = pygame.font.SysFont('arial', int(CELL_SIZE * 0.6), bold=True)
            elif self.is_correct:
                color = COLOR_GREEN
                text_font = font
            elif self.is_incorrect:
                color = COLOR_RED
                text_font = font
            elif self.is_hint:
                color = COLOR_ORANGE
                text_font = font
            else:
                color = COLOR_BLUE
                text_font = font

            text = text_font.render(str(self.value), True, color)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)


class Button:
    """Clickable button for UI"""

    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.SysFont('arial', int(height * 0.4))

    def draw(self, screen):
        """Draw the button"""
        # Button background
        color = COLOR_BUTTON_HOVER if self.is_hovered else COLOR_BUTTON
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_BLACK, self.rect, 2, border_radius=8)

        # Button text
        text_surface = self.font.render(self.text, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        """Check if mouse is hovering over button"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def check_click(self, pos):
        """Check if button was clicked"""
        if self.rect.collidepoint(pos) and self.action:
            return self.action()
        return None


class SudokuGame:
    """Main Sudoku game class """

    def __init__(self):
        # Initialize full screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Sudoku Game")

        # Game state
        self.running = True
        self.selected_cell = None
        self.wrong_guesses = 0
        self.hints_used = 0
        self.max_hints = 3
        self.difficulty = "medium"
        self.game_start_time = time.time()
        self.game_completed = False

        # Fonts
        self.cell_font = pygame.font.SysFont('arial', int(CELL_SIZE * 0.6))
        self.ui_font = pygame.font.SysFont('arial', 28)
        self.title_font = pygame.font.SysFont('arial', 40, bold=True)
        self.small_font = pygame.font.SysFont('arial', 22)

        # Create UI
        self.create_ui()

        # Generate initial game
        self.new_game()

    def create_ui(self):
        """Create all UI elements - CLEAR SEPARATION"""
        # Button dimensions
        button_width = 120
        button_height = 45
        button_spacing = 15

        # First row of buttons (Game Actions)
        row1_y = UI_AREA_Y + 20
        row1_start_x = (SCREEN_WIDTH - (5 * button_width + 4 * button_spacing)) // 2

        self.action_buttons = [
            Button(row1_start_x, row1_y, button_width, button_height, "Hint", self.use_hint),
            Button(row1_start_x + button_width + button_spacing, row1_y, button_width, button_height, "Check",
                   self.check_board),
            Button(row1_start_x + 2 * (button_width + button_spacing), row1_y, button_width, button_height, "Solve",
                   self.solve_visual),
            Button(row1_start_x + 3 * (button_width + button_spacing), row1_y, button_width, button_height, "Reset",
                   self.reset_board),
            Button(row1_start_x + 4 * (button_width + button_spacing), row1_y, button_width, button_height, "New Game",
                   self.new_game),
        ]

        # Second row (Difficulty buttons)
        row2_y = row1_y + button_height + 25
        diff_button_width = 100
        diff_spacing = 20
        row2_start_x = (SCREEN_WIDTH - (3 * diff_button_width + 2 * diff_spacing)) // 2

        self.difficulty_buttons = [
            Button(row2_start_x, row2_y, diff_button_width, 40, "Easy", lambda: self.set_difficulty("easy")),
            Button(row2_start_x + diff_button_width + diff_spacing, row2_y, diff_button_width, 40, "Medium",
                   lambda: self.set_difficulty("medium")),
            Button(row2_start_x + 2 * (diff_button_width + diff_spacing), row2_y, diff_button_width, 40, "Hard",
                   lambda: self.set_difficulty("hard")),
        ]

        # Stats area (right side)
        self.stats_x = SCREEN_WIDTH - 250
        self.stats_y = UI_AREA_Y + 20

        # Quit button (top right corner)
        self.quit_button = Button(SCREEN_WIDTH - 100, 20, 80, 40, "Quit", self.quit_game)

    def set_difficulty(self, difficulty):
        """Set game difficulty"""
        self.difficulty = difficulty
        self.new_game()
        return True

    def new_game(self):
        """Start a new game with current difficulty"""
        # Generate a complete board
        full_board = SudokuSolver.generate_full_board()

        # Remove numbers based on difficulty
        self.puzzle = SudokuSolver.remove_numbers(full_board, self.difficulty)

        # Store solution
        self.solution = deepcopy(full_board)

        # Create cell objects
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.puzzle[i][j]
                is_original = value != 0
                cell = SudokuCell(i, j, value, is_original)
                row.append(cell)
            self.cells.append(row)

        # Reset game state
        self.selected_cell = None
        self.wrong_guesses = 0
        self.hints_used = 0
        self.game_start_time = time.time()
        self.game_completed = False

        return True

    def reset_board(self):
        """Reset board to initial puzzle state"""
        for i in range(9):
            for j in range(9):
                original_value = self.puzzle[i][j]
                self.cells[i][j].value = original_value
                self.cells[i][j].is_original = original_value != 0
                self.cells[i][j].is_correct = False
                self.cells[i][j].is_incorrect = False
                self.cells[i][j].is_hint = False

        self.selected_cell = None
        self.wrong_guesses = 0
        self.hints_used = 0
        self.game_completed = False

        return True

    def select_cell(self, row, col):
        """Select a cell and deselect others"""
        # Deselect all cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].is_selected = False

        # Select new cell if it's not an original clue
        if not self.cells[row][col].is_original:
            self.cells[row][col].is_selected = True
            self.selected_cell = (row, col)
        else:
            self.selected_cell = None

    def handle_click(self, pos):
        """Handle mouse click"""
        # Check if click is in grid
        if (GRID_X <= pos[0] < GRID_X + GRID_WIDTH and
                GRID_Y <= pos[1] < GRID_Y + GRID_WIDTH):
            row = (pos[1] - GRID_Y) // CELL_SIZE
            col = (pos[0] - GRID_X) // CELL_SIZE
            if 0 <= row < 9 and 0 <= col < 9:
                self.select_cell(row, col)

        # Check action buttons
        for button in self.action_buttons:
            if button.check_click(pos):
                return

        # Check difficulty buttons
        for button in self.difficulty_buttons:
            if button.check_click(pos):
                return

        # Check quit button
        if self.quit_button.check_click(pos):
            return

    def handle_keypress(self, key):
        """Handle keyboard input"""
        if not self.selected_cell or self.game_completed:
            return

        row, col = self.selected_cell
        cell = self.cells[row][col]

        # Number keys 1-9
        if pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            self.enter_number(row, col, num)

        # Numpad keys
        elif pygame.K_KP1 <= key <= pygame.K_KP9:
            num = key - pygame.K_KP0
            self.enter_number(row, col, num)

        # Arrow keys for navigation
        elif key == pygame.K_UP and row > 0:
            self.select_cell(row - 1, col)
        elif key == pygame.K_DOWN and row < 8:
            self.select_cell(row + 1, col)
        elif key == pygame.K_LEFT and col > 0:
            self.select_cell(row, col - 1)
        elif key == pygame.K_RIGHT and col < 8:
            self.select_cell(row, col + 1)

        # Clear cell
        elif key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0, pygame.K_KP0):
            if not cell.is_original:
                cell.value = 0
                cell.is_correct = False
                cell.is_incorrect = False

        # Quick actions
        elif key == pygame.K_h:
            self.use_hint()
        elif key == pygame.K_n:
            self.new_game()
        elif key == pygame.K_r:
            self.reset_board()
        elif key == pygame.K_s:
            self.solve_visual()
        elif key == pygame.K_c:
            self.check_board()

        # Escape to quit
        elif key == pygame.K_ESCAPE:
            self.running = False

    def enter_number(self, row, col, num):
        """Enter a number in the selected cell"""
        cell = self.cells[row][col]

        if cell.is_original:
            return

        cell.value = num
        cell.is_hint = False

        # Check if correct
        if num == self.solution[row][col]:
            cell.is_correct = True
            cell.is_incorrect = False
        else:
            cell.is_correct = False
            cell.is_incorrect = True
            self.wrong_guesses += 1

        # Check if puzzle is complete
        self.check_completion()

    def use_hint(self):
        """Use a hint to reveal a correct number"""
        if self.hints_used >= self.max_hints:
            return False

        # Find empty cells
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0 and not self.cells[i][j].is_original:
                    empty_cells.append((i, j))

        if not empty_cells:
            return False

        # Pick a random empty cell and reveal solution
        row, col = random.choice(empty_cells)
        self.cells[row][col].value = self.solution[row][col]
        self.cells[row][col].is_correct = True
        self.cells[row][col].is_hint = True
        self.cells[row][col].is_incorrect = False

        self.hints_used += 1

        # Deselect if hint was used on selected cell
        if self.selected_cell == (row, col):
            self.selected_cell = None
            self.cells[row][col].is_selected = False

        # Check completion
        self.check_completion()

        return True

    def check_board(self):
        """Check the entire board for errors"""
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                if cell.value != 0:
                    if cell.value == self.solution[i][j]:
                        cell.is_correct = True
                        cell.is_incorrect = False
                    else:
                        cell.is_correct = False
                        cell.is_incorrect = True

        self.check_completion()
        return True

    def check_completion(self):
        """Check if puzzle is complete and correct"""
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value != self.solution[i][j]:
                    return False

        # Puzzle is complete!
        self.game_completed = True
        return True

    def solve_visual(self):
        """Solve the puzzle with visualization"""
        # Create a copy of current state
        current_state = [[self.cells[i][j].value for j in range(9)] for i in range(9)]

        def visualization_callback(board, row, col, num, is_placing):
            """Callback for visualization during solving"""
            # Update display
            self.cells[row][col].value = num
            if is_placing:
                self.cells[row][col].is_correct = True
                self.cells[row][col].is_incorrect = False
            else:
                self.cells[row][col].is_correct = False
                self.cells[row][col].is_incorrect = True

            # Redraw
            self.draw()
            pygame.display.flip()

            # Small delay for visualization
            pygame.time.delay(30)

        # Solve with visualization
        SudokuSolver.solve(current_state, True, visualization_callback)

        # Update cells with solution
        for i in range(9):
            for j in range(9):
                self.cells[i][j].value = current_state[i][j]
                self.cells[i][j].is_correct = True
                self.cells[i][j].is_incorrect = False

        self.game_completed = True
        return True

    def quit_game(self):
        """Quit the game"""
        self.running = False
        return True

    def draw_grid(self):
        """Draw the Sudoku grid lines"""
        # Draw thicker lines for 3x3 boxes
        for i in range(0, GRID_SIZE + 1):
            # Vertical lines
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(
                self.screen,
                COLOR_BLACK,
                (GRID_X + i * CELL_SIZE, GRID_Y),
                (GRID_X + i * CELL_SIZE, GRID_Y + GRID_WIDTH),
                thickness
            )

            # Horizontal lines
            pygame.draw.line(
                self.screen,
                COLOR_BLACK,
                (GRID_X, GRID_Y + i * CELL_SIZE),
                (GRID_X + GRID_WIDTH, GRID_Y + i * CELL_SIZE),
                thickness
            )

        # Draw outer border
        pygame.draw.rect(
            self.screen,
            COLOR_BLACK,
            (GRID_X, GRID_Y, GRID_WIDTH, GRID_WIDTH),
            3
        )

    def draw_header(self):
        """Draw game header with title"""
        # Title background
        pygame.draw.rect(self.screen, COLOR_LIGHT_GRAY, (0, 0, SCREEN_WIDTH, 70))

        # Title
        title = self.title_font.render("SUDOKU GAME", True, COLOR_PURPLE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 15))

        # Current difficulty
        diff_text = self.ui_font.render(f"Difficulty: {self.difficulty.upper()}", True, COLOR_BLACK)
        self.screen.blit(diff_text, (SCREEN_WIDTH // 2 - diff_text.get_width() // 2, 50))

        # Draw quit button
        self.quit_button.draw(self.screen)

    def draw_stats(self):
        """Draw game statistics"""
        # Stats background
        stats_bg = pygame.Rect(self.stats_x - 10, self.stats_y - 10, 240, 110)
        pygame.draw.rect(self.screen, COLOR_LIGHT_GRAY, stats_bg, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_GRAY, stats_bg, 2, border_radius=10)

        # Timer
        elapsed = int(time.time() - self.game_start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        timer_text = self.ui_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, COLOR_BLACK)
        self.screen.blit(timer_text, (self.stats_x, self.stats_y))

        # Wrong guesses
        wrong_color = COLOR_RED if self.wrong_guesses > 0 else COLOR_BLACK
        wrong_text = self.ui_font.render(f"Wrong: {self.wrong_guesses}", True, wrong_color)
        self.screen.blit(wrong_text, (self.stats_x, self.stats_y + 35))

        # Hints used
        hints_color = COLOR_ORANGE if self.hints_used > 0 else COLOR_BLACK
        hints_text = self.ui_font.render(f"Hints: {self.hints_used}/{self.max_hints}", True, hints_color)
        self.screen.blit(hints_text, (self.stats_x, self.stats_y + 70))

    def draw_ui_area(self):
        """Draw the UI area below the grid"""
        # Draw a separator line
        pygame.draw.line(self.screen, COLOR_GRAY, (50, UI_AREA_Y - 10), (SCREEN_WIDTH - 50, UI_AREA_Y - 10), 2)

        # Draw action buttons
        for button in self.action_buttons:
            button.draw(self.screen)

        # Draw difficulty label
        diff_label = self.ui_font.render("Select Difficulty:", True, COLOR_BLACK)
        diff_label_x = self.difficulty_buttons[1].rect.centerx - diff_label.get_width() // 2
        self.screen.blit(diff_label, (diff_label_x, self.difficulty_buttons[0].rect.y - 30))

        # Draw difficulty buttons with highlight
        for button in self.difficulty_buttons:
            # Highlight current difficulty
            if self.difficulty in button.text.lower():
                pygame.draw.rect(self.screen, COLOR_GREEN, button.rect, 3, border_radius=8)
            button.draw(self.screen)

        # Draw stats
        self.draw_stats()

        # Draw controls info at bottom
        controls_text = self.small_font.render(
            "CONTROLS: 1-9 to enter | Arrow keys to move | Backspace/Del to clear | H:Hint C:Check S:Solve R:Reset N:New Game ESC:Quit",
            True, COLOR_GRAY
        )
        self.screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 40))

    def draw_completion_message(self):
        """Draw completion message when puzzle is solved"""
        if not self.game_completed:
            return

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Message box
        message_width = 500
        message_height = 300
        message_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - message_width // 2,
            SCREEN_HEIGHT // 2 - message_height // 2,
            message_width,
            message_height
        )
        pygame.draw.rect(self.screen, COLOR_WHITE, message_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLOR_GREEN, message_rect, 4, border_radius=15)

        # Message text
        message_font = pygame.font.SysFont('arial', 48, bold=True)
        congrats_text = message_font.render("PUZZLE SOLVED!", True, COLOR_GREEN)
        self.screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - 100))

        # Stats
        stats_font = pygame.font.SysFont('arial', 32)
        elapsed = int(time.time() - self.game_start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        stats = [
            f"Time: {minutes:02d}:{seconds:02d}",
            f"Wrong guesses: {self.wrong_guesses}",
            f"Hints used: {self.hints_used}"
        ]

        for i, stat in enumerate(stats):
            stat_text = stats_font.render(stat, True, COLOR_BLACK)
            self.screen.blit(stat_text, (SCREEN_WIDTH // 2 - stat_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - 30 + i * 40))

        # Continue message
        continue_font = pygame.font.SysFont('arial', 24)
        continue_text = continue_font.render("Press any key or click to start new game...", True, COLOR_GRAY)
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + 100))

    def draw(self):
        """Draw everything on screen"""
        # Clear screen
        self.screen.fill(COLOR_WHITE)

        # Draw header
        self.draw_header()

        # Draw cells
        for row in self.cells:
            for cell in row:
                cell.draw(self.screen, self.cell_font)

        # Draw grid lines
        self.draw_grid()

        # Draw UI area (buttons, stats, controls)
        self.draw_ui_area()

        # Draw completion message if game is complete
        if self.game_completed:
            self.draw_completion_message()

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()

        # Show initial screen
        self.draw()
        pygame.display.flip()

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif self.game_completed:
                        self.new_game()
                    else:
                        self.handle_keypress(event.key)

            mouse_pos = pygame.mouse.get_pos()
            for button in self.action_buttons:
                button.check_hover(mouse_pos)
            for button in self.difficulty_buttons:
                button.check_hover(mouse_pos)
            self.quit_button.check_hover(mouse_pos)

            # Draw everything
            self.draw()

            # Update display
            pygame.display.flip()

            # Cap frame rate
            clock.tick(FPS)

        # Quit pygame
        pygame.quit()
        sys.exit()


def main():
    print("=" * 60)
    print("SUDOKU GAME - CLEAN FULL SCREEN VERSION")
    print("=" * 60)
    print("\nStarting game in full screen mode...")
    print("Press ESC at any time to quit.")

    # Create and run game
    game = SudokuGame()
    game.run()


if __name__ == "__main__":
    main()