import glm

from render.mesh import Mesh
from scene.objects import Camera, TileMap
from scene.entities import Player
from scene.physicsProcessor import PhysicsProcessor
from render.frameBuffer import FrameBuffer

class Campaign:
    def __init__(self, app):
        self.app = app

        self.renderBuffer = FrameBuffer(self.app, self.app.resolution)
        self.screen = Mesh(self.app, self.app.resolution, "postProcessing")

        self.physics_processor = PhysicsProcessor(self.app)

        self.player = Player(self.app, self)

        self.camera = Camera(self.app, glm.vec2(0), anchor=self.player.physics_body.position, target_offset=glm.vec2(0))
    
    def update(self):
        self.player.update()
        self.physics_processor.update()

        self.camera.update()
    
    def render(self):
        self.renderBuffer.use()

        # render some stuff
        # self.tilemap.render()

        self.player.render()

        self.renderBuffer.reset()
        # repeat for multiple frames
        self.renderBuffer.use_texture()
        self.screen.render()