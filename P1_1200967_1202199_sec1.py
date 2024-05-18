#ziad jalal masalma
#1202199
#sec 1
import tkinter as tk
from PIL import Image, ImageTk
from collections import deque


class MissionariesCannibals:
    def __init__(self):
        self.state = (3, 3, 1, 0, 0)  # Initial state: (missionaries on the left, cannibals on the left, boat position)
        self.solution_bfs = None
        self.solution_dfs = None

    def is_valid_state(self, state):
        m1, c1, b, m2, c2 = state
        return (
                0 <= m1 <= 3 and 0 <= c1 <= 3 and 0 <= m2 <= 3 and 0 <= c2 <= 3 and
                ((m1 == 0 or m1 >= c1) and (m2 == 0 or m2 >= c2)) and
                (b == 0 or b == 1)
        )

    def generate_next_states(self, state):
        m1, c1, b, m2, c2 = state
        possible_moves = [
            (1, 0),  # Move 1 Missionary Right
            (2, 0),  # Move 2 Missionaries Right
            (0, 1),  # Move 1 Cannibal Right
            (0, 2),  # Move 2 Cannibals Right
            (1, 1)  # Move 1 Missionary and 1 Cannibal Right
        ]

        next_states = []

        for dm, dc in possible_moves:
            if b == 1:
                new_state = (m1 - dm, c1 - dc, 0, m2 + dm, c2 + dc)
            else:
                new_state = (m1 + dm, c1 + dc, 1, m2 - dm, c2 - dc)

            if self.is_valid_state(new_state):
                next_states.append(new_state)

        return next_states

    def bfs(self):
        queue = deque([(self.state, [])])
        visited = set()

        while queue:
            current_state, path = queue.popleft()
            if current_state not in visited:
                visited.add(current_state)
                if current_state == (0, 0, 0, 3, 3):
                    self.solution_bfs = path
                    break
                for next_state in self.generate_next_states(current_state):
                    queue.append((next_state, path + [next_state]))

    def dfs(self):
        stack = [(self.state, [])]
        visited = set()

        while stack:
            current_state, path = stack.pop()
            if current_state not in visited:
                visited.add(current_state)
                if current_state == (0, 0, 0, 3, 3):
                    self.solution_dfs = path
                    break
                for next_state in self.generate_next_states(current_state):
                    stack.append((next_state, path + [next_state]))


class MissionariesCannibalsGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Missionaries and Cannibals")

        self.canvas = tk.Canvas(window, width=1000, height=600, bg="lightblue")
        self.canvas.pack()

        # Load images and create Tkinter ImageTk objects
        self.background_image = ImageTk.PhotoImage(Image.open('Img/background.png'))
        self.cannibal_image = ImageTk.PhotoImage(Image.open('Img/Cannibal.png').resize((int(112), int(112))))
        self.man_image = ImageTk.PhotoImage(Image.open('Img/man.png').resize((int(120), int(120))))
        self.boat_image = ImageTk.PhotoImage(Image.open('Img/boat.png').resize((int(190), int(190))))

        # Create buttons
        self.button_reset = tk.Button(window, text='Reset', width=20, height=2, bd='2', command=self.restart_game)
        self.button_reset.place(x=100, y=150)

        self.button_BFS = tk.Button(window, text='BFS', width=20, height=2, bd='2', command=self.solve_with_bfs)
        self.button_BFS.place(x=100, y=100)

        self.button_DFS = tk.Button(window, text='DFS', width=20, height=2, bd='2', command=self.solve_with_dfs)
        self.button_DFS.place(x=100, y=50)

        # Create a Text widget for displaying the solution steps
        self.text_box = tk.Text(window, width=40, height=13, wrap=tk.WORD)
        self.text_box.place(x=500, y=10)

        # Initialize problem solver and update GUI with the initial state
        self.problem_solver = MissionariesCannibals()
        self.update_gui(self.problem_solver.state)

    def restart_game(self):
        self.problem_solver = MissionariesCannibals()
        self.update_gui(self.problem_solver.state)
        self.text_box.delete(1.0, tk.END)  # Clear text box

    def solve_with_bfs(self):
        self.problem_solver.bfs()
        self.display_solution("BFS", self.problem_solver.solution_bfs)

    def solve_with_dfs(self):
        self.problem_solver.dfs()
        self.display_solution("DFS", self.problem_solver.solution_dfs)

    def update_gui(self, state):
        # Clear the canvas before updating with the new state
        self.canvas.delete("all")

        m1, c1, b, m2, c2 = state
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        # Update positions for missionaries on the left
        for i in range(m1):
            x = 50
            y = 250 + i * 120
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.man_image)

        # Update positions for cannibals on the left
        for i in range(c1):
            x = 200
            y = 250 + i * 120
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.cannibal_image)

        # Update positions for missionaries on the right
        for i in range(m2):
            x = 800
            y = 250 + i * 120
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.man_image)

        # Update positions for cannibals on the right
        for i in range(c2):
            x = 650
            y = 250 + i * 120
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.cannibal_image)

        # Update position for the boat
        boat_x = 500 if b == 0 else 300
        self.canvas.create_image(boat_x, 300, anchor=tk.NW, image=self.boat_image)

        self.window.update()

    def display_solution(self, algorithm, solution):
        if solution:
            self.text_box.insert(tk.END, f"Solution using {algorithm}: {len(solution) + 1} steps\n")
            self.text_box.insert(tk.END, f"Step 1: {self.problem_solver.state}\n")
            for i, step in enumerate(solution):
                self.text_box.insert(tk.END, f"Step {i + 2}: {step}\n")
                self.update_gui(step)
                self.window.update()
                self.window.after(1000)
        else:

            self.text_box.insert(tk.END, f"No solution found using {algorithm}\n")


if __name__ == "__main__":
    window = tk.Tk()
    missionaries_cannibals_gui = MissionariesCannibalsGUI(window)
    window.mainloop()