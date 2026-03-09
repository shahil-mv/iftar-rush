import pygame

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
SKY_BLUE = (135, 206, 235)
MIDNIGHT_BLUE = (25, 25, 112)
BOOST_GOLD = (255, 215, 0)

# Game Rules
PHASE_DURATION = 15  # seconds
TOTAL_TIME = 120    # 2 minutes
MIN_SCORE_LIMIT = -2000

# Item Configs (Name: (Points, Probability, Color/ImageKey))
ITEM_DATA = {
    "anandu": (500, 5, "mandhi.png"),     # Mandhi
    "ashwant": (100, 20, "mess_meals.png"),   # Mess Meals
    "ujwal": (150, 15, "kanji.png"),    # Kanji
    "arjun": (300, 10, "shawaya.png"),     # Shawaya
    "jishnu": (400, 8, "biriyani.png"),     # Biriyani
    "anand": (50, 5, "protein_powder.png"),   # Protein Powder
}

DEFAULT_FALL_SPEED = 3
BOOST_FALL_SPEED = 6
BOOST_DURATION = 5

# Physics
GRAVITY = 0.15

# Colleague Side Positions (Left: X < SCREEN_WIDTH/2, Right: X > SCREEN_WIDTH/2)
COLLEAGUE_POSITIONS = {
    "anandu": (50, 150),
    "ashwant": (50, 300),
    "vishnu": (50, 450),
    "arjun": (750, 150),
    "jishnu": (750, 300),
    "anand": (750, 450),
}
