import moderngl as mgl, pygame, glm, numpy as np

class Mesh:
    def __init__(self, app, size: glm.ivec2 | glm.vec2, shaderprogram: str | list[str]="default"):
        self.app = app
        self.ctx: mgl.Context = app.ctx
        
        # convert to vec2 from possible ivec2 as even though this is a pixel size for the mesh it needs to be a float (f4).
        self.size = glm.vec2(size)
        s = self.size / self.app.resolution
        
        self.vertices = np.array([
            -s.x, -s.y, 0.0, 0.0, # bottom-left
             s.x, -s.y, 1.0, 0.0, # bottom-right
             s.x,  s.y, 1.0, 1.0, # top-right
            -s.x,  s.y, 0.0, 1.0 # top-left
        ], dtype="f4")
        
        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype="i4")
        
        self.vbo_format = "2f 2f"
        self.attrs = ["vertexPosition", "vertexUV"]
        
        self.vbo = self.ctx.buffer(self.vertices)
        self.ibo = self.ctx.buffer(self.indices)
        
        self.program = self.app.shader_program.load_program(shaderprogram)
        
        self.vao = self.ctx.vertex_array(self.program, [
            (self.vbo, self.vbo_format, *self.attrs),
        ], self.ibo)
        
        # self.texture = Texture(self.app, self.ctx, "player/Idle.png")
    
    # previously implemented def reload. unsure of necessity now. can implement later if needed.
    
    def render(self):
        # self.texture.bind()
        self.vao.render()
        