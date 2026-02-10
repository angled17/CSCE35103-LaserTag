import pygame


pygame.init()

class Game:
    def __init__(self, db):
        self.db = db

        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()
        self.running = True

        self.run_game()


    def run_game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("purple")

            pygame.display.flip()
            self.clock.tick(60)


        pygame.quit()