import moderngl as mgl, glm, pygame, json, numpy as np

from render.mesh import Mesh
from scene.objects import Camera, TileMap
from render.frameBuffer import FrameBuffer

class MapEditor:
    def __init__(self, app):
        self.app = app

        self.camera = Camera(self.app, glm.vec2(0))

        self.renderBuffer = FrameBuffer(self.app, self.app.resolution)
        self.screen = Mesh(self.app, self.app.resolution, "postProcessing")

        self.tilemap = TileMap(self.app, self, "tileset.png", tilemap_dimensions=glm.vec2(4), tile_layout=[[0]], position=glm.vec2(-512))

        self.world_center = Mesh(self.app, glm.vec2(8, 8), ['sprite', 'fire'])

        self.current_tile = 1
        self.keydown = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.camera.position += glm.vec2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_UP] - keys[pygame.K_DOWN]) * 10

        tile_pos = glm.floor(self.app.mouse_position - self.tilemap.position + self.camera.position + self.app.resolution / 2 * glm.vec2(-1, 1)) // self.tilemap.tile_size

        if keys[pygame.K_MINUS]:
            if not self.keydown:
                self.current_tile = (self.current_tile - 1) % (self.tilemap.tilemap_dimensions.x * self.tilemap.tilemap_dimensions.y)
            self.keydown = True
        elif keys[pygame.K_EQUALS]:
            if not self.keydown:
                self.current_tile = (self.current_tile + 1) % (self.tilemap.tilemap_dimensions.x * self.tilemap.tilemap_dimensions.y)
            self.keydown = True
        else:
            self.keydown = False

        if keys[pygame.K_q]:
            print(self.app.mouse_position + self.camera.position + self.app.resolution / glm.vec2(-2, 2))

        if pygame.mouse.get_pressed()[1] or pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            # Check bounds
            if 0 <= tile_pos.x < len(self.tilemap.tile_layout[0]) and 0 <= tile_pos.y < len(self.tilemap.tile_layout):
                tile = self.tilemap.tile_layout[int(tile_pos.y)][int(tile_pos.x)]
                if tile > 0:
                    self.current_tile = tile
                    print(self.current_tile)

        if pygame.mouse.get_pressed()[0]:
            # Left
            if tile_pos.x < 0:
                x_offset = -tile_pos.x
                for x in range(int(x_offset)):
                    for y in range(len(self.tilemap.tile_layout)):
                            self.tilemap.tile_layout[y].insert(0, 0)
                    self.tilemap.position.x -= self.tilemap.tile_size
                tile_pos.x = 0
            
            # Bottom (Bottom on screen, top of nested list)
            if tile_pos.y < 0:
                y_offset = -tile_pos.y
                for y in range(int(y_offset)):
                    self.tilemap.tile_layout.insert(0, [0] * len(self.tilemap.tile_layout[0]))
                self.tilemap.position.y -= self.tilemap.tile_size * y_offset
                tile_pos.y = 0

            # Right
            if tile_pos.x >= len(self.tilemap.tile_layout[0]):
                x_offset = tile_pos.x - len(self.tilemap.tile_layout[0]) + 1
                for x in range(int(x_offset)):
                    for y in range(len(self.tilemap.tile_layout)):
                        self.tilemap.tile_layout[y].append(0)
                tile_pos.x = len(self.tilemap.tile_layout[0]) - 1

            # Top (Top on screen, bottom of nested list)
            if tile_pos.y >= len(self.tilemap.tile_layout): 
                y_offset = tile_pos.y - len(self.tilemap.tile_layout) + 1
                for y in range(int(y_offset)):
                    self.tilemap.tile_layout.append([0] * len(self.tilemap.tile_layout[0]))
                tile_pos.y = len(self.tilemap.tile_layout) - 1

            self.tilemap.tile_layout[int(tile_pos.y)][int(tile_pos.x)] = self.current_tile  # Set tile to 1 (or any other value you want)
        
        if pygame.mouse.get_pressed()[2]: 
            # Check bounds
            if 0 <= tile_pos.x < len(self.tilemap.tile_layout[0]) and 0 <= tile_pos.y < len(self.tilemap.tile_layout):
                self.tilemap.tile_layout[int(tile_pos.y)][int(tile_pos.x)] = 0

        self.tilemap.update_tilemap()

        if pygame.key.get_pressed()[pygame.K_w]:
            with open(f"{self.app.dir}/assets/maps/test.json", "w") as f: # {input('map name:')}
                json.dump({"tile_layout": self.tilemap.tile_layout, "position": tuple(self.tilemap.position)}, f)
        
        if pygame.key.get_pressed()[pygame.K_l]:
            with open(f"{self.app.dir}/assets/maps/test.json", "r") as f:
                data = json.load(f)
                self.tilemap.tile_layout = data["tile_layout"]
                self.tilemap.position = glm.vec2(data["position"])
        
    def render(self):
        self.renderBuffer.use()

        self.tilemap.render()

        # self.cursor_indicator.program["position"] = self.app.mouse_position / self.app.resolution + glm.vec2(-0.5, 0.5)

        self.world_center.program["position"] = -self.camera.position / (self.app.resolution) # type: ignore
        self.world_center.render()

        self.renderBuffer.reset()
        self.renderBuffer.use_texture()
        self.screen.render()
