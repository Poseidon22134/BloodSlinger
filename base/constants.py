import pygame, os, sys

GL_VERSION = (3, 3, pygame.GL_CONTEXT_PROFILE_ES)
DEPTH_SIZE = 24

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
