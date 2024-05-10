#Run this code 
import pygame
import os

pygame.init()

screen_width = 400
screen_height = 400
grid_size = 8
square_size = screen_width // grid_size
screen = pygame.display.set_mode((screen_width, screen_height + 50))
pygame.display.set_caption("Grid Drawing")
grid = [[0] * grid_size for _ in range(grid_size)]

def draw_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            color = (0, 0, 0) if grid[i][j] == 1 else (255, 255, 255)
            pygame.draw.rect(screen, color, (i * square_size, j * square_size, square_size, square_size))

def toggle_square(pos):
    col = pos[0] // square_size
    row = pos[1] // square_size
    if 0 <= col < grid_size and 0 <= row < grid_size:
        grid[col][row] = 1 - grid[col][row]

def download_screenshot():
    screenshot = pygame.Surface((screen_width, screen_height))
    screenshot.blit(screen, (0, 0))
    pygame.image.save(screenshot, "screenshot.png")
font = pygame.font.Font(None, 36)
download_button = pygame.Rect(10, screen_height + 10, 250, 50)
pygame.draw.rect(screen, (0, 255, 0), download_button)
text = font.render("Download Screenshot", True, (0, 0, 0))
text_rect = text.get_rect(center=download_button.center)
screen.blit(text, text_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                toggle_square(event.pos)
            elif event.button == 3:
                download_screenshot()

    screen.fill((220, 220, 220))
    draw_grid()
    pygame.draw.rect(screen, (0, 255, 0), download_button)
    screen.blit(text, text_rect)
    pygame.display.flip()

pygame.quit()

