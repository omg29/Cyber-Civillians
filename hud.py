# Import necessary libraries
import pygame
import toolbox
import random

# HUD class handles all on-screen displays including ammo, score, and question screen
class HUD():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.state = 'mainmenu'  # Tracks which UI state we're in
        # Fonts for various text sizes
        self.hud_font = pygame.font.SysFont('adobedevanagaribolditaliconpentype', 30)
        self.hud_font_med = pygame.font.SysFont("adobedevanagaribolditaliconpentype", 50)
        self.hud_font_big = pygame.font.SysFont("adobedevanagaribolditaliconpentype", 80)

        # UI elements for the different game states
        self.score_text = self.hud_font.render("Beep boop", True, (255, 255, 255))
        self.title_image = pygame.image.load("assets/Title.png")
        self.start_blink_timer_max = 75
        self.start_blink_timer = self.start_blink_timer_max
        self.start_text = self.hud_font.render("Press any key to start", True, (255, 255, 255))
        self.tutorial_text = self.hud_font.render("WASD to move - CLICK to shoot - SPACE for crate - RIGHT CLICK for explosive crate", True, (255, 255, 255))
        self.game_over_text = self.hud_font_big.render("Game Over", True, (255, 255, 255))
        self.reset_button = pygame.image.load("assets/BtnReset.png")

        # Icons for ammo types and crates
        self.crate_icon = pygame.image.load("assets/Crate.png")
        self.explosive_crate_icon = pygame.image.load("assets/ExplosiveBarrel.png")
        self.split_shot_icon = pygame.image.load("assets/iconSplit.png")
        self.stream_shot_icon = pygame.image.load("assets/Laser Sprites/14.png")
        self.burst_shot_icon = pygame.image.load("assets/Laser Sprites/42.png")
        self.normal_shot_icon = pygame.image.load("assets/Laser Sprites/02.png")

        # Create HUD tiles for different ammo/crates
        self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosive_crate_ammo_tile = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)
        self.balloon_ammo_tile = AmmoTile(self.screen, self.normal_shot_icon, self.hud_font)

        self.high_score = 0
        self.showQuestions = False  # Controls whether the question box is showing

        # ------------------------ QUESTION SYSTEM ------------------------ #
        self.questionBackground = pygame.image.load("assets/QuestionBackground.png")
        # List of questions [id, question, option A, B, C, D, correct index (1-4)]
        self.questions = [None,
            [1, "You're building a login system—what's a critical step to secure user passwords?", "inspect()", "dir()", "hasattar()", "getattar()", 2],
            [2, "What is the goal of a SQL injection attack?", "list", "dict", "tuple", "set", 3],
            [3, "What does this list comprehension do? x for x in range(10) if x % 2 == 0", "Returns only even numbres from 0 to 9", "Filters out even numbers", "Returns numbers 1 through 10", "Creates a dictionary", 1],
            [4, "What is the primary use of with statements in Python?", "Looping over files", "Defining classes", "Managing file context/resources safely", "Declaring constants", 3],
            [5, "Which library is commonly used for password hashing in Python?", "hashlib", "bcrypt", "passlib", "All of the above", 4],
            [6, "What is an example of zero-day vulnerability?", "A bug that causes your game to crash", "A known issue with an available patch", "A flaw no one knew about that attackers exploit", "A phishing email", 3],
            [7, "Which type of cyberattack uses deception to trick users into giving up sensitive information?", "DDoS", "Man-in-the-middle", "Phishing", "Malware injection", 3],
            [8, "Your game connects to an online API - what's the most secure way to store the API key?", "Hardcode it in the game", "Use environment variables", "Write it in plain text in the config", "Email it to yourself", 2]
        ]
        self.questionNumber = random.randint(1, 2)  # Pick a random question
        # Initialize question texts
        self.questionText = self.hud_font.render("Question", True, (255, 255, 255))
        self.questionChoiceA = self.hud_font.render("Question Choice A", True, (225, 225, 255))
        self.questionChoiceB = self.hud_font.render("Question Choice B", True, (225, 225, 255))
        self.questionChoiceC = self.hud_font.render("Question Choice C", True, (225, 225, 255))
        self.questionChoiceD = self.hud_font.render("Question Choice D", True, (225, 225, 255))

    # ------------------------ HANDLE QUESTION ANSWER ------------------------ #
    def answerQuestion(self, answer):
        self.answer = answer
        if self.answer == self.questions[self.questionNumber][6]:  # If correct
            self.player.energy += 500
        self.questionNumber = random.randint(1, 2)  # Pick next question

    # ------------------------ MAIN HUD UPDATE LOOP ------------------------ #
    def update(self):
        if self.state == 'ingame':
            tile_x = 392  # Starting x for ammo tiles
            # Show player score
            self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (255, 255, 255))
            self.screen.blit(self.score_text, (10, 10))

            # Update and draw crate ammo tiles
            self.crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.crate_ammo)
            tile_x += self.crate_ammo_tile.width
            self.explosive_crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.explosive_crate_ammo)
            tile_x += self.explosive_crate_ammo_tile.width

            # Pick icon based on current weapon type
            if self.player.shot_type == 'normal':
                self.balloon_ammo_tile.icon = self.normal_shot_icon
            elif self.player.shot_type == 'split':
                self.balloon_ammo_tile.icon = self.split_shot_icon
            elif self.player.shot_type == 'burst':
                self.balloon_ammo_tile.icon = self.burst_shot_icon
            elif self.player.shot_type == 'stream':
                self.balloon_ammo_tile.icon = self.stream_shot_icon

            # Update special ammo HUD tile
            self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.special_ammo)

            # Update current question and answers
            self.questionText = self.hud_font.render(self.questions[self.questionNumber][1], True, (255, 255, 255))
            self.questionChoiceA = self.hud_font.render(self.questions[self.questionNumber][2], True, (225, 225, 255))
            self.questionChoiceB = self.hud_font.render(self.questions[self.questionNumber][3], True, (225, 225, 255))
            self.questionChoiceC = self.hud_font.render(self.questions[self.questionNumber][4], True, (225, 225, 255))
            self.questionChoiceD = self.hud_font.render(self.questions[self.questionNumber][5], True, (225, 225, 255))

            # Draw question box if toggled
            if self.showQuestions == True:
                self.screen.blit(self.questionBackground, (100, 100))
                self.screen.blit(self.questionText, (110, 150))
                self.screen.blit(self.questionChoiceA, (110, 260))
                self.screen.blit(self.questionChoiceB, (505, 260))
                self.screen.blit(self.questionChoiceC, (110, 415))
                self.screen.blit(self.questionChoiceD, (505, 415))

        # ------------------------ Main Menu State ------------------------ #
        elif self.state == 'mainmenu':
            self.start_blink_timer -= 1
            if self.start_blink_timer <= 0:
                self.start_blink_timer = self.start_blink_timer_max
            title_x, title_y = toolbox.centeringCoords(self.title_image, self.screen)
            title_y -= 40
            self.screen.blit(self.title_image, (title_x, title_y))
            text_x, text_y = toolbox.centeringCoords(self.start_text, self.screen)
            text_y -= 40
            if self.start_blink_timer > 30:
                self.screen.blit(self.start_text, (text_x, text_y+150))
            text_x, text_y = toolbox.centeringCoords(self.tutorial_text, self.screen)
            text_y = self.screen.get_height()- 50
            self.screen.blit(self.tutorial_text, (text_x, text_y))

        # ------------------------ Game Over State ------------------------ #
        elif self.state == 'gameover':
            text_x, text_y = toolbox.centeringCoords(self.game_over_text, self.screen)
            text_y -= 60
            self.screen.blit(self.game_over_text, (text_x, text_y))
            self.score_text = self.hud_font.render("Final score:" + str(self.player.score), True, (255, 255, 255))
            text_x, text_y = toolbox.centeringCoords(self.score_text, self.screen)
            self.screen.blit(self.score_text, (text_x, text_y))
            # Show reset button
            button_x, button_y = toolbox.centeringCoords(self.reset_button, self.screen)
            button_y += 100
            button_rect = self.screen.blit(self.reset_button, (button_x, button_y))

            # Handle reset click
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_position):
                        self.state = 'mainmenu'

# AmmoTile class to render crate/ammo icons and quantities
class AmmoTile():   
    def __init__(self, screen, icon, font):
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bg_image = pygame.image.load("assets/hudTile.png")
        self.width = self.bg_image.get_width()

    def update(self, x, y, ammo):
        tile_rect = self.bg_image.get_rect()
        tile_rect.bottomleft = (x, y)
        self.screen.blit(self.bg_image, tile_rect)

        # Center the icon in the tile
        icon_rect = self.icon.get_rect()
        icon_rect.center = tile_rect.center
        self.screen.blit(self.icon, icon_rect)

        # Show ammo count
        ammo_text = self.font.render(str(ammo), True, (255, 255, 255))
        self.screen.blit(ammo_text, tile_rect.topleft)
