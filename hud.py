import pygame
import toolbox
import random

class HUD():
    def __init__(self, screen, player):
        self.screen = screen          # The game screen to draw on
        self.player = player          # Reference to the player object

        self.state = 'mainmenu'       # Current HUD state (main menu, in-game, game over)
        
        # Fonts of different sizes for HUD text
        self.hud_font = pygame.font.SysFont('adobedevanagaribolditaliconpentype', 30)
        self.hud_font_med = pygame.font.SysFont("adobedevanagaribolditaliconpentype", 50)
        self.hud_font_big = pygame.font.SysFont("adobedevanagaribolditaliconpentype", 80)

        # Default text surfaces (pre-rendered)
        self.score_text = self.hud_font.render("Beep boop", True, (255, 255, 255))

        # Load images used in HUD (title, buttons, icons)
        self.title_image = pygame.image.load("assets/real_title.png")
        self.reset_button = pygame.image.load("assets/BtnReset.png")

        # Load icons for ammo display
        self.crate_icon = pygame.image.load("assets/Crate.png")
        self.explosive_crate_icon = pygame.image.load("assets/ExplosiveBarrel.png")
        self.split_shot_icon = pygame.image.load("assets/iconSplit.png")
        self.stream_shot_icon = pygame.image.load("assets/Laser Sprites/14.png")
        self.burst_shot_icon = pygame.image.load("assets/Laser Sprites/42.png")
        self.normal_shot_icon = pygame.image.load("assets/Laser Sprites/02.png")

        # Create ammo tile objects to display ammo counts on HUD
        self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosive_crate_ammo_tile = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)
        self.balloon_ammo_tile = AmmoTile(self.screen, self.normal_shot_icon, self.hud_font)

        self.high_score = 0           # Track highest score (not used here but can be expanded)
        self.showQuestions = False    # Flag to show/hide question screen

        # Question screen setup
        self.questionBackground = pygame.image.load("assets/QuestionBackground.png")

        # List of questions: each contains [id, question text, choice1, choice2, choice3, choice4, correct_choice_index]
        self.questions = [
            None,  # Index 0 unused, questions start from index 1
            [1, "You're building a login system—what's a critical step to secure user passwords?", "inspect()", "dir()", "hasattar()", "getattar()", 2],
            [2, "What is the goal of a SQL injection attack?", "list", "dict", "tuple", "set", 3],
            [3, "What does this list comprehension do? x for x in range(10) if x % 2 == 0", "Returns only even numbres from 0 to 9", "Filters out even numbers", "Returns numbers 1 through 10", "Creates a dictionary", 1],
            [4, "What is the primary use of with statements in Python?", "Looping over files", "Defining classes", "Managing file context/resources safely", "Declaring constants", 3],
            [5, "Which library is commonly used for password hashing in Python?", "hashlib", "bcrypt", "passlib", "All of the above", 4],
            [6, "What is an example of zero-day vulnerability?", "A bug that cuases your game to crash", "A known issue with an avaible patch", "A flaw no one knew about that attackers exploit", "A phishing email", 3],
            [7, "Which type of cyberattack uses deception to trick users into giving up sesitive information?", "DDoS", "Man-in-the-middle", "Pishing", "Malware injection", 3],
            [8, "Your game ocnnects to an online API = what's the most secure way to store the API key?", "Hardcode it in the game", "Use environment variables", "Write it in plain text in the config", "Email it to yourself", 2]
        ]

        # Choose a random question to start
        self.questionNumber = random.randint(1, 2)

        # Prepare question and choices as rendered text surfaces (to be updated every frame)
        self.questionText = self.hud_font.render("Question", True, (255, 255, 255))
        self.questionChoiceA = self.hud_font.render("Question Choice A", True, (225, 225, 255))
        self.questionChoiceB = self.hud_font.render("Question Choice B", True, (225, 225, 255))
        self.questionChoiceC = self.hud_font.render("Question Choice C", True, (225, 225, 255))
        self.questionChoiceD = self.hud_font.render("Question Choice D", True, (225, 225, 255))

        # Timer to make "Press any key to start" blink on main menu
        self.start_blink_timer_max = 75
        self.start_blink_timer = self.start_blink_timer_max

        # Pre-render static texts
        self.start_text = self.hud_font.render("Press any key to start", True, (255, 255, 255))
        self.tutorial_text = self.hud_font.render("WASD to move - CLICK to shoot - SPACE for crate - RIGHT CLICK for explosive crate", True, (255, 255, 255))
        self.game_over_text = self.hud_font_big.render("Game Over", True, (255, 255, 255))

    def answerQuestion(self, answer):
        """Check if player's answer is correct and update accordingly."""
        self.answer = answer
        if self.answer == self.questions[self.questionNumber][6]:  # Index 6 = correct choice number
            self.player.energy += 500   # Reward player energy if correct
            self.questionNumber = random.randint(1, 2)  # Pick new question randomly
        else:
            self.questionNumber = random.randint(1, 2)  # Pick new question even if wrong

    def update(self):
        """Update and draw HUD elements depending on current state."""
        if self.state == 'ingame':
            tile_x = 392  # Starting x-position for ammo tiles

            # Draw the score at the top-left
            self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (255, 255, 255))
            self.screen.blit(self.score_text, (10, 10))

            # Draw crate ammo tile and update position for next tile
            self.crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.crate_ammo)
            tile_x += self.crate_ammo_tile.width

            # Draw explosive crate ammo tile and update position
            self.explosive_crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.explosive_crate_ammo)
            tile_x += self.explosive_crate_ammo_tile.width

            # Choose the correct icon based on player's current shot type
            if self.player.shot_type == 'normal':
                self.balloon_ammo_tile.icon = self.normal_shot_icon
            elif self.player.shot_type == 'split':
                self.balloon_ammo_tile.icon = self.split_shot_icon
            elif self.player.shot_type == 'burst':
                self.balloon_ammo_tile.icon = self.burst_shot_icon
            elif self.player.shot_type == 'stream':
                self.balloon_ammo_tile.icon = self.stream_shot_icon

            # Draw special ammo tile with the current icon
            self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.special_ammo)

            # Update question text and choices for current question
            self.questionText = self.hud_font.render(self.questions[self.questionNumber][1], True, (255, 255, 255))
            self.questionChoiceA = self.hud_font.render(self.questions[self.questionNumber][2], True, (225, 225, 255))
            self.questionChoiceB = self.hud_font.render(self.questions[self.questionNumber][3], True, (225, 225, 255))
            self.questionChoiceC = self.hud_font.render(self.questions[self.questionNumber][4], True, (225, 225, 255))
            self.questionChoiceD = self.hud_font.render(self.questions[self.questionNumber][5], True, (225, 225, 255))

            # If question screen is active, draw the question and choices
            if self.showQuestions == True:
                self.screen.bli

