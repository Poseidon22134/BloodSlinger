import pygame, moderngl as mgl, glm, numpy as np

class Sprite:
    def __init__(self, app, name, pixel=True): # type: ignore
        self.app = app
        self.ctx = app.ctx
        
        self.image = pygame.image.load(f"{app.dir}/assets/graphics/{name}").convert_alpha()
        self.size = glm.vec2(self.image.get_width(), self.image.get_height())
        
        self.texture: mgl.Texture = self.ctx.texture(glm.ivec2(self.size), 4, pygame.image.tobytes(self.image, 'RGBA'))
        if pixel: self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        
        s = self.size / self.app.resolution * self.app.scale
        self.vertices = np.array([
            -s.x, -s.y, 0.0, 1.0, # bottom-left
             s.x, -s.y, 1.0, 1.0, # bottom-right
             s.x,  s.y, 1.0, 0.0, # top-right
            -s.x,  s.y, 0.0, 0.0 # top-left
        ], dtype="f4")
        
        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype="i4")
        
        self.vbo_format = "2f 2f"
        self.attrs = ["vertexPosition", "vertexUV"]
        
        self.vbo = self.ctx.buffer(self.vertices)
        self.ibo = self.ctx.buffer(self.indices)
        
        self.program = self.app.shader_program.load_program("sprite")    
        
        self.vao = self.ctx.vertex_array(self.program, [
            (self.vbo, self.vbo_format, *self.attrs),
        ], self.ibo)
    
    def render(self):
        self.texture.use()
        self.vao.render()    

class AnimatedSprite:
    def __init__(self, app, camera, name, dimensions: glm.vec2, frame_duration: float, data: dict= None):     
        self.app = app
        self.ctx = app.ctx
        self.camera = camera
        
        self.image = pygame.image.load(f"{app.dir}/assets/graphics/{name}").convert_alpha()
        self.size = glm.vec2(self.image.get_width(), self.image.get_height())
        self.frame_size = self.size / dimensions
        
        self.frame_count = dimensions.x * dimensions.y
        self.frame_duration = frame_duration
        
        self.multi_animation = bool(data)
        if self.multi_animation:
            self.animations = data["animations"]
            self.animation = data["default"]
            self.animation_finished = False
        
        self.time = 0
        self.frame = 0
        
        self.texture: mgl.Texture = self.ctx.texture(glm.ivec2(self.size), 4, pygame.image.tobytes(self.image, 'RGBA'))
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        
        s = self.frame_size / self.app.resolution
        self.vertices = np.array([
            -s.x, -s.y, 0.0, 1.0, # bottom-left
             s.x, -s.y, 1.0, 1.0, # bottom-right
             s.x,  s.y, 1.0, 0.0, # top-right
            -s.x,  s.y, 0.0, 0.0 # top-left
        ], dtype="f4")
        
        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype="i4")
        
        self.vbo_format = "2f 2f"
        self.attrs = ["vertexPosition", "vertexUV"]
        
        self.vbo = self.ctx.buffer(self.vertices)
        self.ibo = self.ctx.buffer(self.indices)
        
        self.program = self.app.shader_program.load_program(["sprite", "animatedSprite"])
        self.program["dimensions"] = dimensions  
        
        self.vao = self.ctx.vertex_array(self.program, [
            (self.vbo, self.vbo_format, *self.attrs),
        ], self.ibo)
    
    def set_animation(self, animation):
        if not self.multi_animation or self.animation == animation:
            return
        self.animation = animation
        self.time = 0
        self.animation_finished = False
    
    def update(self):
        self.time += 1 / self.app.fps
        if self.multi_animation:
            if int(self.time / self.frame_duration) >= self.animations[self.animation]["frames"]:
                if self.animations[self.animation]["repeat"]:
                    self.time = 0
                else:
                    self.animation_finished = True
                    self.time = self.animations[self.animation]["frames"] * self.frame_duration
            self.frame = float(int(self.time / self.frame_duration) % self.animations[self.animation]["frames"]) + self.animations[self.animation]["frame_offset"]
        else:
            self.frame = float(int(self.time / self.frame_duration) % self.frame_count)
        
        self.program["frame"] = self.frame
    
    def render(self):
        self.texture.use()
        self.vao.render()   
        
class ProcSprite:
    def __init__(self, app, camera, size: glm.vec2):
        self.app = app
        self.ctx: mgl.Context = app.ctx
        self.camera = camera

        self.size = size

        s = self.size / self.app.resolution
        self.vertices = np.array([
            -s.x, -s.y, 0.0, 1.0, # bottom-left
             s.x, -s.y, 1.0, 1.0, # bottom-right
             s.x,  s.y, 1.0, 0.0, # top-right
            -s.x,  s.y, 0.0, 0.0 # top-left
        ], dtype="f4")
        
        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype="i4")
        
        self.vbo_format = "2f 2f"
        self.attrs = ["vertexPosition", "vertexUV"]
        
        self.vbo = self.ctx.buffer(self.vertices)
        self.ibo = self.ctx.buffer(self.indices)
        
        self.program = self.app.shader_program.load_program(["sprite", "procSprite"])
        self.program["size"] = self.size

        self.vao = self.ctx.vertex_array(self.program, [
            (self.vbo, self.vbo_format, *self.attrs),
        ], self.ibo)

        # junk
        self.animation_finished = True

    def set_animation(self, animation):
        pass

    def update(self):
        pass

    def render(self):
        self.vao.render()