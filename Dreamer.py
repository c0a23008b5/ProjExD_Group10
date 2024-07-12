import pygame
import sys
import time

# Pygameの初期化
pygame.init()

# 画面サイズと色の設定
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)

# フォントの設定（日本語フォントのパスを指定する）
pygame.font.init()
font_path = "C:\\Users\\Admin\\Desktop\\Noto_Serif_JP\\NotoSerifJP-VariableFont_wght.ttf"
font = pygame.font.Font(font_path, 30)

# ウィンドウの設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typewriter Effect with Pygame")

def typewriter_effect(texts_and_positions):
    rendered_lines = []  # 描画された全ての行を保持するリスト
    
    for text_info in texts_and_positions:
        text = text_info[0]
        x = text_info[1][0]
        y = text_info[1][1]
        is_centered = text_info[2] if len(text_info) > 2 else False
        
        lines = text.split('\n')
        
        for line in lines:
            index = 0
            typing = True
            rendered_text = ""
            
            while typing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                if index <= len(line):
                    rendered_text = line[:index]
                    line_surface = font.render(rendered_text, True, WHITE)
                    
                    # 画面を黒でクリア
                    screen.fill((0, 0, 0))

                    # 描画された全ての行を描画する
                    for rendered_line in rendered_lines:
                        screen.blit(rendered_line[0], rendered_line[1])

                    # 新しい行を描画
                    if is_centered:
                        text_rect = line_surface.get_rect()
                        screen.blit(line_surface, (SCREEN_WIDTH // 2 - text_rect.width // 2, y))
                    else:
                        screen.blit(line_surface, (x, y))
                    
                    pygame.display.flip()  # 画面を更新

                    index += 1
                    pygame.time.wait(100)  # 100ミリ秒待つ

                    if index > len(line):
                        typing = False

            if is_centered:
                rendered_lines.append((line_surface, (SCREEN_WIDTH // 2 - text_rect.width // 2, y)))
            else:
                rendered_lines.append((line_surface, (x, y)))
                
            y += 50  # 次の行を表示するためにY座標を調整

def main():
    texts_and_positions = [
        ("こうかとん", (200, 100)),  # 中央揃え
        ("「うおおおおおおおお」", (200, 150)),
        ("こうかとんは死んだ", (200, 300), True),  # 左揃え（デフォルト）
        ("THE　　END", (SCREEN_WIDTH // 2, 450), True)  # 中央揃え
    ]
    typewriter_effect(texts_and_positions)
    pygame.quit()

if __name__ == "__main__":
    main()