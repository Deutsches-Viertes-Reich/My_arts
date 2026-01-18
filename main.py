import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("My Game")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 128, 255))  # 画面を青く塗る
    pygame.display.flip()

pygame.quit()
