import pygame
import sys
import openai
import os
import time
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Initialize pygame
pygame.init()

# Set up display
window_size = (500, 750)  # Increase the height to 600
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Image Reveal Game')

# Load image
# image = pygame.image.load(r"C:\Users\PC\Pictures\Saved Pictures\Allaho.jpg")
image_paths = [
    r"C:\Users\PC\Pictures\Saved Pictures\trupm.jpg",
    r"C:\Users\PC\Pictures\Saved Pictures\rose.jfif",
    r"C:\Users\PC\Pictures\Saved Pictures\ronaldo.jpg",
    r"C:\Users\PC\Pictures\Saved Pictures\taylor_swift.jfif",
    r"C:\Users\PC\Pictures\Saved Pictures\vietnam.jfif",


    # ... add more image paths as needed ...
]

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
        pygame.draw.rect(screen, (200, 200, 200), (*self.pos, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=((self.pos[0] + self.width//2), (self.pos[1] + self.height//2)))
        screen.blit(text, text_rect.topleft)

    def is_clicked(self, mouse_pos):
        return self.pos[0] <= mouse_pos[0] <= self.pos[0] + self.width and self.pos[1] <= mouse_pos[1] <= self.pos[1] + self.height

class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0



correct_button = Button("Correct", (0, 500), 250, 100)
incorrect_button = Button("Incorrect", (250, 500), 250, 100)

# team1 = Button('turn', (0, 750), 500, 100))

team1 = Team("Team 1")
team2 = Team("Team 2")

def draw_grid():
    for (x, y), active in squares.items():
        if active:
            pygame.draw.rect(screen, (255, 255, 255), (x * square_size, y * square_size, square_size, square_size), 0)
            font = pygame.font.Font(None, 36)
            text = font.render(str(y * grid_size + x), True, (0, 0, 0))
            screen.blit(text, (x * square_size + square_size//3, y * square_size + square_size//3))

def draw_turn():
    font = pygame.font.Font(None, 36)
    turn_text = f"It's {game_state.current_team.name}'s turn"
    text = font.render(turn_text, True, (0, 0, 0))
    screen.blit(text, (140, 660))  # Adjust position as needed

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

class GameState:
    def __init__(self):
        self.display_question = False
        self.selected_square = None
        self.display_question = False
        self.correct_answer = False
        self.current_question = None
        self.current_team = team1
        self.other_team = team2
        self.current_image_index = 0  # Initialize the image index
        self.load_new_image()  # Load the first image when GameState is initialized

    def load_new_image(self):
        self.current_image = pygame.image.load(image_paths[self.current_image_index])
        self.current_image = pygame.transform.scale(self.current_image, (500, 500))
        self.current_image_index = (self.current_image_index + 1) % len(image_paths)  # Update index for next image
        # Reset the grid overlay directly here, without modifying the global image and squares variables.
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
        draw_turn()
        draw_scoreboard()
        # Update display
        pygame.display.update()
        pygame.time.wait(4000)  # Wait for 2 seconds (2000 milliseconds)
        self.load_new_image()  # Load the next image and reset the game state


    def award_points_to_other_team(self):
        if self.other_team is not None:
            self.other_team.score += 10

    def reveal_picture(self):
        global squares  # Ensure you are modifying the global squares dictionary
        for key in squares:
            squares[key] = False  # Set all squares to False to reveal the entire picture

    # Create buttons



game_state = GameState()

well_done = Button("Well Done", (0, 650), 500, 100, onclick=game_state.well_done_action)

def generate_question():
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" as GPT-4 is not publicly available yet
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Create a question based on english vocab for a grade 3 ESL class"}
        ],
        max_tokens=50,
        temperature=0.7
    )
    question = response['choices'][0]['message']['content'].strip()
    return question






question = generate_question()




def draw_question_box(question):
    box_width, box_height = 500, 200  # dimensions of the question box
    box = pygame.Surface((box_width, box_height))  # create a new surface for the question box
    box.fill((200, 200, 200))  # fill the box with a color
    font = pygame.font.Font(None, 16)
    text = font.render(question, True, (0, 0, 0))
    text_rect = text.get_rect(center=(box_width//2, box_height//2))  # center the text in the box
    box.blit(text, text_rect.topleft)
    screen.blit(box, ((window_size[0]-box_width)//2, (window_size[1]-box_height)//2))  # center the box on the screen


def draw_scoreboard():
    # Fill the space below the buttons with a white background
    pygame.draw.rect(screen, (255, 255, 255), (0, 600, 500, 50))
    font = pygame.font.Font(None, 36)
    team1_score_text = f"{team1.name}: {team1.score}"
    team2_score_text = f"{team2.name}: {team2.score}"
    screen.blit(font.render(team1_score_text, True, (0, 0, 0)), (10, 610))
    screen.blit(font.render(team2_score_text, True, (0, 0, 0)), (350, 610))



# Main game loop
running = True
while running:
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
                    game_state.current_question = generate_question()  # Generate question here

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
                #elif well_done.is_clicked(event.pos):
                elif well_done.is_clicked(event.pos):
                    well_done.click()

    # Draw image and grid overlay
    # In your main game loop:
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
    well_done.draw()
    draw_turn()

    draw_scoreboard()

    # Update display
    pygame.display.update()

# Quit pygame
pygame.quit()
sys.exit()

#create a database of questions that you can feed to the gpt model at random
#pushed to git
