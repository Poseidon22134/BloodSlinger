import pygame, moderngl as mgl, glm, os

from base.constants import GL_VERSION, DEPTH_SIZE
from render.shader import ShaderProgram

class App:
    def __init__(self, resolution: glm.vec2, fullscreen=False, resizable=False): # assume non-fullscreen and non-resizable for now
        pygame.init()
        
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, GL_VERSION[0])
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, GL_VERSION[1])
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, GL_VERSION[2])
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, DEPTH_SIZE)
        
        # init window here later
        self.window = pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.OPENGL, display=0, vsync=True)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'
         
        self.dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        self.shader_program = ShaderProgram(self.ctx, self.dir)
        # self.compute_program = ComputeProgram(self.ctx)
    
        self.clock = pygame.time.Clock()
        self.frame_rate = 0
        self.game_speed = 1
        self.min_frame_rate = 15
        self.fps = 0
        self.runtime = 0

        self.running = True
    
    def handle_events(self):
        pass
        
    def update(self):
        pass

    def render(self):
        pass
    
    def run(self):
        while self.running:
            self.clock.tick(self.frame_rate)
            self.fps = self.clock.get_fps()
            self.runtime += self.clock.get_time()
            
            if self.fps < self.min_frame_rate:
                continue # skip frame to avoid calculations with low fps.
            self.fps /= self.game_speed
            
            self.handle_events()
            self.update()
            self.render()
            
        pygame.quit()
