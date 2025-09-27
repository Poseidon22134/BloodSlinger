import moderngl as mgl, glm

class FrameBuffer:
    def __init__(self, app, resolution):
        self.app = app
        self.ctx: mgl.Context = app.ctx

        self.resolution = resolution
        self.fbo = self.ctx.framebuffer(color_attachments=[self.ctx.texture(glm.ivec2(self.resolution), 4)])
        self.fbo.color_attachments[0].repeat_x = False
        self.fbo.color_attachments[0].repeat_y = False
        self.fbo.color_attachments[0].filter = (mgl.NEAREST, mgl.NEAREST)
    
    def use(self):
        self.fbo.clear()
        self.fbo.use()
    
    def reset(self):
        self.ctx.screen.use()
        self.ctx.clear()
    
    def use_texture(self, location=0):
        self.fbo.color_attachments[0].use(location)
