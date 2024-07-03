import pygame
import sys
import random
import pygame_menu

pygame.init()
SIZE_BLOCK = 20
FRAME_COLOR = (0, 255, 204)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (204, 255, 255)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courer', 36)


class Snake_Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, Snake_Block) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = Snake_Block(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [Snake_Block(9, 8), Snake_Block(9, 9), Snake_Block(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f"Total:{total}", 0, WHITE)
        text_speed = courier.render(f"Speed:{speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                draw_block(color, row, column)
        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            break
            # pygame.quit()
            # sys.exit()
        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)
        pygame.display.flip()
        if apple == head:
            total += 1
            speed = total // 5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()
        d_row = buf_row
        d_col = buf_col
        new_head = Snake_Block(head.x + d_row, head.y + d_col)
        if new_head in snake_blocks:
            print('crash yourself')
            pygame.quit()
            sys.exit()

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        timer.tick(5 + speed)


main_theme = pygame_menu.themes.THEME_GREEN.copy()
main_theme.set_background_color_opacity(1.0)
menu = pygame_menu.Menu('Snake game', 400, 320,
                        theme=main_theme)

menu.add.text_input('Name :', default='Name1')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)