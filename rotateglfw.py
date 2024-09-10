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
import argparse

class Scene:
    """OpenGL 3D scene class"""

    def __init__(self, vertex_data=None, n=4):
        
        # Store the tiling factor
        self.n = math.floor(n/4)
        
        # Load shaders and set up shader uniforms
        self.init_shaders()

        # Initialize buffers
        if vertex_data is None:
            # Vertex data with positions and texture coordinates
            vertex_data = np.array([
                # Positions        # Texture Coordinates
                -0.5, -0.5, 0.0,    0.0, 0.0,  # Bottom-left
                0.5, -0.5, 0.0,    4.0, 0.0,  # Bottom-right
                -0.5,  0.5, 0.0,    0.0, 4.0,  # Top-left
                0.5,  0.5, 0.0,    4.0, 4.0   # Top-right
            ], dtype=np.float32)

        self.init_buffers(vertex_data)

        # Load textures
        self.init_textures()

        # Time variable for animation
        self.t = 0

        # Toggle for showing the circle
        self.showCircle = False

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
            self.uTilingFactor = glGetUniformLocation(self.program, b'uTilingFactor')
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
        
        
        # Set vertex attribute pointers
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))  # Position
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(12)) # Texture Coord

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
        glUniform1f(self.uTilingFactor, self.n)  # Pass the tiling factor (n)
        glUniform1i(self.showCircleLoc, self.showCircle)

        # Bind and render texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glUniform1i(self.tex2D, 0)

        # Bind VAO and draw
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(0)

    def step(self):
        """Advance the scene's animation."""
        self.t = (self.t + 1) % 360


class RenderWindow:
    """GLFW Rendering window class"""

    def __init__(self, width: int = 800, height: int = 600, title: str = 'rotateglfw', n: int = 4):
        """Initialize the rendering window."""
        self.width = width
        self.height = height
        self.aspect = width / float(height)
        self.title = title
        self.window: Optional[glfw._GLFWwindow] = None

        logging.info("Initializing GLFW")
        if not glfw.init():
            logging.error("Failed to initialize GLFW")
            raise RuntimeError("Failed to initialize GLFW")

        self.configure_glfw()
        self.window = glfw.create_window(
            self.width, self.height, self.title, None, None)
        if not self.window:
            logging.error("Failed to create GLFW window")
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        self.create_context()
        self.configure_opengl()

        self.scene = Scene(n=n)
        glfw.set_framebuffer_size_callback(
            self.window, self.framebuffer_size_callback)
        glfw.set_key_callback(self.window, self.on_keyboard)
        atexit.register(self.cleanup)

    def configure_glfw(self):
        """Configure GLFW settings."""
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    def configure_opengl(self):
        """Configure OpenGL settings."""
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.5, 0.5, 1.0)

    def create_context(self):
        """Create the OpenGL context."""
        if not self.window:
            logging.error("Cannot make context current, no window available.")
            raise RuntimeError(
                "Cannot make context current, no window available.")

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Enable VSync
        logging.info("OpenGL context created and VSync enabled")

    def framebuffer_size_callback(self, window: glfw._GLFWwindow, width: int, height: int):
        """Handle framebuffer size changes."""
        if height == 0:
            height = 1  # Avoid division by zero, set height to 1
        glViewport(0, 0, width, height)
        self.width, self.height = width, height
        self.aspect = width / float(height)

    def on_keyboard(self, window, key, scancode, action, mods):
        """Handle keyboard input."""
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                logging.info("ESC pressed, closing window.")
                glfw.set_window_should_close(self.window, True)
            else:
                logging.info(f"Key {key} pressed.")


    def render(self, delta_time: float):
        """Render the scene."""
        self.width, self.height = glfw.get_framebuffer_size(self.window)
        self.aspect = self.width / float(self.height)

        glViewport(0, 0, self.width, self.height)
        pMatrix = utils.perspective(45.0, self.aspect, 0.1, 100.0)
        mvMatrix = utils.lookAt(
            [0.0, 0.0, -2.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0])

        self.scene.render(pMatrix, mvMatrix)
        self.scene.step()

    def run(self, target_fps: int = 60):
        """Main rendering loop with frame rate limiting."""
        previous_time = glfw.get_time()
        frame_time = 1.0 / target_fps

        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            delta_time = current_time - previous_time

            # Catch up with missed frames
            while delta_time >= frame_time:
                previous_time += frame_time
                delta_time -= frame_time

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self.render(frame_time)

                glfw.swap_buffers(self.window)
                glfw.poll_events()

    def cleanup(self):
        """Cleanup resources."""
        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()
        logging.info("GLFW terminated")


def main():
    """Main function to start the application."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='RotateGLFW with customizable tiling.')
    parser.add_argument('-n', type=int, default=4, help='Number of tiles along each axis (n x n tiling).')
    args = parser.parse_args()
    render_window = None
    try:
        render_window = RenderWindow(n=args.n)
        render_window.run()
    except RuntimeError as e:
        logging.error(f"An error occurred in the application: {e}")
    finally:
        if render_window:
            render_window.cleanup()


# Call main
if __name__ == '__main__':
    main()
