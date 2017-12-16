import pygame
import math
import threading


class Gui(threading.Thread):
    def __init__(self):
        pygame.init()
        self.window_size = self.window_width, self.window_height = 1300, 700
        self.gameWindow = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("RW")
        self.clock = pygame.time.Clock()

        # Colors
        # 定義顏色的rgb值
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)

        self.animation(50, 50, 5)

    def animation(self, letterFontSize, titleBarWidth, normalBarWidth):
        # list
        # 測試用的list
        schedule_list = []
        for i in range(20):
            lett = "W"
            if i % 2 == 0:
                lett = "R"
            schedule_list.append((lett, i + 1))

        #######################################################################
        ##                         版型與大小(可調整)                         ####
        #######################################################################
        # letter(writer,reader)
        # 以英文字W代表writer, R代表rider
        # 其字母右下有小數字來區別不同的writer, 和不同的rider, 譬如可以定義Wn 是第n個writer
        # 我們可以調整字母的字體大小，letter_rect 是字母的文字框
        self.letter_font_size = letterFontSize
        self.letter_rect_size = self.letter_width, self.letter_height\
                         = self.PtToPixel(self.letter_font_size), self.PtToPixel(self.letter_font_size)
        self.id_rect_size = self.id_rect_width, self.id_rect_height\
                     = self.letter_width / 2, self.letter_height / 2
        self.id_font_size = self.PixelToPt(self.id_rect_height)
        # Bar
        # 分成要寫欄位title在上面的分隔線寬度和一般的分隔線寬度
        text_bar_width = titleBarWidth
        title_font_size = self.PixelToPt(text_bar_width)
        normal_bar_width = normalBarWidth
        # Scheduling Block
        # 設定scheduling block 可以容納幾乘幾個字母，來決定的此block的大小
        schedule_capacity = schedule_num_row, schedule_num_col \
                          = 2, (self.window_width / self.letter_width)
        schedule_size = schedule_width, schedule_height \
                      = self.window_width, (schedule_num_row * self.letter_height)
        schedule_point = schedule_x, schedule_y = 0, text_bar_width
        # 除去scheduling block和分隔線所佔的空間，大概分成三份給writer wait, file, reader_wait
        # Writer_wait
        w_wait_size = w_wait_width, w_wait_height \
                    = ((self.window_width - 2 * normal_bar_width) / 3), \
                    (self.window_height - schedule_height - 2 * text_bar_width)
        w_wait_point = w_wait_x, w_wait_y = 0, (
            self.window_height - w_wait_height)
        w_wait_capacity = w_num_row, w_num_col \
                        = (w_wait_height / self.letter_height), (w_wait_width / self.letter_width)
        # reader_wait
        r_wait_size = r_wait_width, r_wait_height = w_wait_width, w_wait_height
        r_wait_point = r_wait_x, r_wait_y = (
            self.window_width - r_wait_width), w_wait_y
        r_wait_capacity = r_num_row, r_num_col \
                        = (r_wait_height / self.letter_height), (r_wait_width / self.letter_width)
        # file
        file_size = file_width, file_height \
                  = (self.window_width - w_wait_width - r_wait_width
                    - 2 * normal_bar_width), w_wait_height
        file_point = file_x, file_y = (
            w_wait_width + normal_bar_width), w_wait_y
        file_capacity = file_num_row, file_num_col \
                      = (file_height / self.letter_height), (file_width / self.letter_width)

        ####################################################################
        ####                        主要的動畫Loop                      ####
        ####################################################################
        while True:
            # Detect QUIT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Draw Things
            self.gameWindow.fill(self.black)
            # draw_block 是畫欄位的裏面部份，沒有被覆蓋到的背景就會成為區隔線部份
            # draw_text 則是在區隔線部份上印字，當作該欄位的title
            self.draw_block(schedule_x, schedule_y, schedule_width,
                            schedule_height, self.white)
            self.draw_text_in_middle("Scheduling", 0, 0, schedule_width,
                                     text_bar_width, self.white,
                                     title_font_size)
            self.draw_block(w_wait_x, w_wait_y, w_wait_width, w_wait_height,
                            self.white)
            self.draw_text_in_middle(
                "Writer_wait", w_wait_x, (w_wait_y - text_bar_width),
                w_wait_width, text_bar_width, self.white, title_font_size)
            self.draw_block(r_wait_x, r_wait_y, r_wait_width, r_wait_height,
                            self.white)
            self.draw_text_in_middle(
                "Reader_wait", r_wait_x, (r_wait_y - text_bar_width),
                r_wait_width, text_bar_width, self.white, title_font_size)
            self.draw_block(file_x, file_y, file_width, file_height,
                            self.white)
            self.draw_text_in_middle("File", file_x, (file_y - text_bar_width),
                                     file_width, text_bar_width, self.white,
                                     title_font_size)

            # 試印W/R 於scheduling block
            for e in schedule_list:
                n = e[1]
                n -= 1
                x = n % schedule_num_col * self.letter_width + 0
                y = 0
                if n >= schedule_num_col:
                    y = 1
                y = y * self.letter_height + schedule_y
                self.draw_er(e[0], x, y, e[1])

            # Update
            pygame.display.update()
            self.clock.tick(60)

    ###########################################################################
    ####                            繪圖工具                                ###
    ###########################################################################
    # 1 pt = 0.0358 cm, 1 cm = 37.795276 pixels
    def PtToPixel(self, pt):
        # Don't know why, ceil will return XX.0 instead fo an integer like when I compile it at repl.com
        return int(math.ceil(pt * 0.0358 * 37.795276))

    def PixelToPt(self, pixel):
        # Don't know why, floor will return XX.0 instead fo an integer like when I compile it at repl.com
        return int(math.floor(pixel / 37.79256 / 0.0358))

    # 畫象徵writer/reader 的 W/R
    def draw_er(self, letter, x, y, idNumber):
        # 以(x,y)處為文字框左上角，依預先定好的字體大小，畫letter("R"/"W")上去，並在右下畫區別用的小數字
        self.draw_text_in_middle(letter, x, y, self.letter_width,
                                 self.letter_height, self.black,
                                 self.letter_font_size)
        self.draw_text_in_middle(
            str(idNumber), (self.letter_width - self.id_rect_width + x),
            (self.letter_height - self.id_rect_height + y),
            self.id_rect_width, self.id_rect_height, self.red,
            self.id_font_size)

    # 畫出Block
    def draw_block(self, x, y, w, h, color):
        # 給左上頂點(x,y)和self.長寬，定義出長方self.形，並決定裏面填的顏色
        pygame.draw.rect(self.gameWindow, color, [x, y, w, h])

    def text_ojects(self, msg, font, color):
        textSurface = font.render(msg, True, color)
        return textSurface, textSurface.get_rect()

    # 給定一長方形區域，將給定字體大小的文字畫在其置中處
    def draw_text_in_middle(self, txt, x, y, w, h, color, font_size):
        font = pygame.font.SysFont(None, font_size)
        TextSurf, TextRect = self.text_ojects(txt, font, color)
        TextRect.center = ((w / 2) + x, (h / 2) + y)
        self.gameWindow.blit(TextSurf, TextRect)


g = Gui()
