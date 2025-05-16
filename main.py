import pygame
import sys
import os
from src.game import Game
from src.utils.path_utils import resource_path

# Initialize pygame
pygame.init()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 