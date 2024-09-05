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
from typing import Optional, Union, List


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

    if not texture:
        print(f"Failed to generate texture for {filename}")
        return None

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


def perspective(fov: Union[int, float], aspect: float, zNear: float, zFar: float) -> np.ndarray:
    """Returns the perspective projection matrix equivalent to gluPerspective.

    Args:
        fov (Union[int, float]): Field of view in degrees.
        aspect (float): Aspect ratio of the view (width/height).
        zNear (float): Near clipping plane.
        zFar (float): Far clipping plane.

    Returns:
        np.ndarray: The perspective projection matrix.
    """
    fovR = math.radians(fov)
    f = 1.0 / math.tan(fovR / 2.0)
    return np.array([
        [f / aspect, 0.0, 0.0, 0.0],
        [0.0, f, 0.0, 0.0],
        [0.0, 0.0, (zFar + zNear) / (zNear - zFar), -1.0],
        [0.0, 0.0, (2.0 * zFar * zNear) / (zNear - zFar), 0.0]
    ], dtype=np.float32)


def lookAt(eye: np.ndarray, center: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Returns the view matrix equivalent to gluLookAt.

    Args:
        eye (Union[List[float], np.ndarray]): The position of the camera.
        center (Union[List[float], np.ndarray]): The point to look at.
        up (Union[List[float], np.ndarray]): The up direction.

    Returns:
        np.ndarray: The view matrix.
    """
    eye = np.array(eye, dtype=np.float32)
    center = np.array(center, dtype=np.float32)
    up = np.array(up, dtype=np.float32)

    forward = center - eye
    forward /= np.linalg.norm(forward)

    up /= np.linalg.norm(up)

    side = np.cross(forward, up)
    up = np.cross(side, forward)

    m = np.identity(4, dtype=np.float32)
    m[0, :3] = side
    m[1, :3] = up
    m[2, :3] = -forward

    t = np.identity(4, dtype=np.float32)
    t[:3, 3] = -eye

    return m @ t


def loadShaders(vertex_shader_source: str, fragment_shader_source: str) -> int:
    """Load vertex and fragment shaders from strings and create a shader program.

    Args:
        vertex_shader_source (str): The source code of the vertex shader.
        fragment_shader_source (str): The source code of the fragment shader.

    Returns:
        int: The shader program ID.

    Raises:
        RuntimeError: If shader compilation or program linking fails.
    """
    # Compile vertex shader
    vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    # Compile fragment shader
    fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)

    # Create the program object
    program = glCreateProgram()
    if not program:
        raise RuntimeError('glCreateProgram failed!')

    # Attach shaders
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)

    # Link the program
    glLinkProgram(program)

    # Check the link status
    linked = glGetProgramiv(program, GL_LINK_STATUS)
    if not linked:
        info_len = glGetProgramiv(program, GL_INFO_LOG_LENGTH)
        info_log = ""
        if info_len > 1:
            info_log = glGetProgramInfoLog(program, info_len, None)
        glDeleteProgram(program)
        raise RuntimeError(f"Error linking program:\n{info_log}\n")

    return program
