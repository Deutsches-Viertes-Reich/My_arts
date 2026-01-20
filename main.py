import pygame
import sys
import random
from parts import ALL_PARTS

# --- 初期設定 ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("戦艦パーツガチャ")
clock = pygame.time.Clock()

# カラー設定
WHITE = (255, 255, 255)
BLACK = (20, 20, 25)
GREEN = (100, 255, 100)
GOLD = (255, 215, 0)
GRAY = (150, 150, 150)

# フォント設定 (日本語が表示できるフォントを指定)
# Windowsの場合は "msgothic", Macの場合は "hiraginosansgb" など
FONT_NAME = "msgothic" if sys.platform == "win32" else "applesymbol"
font_m = pygame.font.SysFont(FONT_NAME, 30)
font_l = pygame.font.SysFont(FONT_NAME, 50)
font_s = pygame.font.SysFont(FONT_NAME, 20)

# --- ガチャロジック ---
RARITY_WEIGHTS = {"N": 40, "R": 30, "SR": 15, "SSR": 10, "LEGEND": 5}


def get_parts_by_rarity(rarity):
    pool = []
    # 船体
    for ship_type in ALL_PARTS["hull"]:
        for item in ALL_PARTS["hull"][ship_type]:
            if item["rarity"] == rarity:
                pool.append(item)
    # その他
    categories = ["main_cannon", "secondary_cannon", "anti_air",
                  "bridge", "captain", "armor", "engine", "item", "skill"]
    for cat in categories:
        for item in ALL_PARTS[cat]:
            if item["rarity"] == rarity:
                pool.append(item)
    return pool


def spin_gacha(times):
    results = []
    rarities = list(RARITY_WEIGHTS.keys())
    weights = list(RARITY_WEIGHTS.values())
    for _ in range(times):
        chosen_rarity = random.choices(rarities, weights=weights, k=1)[0]
        pool = get_parts_by_rarity(chosen_rarity)
        results.append(random.choice(pool) if pool else random.choice(
            get_parts_by_rarity("N")))
    return results

# --- メインループ ---


def main():
    menu_options = ["単発ガチャを引く", "10連ガチャを引く", "終了"]
    selected_index = 0
    gacha_results = []
    state = "MENU"  # "MENU" か "RESULT"

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "MENU":
                    if event.key == pygame.K_UP:
                        selected_index = (
                            selected_index - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (
                            selected_index + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:
                            gacha_results = spin_gacha(1)
                            state = "RESULT"
                        elif selected_index == 1:
                            gacha_results = spin_gacha(10)
                            state = "RESULT"
                        elif selected_index == 2:
                            pygame.quit()
                            sys.exit()

                elif state == "RESULT":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        state = "MENU"

        # --- 描画処理 ---
        if state == "MENU":
            title = font_l.render("戦艦パーツガチャ", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

            for i, option in enumerate(menu_options):
                color = GREEN if i == selected_index else GRAY
                prefix = "> " if i == selected_index else "  "
                text = font_m.render(prefix + option, True, color)
                screen.blit(text, (SCREEN_WIDTH//2 - 150, 250 + i * 60))

            hint = font_s.render("矢印キーで選択 / Enterで決定", True, GRAY)
            screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 500))

        elif state == "RESULT":
            header = font_m.render(
                f"ガチャ結果 ({len(gacha_results)}連)", True, GOLD)
            screen.blit(header, (50, 50))

            for i, item in enumerate(gacha_results):
                rarity_color = GOLD if item['rarity'] in [
                    "SSR", "LEGEND"] else WHITE
                # 10連の結果を2列に分けて表示
                x = 50 if i < 5 else 400
                y = 120 + (i % 5) * 70

                rarity_text = font_s.render(
                    f"[{item['rarity']}]", True, rarity_color)
                name_text = font_m.render(item['name'], True, WHITE)

                screen.blit(rarity_text, (x, y))
                screen.blit(name_text, (x, y + 25))

            footer = font_s.render("Enterキーでメニューに戻る", True, GRAY)
            screen.blit(footer, (SCREEN_WIDTH//2 - footer.get_width()//2, 550))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
