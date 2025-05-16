import pygame
from src.renderers.base_renderer import BaseRenderer

# Compatibility layer for backwards compatibility
class Renderer(BaseRenderer):
    """
    This class is maintained for backwards compatibility.
    It extends BaseRenderer from the new modular renderer system.
    """
    pass 