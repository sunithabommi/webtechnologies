import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.width = 500
        self.height = 400
        self.cell_size = 20
        self.direction = 'Right'
        self.score = 0

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.game_running = True

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()

        self.root.bind('<Left>', self.change_direction)
        self.root.bind('<Right>', self.change_direction)
        self.root.bind('<Up>', self.change_direction)
        self.root.bind('<Down>', self.change_direction)

        self.draw_elements()
        self.perform_actions()

    def set_new_food_position(self):
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            if (x, y) not in self.snake_positions:
                return (x, y)

    def change_direction(self, event):
        new_direction = event.keysym
        all_directions = ('Up', 'Down', 'Left', 'Right')
        opposites = ({'Up', 'Down'}, {'Left', 'Right'})

        if new_direction in all_directions:
            # Prevent snake from reversing
            if {new_direction, self.direction} not in opposites:
                self.direction = new_direction

    def perform_actions(self):
        if self.game_running:
            self.move_snake()
            self.check_collisions()
            self.check_food_collision()
            self.draw_elements()
            self.root.after(100, self.perform_actions)
        else:
            self.game_over()

    def move_snake(self):
        head_x, head_y = self.snake_positions[0]

        if self.direction == 'Left':
            new_head = (head_x - self.cell_size, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + self.cell_size, head_y)
        elif self.direction == 'Up':
            new_head = (head_x, head_y - self.cell_size)
        else:  # Down
            new_head = (head_x, head_y + self.cell_size)

        self.snake_positions = [new_head] + self.snake_positions[:-1]

    def check_collisions(self):
        head_x, head_y = self.snake_positions[0]

        # Check wall collision
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            self.game_running = False

        # Check self collision
        if self.snake_positions[0] in self.snake_positions[1:]:
            self.game_running = False

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.snake_positions.append(self.snake_positions[-1])  # Grow snake
            self.food_position = self.set_new_food_position()

    def draw_elements(self):
        self.canvas.delete(tk.ALL)

        # Draw food
        x, y = self.food_position
        self.canvas.create_oval(x, y, x + self.cell_size, y + self.cell_size, fill="red", outline="")

        # Draw snake
        for i, (x, y) in enumerate(self.snake_positions):
            color = "green" if i == 0 else "lightgreen"
            self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill=color, outline="")

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(self.width // 2, self.height // 2, text=f"Game Over!\nFinal Score: {self.score}",
                                fill="white", font=("Arial", 24))
        

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
