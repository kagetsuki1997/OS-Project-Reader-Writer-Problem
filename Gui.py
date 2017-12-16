import pygame
import math

pygame.init()
window_size = window_width, window_height = 1300, 700
gameWindow = pygame.display.set_mode(window_size)
pygame.display.set_caption("RW")
clock = pygame.time.Clock()

# list
# 測試用的list
schedule_list = []
for i in range(20):
    lett = "W"
    if i % 2 == 0:
        lett = "R"
    schedule_list.append((lett, i + 1))
print schedule_list


###############################################################################
##                         版型與大小(可調整)                                ##
###############################################################################
# Letter (writer, reader)
# 1 pt = 0.0358 cm, 1 cm = 37.795276 pixels
def PtToPixel(pt):
    # I don't know why, but ceil will return XX.0 instead fo an integer like when I compile it at repl.com
    return int(math.ceil(letter_font_size * 0.0358 * 37.795276))


def PixelToPt(pixel):
    # I don't know why, but floor will return XX.0 instead fo an integer like when I compile it at repl.com
    return int(math.floor(pixel / 37.79256 / 0.0358))


# letter
# 以英文字W代表writer, R代表rider
# 其字母右下有小數字來區別不同的writer, 和不同的rider, 譬如可以定義Wn 是第n個writer
# 我們可以調整字母的字體大小，letter_rect 是字母的文字框
letter_font_size = 50
letter_rect_size = letter_width, letter_height\
                 = PtToPixel(letter_font_size), PtToPixel(letter_font_size)
id_rect_size = id_rect_width, id_rect_height\
             = letter_width / 2, letter_height / 2
id_font_size = PixelToPt(id_rect_height)
# Bar
# 分成要寫欄位title在上面的分隔線寬度和一般的分隔線寬度
text_bar_width = 50
title_font_size = PixelToPt(text_bar_width)
print title_font_size
normal_bar_width = 5
# Scheduling Block
# 設定scheduling block 可以容納幾乘幾個字母，來決定的此block的大小
schedule_capacity = schedule_num_row, schedule_num_col \
                  = 2, (window_width / letter_width)
schedule_size = schedule_width, schedule_height \
              = window_width, (schedule_num_row * letter_height)
schedule_point = schedule_x, schedule_y = 0, text_bar_width
# 除去scheduling block和分隔線所佔的空間，大概分成三份給writer wait, file, reader_wait
# Writer_wait
w_wait_size = w_wait_width, w_wait_height \
            = ((window_width - 2 * normal_bar_width) / 3), \
                (window_height - schedule_height - 2 * text_bar_width)
w_wait_point = w_wait_x, w_wait_y = 0, (window_height - w_wait_height)
w_wait_capacity = w_num_row, w_num_col \
                = (w_wait_height / letter_height), (w_wait_width / letter_width)
# reader_wait
r_wait_size = r_wait_width, r_wait_height = w_wait_width, w_wait_height
r_wait_point = r_wait_x, r_wait_y = (window_width - r_wait_width), w_wait_y
r_wait_capacity = r_num_row, r_num_col \
                = (r_wait_height / letter_height), (r_wait_width / letter_width)
# file
file_size = file_width, file_height \
          = (window_width - w_wait_width - r_wait_width
             - 2 * normal_bar_width), w_wait_height
file_point = file_x, file_y = (w_wait_width + normal_bar_width), w_wait_y
file_capacity = file_num_row, file_num_col \
                = (file_height / letter_height), (file_width / letter_width)
# Colors
# 定義顏色的rgb值
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)


############################################################################
####                            繪圖工具                                ####
############################################################################
# 畫象徵writer/reader 的 W/R
def draw_er(letter, x, y, idNumber):
    # 以(x,y)處為文字框左上角，依預先定好的字體大小，畫letter("R"/"W")上去，並在右下畫區別用的小數字
    draw_text_in_middle(letter, x, y, letter_width, letter_height, black,
                        letter_font_size)
    draw_text_in_middle(
        str(idNumber), (letter_width - id_rect_width + x),
        (letter_height - id_rect_height + y), id_rect_width, id_rect_width,
        red, id_font_size)


# 畫出Block
def draw_block(x, y, w, h, color):
    # 給左上頂點(x,y)和長寬，定義出長方形，並決定裏面填的顏色
    pygame.draw.rect(gameWindow, color, [x, y, w, h])


def text_ojects(msg, font, color):
    textSurface = font.render(msg, True, color)
    return textSurface, textSurface.get_rect()


# 給定一長方形區域，將給定字體大小的文字畫在其置中處
def draw_text_in_middle(txt, x, y, w, h, color, font_size):
    font = pygame.font.SysFont(None, font_size)
    TextSurf, TextRect = text_ojects(txt, font, color)
    TextRect.center = ((w / 2) + x, (h / 2) + y)
    gameWindow.blit(TextSurf, TextRect)


###########################################################################
####                        主要的動畫Loop                             ####
###########################################################################
while True:
    # Detect QUIT
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Draw Things
    gameWindow.fill(black)
    # draw_block 是畫欄位的裏面部份，沒有被覆蓋到的背景就會成為區隔線部份
    # draw_text 則是在區隔線部份上印字，當作該欄位的title
    draw_block(schedule_x, schedule_y, schedule_width, schedule_height, white)
    draw_text_in_middle("Scheduling", 0, 0, schedule_width, text_bar_width,
                        white, title_font_size)
    draw_block(w_wait_x, w_wait_y, w_wait_width, w_wait_height, white)
    draw_text_in_middle("Writer_wait", w_wait_x, (w_wait_y - text_bar_width),
                        w_wait_width, text_bar_width, white, title_font_size)
    draw_block(r_wait_x, r_wait_y, r_wait_width, r_wait_height, white)
    draw_text_in_middle("Reader_wait", r_wait_x, (r_wait_y - text_bar_width),
                        r_wait_width, text_bar_width, white, title_font_size)
    draw_block(file_x, file_y, file_width, file_height, white)
    draw_text_in_middle("File", file_x, (file_y - text_bar_width), file_width,
                        text_bar_width, white, title_font_size)
    # 試印W/R 於scheduling block
    for e in schedule_list:
        n = e[1]
        n -= 1
        x = n % schedule_num_col * letter_width + 0
        y = 0
        if n >= schedule_num_col:
            y = 1
        y = y * letter_height + schedule_y
        draw_er(e[0], x, y, e[1])

    # Update
    pygame.display.update()
    clock.tick(60)
