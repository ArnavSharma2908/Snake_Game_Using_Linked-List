import random
import os
import time
try:
    import numpy as np
except ModuleNotFoundError:
    os.system('pip install numpy')
    import numpy as np


# Node representing each segment of the snake
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

# Snake represented as a linked list
class Snake:
    def __init__(self, x, y):
        # Initial position of the snake's head
        self.head = Node(x, y)
        self.tail = self.head

    # Move the snake in the given direction
    def move(self, direction, food_pos):
        head_x, head_y = self.head.x, self.head.y
        
        # Update coordinates based on direction
        if direction == 'UP':
            head_x -= 1
        elif direction == 'DOWN':
            head_x += 1
        elif direction == 'LEFT':
            head_y -= 1
        elif direction == 'RIGHT':
            head_y += 1
        
        # Create a new node for the new head position
        new_head = Node(head_x, head_y)
        new_head.next = self.head
        self.head = new_head

        # Check if snake eats food
        if (head_x, head_y) == food_pos:
            return True  # Snake grows, so no need to remove tail
        else:
            # Remove the tail (snake moves without growing)
            current = self.head
            while current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current
            return False

    # Check if the snake collides with itself or walls
    def check_collision(self, width, height):
        head_x, head_y = self.head.x, self.head.y
        
        # Check if snake hits the wall
        if head_x <= 0 or head_x >= height - 1 or head_y <= 0 or head_y >= width - 1:
            return True
        
        # Check if snake hits itself
        current = self.head.next
        while current:
            if current.x == head_x and current.y == head_y:
                return True
            current = current.next
        
        return False

    # Get the snake's body as a list of coordinates for rendering
    def get_body(self):
        body = []
        current = self.head
        while current:
            body.append((current.x, current.y))
            current = current.next
        return body

# Function to clear the console for rendering (cross-platform)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the game grid using numpy
def display_grid(snake, food_pos, width, height):
    grid = np.full((height, width), ' ', dtype=str)

    # Draw borders
    grid[0, :] = '#'
    grid[:, 0] = '#'
    grid[height-1, :] = '#'
    grid[:, width-1] = '#'

    # Place food on the grid
    food_x, food_y = food_pos
    grid[food_x, food_y] = 'O'
    
    # Place the snake on the grid
    for x, y in snake.get_body():
        grid[x, y] = '*'
    
    # Render the grid
    clear_console()
    for row in grid:
        print(''.join(row))

# Generate random position for the food
def generate_food(snake, width, height):
    while True:
        food_pos = (random.randint(1, height - 2), random.randint(1, width - 2))
        if food_pos not in snake.get_body():
            return food_pos

# Main game loop
def main():
    width, height = 20, 10
    snake = Snake(height // 2, width // 2)  # Start snake in the middle
    food_pos = generate_food(snake, width, height)  # Randomly place the food
    direction = 'RIGHT'  # Initial direction of movement
    score = 0

    # Main game loop
    while True:
        display_grid(snake, food_pos, width, height)
        print(f"Score: {score}")
        
        # Get user input (simple movement logic)
        user_input = input("Move (WASD): ").upper()
        if user_input == 'W':
            direction = 'UP'
        elif user_input == 'S':
            direction = 'DOWN'
        elif user_input == 'A':
            direction = 'LEFT'
        elif user_input == 'D':
            direction = 'RIGHT'

        # Move the snake in the given direction
        if snake.move(direction, food_pos):
            score += 1  # Increase score if snake eats food
            food_pos = generate_food(snake, width, height)  # Generate new food

        # Check for collisions
        if snake.check_collision(width, height):
            print("Game Over!")
            break

        time.sleep(0)  # Slow down the game loop for easier play

if __name__ == "__main__":
    main()

