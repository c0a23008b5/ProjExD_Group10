import os
import sys
import random
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class small_enemy(pg.game.sprite.Sprite):
    """
    小ボスに関するクラス
    """
    

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/background1.jpg") #背景画像
    bg_img2 = pg.transform.flip(bg_img, True, False) #背景画像
    kk_img = pg.image.load("fig/koukaton.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.3)
    kk_rect = kk_img.get_rect() #こうかとんrectの抽出
    kk_rect.center = 300, 200
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        x = tmr%3200
        screen.blit(bg_img, [-x, 0]) #背景画像を表すsurfase
        screen.blit(bg_img2, [-x+1600, 0])
        screen.blit(bg_img, [-x+3200, 0]) #背景画像を表すsurfase
        screen.blit(bg_img2, [-x+4800, 0])
        
        kye_lst = pg.key.get_pressed()
        if kye_lst[pg.K_UP]: #上矢印を押したとき
            a = -1
            b = -1
        elif kye_lst[pg.K_DOWN]:
            a = -1
            b = +1
        elif kye_lst[pg.K_LEFT]:
            a = -1
            b = 0
        elif kye_lst[pg.K_RIGHT]:
            a = +2
            b = 0
        else:
            a = -1
            b = 0
        kk_rect.move_ip(a, b)
        screen.blit(kk_img, kk_rect) #kk_imageをkk_rectの設定に従って貼り付け
        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()