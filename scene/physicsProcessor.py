import glm

class CollisionBounds:
  def __init__(self, position, size):
    self.position = position
    self.size = size

class staticBody:
  type = "static"
  def __init__(self, position, size):
    # position is the center of the body, the size will extend half both ways
    self.position = position
    self.size = size

  def update(self):
    pass
  
  def get_collision_bounds(self, otherBody):
    col = abs(otherBody.position - self.position) < (otherBody.size + self.size) / 2
    if col.x and col.y:
      return [CollisionBounds(self.position, self.size)]

gravity = 1024

class dynamicBody:
  type = "dynamic"
  def __init__(self, app, position, size):
    self.app = app
    # position is the center of the body, the size will extend half both ways
    self.position = position
    self.size = size
    self.velocity = glm.vec2(0)
    self.acceleration = glm.vec2(0, -gravity)

    self.colliding = {"top": False, "bottom": False, "left": False, "right": False}

  def update(self):
    self.position += self.velocity / self.app.fps + 0.5 * self.acceleration / self.app.fps**2
    self.velocity += self.acceleration / self.app.fps

class StaticTileMapBody:
  type = "static"
  def __init__(self, app, tilemap):
    self.app = app
    self.tilemap = tilemap

    self.position = tilemap.position
    self.tile_size = tilemap.tile_size

  def get_collision_bounds(self, otherBody):
    # at first pretending the tilemap is located at origin.
    min_col_tile = glm.ivec2(glm.floor((otherBody.position - otherBody.size / 2 - self.position) / self.tile_size))
    max_col_tile = glm.ivec2(glm.ceil((otherBody.position + otherBody.size / 2 - self.position) / self.tile_size))

    covered_tiles = []
    for y in range(min_col_tile.y, max_col_tile.y):
        for x in range(min_col_tile.x, max_col_tile.x):
          if (0 <= int(y) < len(self.tilemap.tile_layout) and 0 <= int(x) < len(self.tilemap.tile_layout[0])) and self.tilemap.tile_layout[int(y)][int(x)] > 0:
            covered_tiles.append(CollisionBounds(self.position + glm.vec2(x, y) * self.tile_size + 0.5 * self.tile_size, glm.vec2(self.tile_size)))
    return covered_tiles if covered_tiles else None

class PhysicsProcessor:
  def __init__(self, app):
    self.app = app

    self.children = {
      "static": [],
      "dynamic": []
    }

  def add_body(self, body):
    self.children[body.type].append(body)

  def update(self):
    for child in self.children["dynamic"]:
      child.update()
      child.colliding = {"top": False, "bottom": False, "left": False, "right": False}

      for otherChild in self.children["static"]:

        collision_bounds = otherChild.get_collision_bounds(child) # returns a list of collision bounds. This way a regular static body can still be used, and just sends a single item in the list, but the tilemap can send multiple bounds if needed.
        if not collision_bounds:
          continue

        for body in collision_bounds:
          overlap = (child.size + body.size) / 2 - abs(child.position - body.position)
          collision_domain = glm.vec2(1, 0) if overlap.x < overlap.y else glm.vec2(0, 1)
          collision_direction = (child.position.x > body.position.x) if collision_domain.x else (child.position.y > body.position.y)
          if (collision_domain.x and child.colliding["right" if collision_direction else "left"]) or (collision_domain.y and child.colliding["top" if collision_direction else "bottom"]):
            collision_domain = collision_domain.yx
            collision_direction = (child.position.x > body.position.x) if collision_domain.x else (child.position.y > body.position.y)

          child.position += overlap * glm.sign(child.position - body.position) * collision_domain
          child.velocity -= (glm.min(child.velocity, glm.vec2(0)) if collision_direction else glm.max(child.velocity, glm.vec2(0))) * collision_domain

          child.colliding["left" if collision_direction else "right"] |= bool(collision_domain.x)
          child.colliding["bottom" if collision_direction else "top"] |= bool(collision_domain.y)