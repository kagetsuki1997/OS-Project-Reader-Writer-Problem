import pygame
from pygame.locals import *
import sys
import time

pygame.init() #初始化pygame
screen=pygame.display.set_mode([640,480])  #窗口大小：640*480
screen.fill([255,255,200])#用白色填充窗口
myReader=pygame.image.load('C:/Users/莊凱鈞/desktop/Reader_priority.png') #把变量myimage赋给导入的图片
width_reader, height_reader = myReader.get_size()
myWriter=pygame.image.load('C:/Users/莊凱鈞/desktop/Writer_priority.png')
width_writer, height_writer = myWriter.get_size()
screen.blit(myReader,[100,100]) #在100,100的地方画出这个图片（100和100为左部和上部）
screen.blit(myWriter,[100,300])
pygame.display.flip()

while True:
    for e in pygame.event.get():#获得事件
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN: #判断鼠标位置以及是否摁了下去。
            mx, my = pygame.mouse.get_pos()
            if mx >=100 and mx<=width_reader+100 and my>=100 and my<=height_reader+100:
            #做需要做的事情，如开始游戏。
                screen.fill([255,0,0])# Click on Reader_priority
            elif mx>=100 and mx<=width_writer+100 and my>=300 and my<=height_writer+300:
                screen.fill([0,0, 255]) #Click on Writer_priority
            else:
                screen.fill([0,255,0]) #Click on neither

    #time.sleep(0.5)
    pygame.display.update()
