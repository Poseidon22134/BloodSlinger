import glm, pygame, moderngl as mgl, numpy as np, random

from render.mesh import Mesh
from scene.physicsProcessor import StaticTileMapBody

class Camera:
    def __init__(self, app, position, anchor=None, target_offset=None):
        self.app = app
        
        self.position = position
        self.offset = glm.vec2(0)

        self.anchored = anchor and target_offset
        self.anchor = anchor
        self.target_offset = target_offset
    
    def update(self):
        if self.anchored:
            self.offset = glm.lerp(self.offset, self.target_offset, 0.08)
            self.position = self.anchor + self.offset

class StaticObject:
    def __init__(self, app, parent, name, position=glm.vec2(0)):
        self.app = app
        self.parent = parent

        self.position = position

        self.image = pygame.image.load(f"{app.dir}/assets/graphics/{name}").convert_alpha()
        self.size = glm.vec2(self.image.get_width(), self.image.get_height())
        self.texture: mgl.Texture = self.app.ctx.texture(glm.ivec2(self.size), 4, pygame.image.tobytes(self.image, 'RGBA', flipped=True))
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)

        self.mesh = Mesh(self.app, self.size, "sprite")

    def render(self):
        self.texture.use()
        self.mesh.program["position"] = (self.position - self.parent.camera.position) / self.app.resolution
        self.mesh.render()

class TileMap:
    def __init__(self, app, parent, name, tile_size=32, tilemap_dimensions=glm.vec2(32), tile_layout=None, position=glm.vec2(0), collision=False):
        self.app = app
        self.parent = parent

        self.position = position

        self.tilemap_dimensions = tilemap_dimensions
        self.tile_size = tile_size
        
        self.image = pygame.image.load(f"{app.dir}/assets/graphics/atlas/{name}").convert_alpha()
        self.size = glm.vec2(self.image.get_width(), self.image.get_height())
        self.texture: mgl.Texture = self.app.ctx.texture(glm.ivec2(self.size), 4, pygame.image.tobytes(self.image, 'RGBA'))
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)

        self.mesh = Mesh(self.app, self.app.resolution, ["sprite", "tilemap"])

        self.mesh.program["tileSize"] = self.tile_size
        self.mesh.program["tilemapDimensions"] = self.tilemap_dimensions
        self.mesh.program["screenResolution"] = self.app.resolution

        self.mesh.program["tilemap"] = 0
        self.mesh.program["tilemapLayout"] = 1

        self.tile_layout = tile_layout

        self.update_tilemap()

        if collision:
            self.physics_body = StaticTileMapBody(self.app, self)
            self.parent.physics_processor.add_body(self.physics_body)
    
    def update_tilemap(self):
        new_tiles = np.array(self.tile_layout, dtype=np.int32)

        # If the tilemap size has changed, we need to recreate the texture
        if hasattr(self, 'tiles') and self.tiles.shape == new_tiles.shape:
            self.tiles = new_tiles
            self.tilemap_texture.write(self.tiles.tobytes())
        else:
            self.tiles = new_tiles
            if hasattr(self, 'tilemap_texture'):
                self.tilemap_texture.release()
            self.tilemap_texture: mgl.Texture = self.app.ctx.texture((self.tiles.shape[1], self.tiles.shape[0]), 1, self.tiles.tobytes(), dtype="i4")
            self.tilemap_texture.filter = (mgl.NEAREST, mgl.NEAREST)
    
    def render(self):
        self.tilemap_texture.use(1)
        self.texture.use(0)

        self.mesh.program["offset"] = glm.ivec2(self.parent.camera.position - self.position)
        self.mesh.program["mapScale"] = glm.vec2(1)
        self.mesh.render()

class TileCursor:
    def __init__(self, app, parent, tilemap, position=glm.vec2(0), tile_size=32):
        self.app = app
        self.parent = parent
        self.tilemap = tilemap

        self.position = position
        self.tile_size = tile_size

        self.mesh = Mesh(self.app, glm.vec2(tile_size), ["sprite", "tileCursor"])
        self.mesh.program["tileSize"] = tile_size
