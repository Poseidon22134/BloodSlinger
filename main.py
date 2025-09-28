import pygame, glm, asyncio

from base.main import App
from campaign import Campaign
from mapEditor import MapEditor
from base.constants import app_path
# from menus import TitleScreen

class Metroidvania(App):
    def __init__(self):
        self.scale = 2
        self.resolution: glm.vec2 = glm.vec2(640, 360)
        super().__init__(self.resolution * self.scale)

        pygame.mixer_music.load(f"{app_path}/assets/Bg Music.mp3")
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)

        self.state = Campaign(self)
        # self.state = MapEditor(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                self.running = False

    def update(self):
        self.mouse_position = (
            glm.vec2(*pygame.mouse.get_pos()) / self.scale * glm.vec2(1, -1)
        )

        self.state.update()

    def render(self):
        self.ctx.screen.clear()

        self.state.render()

        pygame.display.flip()

if __name__ == "__main__":
    game = Metroidvania()
    asyncio.run(game.run())
