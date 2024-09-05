"""
utils.py

Author: Nishat Mukherji

Helper functions for OpenGL.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from PIL import Image
import math
from typing import Optional

def loadTexture(filename: str) -> Optional[int]:
    """Load OpenGL 2D texture from given image file.

    Args:
        filename (str): Path to the image file.

    Returns:
        Optional[int]: The texture ID if successful, None otherwise.
    """
    try:
        img = Image.open(filename)
        imgData = np.array(list(img.getdata()), np.uint8)
    except IOError as e:
        print(f"Error loading image file {filename}: {e}")
        return None

    texture = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 
                 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture