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
        try:
            with open('vertex_shader.glsl', 'r') as vs_file:
                vertex_shader_src = vs_file.read()
            with open('fragment_shader.glsl', 'r') as fs_file:
                fragment_shader_src = fs_file.read()

            self.program = utils.loadShaders(
                vertex_shader_src, fragment_shader_src)
            glUseProgram(self.program)
            self.pMatrixUniform = glGetUniformLocation(
                self.program, b'uPMatrix')
            self.mvMatrixUniform = glGetUniformLocation(
                self.program, b'uMVMatrix')
            self.tex2D = glGetUniformLocation(self.program, b'tex2D')
            self.uThetaLoc = glGetUniformLocation(self.program, b'uTheta')
            self.showCircleLoc = glGetUniformLocation(
                self.program, b'showCircle')
        except Exception as e:
            logging.error(f"Error loading shaders: {e}")
            raise

    def init_buffers(self, vertex_data):
        """Set up VAO and buffers."""
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertex_data),
                     vertex_data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindVertexArray(0)

    def init_textures(self):
        """Load textures."""
        pass

    def render(self):
        """Render the scene."""
        pass

    def step(self):
        """Update the scene."""
        pass
