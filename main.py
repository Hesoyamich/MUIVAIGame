import pygame

class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.f1 = pygame.font.Font(None, 36)
        SCREEN_HEIGHT, SCREEN_WIDTH = 1000, 1000

        self.is_running = True
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False


            self.display.fill((10,50,255))
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    g = Game()
    g.run()