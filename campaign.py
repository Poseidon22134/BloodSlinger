import glm, json

from render.mesh import Mesh
from scene.objects import Camera, TileMap, StaticObject
from scene.entities import Player, Animal
from scene.physicsProcessor import PhysicsProcessor
from render.frameBuffer import FrameBuffer

class Campaign:
    def __init__(self, app):
        self.app = app

        self.renderBuffer = FrameBuffer(self.app, self.app.resolution)
        self.screen = Mesh(self.app, self.app.resolution, "postProcessing")

        self.physics_processor = PhysicsProcessor(self.app)

        self.player = Player(self.app, self)

        self.cat = Animal(self.app, self, "f", position=glm.vec2(64, 0))
        self.rabbit = Animal(self.app, self, "r", position=glm.vec2(-64, 0))

        with open(f"{self.app.dir}/assets/maps/test.json", "r") as f:
            data = json.load(f)
            tile_layout = data["tile_layout"]
            position = glm.vec2(data["position"])
        self.tilemap = TileMap(self.app, self, "tileset.png", tilemap_dimensions=glm.vec2(4, 4), tile_layout=tile_layout, position=position, collision=True)
        self.alter = StaticObject(self.app, self, "Sacrifice bowl.png", glm.vec2(0, 32))

        self.camera = Camera(self.app, glm.vec2(0), anchor=self.player.physics_body.position, target_offset=glm.vec2(0))
    
    def update(self):
        self.cat.update()
        self.rabbit.update()
        self.player.update()
        self.physics_processor.update()

        self.camera.target_offset = self.player.physics_body.velocity * glm.vec2(0.2, 0)
        self.camera.update()
    
    def render(self):
        self.renderBuffer.use()

        # render some stuff
        self.tilemap.render()
        self.alter.render()

        self.cat.render()
        self.rabbit.render()

        self.player.render()

        self.renderBuffer.reset()
        # repeat for multiple frames
        self.renderBuffer.use_texture()
        self.screen.render()