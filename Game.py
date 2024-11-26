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
        pygame.mixer.init()
        # Game states
        self.running = True
        self.in_menu = True
        
        # Initialize display
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Hangman Game")
        self.clock = pygame.time.Clock()
        
        



        self.Paths = Paths
        self.menu_music = Paths.startmenu_fx


        # Game variables
        self.setup_game_variables()
        self.init_components()







    def setup_game_variables(self):
        """Initialize game state variables."""
        self.current_word = ""
        self.guesses = []
        self.attempts = 0
        self.timer_remaining = constants.TIMER_DURATION
        self.hint_count = 1
        self.level = 1
        self.start_time = time.time()
        self.popup_active = False
        self.button_positions = {}

    def init_components(self):
        """Initialize game components."""
        self.GameDisplay = GameDisplay(self)
        self.GameElements = GameElements(self)
        self.GameInput = GameInputs(self)
        self.GameState = GameState(self)

    
    # In Game.py, update run method:
    
    def run(self):
        """Main game loop."""
        while self.running:
            if self.in_menu:
                buttons = self.GameDisplay.start_menu()
                
                for event in pygame.event.get():
                    self.GameInput.handle_menu_input(event, *buttons)
            else:
                if not self.popup_active:
                    self.screen.fill(constants.BG_COLOR)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            # Save progress before quitting
                            self.GameState.save_progress()
                            self.running = False
                        self.GameInput.handle_game_input(event)
                    
                    self.GameState.update_timer()
                    self.GameElements.draw_game_elements()
                    self.GameState.check_game_state()
            
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        
if __name__ == "__main__":
    game = HangmanGame()
    game.run()