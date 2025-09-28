import glm, json, random

from render.mesh import Mesh
from scene.objects import Camera, TileMap, StaticObject
from scene.entities import Player, Animal
from render.sprite import AnimatedSprite, Sprite
from scene.physicsProcessor import PhysicsProcessor
from render.frameBuffer import FrameBuffer
# from scene.particles import Particle

class Campaign:
    def __init__(self, app):
        self.app = app

        self.renderBuffer = FrameBuffer(self.app, self.app.resolution)
        self.screen = Mesh(self.app, self.app.resolution, "postProcessing")

        self.physics_processor = PhysicsProcessor(self.app)

        self.player = Player(self.app, self)
        self.manaBar = AnimatedSprite(self.app, "Blood vials.png", glm.vec2(4, 3), 0.2, {
            "animations": {
                "0": {"frames": 1, "frame_offset": 0, "repeat": False},
                "1": {"frames": 1, "frame_offset": 1, "repeat": False},
                "2": {"frames": 1, "frame_offset": 2, "repeat": False},
                "3": {"frames": 1, "frame_offset": 3, "repeat": False},
                "4": {"frames": 1, "frame_offset": 4, "repeat": False},
                "5": {"frames": 1, "frame_offset": 5, "repeat": False},
                "6": {"frames": 1, "frame_offset": 6, "repeat": False},
                "7": {"frames": 1, "frame_offset": 7, "repeat": False},
                "8": {"frames": 1, "frame_offset": 8, "repeat": False},
                "9": {"frames": 1, "frame_offset": 9, "repeat": False},
            },
            "default": "9"
        })

        self.healthBar = Sprite(self.app, "health.png")
        self.healthmeter = Sprite(self.app, "healthbar.png")

        self.particles = []
        self.animals = [
            Animal(self.app, self, "f", position=glm.vec2(64, 0)),
            Animal(self.app, self, "r", position=glm.vec2(-64, 0)),
            Animal(self.app, self, "b", position=glm.vec2(0, 64)),
        ]

        with open(f"{self.app.dir}/assets/maps/test.json", "r") as f:
            data = json.load(f)
            tile_layout = data["tile_layout"]
            position = glm.vec2(data["position"])
        self.tilemap = TileMap(self.app, self, "tileset.png", tilemap_dimensions=glm.vec2(4, 4), tile_layout=tile_layout, position=position, collision=True)
        self.alter = StaticObject(self.app, self, "Sacrifice bowl.png", glm.vec2(0, 32))

        self.camera = Camera(self.app, glm.vec2(0), anchor=self.player.physics_body.position, target_offset=glm.vec2(0))
    
    def update(self):
        self.player.update()
        self.manaBar.set_animation(str((27 - min(self.player.mana, 25)) // 3))
        self.manaBar.update()

        if glm.abs(self.alter.position.x - self.player.physics_body.position.x) < 32 and glm.abs(self.alter.position.y - self.player.physics_body.position.y) < 64:
            for animal in self.animals:
                if animal.animal_alignment == "d" and animal.physics_body.acceleration == glm.vec2(0):
                    self.animals.remove(animal)
                    self.physics_processor.remove(animal.physics_body)
                    self.player.sacrificed += 1
                    self.player.mana += 1  

                    # if self.player.sacrificed == 10:
                        # self.tilemap.tile_layout         
        
        random_pos = glm.ivec2(random.randint(0, len(self.tilemap.tile_layout[0])-1), random.randint(0, len(self.tilemap.tile_layout)-1))
        if self.tilemap.tile_layout[random_pos.y][random_pos.x] == 1 and len(self.animals) < 50:
            self.animals.append(Animal(self.app, self, random.choice(["r", "c", "b", "f"]), position=glm.vec2(random_pos) * self.tilemap.tile_size + self.tilemap.position + glm.vec2(0, 48)))

        for animal in self.animals:
            animal.update()
            pass
        for particle in self.particles:
            particle.update()

        self.physics_processor.update()

        self.camera.target_offset = self.player.physics_body.velocity * glm.vec2(0.2, 0)
        self.camera.update()
    
    def render(self):
        self.renderBuffer.use()

        # render some stuff
        self.tilemap.render()
        self.alter.render()

        for particle in self.particles:
            particle.render()

        self.player.render()
        
        for animal in self.animals:
            animal.render()

        self.manaBar.program["position"] = glm.vec2(-0.45, 0.4)
        self.manaBar.program["scale"] = glm.vec2(2)
        self.manaBar.render()

        self.healthBar.program["position"] = glm.vec2(-0.25, 0.42)
        self.healthBar.program["scale"] = glm.vec2(1)
        self.healthBar.render()

        self.renderBuffer.reset()
        # repeat for multiple frames
        self.renderBuffer.use_texture()
        self.screen.render()