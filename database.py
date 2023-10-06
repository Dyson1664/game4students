import sqlite3
import random

def initialize_db():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS questions
              (id INTEGER PRIMARY KEY,
              question_text TEXT)
              ''')
    conn.commit()
    conn.close()

def add_question(questions):
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("INSERT INTO questions (question_text) VALUES (?)", (questions,))
    conn.commit()
    conn.close()

def get_random_question():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    all_questions = c.fetchall()
    conn.close()
    if all_questions:
        random_question = random.choice(all_questions)
        return random_question[1]
    else:
        return None


def all_questions():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    all_questions = c.fetchall()
    for question in all_questions:
        print(question)

# all_questions()
# initialize_db()




questions = ([
    "What is the capital of Spain?",
    "What planet is known as the Blue Planet?",
    "Who is known as the 'Iron Lady'?",
    "What is the deepest ocean on Earth?",
    "What is the longest river in Africa?",
    "What is the name of the ship that sank in 1912?",
    "Who is known as the 'Flying Finn'?",
    "What is the square root of 49?",
    "Who wrote the novel 'Oliver Twist'?",
    "What process turns liquid into gas?",
    "What are the three types of rocks?",
    "What is the next prime number after 7?",
    "What is the smallest continent on Earth?",
    "Who invented the light bulb?",
    "What is the largest land animal?",
    "What is the smallest country in the world by area?",
    "Who was the first woman to fly solo across the Atlantic Ocean?",
    "What are the three secondary colors?",
    "What is the name of the galaxy we live in?",
    "What is the symbol for oxygen in chemical notation?",
    "Who is known as the 'Wizard of Menlo Park'?",
    "Who was known as the 'Maid of Orléans'?",
    "What is the tallest bird on Earth?",
    "Who painted the 'Last Supper'?",
    "What is the name of the cowboy in 'Toy Story'?",
    "What is the highest mountain in South America?",
    "What is the name of the tiger in 'The Jungle Book'?",
    "What is the chemical symbol for iron?",
    "What is the chemical symbol for carbon?",
    "What is the hottest desert in the world?"
])

# for question in questions:
#     add_question(question)
