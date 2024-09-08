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
        """Load texture for the scene."""
        self.texId = utils.loadTexture('emoji.png')
        if self.texId is None:
            logging.error("Failed to load texture")
            raise RuntimeError("Failed to load texture")

    def render(self, pMatrix, mvMatrix):
        """Render the scene."""
        glUseProgram(self.program)

        # Set the uniform values for shaders
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, pMatrix)
        glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, mvMatrix)
        glUniform1f(self.uThetaLoc, math.radians(self.t))
        glUniform1i(self.showCircleLoc, self.showCircle)

        # Bind and render texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texId)
        glUniform1i(self.tex2D, 0)

        # Bind VAO and draw
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(0)

    def step(self):
        """Update the scene."""
        pass
