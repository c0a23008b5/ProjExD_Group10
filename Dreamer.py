import os
import sys
import random
import math
import pygame as pg

WIDTH = 1200  # ゲームウィンドウの幅
HEIGHT = 700  # ゲームウィンドウの高さ

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect, buffer: int = 50) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < buffer or WIDTH - buffer < obj_rct.right:
        yoko = False
    if obj_rct.top < buffer or HEIGHT - buffer < obj_rct.bottom:
        tate = False
    return yoko, tate

class MusicPlayer:
    """
    音楽再生を管理するクラス
    """
    def __init__(self, file_path, volume=0.5):
        """
        初期化メソッド
        :param file_path: 再生する音楽ファイルのパス
        :param volume: 音量（デフォルトは0.5）
        """
        self.sound = pg.mixer.Sound(file_path)
        self.sound.set_volume(volume)
        self.playing = False

    def play(self):
        """
        音楽を再生するメソッド
        """
        if not self.playing:
            self.sound.play(-1)  # -1 はループ再生を意味するフラグ
            self.playing = True

    def stop(self):
        """
        音楽を停止するメソッド
        """
        if self.playing:
            self.sound.stop()
            self.playing = False

    def update(self):
        """
        音楽の更新（ここでは特に何もしない）
        """
        pass

class Bigenemy(pg.sprite.Sprite):
    """
    大ボスに関するクラス
    """
    def __init__(self, x, y):
        """
        大ボスSurfaceを作成する
        引数1 x：大ボスのx座標
        引数2 y：大ボスのy座標
        """
        super().__init__()
        self.bg_img = pg.image.load("fig/23300955.jpg")
        self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/boss_koukaton.png"), 0, 0.2)
        img = pg.transform.flip(s_boss_img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = 5
        self.direction = random.uniform(0, 2 * math.pi)
        self.target_direction = self.direction
        self.last_x = self.rect.x
        self.last_y = self.rect.y
        self.curve_factor = 0.1  # カーブの強さを調整する係数

        # 音楽プレイヤーを初期化
        self.music_player = MusicPlayer("fig/4m.rarara.mp3", volume=0.5)

        # サウンドの再生時間管理用のタイマー
        self.sound_timer = 0
        self.sound_duration = 500  # 500フレームごとに音楽を再生

        # 初期状態では音楽は停止しておく
        self.stop_music()

    def update(self):
        if random.random() < 0.04:  # ランダムに方向を変える確率
            self.target_direction = random.uniform(0, 2 * math.pi)
            self.speed = random.uniform(5, 15)  # ランダムな速さに変更

        # 方向を徐々にターゲット方向に向けて変更
        self.direction += (self.target_direction - self.direction) * 0.05

        # 移動量を計算
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction)

        # 新しい位置を計算
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # 画面端に近づいたら滑らかに曲がる
        buffer = 100  # 画面端からの距離
        if self.rect.left < buffer:
            self.direction += self.curve_factor * (1 - self.rect.centery / HEIGHT)
        elif self.rect.right > WIDTH - buffer:
            self.direction -= self.curve_factor * (1 - self.rect.centery / HEIGHT)
        if self.rect.top < buffer:
            self.direction += self.curve_factor * (self.rect.centerx / WIDTH)
        elif self.rect.bottom > HEIGHT - buffer:
            self.direction -= self.curve_factor * (self.rect.centerx / WIDTH)

        # 新しい位置を設定
        self.rect.x = new_x
        self.rect.y = new_y

        # 画面の端に近づいたら反転
        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.direction = math.pi - self.direction
            self.target_direction = self.direction
        if not tate:
            self.direction = -self.direction
            self.target_direction = self.direction

    def stop_music(self):
        """
        音楽を停止するメソッド
        """
        self.music_player.stop()

    def switch_to_bigboss(self):
        """
        大ボスに切り替わった際の処理
        ここで音楽を再生するなどの追加の処理を行う
        """
        print("a")
        self.music_player.play()  # 音楽を再生
        self.sound_timer = self.sound_duration  # 再生タイマーを終了間隔にセット



class Smallenemy(pg.sprite.Sprite):
    """
    小ボスに関するクラス
    """
    def __init__(self, x, y):
        """
        小ボスSurfaceを作成する
        引数1 x：小ボスのx座標
        引数2 y：小ボスのy座標
        """
        super().__init__()
        self.bg_img = pg.image.load("fig/24535830.jpg")
        self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/alien1.png"), 0, 2)
        img = pg.transform.flip(s_boss_img, True, False)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.center = x, y
        self.speed = 5
        self.angle = 0
        self.mode = 'circle'
        self.timer = 0
        self.warp_count = 0
        self.warp_duration = 60  # 1秒（60fps * 1）
        self.warp_mode = False
        self.mode_duration = 300  # 各モードの持続時間（60fps * 5）
        self.current_mode_timer = 0
        self.current_mode = 'rotate'  # 初期モードは回転

    def update(self):
        self.current_mode_timer += 1

        if self.current_mode == 'rotate':
            self.angle += 0.05
            radius = 100  # 回転の半径を調整
            cx = WIDTH - radius - 100  # 右中央に収まるように中心を調整
            cy = HEIGHT // 2

            self.rect.centerx = cx + radius * math.cos(self.angle)
            self.rect.centery = cy + radius * math.sin(self.angle)

            if self.current_mode_timer > self.mode_duration:  # 持続時間が終わったら次のモードへ
                self.current_mode = 'vertical'
                self.current_mode_timer = 0
                self.rect.x = 1000
                self.speed = 5
                self.warp_mode = True

        elif self.current_mode == 'vertical':
            self.rect.y += self.speed
            _, tate = check_bound(self.rect)
            if not tate:
                self.speed = -self.speed  # 方向を反転
            if self.current_mode_timer > self.mode_duration:  # 持続時間が終わったら次のモードへ
                self.current_mode = 'warp'
                self.current_mode_timer = 0

        elif self.current_mode == 'warp':
            if self.warp_mode:
                # 画面外にはみ出さないようにする
                self.rect.centerx = random.randint(self.rect.width // 2, WIDTH - self.rect.width // 2)
                self.rect.centery = random.randint(self.rect.height // 2, HEIGHT - self.rect.height // 2)
                self.current_mode_timer = 0
                self.warp_mode = False
                self.warp_count += 1
            else:
                if self.current_mode_timer >= self.warp_duration:
                    self.current_mode_timer = 0
                    self.warp_mode = True

        # すべてのワープが終了したら最初のモードに戻す
        if self.warp_count >= 10:
            self.current_mode = 'rotate'
            self.angle = 0
            self.rect.center = self.center
            self.warp_count = 0
        
    def stop_music(self):
        """
        音楽を停止するメソッド
        """
        pass  # Smallenemyにおいては音楽を停止する必要がないので、何も処理しない


class Midboss(pg.sprite.Sprite):
    """
    中ボスのクラス
    """
    def __init__(self, x, y):
        """
        中ボスのSurfaceを作成します。
        引数1 x：中ボスのx座標
        引数2 y：中ボスのy座標
        """
        super().__init__()
        # 中ボスの画像を読み込み、サイズを調整して反転させます
        self.bg_img = pg.image.load("fig/24535848.jpg")
        self.bg_img = pg.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        s_boss_img = pg.transform.rotozoom(pg.image.load("fig/alien1.png"), 0, 2)
        self.image = pg.transform.rotozoom(s_boss_img, 0, 0.2)
        self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.speed = 7  # 移動速度を小さくする
        self.target_y = self.rect.y  # 垂直移動の目標Y座標
        self.set_new_target()  # 初期目標位置を設定

    def set_new_target(self):
        """
        新しい目標位置を設定する関数
        """
        move_distance = random.randint(-300, 300)  # 小さなランダムな移動距離を設定
        new_target_y = self.rect.y + move_distance
        # 画面内に収まるように調整
        self.target_y = max(self.rect.height // 2, min(new_target_y, HEIGHT - self.rect.height // 2))

    def update(self):
        # 縦移動を実行
        if abs(self.rect.y - self.target_y) < self.speed:
            self.rect.y = self.target_y
            self.set_new_target()  # 目標位置に達したら新しい目標位置を設定
        else:
            direction = 1 if self.target_y > self.rect.y else -1
            self.rect.y += direction * self.speed

        # 画面外に出ないように調整
        yoko, tate = check_bound(self.rect)
        if not yoko:
            self.speed *= -1  # 横方向の速度を反転

        _, tate = check_bound(self.rect)
        if not tate:
            self.set_new_target()  # 垂直移動を元に戻すために新しい目標位置を設定

    def stop_music(self):
        """
        音楽を停止するメソッド
        """
        pass  # Midbossにおいては音楽を停止する必要がないので、何も処理しない



def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    b_enemy = Bigenemy(800, 300)
    s_enemy = Smallenemy(1100, 650)
    m_enemy = Midboss(1000, 400)

    enemies = [s_enemy, m_enemy, b_enemy]
    current_enemy = 0  # 現在表示中の敵のインデックス
    enemy_group = pg.sprite.Group(enemies[current_enemy])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Enterキーでクラスを切り替え
                    # 前の敵の音楽を停止
                    enemies[current_enemy].stop_music()
                    current_enemy = (current_enemy + 1) % len(enemies)
                    enemy_group = pg.sprite.Group(enemies[current_enemy])

                    # 新しい敵が大ボスならば、switch_to_bigbossを呼ぶ
                    if isinstance(enemies[current_enemy], Bigenemy):
                        enemies[current_enemy].switch_to_bigboss()


        # 現在の敵クラスに応じて背景を描画
        current_bg_img = enemies[current_enemy].bg_img
        screen.blit(current_bg_img, (0, 0))
        enemy_group.update()
        enemy_group.draw(screen)

        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()