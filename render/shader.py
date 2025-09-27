import moderngl as mgl

class ShaderProgram:
    def __init__(self, ctx, dir):
        self.ctx = ctx
        self.dir = dir
        
        # self.programs = {}
    
    def load_program(self, name):
        # if str(name) not in self.programs:
        if isinstance(name, list):
            vs, fs = name
        else:
            vs = fs = name
        with open(f"{self.dir}/shaders/{vs}.vert", "r") as f:
            vert = f.read()
        with open(f"{self.dir}/shaders/{fs}.frag", "r") as f:
            frag = f.read()
        # self.programs[str(name)] = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
        # return self.programs[str(name)]
        return self.ctx.program(vertex_shader=vert, fragment_shader=frag)

# Test - to complete and test in future when rendering is implemented completely
# class ComputeProgram:
#     def __init__(self, ctx):
#         self.ctx = ctx
        
#         self.programs = {}
    
#     def load_program(self, name):
#         if str(name) not in self.programs:
#             with open(f"{dir}/shaders/{name}.comp", "r") as f:
#                 comp = f.read()
#             self.programs[str(name)] = self.ctx.compute_shader(comp)
#         return self.programs[str(name)]
