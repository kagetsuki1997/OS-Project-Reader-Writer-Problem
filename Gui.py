import pygame

pygame.init()
window_size = window_width, window_height = 1300, 700
gameWindow = pygame.display.set_mode(window_size)
pygame.display.set_caption("RW")
clock = pygame.time.Clock()

# Letter (writer, reader)
letter_size = letter_x, letter_y = 40, 40
# Bar
text_bar_width = 50
normal_bar_width = 5
# Block scheduling
schedule_capacity = schedule_num_row, schedule_num_col \
                  = 2, (window_width / letter_x)
schedule_size = schedule_width, schedule_height \
              = window_width, (schedule_num_row * letter_y)
schedule_point = schedule_x, schedule_y = 0, text_bar_width
# Writer_wait
w_wait_size = w_wait_width, w_wait_height \
            = ((window_width - 2 * normal_bar_width) / 3), \
                (window_height - schedule_height - 2 * text_bar_width)
w_wait_point = w_wait_x, w_wait_y = 0, (window_height - w_wait_height)
w_wait_capacity = w_num_row, w_num_col \
                = (w_wait_height / letter_y), (w_wait_width / letter_x)
# reader_wait
r_wait_size = r_wait_width, r_wait_height = w_wait_width, w_wait_height
r_wait_point = r_wait_x, r_wait_y = (window_width - r_wait_width), w_wait_y
r_wait_capacity = r_num_row, r_num_col \
                = (r_wait_height / letter_y), (r_wait_width / letter_x)
# file
file_size = file_width, file_height \
          = (window_width - w_wait_width - r_wait_width
             - 2 * normal_bar_width), w_wait_height
file_point = file_x, file_y = (w_wait_width + normal_bar_width), w_wait_y
file_capacity = file_num_row, file_num_col \
                = (file_height / letter_y), (file_width / letter_x)
# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)


def draw_block(x, y, w, h, color):
    pygame.draw.rect(gameWindow, color, [x, y, w, h])


def text_ojects(msg, font, color):
    textSurface = font.render(msg, True, color)
    return textSurface, textSurface.get_rect()


def draw_text_in_middle(txt, x, y, w, h, color):
    font = pygame.font.SysFont(None, 40)
    TextSurf, TextRect = text_ojects(txt, font, color)
    TextRect.center = ((w / 2) + x, (h / 2) + y)
    gameWindow.blit(TextSurf, TextRect)


while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Draw Things
    gameWindow.fill(black)
    draw_block(schedule_x, schedule_y, schedule_width, schedule_height, white)
    draw_text_in_middle("Schduling", 0, 0, schedule_width, text_bar_width,
                        white)
    draw_block(w_wait_x, w_wait_y, w_wait_width, w_wait_height, white)
    draw_text_in_middle("Writer_wait", w_wait_x, (w_wait_y - text_bar_width),
                        w_wait_width, text_bar_width, white)
    draw_block(r_wait_x, r_wait_y, r_wait_width, r_wait_height, white)
    draw_text_in_middle("Reader_wait", r_wait_x, (r_wait_y - text_bar_width),
                        r_wait_width, text_bar_width, white)
    draw_block(file_x, file_y, file_width, file_height, white)
    draw_text_in_middle("File", file_x, (file_y - text_bar_width), file_width,
                        text_bar_width, white)

    # Update
    pygame.display.update()
    clock.tick(60)
