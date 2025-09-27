import pygame, glm, random

from render.sprite import AnimatedSprite
from scene.physicsProcessor import dynamicBody

directions = {
  -1: "left",
  1: "right"
}

# my height: 172cm
# player height: 36px

# g = 9.81  # m/s
# g = 128
# PIXELS_PER_METER = 0.05
# GRAVITY = PIXELS_PER_METER * g
GRAVITY = 1024

FULL_JUMP = True

JUMP_VELOCITY = 416
LIFT = 8 # pixels up after release of jump button
LIFT_OFFSET = glm.sqrt(JUMP_VELOCITY ** 2 - 2 * GRAVITY * (JUMP_VELOCITY ** 2 / GRAVITY - JUMP_VELOCITY ** 2 / (2 * GRAVITY) - LIFT)) / GRAVITY

STOPPED_VELOCITY = 64
STOP_MODIFIER = 0.8

AIR_RESISTANCE = 0.995
GROUND_RESISTANCE = 16
DASH_FINISH_TIME = 0.1

DASH_VELOCITY = 512
DASH_DURATION = 0.2
DASH_COOLDOWN = 0.4

MAX_RUN_SPEED = 256
RUN_ACCELERATION = MAX_RUN_SPEED * GROUND_RESISTANCE * 4
MAX_FLOAT_SPEED = 128
FLOAT_ACCELERATION = MAX_FLOAT_SPEED * AIR_RESISTANCE * 4

DOUBLE_JUMP_ENABLED = False
DASH_ENABLED = True

COYOTE_TIME = 0.15

class Player:
    def __init__(self, app, parent):
        self.app = app
        self.parent = parent

        self.physics_body = dynamicBody(self.app, glm.vec2(0), glm.vec2(40, 90))
        self.parent.physics_processor.add_body(self.physics_body)

        self.sprite = AnimatedSprite(self.app, "player.png", glm.vec2(7, 1), 0.2, {
                "animations": {
                    "Idle": { "frames": 3, "frame_offset": 0, "repeat": True },
                    # "Run": { "frames": 8, "frame_offset": 11, "repeat": True },
                    # "Jump": { "frames": 1, "frame_offset": 19, "repeat": False },
                    # "Fall": { "frames": 6, "frame_offset": 20, "repeat": False },
                    # "Land": { "frames": 2, "frame_offset": 26, "repeat": False },
                    "Dash": { "frames": 4, "frame_offset": 3, "repeat": False }
                },
                "default": "Idle"                   
        })
        self.sprite_offset = glm.vec2(0)

        self.actions = [0] * 6
        self.state = 0
        self.direction = 1

        self.jump_timer = 0
        self.jump_end = 0
        self.max_jump = (JUMP_VELOCITY - glm.sqrt(2 * GRAVITY * LIFT)) / GRAVITY

        self.coyote_time = 0.1
        self.double_jump = True

        self.dash_reset = True
        self.dash_duration = 0
        self.dash_cooldown = 0

        self.paricle_timer = 0

        self.always_running = True
    
    def update(self):
        self.update_actions()
        self.handle_state()
        self.sprite.update()
    
    def update_actions(self):
        keys = pygame.key.get_pressed()
        actions = [
        keys[pygame.K_UP] | keys[pygame.K_w] | keys[pygame.K_z] | keys[pygame.K_SPACE],  # Jump
        keys[pygame.K_LEFT] | keys[pygame.K_a],  # left
        keys[pygame.K_RIGHT] | keys[pygame.K_d],  # right
        keys[pygame.K_LCTRL] | keys[pygame.K_RCTRL] | keys[pygame.K_LSHIFT] | self.always_running,  # Run
        keys[pygame.K_x],  # Attack
        keys[pygame.K_c] | keys[pygame.K_i]  # Dash
        ]
        for idx, action in enumerate(actions):
            if action:
                self.actions[idx] = 2 if self.actions[idx] else 1
            else:
                self.actions[idx] = 0
    
    def run(self, direction, running):
        if direction:
            self.direction = direction
            if self.physics_body.colliding["bottom"]:
                self.physics_body.velocity.x = MAX_RUN_SPEED * direction
                return True
            else:
                self.physics_body.velocity.x = max(MAX_FLOAT_SPEED, abs(self.physics_body.velocity.x)) * direction # this is technically broken as it allows for the player to switch direction quickly
            # I guess I'll just add this to run and dash then
        else:
            self.physics_body.velocity.x *= STOP_MODIFIER
            # I'll deal with this later

    def jump(self, inp):
        if self.jump_timer > 0: # already jumping
            self.physics_body.velocity.x *= AIR_RESISTANCE
            self.jump_timer += 1 / self.app.fps
            if self.physics_body.velocity.y <= 0: # falling
                self.jump_timer = 0
                self.jump_end = 0
                return False
            if (inp and not self.jump_end) or self.jump_end > self.max_jump or FULL_JUMP:
                self.physics_body.velocity.y = JUMP_VELOCITY - GRAVITY * self.jump_timer
            else:
                if self.jump_end == 0:
                    self.jump_end = self.jump_timer
                self.physics_body.velocity.y = JUMP_VELOCITY - GRAVITY * (self.jump_timer - self.jump_end + JUMP_VELOCITY / GRAVITY - LIFT_OFFSET)
            return True
        if inp == 1 and (self.physics_body.colliding["bottom"] or self.coyote_time or (self.double_jump and DOUBLE_JUMP_ENABLED)):
            self.jump_timer = 1 / self.app.fps
            self.physics_body.velocity.y = JUMP_VELOCITY
            self.double_jump = self.physics_body.colliding["bottom"] if self.coyote_time <= 0 else True
            self.coyote_time = 0 if self.physics_body.colliding["bottom"] else self.coyote_time
            return True 

    def dash(self, direction):
        if self.dash_cooldown <= 0 and self.dash_reset and DASH_ENABLED:
            self.physics_body.velocity.x = DASH_VELOCITY * (direction if direction else self.direction)
            self.dash_duration = DASH_DURATION
            self.dash_cooldown = DASH_COOLDOWN
            self.dash_reset = False

            # self.app.state.scene.particle_handler.add_child("dash", self.physics_body.position, direction=directions[self.direction])
            return True
        # I guess I'll just add this to run and dash then
        self.direction = direction if direction else self.direction

    def attack(self):
        pass

    def handle_state(self):
        print(self.state)
        
        if self.physics_body.colliding["bottom"]:
            self.dash_reset = True
            self.double_jump = True
            self.coyote_time = COYOTE_TIME
        else:
            self.coyote_time -= 1 / self.app.fps
            self.coyote_time = max(self.coyote_time, 0)
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1 / self.app.fps
            self.dash_cooldown = max(self.dash_cooldown, 0)
        
        if self.paricle_timer > 0:
            self.paricle_timer -= 1 / self.app.fps
            self.paricle_timer = max(self.paricle_timer, 0)
                        
        if self.state == 0: # Idle
            self.sprite.set_animation("Idle")

            if not self.physics_body.colliding["bottom"]:
                self.state = 2
                return # todo add some coyote time here

            if self.run(min(self.actions[2], 1) - min(self.actions[1], 1), self.actions[3]):
                self.state = 4
            
            if self.jump(self.actions[0]):
                self.state = 1
                return

            if self.actions[5]:
                if self.dash(min(self.actions[2], 1) - min(self.actions[1], 1)):
                    self.state = 5
        elif self.state == 1: # Jumping
            # self.sprite.set_animation("Jump")

            self.run(min(self.actions[2], 1) - min(self.actions[1], 1), self.actions[3])

            if not self.jump(self.actions[0]):
                self.state = 2

            if self.actions[5]:
                if self.dash(min(self.actions[2], 1) - min(self.actions[1], 1)):
                    self.state = 5
        elif self.state == 2: # Falling
            # self.sprite.set_animation("Fall")

            self.run(min(self.actions[2], 1) - min(self.actions[1], 1), self.actions[3])

            # if self.actions[1] and self.physics_body.colliding["left"]:
            #   self.physics_body.velocity.y = 2
            # elif self.actions[2] and self.physics_body.colliding["right"]:
            #   self.physics_body.velocity.y = 2
            if self.physics_body.colliding["bottom"]:
                self.state = 3

            if self.jump(self.actions[0]):
                self.state = 1
                return

            if self.actions[5]:
                if self.dash(min(self.actions[2], 1) - min(self.actions[1], 1)):
                    self.state = 5
        elif self.state == 3: # Landing
            # self.sprite.set_animation("Land")

            if abs(self.physics_body.velocity.x) < STOPPED_VELOCITY and self.sprite.animation_finished:
                self.state = 0

            if self.jump(self.actions[0]):
                self.state = 1
                return

            if self.run(min(self.actions[2], 1) - min(self.actions[1], 1), self.actions[3]):
                self.state = 4
        elif self.state == 4: # Running/Walking
            # self.sprite.set_animation("Run")

            self.run(min(self.actions[2], 1) - min(self.actions[1], 1), self.actions[3])

            if self.paricle_timer <= 0:
                # self.app.state.scene.particle_handler.add_child("dust", deepcopy(self.physics_body.position), direction=directions[self.direction])
                self.paricle_timer = random.uniform(0.2, 0.6)

            if not self.physics_body.colliding["bottom"]:
                self.state = 2
                self.sprite_offset.x = 0
                return

            if self.jump(self.actions[0]):
                self.state = 1
                self.sprite_offset.x = 0
                return

            if self.actions[5]:
                if self.dash(min(self.actions[2], 1) - min(self.actions[1], 1)):
                    self.state = 5
                    return

            if abs(self.physics_body.velocity.x) < STOPPED_VELOCITY:
                self.state = 0
        elif self.state == 5: # Dash
            self.sprite.set_animation("Dash")

            self.dash_duration -= 1 / self.app.fps
            self.physics_body.velocity.y = 0
            self.physics_body.acceleration.y = 0

            if self.dash_duration <= 0:
                self.physics_body.velocity.x *= max((1 - (2 * DASH_VELOCITY) / self.app.fps), 0)
                self.physics_body.acceleration.y = -GRAVITY
                if self.physics_body.colliding["bottom"]:
                    if self.run(min(self.actions[2], 1) - min(self.actions[1], 1), self.actions[3]):
                        self.state = 4
                        return
                    self.state = 3
                else:
                    self.state = 2
        elif self.state == 6: # Attacking
            # self.sprite.set_animation("Attack")

            if self.sprite.animation_finished:
                if self.physics_body.colliding["bottom"] and abs(self.physics_body.velocity.x) < STOPPED_VELOCITY:
                    self.state = 0
                else:
                    self.state = 4

    def render(self):
        self.sprite.program["position"] = (self.physics_body.position + self.sprite_offset - self.parent.camera.position) / self.app.resolution
        self.sprite.program["scale"] = glm.vec2(1)
        self.sprite.program["flipped"] = self.direction == -1
        self.sprite.render()

class Animal:
    def __init__(self, app, parent, animal_type, position):
        self.app = app
        self.parent = parent

        self.type = animal_type

        self.physics_body = dynamicBody(self.app, position, glm.vec2(16))