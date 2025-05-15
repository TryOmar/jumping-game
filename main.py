import pygame
import sys

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        # Setup game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jumping Ball Game")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        
    def handle_events(self):
        """Process all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Process keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game state"""
        # This will be filled with game logic later
        pass
    
    def render(self):
        """Draw everything to the screen"""
        # Clear the screen
        self.screen.fill(WHITE)
        
        # Draw a temporary rectangle to show the game is working
        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 50, 100, 100))
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Process input
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Render new frame
            self.render()
            
            # Control the game speed
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 