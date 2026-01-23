import pygame
import sys
from assets_loading_system import AssetManager
from your_ship import Player  # ファイル名を your_ship.py に合わせました
from enemy import EnemyShip
from gacha import spin_gacha
from parts import HULL_DATA, MAIN_CANNONS, ANTI_AIR

# --- 定数設定 ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# カラー
WHITE = (255, 255, 255)
BLACK = (20, 20, 25)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
GOLD = (255, 215, 0)


class GameMaster:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("艦隊RPG - 戦略ガチャバトル")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("msgothic", 24)

        self.assets = AssetManager()
        self.player = Player()
        self.state = "MENU"  # MENU, GACHA, BATTLE

        # メニュー管理
        self.menu_options = ["ガチャを引く", "戦闘開始", "終了"]
        self.battle_options = ["たたかう", "のうりょく", "アイテム", "にげる"]
        self.selected_idx = 0

        # 戦闘用データ
        self.current_enemy = None

    def create_enemy(self):
        """敵艦を生成（疑似AI搭載）"""
        # parts.pyのデータを使って敵を構成
        self.current_enemy = EnemyShip(
            "駆逐艦ハエタタキ",
            HULL_DATA["駆逐艦"][0],
            main_cannon=MAIN_CANNONS[0],
            anti_air=ANTI_AIR[1]
        )

    def draw_text(self, text, x, y, color=WHITE, center=False):
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(topleft=(x, y))
        if center:
            rect.centerx = x
        self.screen.blit(surf, rect)

    def run(self):
        # BGM開始（assetsにwaveファイルがある想定）
        self.assets.play_bgm("menu_bgm.wav")

        while True:
            self.screen.fill(BLACK)
            self.handle_events()

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "BATTLE":
                self.draw_battle()

            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_idx = (
                        self.selected_idx - 1) % self.get_current_options_len()
                elif event.key == pygame.K_DOWN:
                    self.selected_idx = (
                        self.selected_idx + 1) % self.get_current_options_len()
                elif event.key == pygame.K_RETURN:
                    self.execute_selection()

    def get_current_options_len(self):
        if self.state == "MENU":
            return len(self.menu_options)
        if self.state == "BATTLE":
            return len(self.battle_options)
        return 1

    def execute_selection(self):
        if self.state == "MENU":
            if self.selected_idx == 0:  # ガチャ
                results = spin_gacha(1)
                # 当たったものをとりあえずhullに装備する例
                self.player.equip("hull", results[0])
                print(f"獲得: {results[0]['name']}")
            elif self.selected_idx == 1:  # 戦闘開始
                self.create_enemy()
                self.state = "BATTLE"
                self.selected_idx = 0
                self.assets.play_bgm("battle_bgm.wav")
            elif self.selected_idx == 2:
                pygame.quit()
                sys.exit()

        elif self.state == "BATTLE":
            if self.selected_idx == 0:  # たたかう
                damage = max(
                    10, self.player.stats["atk"] - self.current_enemy.stats["def"])
                self.current_enemy.take_damage(damage)
                # 敵の反撃（疑似AI）
                enemy_action = self.current_enemy.choose_action(
                    self.player.stats)
                print(f"敵の行動: {enemy_action}")
                if self.current_enemy.is_defeated():
                    self.state = "MENU"
                    self.assets.play_bgm("menu_bgm.wav")

    def draw_menu(self):
        self.draw_text("艦隊戦略メインメニュー", SCREEN_WIDTH//2, 100, GOLD, True)
        for i, opt in enumerate(self.menu_options):
            color = GREEN if i == self.selected_idx else WHITE
            prefix = "> " if i == self.selected_idx else "  "
            self.draw_text(prefix + opt, SCREEN_WIDTH //
                           2, 250 + i*40, color, True)

    def draw_battle(self):
        # 敵の描画（assets/enemy1.png）
        enemy_img = self.assets.get_image("enemy1.png", scale=(200, 150))
        self.screen.blit(enemy_img, (SCREEN_WIDTH//2 - 100, 100))

        # ステータス表示
        self.draw_text(f"ENEMY: {self.current_enemy.name}", 500, 50, RED)
        self.draw_text(f"HP: {self.current_enemy.current_hp}", 500, 80)

        self.draw_text(f"PLAYER HP: {self.player.stats['hp']}", 50, 450, GREEN)

        # コマンドウィンドウ
        pygame.draw.rect(self.screen, WHITE, (50, 480, 700, 100), 2)
        for i, opt in enumerate(self.battle_options):
            color = GREEN if i == self.selected_idx else WHITE
            x = 100 + (i % 2) * 200
            y = 500 + (i // 2) * 30
            prefix = "> " if i == self.selected_idx else "  "
            self.draw_text(prefix + opt, x, y, color)


if __name__ == "__main__":
    game = GameMaster()
    game.run()
