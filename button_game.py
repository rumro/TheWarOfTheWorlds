import pygame


class Button:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height

    def draw(self, x, y, massage, action=None, font_size=10):
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(self.game.screen, (255, 20, 147), (x, y, self.width, self.height))
            if mouse_click[0] == 1:
                if action is not None:
                    if action == quit:
                        pygame.quit()
                    else:
                        action()
        self.game.print_text(massage, x + 30, y + 15)
