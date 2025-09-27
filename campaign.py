import glm

from render.mesh import Mesh
from scene.objects import Camera, TileMap, StaticObject
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

        tile_layout = []

        with open("test.txt", "r") as file:
            lines = file.readlines()

            for line in lines:
                tile_layout.insert(0, [])
                for tile in line:
                    try:
                        tile_layout[0].append(int(tile))
                    except ValueError:
                        pass

        self.tilemap = TileMap(self.app, self, "tileset.png", tilemap_dimensions=glm.vec2(4, 4), tile_layout=tile_layout, position=glm.vec2(-128, -64), collision=True)
        self.alter = StaticObject(self.app, self, "Sacrifice bowl.png", glm.vec2(0, 16))

        self.camera = Camera(self.app, glm.vec2(0), anchor=self.player.physics_body.position, target_offset=glm.vec2(0))
    
    def update(self):
        self.player.update()
        self.physics_processor.update()

        self.camera.target_offset = self.player.physics_body.velocity * glm.vec2(0.2, 0)
        self.camera.update()
    
    def render(self):
        self.renderBuffer.use()

        # render some stuff
        self.tilemap.render()
        self.alter.render()

        self.player.render()

        self.renderBuffer.reset()
        # repeat for multiple frames
        self.renderBuffer.use_texture()
        self.screen.render()