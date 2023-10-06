import pygame
import sys
import openai
import os
import time
import database as db_ops
from dotenv import load_dotenv
import textwrap
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Get a random question
random_question = db_ops.get_random_question()


# Initialize pygame
pygame.init()

# Set up display
window_size = (500, 800)  # Increase the height to 600
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Image Reveal Game')

image_paths = [
    r"C:\Users\PC\Pictures\Saved Pictures\trupm.jpg",
    r"C:\Users\PC\Pictures\Saved Pictures\rose.jfif",
    r"C:\Users\PC\Pictures\Saved Pictures\ronaldo.jpg",
    r"C:\Users\PC\Pictures\Saved Pictures\taylor_swift.jfif",
    r"C:\Users\PC\Pictures\Saved Pictures\vietnam.jfif",
]

wins_pic = [r"C:\Users\PC\Pictures\Saved Pictures\winners.jfif"]

# Create grid overlay
grid_size = 6
square_size = window_size[0] // grid_size
squares = {(x, y): True for x in range(grid_size) for y in range(grid_size)}

class Button:
    def __init__(self, text, pos, width, height, onclick=None):
        self.text = text
        self.pos = pos
        self.width = width
        self.height = height
        self.onclick = onclick

    def click(self):
        if self.onclick is not None:
            self.onclick()

    def draw(self):
        # Draw button background
        pygame.draw.rect(screen, (200, 200, 200), (*self.pos, self.width, self.height))
        # Draw button border (change border_color and border_width as desired)
        border_color = (0, 0, 0)  # Black
        border_width = 5  # Set border width
        pygame.draw.rect(screen, border_color, (*self.pos, self.width, self.height), border_width)
        # Draw button text
        font = pygame.font.Font('Roboto-Regular.ttf', 36)


        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=((self.pos[0] + self.width // 2), (self.pos[1] + self.height // 2)))
        screen.blit(text, text_rect.topleft)

    def is_clicked(self, mouse_pos):
        return self.pos[0] <= mouse_pos[0] <= self.pos[0] + self.width and self.pos[1] <= mouse_pos[1] <= self.pos[1] + self.height

class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0



correct_button = Button("Correct", (0, 500), 250, 100)
incorrect_button = Button("Incorrect", (250, 500), 250, 100)

team1 = Team("Team 1")
team2 = Team("Team 2")

def draw_grid():
    for (x, y), active in squares.items():
        if active:
            pygame.draw.rect(screen, (255, 255, 255), (x * square_size, y * square_size, square_size, square_size), 0)
            font = pygame.font.Font(None, 36)
            text = font.render(str(y * grid_size + x), True, (0, 0, 0))
            screen.blit(text, (x * square_size + square_size//3, y * square_size + square_size//3))

def get_square(pos):
    x, y = pos
    grid_x, grid_y = x // square_size, y // square_size
    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
        return grid_x, grid_y
    return None  # Return None if the click is outside the grid

def award_points():
    global current_team  # Assumes a global variable to keep track of the current team
    if current_team is not None:
        current_team.score += 10

def draw_team_borders():
    border_color = (0, 0, 0)  # Black
    border_width = 5  # Set border width
    team1_border_rect = pygame.Rect(0, 600, 250, 50)
    team2_border_rect = pygame.Rect(250, 600, 250, 50)

    pygame.draw.rect(screen, border_color, team1_border_rect, border_width)
    pygame.draw.rect(screen, border_color, team2_border_rect, border_width)

class GameState:
    def __init__(self):
        self.display_question = False
        self.selected_square = None
        self.display_question = False
        self.correct_answer = False
        self.current_question = None
        self.current_team = team1
        self.other_team = team2
        self.current_image_index = 0
        self.load_new_image()
        self.images_revealed = 0

    def load_new_image(self):
        self.current_image = pygame.image.load(image_paths[self.current_image_index])
        self.current_image = pygame.transform.scale(self.current_image, (500, 500))
        self.current_image_index = (self.current_image_index + 1) % len(image_paths)  # Update index for next image
        # Reset the grid
        for key in squares:
            squares[key] = True

    def switch_team(self):
        self.other_team = self.current_team  # Store the current team as the other team before switching
        self.current_team = team2 if self.current_team == team1 else team1

    def well_done_action(self):
        self.award_points_to_other_team()
        self.reveal_picture()
        # Draw image and grid overlay
        screen.blit(self.current_image, (0, 0))
        draw_grid()
        # Draw buttons
        correct_button.draw()
        incorrect_button.draw()
        well_done.draw()
        # draw_turn()
        draw_scoreboard()
        # Update display
        pygame.display.update()
        pygame.time.wait(4000)
        self.images_revealed += 1
        if self.images_revealed == len(image_paths):  # Check if all images have been revealed
            self.game_over()
        else:
            self.load_new_image()

    def game_over(self):
        # Load the winning image
        winning_image_path = wins_pic[0]
        winning_image = pygame.image.load(winning_image_path)
        winning_image = pygame.transform.scale(winning_image, window_size)

        # Display the winning image
        screen.blit(winning_image, (0, 0))

        # Determine the winning team
        winning_team = team1 if team1.score > team2.score else team2

        font = pygame.font.Font('Roboto-Regular.ttf', 40)
        game_over_text = f"Game Over! {winning_team.name} wins!"
        text = font.render(game_over_text, True, (0, 255, 0))  # Green text
        text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 8))  # Adjusted y-coordinate
        screen.blit(text, text_rect.topleft)

        pygame.display.update()
        # Wait for a few seconds before closing the game
        pygame.time.wait(8000)

        # Quit the game
        pygame.quit()
        sys.exit()

    def award_points_to_other_team(self):
        if self.other_team is not None:
            self.other_team.score += 10

    def reveal_picture(self):
        global squares  # Ensure you are modifying the global squares dictionary
        for key in squares:
            squares[key] = False  # Set all squares to False to reveal the entire picture

    def dont_know_action(self):
        self.reveal_picture()
        # Draw image and grid overlay
        screen.blit(self.current_image, (0, 0))
        draw_grid()
        pygame.display.update()
        pygame.time.wait(4000)  # Wait for 4 seconds (4000 milliseconds)
        self.load_new_image()

game_state = GameState()

well_done = Button("Well Done", (0, 650), 500, 100, onclick=game_state.well_done_action)
dont_know_button = Button("Don't Know", (150, 750), 200, 50, onclick=game_state.dont_know_action)

def draw_question_box(question):
    box_width, box_height = 500, 200
    box = pygame.Surface((box_width, box_height))
    box.fill((200, 200, 200))  # fill the box with a color
    font = pygame.font.Font('Roboto-Regular.ttf', 32)

    wrapped_text = textwrap.fill(question, width=30)
    wrapped_text_lines = wrapped_text.split('\n')
    total_text_height = len(wrapped_text_lines) * font.get_linesize()
    start_y = (box_height - total_text_height) // 2

    for i, line in enumerate(wrapped_text_lines):
        text = font.render(line, True, (0, 0, 0))
        text_rect = text.get_rect(center=(box_width // 2, start_y + i * font.get_linesize()))
        box.blit(text, text_rect.topleft)

    screen.blit(box,
                ((window_size[0] - box_width) // 2, (window_size[1] - box_height) // 2))

def draw_scoreboard():
    pygame.draw.rect(screen, (255, 255, 255), (0, 600, 500, 50))
    font = pygame.font.Font(None, 36)
    if game_state.current_team == team1:
        pygame.draw.rect(screen, (0, 255, 0), (0, 600, 250, 50))  # Green background for Team 1
    elif game_state.current_team == team2:
        pygame.draw.rect(screen, (0, 255, 0), (250, 600, 250, 50))  # Green background for Team 2
    team1_score_text = f"{team1.name}: {team1.score}"
    team2_score_text = f"{team2.name}: {team2.score}"
    screen.blit(font.render(team1_score_text, True, (0, 0, 0)), (10, 610))
    screen.blit(font.render(team2_score_text, True, (0, 0, 0)), (350, 610))
    draw_team_borders()


# Main game loop
running = True
while running:
    background_color = (30, 30, 30)
    screen.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if a grid square is clicked
                square = get_square(event.pos)
                if square is not None and squares[square] and not game_state.display_question:
                    game_state.selected_square = square
                    game_state.display_question = True
                    game_state.current_question = db_ops.get_random_question()  # Generate question here

                elif correct_button.is_clicked(event.pos) and game_state.display_question:
                    game_state.correct_answer = True
                    game_state.display_question = False
                    game_state.current_team.score += 1 # Increment score
                    game_state.switch_team()  # Switch team after answering
                    print("Correct button clicked")  # Debugging print statement
                elif incorrect_button.is_clicked(event.pos) and game_state.display_question:
                    game_state.correct_answer = False
                    game_state.display_question = False
                    game_state.switch_team()
                    print("Incorrect button clicked")  # Debugging print statement
                elif well_done.is_clicked(event.pos):
                    well_done.click()
                elif dont_know_button.is_clicked(event.pos):
                    dont_know_button.click()

    # Draw image and grid overlay
    screen.blit(game_state.current_image, (0, 0))  # use game_state.current_image instead of image
    draw_grid()

    if game_state.display_question:
        draw_question_box(game_state.current_question)

        # If a correct answer was given, reveal part of the image
    if game_state.correct_answer and game_state.selected_square is not None:
        squares[game_state.selected_square] = False
        game_state.correct_answer = False

    # Draw buttons
    correct_button.draw()
    incorrect_button.draw()
    dont_know_button.draw()

    well_done.draw()
    # draw_turn()

    draw_scoreboard()

    # Update display
    pygame.display.update()

# Quit pygame
pygame.quit()
sys.exit()

