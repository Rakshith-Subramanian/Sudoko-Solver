import tkinter as tk
from tkinter import font
import time

WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#FF0000"

sudoku_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.canvas = tk.Canvas(root, width=450, height=500)
        self.canvas.pack()

        self.font = font.Font(family="Helvetica", size=18)

        self.entry_cells = [[None for _ in range(9)] for _ in range(9)]

        self.draw_board(sudoku_board)
        self.draw_solve_button()
        self.draw_reset_button()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_board(self, board):
        for i in range(9):
            for j in range(9):
                x, y = j * 50, i * 50
                if board[i][j] != 0:
                    self.canvas.create_rectangle(x, y, x + 50, y + 50, fill=WHITE)
                    self.canvas.create_text(x + 25, y + 25, text=str(board[i][j]), font=self.font, fill=BLACK)
                    self.draw_solve_button()
                    self.draw_reset_button()
                else:
                    self.entry_cells[i][j] = tk.Entry(self.root, justify="center", font=self.font, width=2)
                    self.canvas.create_window(x + 25, y + 25, window=self.entry_cells[i][j])
                    self.draw_solve_button()
                    self.draw_reset_button()

    def get_user_input(self):
        input_board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if self.entry_cells[i][j] is not None:
                    value = self.entry_cells[i][j].get()
                    input_board[i][j] = int(value) if value.isdigit() else 0
        return input_board

    def draw_solve_button(self):
        self.canvas.create_rectangle(150, 460, 225, 500, fill=WHITE)
        self.canvas.create_text(187.5, 480, text="Solve", font=self.font, fill=BLACK)

    def draw_reset_button(self):
        self.canvas.create_rectangle(225, 460, 300, 500, fill=WHITE, tags="reset_button")
        self.canvas.create_text(262.5, 480, text="Reset", font=self.font, fill=BLACK, tags="reset_button")

    def reset_board(self, event):
        for i in range(9):
            for j in range(9):
                if self.entry_cells[i][j] is not None:
                    self.entry_cells[i][j].delete(0, tk.END)

    def on_canvas_click(self, event):
        start_time = time.time()  # Record the start time
        mouse_pos = (event.x, event.y)
        if 150 <= mouse_pos[0] <= 225 and 460 <= mouse_pos[1] <= 500:
            user_input_board = self.get_user_input()
            solved_board = self.a_star_search(user_input_board)
            if solved_board:
                self.canvas.delete("all")
                self.draw_board(solved_board)
                end_time = time.time()  # Record the end time
                total_time = end_time - start_time
                print(f"Total time taken: {total_time} seconds")
        elif 225 <= mouse_pos[0] <= 300 and 460 <= mouse_pos[1] <= 500:
            self.reset_board(event)

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    def solve_sudoku(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return (row, col)
        return None

    def a_star_search(self, board):
        open_set = [(0, board)]

        while open_set:
            _, current_board = open_set.pop(0)
            empty_cell = self.solve_sudoku(current_board)

            if empty_cell is None:
                return current_board

            row, col = empty_cell

            for num in range(1, 10):
                if self.is_valid(current_board, row, col, num):
                    new_board = [row[:] for row in current_board]
                    new_board[row][col] = num
                    heuristic = sum(row.count(0) for row in new_board)
                    open_set.append((heuristic, new_board))
                    open_set.sort()

        return None
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()
