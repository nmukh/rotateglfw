"""
rotateglfw.py

Author: Nishat Mukherji

 PyOpenGL and glfw program using OpenGL to manipulate graphic.
"""

import glfw
import logging
from OpenGL.GL import *
from typing import Optional
import atexit
import utils
import math

import numpy as np


class Scene:
    """OpenGL 3D scene class"""
    def __init__(self, vertex_data=None):
        pass
    
    def init_shaders(self):
        """Load shaders and get uniform locations."""
        pass
    
    def init_buffers(self, vertex_data):
        """Set up VAO and buffers."""
        pass
    
    def init_textures(self):
        """Load textures."""
        pass    
    
    def render(self):
        """Render the scene."""
        pass    
    
    def step(self):
        """Update the scene."""
        pass
    

    
    
