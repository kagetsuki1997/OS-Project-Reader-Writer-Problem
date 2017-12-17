import pygame
import math
import threading
import time

# Colors
# Define rgb value for colors
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)


class Gui():
    def __init__(self):
        # Initiate Pygame and Display window
        pygame.init()
        self.window_size = self.window_width, self.window_height = 1300, 700
        self.gameWindow = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("RW")
        self.clock = pygame.time.Clock()

        # The lists of reader/ writer for the blocks and lock for these lists
        self.scheduling = []
        self.w_waiting = []
        self.filing = []
        self.r_waiting = []
        self.nowhere = []
        self.lists_lock = threading.Lock()

        # test list input
        # for i in range(20):
        #     letter = "R"
        #     if i % 2 == 0:
        #         letter = "W"
        #     self.scheduling.append((letter, i + 1))
        #     self.w_waiting.append((letter, i + 1))
        #     self.r_waiting.append((letter, i + 1))
        #     self.filing.append((letter, i + 1))

    def animation(self, letterFontSize, titleBarWidth, normalBarWidth):
        #######################################################################
        ##                    Design and size of Display                   ####
        #######################################################################
        # letter(writer,reader)
        # letter 'W' for writer, 'R' for reader
        # There's small number at right-bottom of letter, to represent id and distinguish different writers or readers
        # we can adjust font of letter to change the size of blocks of the display
        self.letter_font_size = letterFontSize
        self.letter_rect_size = self.letter_width, self.letter_height\
                         = self.PtToPixel(self.letter_font_size), self.PtToPixel(self.letter_font_size)
        self.id_rect_size = self.id_rect_width, self.id_rect_height\
                     = self.letter_width / 2, self.letter_height / 2
        self.id_font_size = self.PixelToPt(self.id_rect_height)
        # Bar
        # we will write title of block on text bar
        text_bar_width = titleBarWidth
        title_font_size = self.PixelToPt(text_bar_width)
        normal_bar_width = normalBarWidth
        # Scheduling Block
        # set how many letters can scheduling block constains, by this, we decide the size of block
        schedule_capacity = schedule_num_row, schedule_num_col \
                          = 2, (self.window_width / self.letter_width)
        schedule_size = schedule_width, schedule_height \
                      = self.window_width, (schedule_num_row * self.letter_height)
        schedule_point = schedule_x, schedule_y = 0, text_bar_width
        # the rest space from space of scheduling block and bars, divide into about equally three piece to writer wait, file, reader_wait
        # Writer_wait
        w_wait_size = w_wait_width, w_wait_height \
                    = ((self.window_width - 2 * normal_bar_width) / 3), \
                    (self.window_height - schedule_height - 2 * text_bar_width)
        w_wait_point = w_wait_x, w_wait_y = 0, (
            self.window_height - w_wait_height)
        w_wait_capacity = w_wait_num_row, w_wait_num_col \
                        = (w_wait_height / self.letter_height), (w_wait_width / self.letter_width)
        # reader_wait
        r_wait_size = r_wait_width, r_wait_height = w_wait_width, w_wait_height
        r_wait_point = r_wait_x, r_wait_y = (
            self.window_width - r_wait_width), w_wait_y
        r_wait_capacity = r_wait_num_row, r_wait_num_col \
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
        ####                   Main Animation Loop                      ####
        ####################################################################
        while True:

            # detect quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Draw Things
            self.gameWindow.fill(Black)
            # draw_block draw the block and where didn't be drawned in the background becomes bars
            # draw_text print text on text bar to be the block's title
            self.draw_block(schedule_x, schedule_y, schedule_width,
                            schedule_height, White)
            self.draw_text_in_middle("Scheduling", 0, 0, schedule_width,
                                     text_bar_width, White, title_font_size)
            self.draw_block(w_wait_x, w_wait_y, w_wait_width, w_wait_height,
                            White)
            self.draw_text_in_middle("Writer_wait", w_wait_x,
                                     (w_wait_y - text_bar_width), w_wait_width,
                                     text_bar_width, White, title_font_size)
            self.draw_block(r_wait_x, r_wait_y, r_wait_width, r_wait_height,
                            White)
            self.draw_text_in_middle("Reader_wait", r_wait_x,
                                     (r_wait_y - text_bar_width), r_wait_width,
                                     text_bar_width, White, title_font_size)
            self.draw_block(file_x, file_y, file_width, file_height, White)
            self.draw_text_in_middle("File", file_x, (file_y - text_bar_width),
                                     file_width, text_bar_width, White,
                                     title_font_size)

            self.lists_lock.acquire()
            # draw readers and writers contained by each blocks
            self.draw_list(self.scheduling, schedule_x, schedule_y,
                           schedule_num_row, schedule_num_col, "horizontal")
            self.draw_list(self.w_waiting, w_wait_x, w_wait_y, w_wait_num_row,
                           w_wait_num_col, "vertical")
            self.draw_list(self.r_waiting, r_wait_x, r_wait_y, r_wait_num_row,
                           r_wait_num_col, "vertical")
            self.draw_list(self.filing, file_x, file_y, file_num_row,
                           file_num_col, "vertical")
            self.lists_lock.release()

            # Update
            pygame.display.update()
            self.clock.tick(60)

    #####################################################################
    ####                          Interface                          ####
    #####################################################################

    def change_state(self, accessTypeChar, idNumber, fromList, toList):
        self.lists_lock.acquire()
        # Get out of block where it is now
        if fromList is not self.nowhere:
            fromList.remove((accessTypeChar, idNumber))
        # Move to block assingend
        toList.append((accessTypeChar, idNumber))
        self.lists_lock.release()

    def test_ers(self):
        i = 0
        while True:
            self.lists_lock.acquire()
            print i
            if i % 4 == 0:
                self.scheduling.append(("W", i))
            elif i % 4 == 1:
                self.w_waiting.append(("W", i))
            elif i % 4 == 2:
                self.r_waiting.append(("R", i))
            else:
                self.filing.append(("R", i))
            i = i + 1
            time.sleep(1)
            self.lists_lock.release()

    ###########################################################################
    ####                       Drawing Tools                                ###
    ###########################################################################
    # 1 pt = 0.0358 cm, 1 cm = 37.795276 pixels
    def PtToPixel(self, pt):
        # Don't know why, ceil will return XX.0 instead fo an integer like when I compile it at repl.com
        return int(math.ceil(pt * 0.0358 * 37.795276))

    def PixelToPt(self, pixel):
        # Don't know why, floor will return XX.0 instead fo an integer like when I compile it at repl.com
        return int(math.floor(pixel / 37.79256 / 0.0358))

    # every block maintain a list to store the readers and writers in this state
    # this functions draw the writers and readers of a block
    def draw_list(self, l, Block_x, Block_y, num_row, num_col, pattern):
        if pattern == "horizontal":
            for index, er in enumerate(l):
                c = index % num_col
                r = index / num_col
                x = c * self.letter_width + Block_x
                y = r * self.letter_height + Block_y
                self.draw_er(er[0], x, y, er[1])
        else:
            for index, er in enumerate(l):
                r = index % num_row
                c = index / num_row
                x = c * self.letter_width + Block_x
                y = r * self.letter_height + Block_y
                self.draw_er(er[0], x, y, er[1])

    # Draw W/R which represents writer/reader
    def draw_er(self, letter, x, y, idNumber):
        self.draw_text_in_middle(letter, x, y, self.letter_width,
                                 self.letter_height, Black,
                                 self.letter_font_size)
        self.draw_text_in_middle(
            str(idNumber), (self.letter_width - self.id_rect_width + x),
            (self.letter_height - self.id_rect_height + y), self.id_rect_width,
            self.id_rect_height, Red, self.id_font_size)

    # Draw Block
    def draw_block(self, x, y, w, h, color):
        pygame.draw.rect(self.gameWindow, color, [x, y, w, h])

    def text_ojects(self, msg, font, color):
        textSurface = font.render(msg, True, color)
        return textSurface, textSurface.get_rect()

    # Given a Rectangle area, draw text in the middle of it
    def draw_text_in_middle(self, txt, x, y, w, h, color, font_size):
        font = pygame.font.SysFont(None, font_size)
        TextSurf, TextRect = self.text_ojects(txt, font, color)
        TextRect.center = ((w / 2) + x, (h / 2) + y)
        self.gameWindow.blit(TextSurf, TextRect)


class GuiRunner(threading.Thread):
    def __init__(self, gui, act):
        threading.Thread.__init__(self)
        self.mygui = gui
        self.action = act

    def run(self):
        if self.action == "animation":
            self.mygui.animation(50, 50, 5)
        else:
            self.mygui.test_ers()


# How to use this GUI
'''Example of main:
from Writer import Writer
from Reader import Reader
from Book import Book
from GG import Gui
from GG import GuiRunner

def main():
    b = Book()
    g = Gui()
    GuiRunner(g, "animation").start()

    g.change_state("W", 7, g.nowhere, g.scheduling)
    Writer(b, 7, g).start()
    for i in range(0, 3):
        g.change_state("R", i, g.nowhere, g.scheduling)
        Reader(b, i, g).start()

    for i in range(0, 2):
        g.change_state("W", i, g.nowhere, g.scheduling)
        Writer(b, i, g).start()

main()
'''
'''Example of reader
import threading
import time
from GG import Gui

class Reader(threading.Thread):
    def __init__(self, book, tid, g):
        threading.Thread.__init__(self)
        self.book = book
        self.tid = tid
        self.gui = g

    def run(self):
        print("The reader " + str(self.tid) + " comes to the reading room")
        self.gui.change_state("R", self.tid, self.gui.scheduling, self.gui.r_waiting)
        self.book.want_to_read()
        print("The reader " + str(self.tid) + " begins reading")
        self.gui.change_state("R", self.tid, self.gui.r_waiting, self.gui.filing)
        time.sleep(3)
        print("The reader " + str(self.tid) + " ends reading")
        self.gui.change_state("R", self.tid, self.gui.filing, self.gui.scheduling)
        self.book.end_reading()
        print("The reader " + str(self.tid) + " leaves the reading room")
'''
