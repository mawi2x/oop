import pygame
import pygame.mixer
import time
import random
from modules.GameUtility import *
from modules.GameConstants import *
from modules.GameElements import *





class GameState:
    def __init__(self, game):
        """Initialize with reference to main game instance."""
        self.game = game
        pygame.mixer.init()
        self.game_over_sound = paths.gameover_fx
        self.GameElements = GameElements(self)
      
    
   
    # GAME OVER
    def game_over(self, reset_level=False):
        """Display game over popup with messages and buttons."""
        self.game.popup_active = True
    
        # Store original screen
        original_screen = self.game.screen.copy()

        # Play game over sound
        self.game_over_sound.play()
    
        # Animation setup
        row_height = 150  # Height of each row
        animation_speed = 200
        red_overlay = pygame.Color("#a11d33")
        # Use math.ceil to ensure we have enough rows to cover the screen
        total_rows = (constants.SCREEN_HEIGHT + row_height - 1) // row_height
    
        # Animate overlay row by row
        for row in range(total_rows):
            animation_width = 0
            is_right_to_left = row % 2 == 1  # Alternate direction
            
            # Calculate actual height for last row to fill any gap
            current_row_height = min(row_height, 
                                   constants.SCREEN_HEIGHT - (row * row_height))
            
            while animation_width < constants.SCREEN_WIDTH:
                animation_width += animation_speed
                
                # Reset screen to original
                self.game.screen.blit(original_screen, (0, 0))
                
                # Draw all completed rows
                for completed_row in range(row):
                    completed_overlay = pygame.Surface((constants.SCREEN_WIDTH, row_height))
                    completed_overlay.set_alpha(128)
                    completed_overlay.fill(red_overlay)
                    self.game.screen.blit(completed_overlay, (0, completed_row * row_height))
                
                # Draw current animating row with adjusted height
                current_row_overlay = pygame.Surface((animation_width, current_row_height))
                current_row_overlay.set_alpha(128)
                current_row_overlay.fill(red_overlay)
                
                # Position based on direction
                x_pos = constants.SCREEN_WIDTH - animation_width if is_right_to_left else 0
                self.game.screen.blit(current_row_overlay, (x_pos, row * row_height))
                
                pygame.display.flip()
                self.game.clock.tick(30)            
            # After animation, draw messages
            messages = ["Game Over!", "You got hanged!", f"The word was '{self.game.current_word}'"]
            center_x = constants.SCREEN_WIDTH // 2
            base_y = constants.SCREEN_HEIGHT // 2 - 100
            line_spacing = 80
            box_padding = 30
    
        # Draw messages with boxes
        for i, msg in enumerate(messages):
            if i == 0:  # Game Over message
                text_surf = constants.FONT_LARGE.render(msg, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, base_y + (i * line_spacing)))
                box_rect = pygame.Rect(0, 0, 400, text_rect.height + box_padding)
                box_rect.centerx = center_x
                box_rect.centery = text_rect.centery
            else:
                text_surf = constants.FONT_MEDIUM.render(msg, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, base_y + (i * line_spacing)))
                box_rect = text_rect.inflate(box_padding * 2, box_padding)
            
            pygame.draw.rect(self.game.screen, constants.BUTTON_COLOR, box_rect)
            pygame.draw.rect(self.game.screen, constants.FONT_COLOR, box_rect, 3)
            self.game.screen.blit(text_surf, text_rect)
    
        # Setup buttons
        quit_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH // 2 - 200,
            constants.SCREEN_HEIGHT // 2 + 130,
            150, 50
        )
        try_again_button_rect = pygame.Rect(
            constants.SCREEN_WIDTH // 2 + 50,
            constants.SCREEN_HEIGHT // 2 + 130,
            150, 50
        )
    
        # Draw buttons
        pygame.draw.rect(self.game.screen, pygame.Color("#FF0000"), quit_button_rect)
        pygame.draw.rect(self.game.screen, constants.FONT_COLOR, quit_button_rect, 3)
        quit_text = constants.FONT_SMALL.render("Quit", True, constants.FONT_COLOR)
        self.game.screen.blit(quit_text, quit_text.get_rect(center=quit_button_rect.center))
    
        pygame.draw.rect(self.game.screen, pygame.Color("#00FF00"), try_again_button_rect)
        pygame.draw.rect(self.game.screen, constants.FONT_COLOR, try_again_button_rect, 3)
        try_text = constants.FONT_SMALL.render("Try Again", True, constants.FONT_COLOR)
        self.game.screen.blit(try_text, try_text.get_rect(center=try_again_button_rect.center))
    
        pygame.display.flip()
    
        # Event handling loop
        while self.game.popup_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    if try_again_button_rect.collidepoint(event.pos):
                        self.reset_game(reset_level=True)
                        self.game.popup_active = False
            
            self.game.clock.tick(30)    # GAME OVER


    # NEXT LEVEL
    def next_level(self):
        """Display a success pop-up message."""
        self.game.GameElements.shuffle_letters()
        self.game.popup_active = True
        center_x = constants.SCREEN_WIDTH // 2
        y_start = constants.SCREEN_HEIGHT // 2 - 100
        box_spacing = 70

        # Draw overlay
        overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(pygame.Color("#68c3a3"))
        self.game.screen.blit(overlay, (0, 0))

        # Define messages
        messages = [
            f"Level {self.game.level} Cleared!",
            "Congrats!",
            f"You guessed the word '{self.game.current_word}'!",
        ]

        # Draw messages
        for i, message in enumerate(messages):
            if i == 0:  # Level cleared message
                box_width = 400
                text_surf = constants.FONT_LARGE.render(message, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, y_start + (i * box_spacing)))
                box_rect = pygame.Rect(0, 0, box_width, text_rect.height + 30)
                box_rect.centerx = center_x
                box_rect.centery = text_rect.centery
            else:
                text_surf = constants.FONT_MEDIUM.render(message, True, constants.FONT_COLOR)
                text_rect = text_surf.get_rect(center=(center_x, y_start + (i * box_spacing)))
                box_rect = text_rect.inflate(40, 20)

            pygame.draw.rect(self.game.screen, constants.BUTTON_COLOR, box_rect)
            pygame.draw.rect(self.game.screen, constants.FONT_COLOR, box_rect, 3)
            self.game.screen.blit(text_surf, text_rect)

        pygame.display.flip()

        # Set a timer event for 2 seconds later
        pygame.time.set_timer(pygame.USEREVENT + 3, 2000)

        # Event loop waiting for the timer
        while self.game.popup_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.USEREVENT + 3:
                    # Timer finished
                    self.game.popup_active = False
                    pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                    # Proceed to next level
                    self.game.level += 1
                    self.game.hint_count += 1
                    self.reset_game()

            self.game.clock.tick(30)
    # NEXT LEVEL

    # RESET 
    def reset_game(self, reset_level=False):
        """Reset game state."""
        self.game.current_word = random.choice(self.game.WORD_LIST)
        self.game.guesses = []
        self.game.attempts = 0
        self.game.GameElements.shuffle_letters()
        self.game.timer_remaining = constants.TIMER_DURATION
        self.game.start_time = time.time()  
        if reset_level:
            self.game.level = 1             
            self.game.hint_count = 1        
    # RESET

    # CHECK GAME STATE
    def check_game_state(self):
        """Check win/lose conditions."""
        if self.game.attempts >= constants.MAX_ATTEMPTS or self.game.timer_remaining <= 0:
            self.game_over(reset_level=True)
        elif all(letter in self.game.guesses for letter in self.game.current_word):
            self.next_level()  # Removed extra .next_level()
    # CHECK GAME STATE

    # UPDATE TIMER
    def update_timer(self):
        """Update game timer."""
        elapsed_time = time.time() - self.game.start_time
        self.game.timer_remaining = constants.TIMER_DURATION - int(elapsed_time)
    # UPDATE TIMER