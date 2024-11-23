import pygame
import random
import string
import time

# for ruff ignored errors
# ruff: noqa: F403, F405, F541 - ignore import errors - dahil pala sa ruff na yan kaya nagkakaroon ng error
from modules.constants import *
from modules.GameUtility import *
from modules.GameOver import *
from modules.NextLevel import *


# INITIALIZE
pygame.init()


class HangmanGame:
    # VARIABLES
    def __init__(self):
        with open(paths.wordlist_1, "r") as file:
            self.WORD_LIST = [line.strip().lower() for line in file]
        
        self.next_level = nextlevel(self)
        self.gameover = gameover(self)
        self.current_word = ""
        self.guesses = []
        self.attempts = 0
        self.timer_remaining = constants.TIMER_DURATION
        self.hint_count = 1
        self.level = 1
        self.running = True
        self.notification_message = ""
        self.notification_timer = 0
        self.start_time = time.time()
        self.popup_active = False


        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Hangman Game")
        self.clock = pygame.time.Clock()

        # IMAGES
        self.images = paths.hangman_stages
        self.button_positions = {}
        # DISPLAY

    
    # LETTER BUTTONS
    def draw_buttons_letter(self):
        button_width = 50
        button_height = 50
        max_columns = 13
        spacing = 10  # Space between buttons
        border_thickness = 2  # Border thickness in pixels

        # Calculate total width of a row of buttons
        total_width = (button_width + spacing) * max_columns - spacing

        # Start x position to center the buttons
        x = (constants.SCREEN_WIDTH - total_width) // 2
        y = constants.SCREEN_HEIGHT - 150  # Vertical position

        mouse_pos = pygame.mouse.get_pos()

        for i, letter in enumerate(self.alphabet):
            if letter not in self.guesses:
                column = i % max_columns
                row = i // max_columns
                x_pos = x + column * (button_width + spacing)
                y_pos = y + row * (button_height + spacing)

                # Create button rectangle
                rect = pygame.Rect(x_pos, y_pos, button_width, button_height)

                # Draw filled button
                color = (
                    constants.BUTTON_HOVER_COLOR
                    if rect.collidepoint(mouse_pos)
                    else constants.BUTTON_COLOR
                )
                pygame.draw.rect(self.screen, color, rect)

                # Draw border
                pygame.draw.rect(
                    self.screen, (0, 0, 0), rect, border_thickness
                )  # Black border


                # Draw letter
                letter_surf = constants.FONT_MEDIUM.render(
                    letter.upper(), True, constants.FONT_COLOR
                )
                letter_rect = letter_surf.get_rect(
                    center=(x_pos + button_width // 2, y_pos + button_height // 2)
                )
                self.screen.blit(letter_surf, letter_rect)
                self.button_positions[letter] = rect
            else:
                if letter in self.button_positions:
                    del self.button_positions[letter]




    def draw_hint_button(self):
        button_width = 50
        max_columns = 13
        spacing = 10
        y_offset = -100
        total_keyboard_width = (button_width + spacing) * max_columns - spacing
        keyboard_x = (constants.SCREEN_WIDTH - total_keyboard_width) // 2
        keyboard_y = constants.SCREEN_HEIGHT - 150 + y_offset

        # Hint button dimensions
        hint_button_width = 150
        hint_button_height = 50
        hint_x = keyboard_x + total_keyboard_width - hint_button_width
        hint_y = keyboard_y - hint_button_height - spacing
        hint_button_rect = pygame.Rect(
            hint_x, hint_y, hint_button_width, hint_button_height
        )

        # Draw button background and border
        pygame.draw.rect(self.screen, constants.BUTTON_COLOR, hint_button_rect)  # Fill
        pygame.draw.rect(self.screen, (0, 0, 0), hint_button_rect, 2)  # Border

        # Render and center hint text
        hint_text = constants.FONT_SMALL.render("Hint", True, constants.FONT_COLOR)
        hint_text_rect = hint_text.get_rect(
            center=(hint_x + hint_button_width // 2, hint_y + hint_button_height // 2)
        )
        self.screen.blit(hint_text, hint_text_rect)

        # Render and position hint count
        hint_count_text = constants.FONT_SMALL.render(
            f"Hints: {self.hint_count}", True, constants.TEXT_COLOR
        )
        hint_count_rect = hint_count_text.get_rect(
            center=(
                hint_x + hint_button_width // 2,
                hint_y + hint_button_height + spacing + 10,
            )
        )
        self.screen.blit(hint_count_text, hint_count_rect)

        self.button_positions["hint"] = hint_button_rect



    def use_hint(self):
        """Reveal one unguessed letter as a hint."""
        if self.hint_count > 0:
            unguessed_letters = [
                letter for letter in self.current_word if letter not in self.guesses
            ]
            if unguessed_letters:
                hint_letter = random.choice(unguessed_letters)
                self.guesses.append(hint_letter)
                self.hint_count -= 1
                self.notification_message = f"Hint: Revealed '{hint_letter.upper()}'!"
                self.notification_timer = 60
        else:
            self.notification_message = "No hints available!"
            self.notification_timer = 60
    

    def draw_hangman(self):
        if self.attempts < len(self.images):
            self.screen.blit(
                self.images[self.attempts],
                (
                    constants.SCREEN_WIDTH // 2 - constants.width // 2,
                    constants.SCREEN_HEIGHT // 4,
                ),
            )



    def get_display_word(self):
        return " ".join(
            [letter if letter in self.guesses else "_" for letter in self.current_word]
        )


    def reset_game(self, reset_level=False):
        self.current_word = random.choice(self.WORD_LIST)
        self.guesses = []
        self.attempts = 0
        self.timer_remaining = constants.TIMER_DURATION
        self.start_time = time.time()
        self.alphabet = list(string.ascii_lowercase)
        random.shuffle(self.alphabet)
        if reset_level:
            self.level = 1
            self.hint_count = 1


    def handle_input(self, event):
        if self.popup_active:
            # Ignore all inputs when a popup is active
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for letter, rect in self.button_positions.items():
                if rect.collidepoint(mouse_pos):
                    if letter == "hint":
                        self.use_hint()
                    elif letter in self.guesses:
                        self.notification_message = (
                            f"Letter '{letter.upper()}' already guessed!"
                        )
                        self.notification_timer = 60
                    else:
                        self.guesses.append(letter)
                        if letter not in self.current_word:
                            self.attempts += 1
                    break

        elif event.type == pygame.KEYDOWN:
            # Handle keyboard input
            letter = event.unicode.lower()  # Get the pressed key as a string
            if letter.isalpha() and len(letter) == 1:  # Ensure it's a valid letter
                if letter in self.guesses:
                    self.notification_message = (
                        f"Letter '{letter.upper()}' already guessed!"
                    )
                    self.notification_timer = 60
                else:
                    self.guesses.append(letter)
                    if letter not in self.current_word:
                        self.attempts += 1




    # GAME OVER UI

    # def show_popup(self, reset_level=False):
    #     self.popup_active = True

    #     # Create overlay
    #     overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    #     overlay.set_alpha(128)
    #     overlay.fill(pygame.Color("#a11d33"))
    #     self.screen.blit(overlay, (0, 0))

    #     # Define messages
    #     messages = ["Game Over!", f"The word was '{self.current_word}'"]

    #     # Calculate positions with more spacing
    #     center_x = constants.SCREEN_WIDTH // 2
    #     base_y = constants.SCREEN_HEIGHT // 2 - 100  # Move up starting position
    #     line_spacing = 80  # Increase spacing between lines
    #     box_padding = 30  # Add padding around text

    #     # Draw each message line
    #     for i, msg in enumerate(messages):
    #         if i == 0:  # Game Over message
    #             # Set specific width for first message box
    #             box_width = 400  # Adjust this value as needed

    #             text_surf = constants.FONT_LARGE.render(msg, True, constants.FONT_COLOR)
    #             text_rect = text_surf.get_rect(
    #                 center=(center_x, base_y + (i * line_spacing))
    #             )

    #             # Create box rect with fixed width
    #             box_rect = pygame.Rect(0, 0, box_width, text_rect.height + box_padding)
    #             box_rect.centerx = center_x
    #             box_rect.centery = text_rect.centery

    #         else:
    #             text_surf = constants.FONT_MEDIUM.render(
    #                 msg, True, constants.FONT_COLOR
    #             )
    #             text_rect = text_surf.get_rect(
    #                 center=(center_x, base_y + (i * line_spacing))
    #             )
    #             box_rect = text_rect.inflate(box_padding * 2, box_padding)

    #         # Draw box and border
    #         pygame.draw.rect(self.screen, constants.BUTTON_COLOR, box_rect)
    #         pygame.draw.rect(self.screen, constants.FONT_COLOR, box_rect, 3)

    #         # Draw text
    #         self.screen.blit(text_surf, text_rect)

    #     # Button definitions remain the same
    #     quit_button_rect = pygame.Rect(
    #         constants.SCREEN_WIDTH // 2 - 200,
    #         constants.SCREEN_HEIGHT // 2 + 50,
    #         150,
    #         50,
    #     )
    #     try_again_button_rect = pygame.Rect(
    #         constants.SCREEN_WIDTH // 2 + 50, constants.SCREEN_HEIGHT // 2 + 50, 150, 50
    #     )

    #     # Button text
    #     try_box = "Try Again"
    #     quit_box = "Quit"

    #     # Draw Quit button
    #     pygame.draw.rect(self.screen, pygame.Color("#FF0000"), quit_button_rect)
    #     pygame.draw.rect(self.screen, constants.FONT_COLOR, quit_button_rect, 3)
    #     quit_text = constants.FONT_SMALL.render(quit_box, True, constants.FONT_COLOR)
    #     quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    #     self.screen.blit(quit_text, quit_text_rect)

    #     # Draw Try Again button
    #     pygame.draw.rect(self.screen, pygame.Color("#00FF00"), try_again_button_rect)
    #     pygame.draw.rect(self.screen, constants.FONT_COLOR, try_again_button_rect, 3)
    #     try_text = constants.FONT_SMALL.render(try_box, True, constants.FONT_COLOR)
    #     try_text_rect = try_text.get_rect(center=try_again_button_rect.center)
    #     self.screen.blit(try_text, try_text_rect)

    #     pygame.display.flip()

    #     # Event handling loop
    #     while self.popup_active:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 exit()
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #                 mouse_pos = event.pos
    #                 if quit_button_rect.collidepoint(mouse_pos):
    #                     pygame.quit()
    #                     exit()
    #                 if try_again_button_rect.collidepoint(mouse_pos):
    #                     self.reset_game(reset_level=True)
    #                     self.popup_active = False

    #         self.clock.tick(30)


    # def show_success_popup(self):
    #     """Display a success pop-up message."""
    #     self.popup_active = True
    #     center_x = constants.SCREEN_WIDTH // 2
    #     y_start = constants.SCREEN_HEIGHT // 2 - 100
    #     box_spacing = 70

    #     # Draw overlay
    #     overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    #     overlay.set_alpha(128)
    #     overlay.fill(pygame.Color("#68c3a3"))
    #     self.screen.blit(overlay, (0, 0))

    #     # Define messages
    #     messages = [
    #         f"Level {self.level} Cleared!",
    #         "Congrats!",
    #         f"You guessed the word '{self.current_word}'!",
    #     ]


    #     for i, message in enumerate(messages):
    #         # Render text
    #         text_surface = constants.FONT_MEDIUM.render(
    #             message, True, constants.FONT_COLOR
    #         )
    #         text_rect = text_surface.get_rect(
    #             center=(center_x, y_start + box_spacing * i)
    #         )

    #         # Draw box background and border
    #         box_rect = text_rect.inflate(20, 20)
    #         pygame.draw.rect(self.screen, constants.BG_COLOR, box_rect)  # Background
    #         pygame.draw.rect(self.screen, constants.FONT_COLOR, box_rect, 2)  # Border

    #         # Draw text
    #         self.screen.blit(text_surface, text_rect)

    #     pygame.display.flip()  # Update the display

    #     # Set a timer event for 2 seconds later
    #     pygame.time.set_timer(pygame.USEREVENT + 3, 2000)  # Custom event ID

    #     # Event loop waiting for the timer
    #     while self.popup_active:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 exit()
    #             elif event.type == pygame.USEREVENT + 3:
    #                 # Timer finished
    #                 self.popup_active = False
    #                 pygame.time.set_timer(pygame.USEREVENT + 3, 0)  # Disable the timer
    #                 # Proceed to next level or reset
    #                 self.level += 1
    #                 self.hint_count += 1
    #                 self.reset_game()
    #             else:
    #                 # Ignore other events
    #                 pass

    #         self.clock.tick(30)  # Maintain 30 FPS during popup


    def run(self):
        """Main game loop."""
        self.reset_game(reset_level=True)
        while self.running:
            self.screen.fill(constants.BG_COLOR)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            # Timer logic
            elapsed_time = time.time() - self.start_time
            self.timer_remaining = constants.TIMER_DURATION - int(elapsed_time)
            if self.timer_remaining <= 0:
                self.show_popup(
                    f"Game Over! You reached Level {self.level}.", reset_level=True
                )

            # Draw elements with boxes
            center_x = constants.SCREEN_WIDTH // 2

            # Level box and text
            level_text = constants.FONT_MEDIUM.render(
                f"Level: {self.level}", True, constants.TEXT_COLOR
            )
            level_rect = level_text.get_rect(center=(center_x, 50))
            level_box = level_rect.inflate(40, 20)  # Add padding around text
            pygame.draw.rect(
                self.screen, constants.BUTTON_COLOR, level_box
            )  # Box background
            pygame.draw.rect(
                self.screen, constants.TEXT_COLOR, level_box, 2
            )  # Box border
            self.screen.blit(level_text, level_rect)

            # Timer box and text
            timer_text = constants.FONT_SMALL.render(
                f"Time Remaining: {self.timer_remaining}s", True, constants.TEXT_COLOR
            )
            timer_rect = timer_text.get_rect(center=(center_x, 120))
            timer_box = timer_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, constants.BUTTON_COLOR, timer_box)
            pygame.draw.rect(self.screen, constants.TEXT_COLOR, timer_box, 2)
            self.screen.blit(timer_text, timer_rect)

            # Word text
            word_text = constants.FONT_LARGE.render(
                self.get_display_word(), True, constants.FONT_COLOR
            )
            word_rect = word_text.get_rect(
                center=(center_x, constants.SCREEN_HEIGHT - 200)
            )
            self.screen.blit(word_text, word_rect)

            self.draw_buttons_letter()
            self.draw_hint_button()
            self.draw_hangman()

            if self.attempts >= constants.MAX_ATTEMPTS:
                self.gameover.show_popup(reset_level=True)
                # self.show_popup(reset_level=True)

            elif all(letter in self.guesses for letter in self.current_word):
                # self.show_success_popup()
                self.next_level.show_success_popup()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = HangmanGame()
    game.run()
