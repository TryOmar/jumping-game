import pygame
import sys
from src.game import Game

# Initialize pygame
pygame.init()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 