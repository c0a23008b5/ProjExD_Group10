import os
import sys
import time
import random
import pygame as pg

WIDTH = 1200  # ゲームウィンドウの幅
HEIGHT = 700  # ゲームウィンドウの高さ

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

class Smallenemy(pg.sprite.Sprite):
    """
    小ボスに関するクラス
    """
    def __init__(self, x, y):
        """
        小ボスSurfeceを作成する
        引数1 x：小ボスのx座標
        引数2 y：小ボスのy座標
        """
        super().__init__()
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/boss_koukaton.png"), 0, 0.2)
        img = pg.transform.flip(s_boss_img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 5
        self.speed_y = 5
    
    def update(self):
        self.rect.x += random.randint(0, 1) * self.speed_x
        self.rect.y += random.randint(0, 1) * self.speed_y

        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.speed_x *= -1  # Invert x direction
        if not tate:
            self.speed_y *= -1  # Invert y direction
            
        

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/24535830.jpg") #背景画像
    kk_img = pg.image.load("fig/main.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.3)
    kk_rect = kk_img.get_rect() #こうかとんrectの抽出
    kk_rect.center = 50, 500

    s_enemy = Smallenemy(800, 300)
    enemy = pg.sprite.Group(s_enemy)

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        screen.blit(bg_img, (0, 0))
        
        kye_lst = pg.key.get_pressed()
        if kye_lst[pg.K_UP]: #上矢印を押したとき
            b = 0
        elif kye_lst[pg.K_DOWN]:
            b = 0
        elif kye_lst[pg.K_LEFT]:
            a = -1
            b = 0
        elif kye_lst[pg.K_RIGHT]:
            a = +1
            b = 0
        else:
            a = 0
            b = 0
        kk_rect.move_ip(a, b)
        screen.blit(kk_img, kk_rect) #kk_imageをkk_rectの設定に従って貼り付け

        enemy.update()
        enemy.draw(screen)

        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()