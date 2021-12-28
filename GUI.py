from ModuleBase import Module
import pygame
from pubsub import pub

class GUI(Module):
    def __init__(self):
        super().__init__()

        # init pygame modules
        pygame.display.init()
        pygame.font.init()

        pygame.display.set_caption("GUI")
        self.screen = pygame.display.set_mode((1920, 1080))

        self.background = pygame.Surface((1920, 1080))
        self.background.fill(pygame.Color('#00FF00'))
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

        self.movement = [0 for i in range(6)]
        pub.subscribe(self.movement_handler, "joystick.movement")

    def movement_handler(self, message):
        self.movement = message["joystick_movement"]

    def run(self):
        text = self.font.render(f"{self.movement}", False, (0,0,0))

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text, (0,0))
        pygame.display.flip()
