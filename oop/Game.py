import pygame
import time
from modules.GameConstants import *
from modules.GameUtility import *
from modules.GameInputs import *
from modules.GameDisplay import *
from modules.GameState import *
from modules.GameElements import *



class HangmanGame:
    def __init__(self):
        pygame.init()
        self.setup_game()
        self.init_components()

    def setup_game(self):
        with open(paths.wordlist_1, "r") as file:
            self.WORD_LIST = [line.strip().lower() for line in file]
        
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Hangman Game")


        # self.screen_display = GameDisplay(self)
        self.clock = pygame.time.Clock()
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
        self.button_positions = {}

    def init_components(self):
        """Initialize game components."""

        self.GameDisplay = GameDisplay(self)
        self.GameElements = GameElements(self)
        self.GameInput = GameInputs(self)
        self.GameState = GameState(self)



    def draw_text_box(self, text, font, center_pos, padding=(40, 20)):
        """Draw text with surrounding box."""
        text_surface = font.render(text, True, constants.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=center_pos)
        box_rect = text_rect.inflate(*padding)
        
        pygame.draw.rect(self.screen, constants.BUTTON_COLOR, box_rect)
        pygame.draw.rect(self.screen, constants.TEXT_COLOR, box_rect, 2)
        self.screen.blit(text_surface, text_rect)



    def draw_game_elements(self):
        """Draw all game elements."""
        center_x = constants.SCREEN_WIDTH // 2
        
        # Draw UI elements
        self.draw_text_box(f"Level: {self.level}", constants.FONT_MEDIUM, (center_x, 50))
        self.draw_text_box(f"Time: {self.timer_remaining}s", constants.FONT_SMALL, (center_x, 120))
        
        # Draw word
        word_text = constants.FONT_LARGE.render(self.get_display_word(), True, constants.FONT_COLOR)
        word_rect = word_text.get_rect(center=(center_x, constants.SCREEN_HEIGHT - 200))
        self.screen.blit(word_text, word_rect)
        
        # Draw game components
        self.GameElements.draw_buttons_letter()
        self.GameElements.draw_hint_button()
        self.GameDisplay.draw_hangman()


    def get_display_word(self):
        """Get the word display with revealed letters."""
        return " ".join(letter if letter in self.guesses else "_" for letter in self.current_word)


    def run(self):
        """Main game loop."""
        self.GameState.reset_game(reset_level=True)
        while self.running:
            self.screen.fill(constants.BG_COLOR)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.GameInput.handle_input(event)
            
            # Update and draw
            self.GameState.update_timer()
            self.draw_game_elements()
            self.GameState.check_game_state()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()

if __name__ == "__main__":
    game = HangmanGame()
    game.run()