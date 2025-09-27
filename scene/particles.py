import glm

from render.sprite import AnimatedSprite
from scene.physicsProcessor import dynamicHurtBody


class Particle:
    def __init__(self, app, parent, ptype, position, direction=1):
        self.app = app
        self.parent = parent

        self.type = ptype

        self.direction = direction

        print(self.type)
        if self.type == "a1":
            self.sprite = AnimatedSprite(self.app, "spells.png", glm.vec2(2, 4), 0.1, {
                "animations": {
                    "a": {"frames": 4, "frame_offset": 0, "repeat": False}
                },
                "default": "a"
            })
            self.physics_body = dynamicHurtBody(self.app, position, glm.vec2(16), 1)
            self.parent.physics_processor.add_body(self.physics_body)
        elif self.type == "a2":
            self.sprite = AnimatedSprite(self.app, "spells.png", glm.vec2(1, 8), 0.1, {
                "animations": {
                    "a": {"frames": 4, "frame_offset": 4, "repeat": False}
                },
                "default": "a"
            })
            self.physics_body = dynamicHurtBody(self.app, position, glm.vec2(16), 1)
            self.parent.physics_processor.add_body(self.physics_body)
        else:
            return # Invalid type
    
    def update(self):
        self.sprite.update()
        print(self.sprite.animation_finished, self.physics_body.colliding["object"])
        if self.sprite.animation_finished:
            self.parent.physics_processor.remove(self.physics_body)
            self.parent.particles.remove(self)
            return

    
    def render(self):
        self.sprite.program["position"] = (self.physics_body.position - self.parent.camera.position) / self.app.resolution
        self.sprite.program["scale"] = glm.vec2(1)
        self.sprite.program["flipped"] = self.direction == -1
        self.sprite.render()