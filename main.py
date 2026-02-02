import pygame
import sys
import random
from assets_loading_system import AssetManager
from your_ship import Player
from assembly import AssemblyScene
from gacha import spin_gacha
from battle_scene import BattleScene
from enemy import EnemyShip
import parts


class GameMaster:
    def __init__(self):
        pygame.init()
        # 画面設定
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("艦隊RPG：10スロット・レジェンドバトル版")
        self.clock = pygame.time.Clock()

        # システム初期化
        self.assets = AssetManager()
        self.player = Player()

        # 状態管理
        self.state = "MENU"
        self.options = ["ガチャを引く", "編成ドック", "出撃", "終了"]
        self.idx = 0

        # フォント
        self.font = pygame.font.SysFont("msgothic", 30)
        self.sub_font = pygame.font.SysFont("msgothic", 20)

        # シーン保持用
        self.assembly = None
        self.battle_view = None

    def run(self):
        """メインループ"""
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if self.state == "MENU":
                self.handle_menu_input(event)
            elif self.state == "ASSEMBLY":
                res = self.assembly.handle_event(event)
                if res == "MENU":
                    self.state = "MENU"
            elif self.state == "BATTLE":
                res = self.battle_view.handle_event(event)
                if res in ["VICTORY", "DEFEAT", "ESCAPE"]:
                    print(f"戦闘終了: {res}")
                    pygame.mixer.music.stop()  # 戦闘BGMを止める
                    self.state = "MENU"

    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.idx = (self.idx - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.idx = (self.idx + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.execute_menu()

    def execute_menu(self):
        if self.idx == 0:  # ガチャ
            new_parts = spin_gacha(1)
            for p in new_parts:
                self.player.add_to_inventory(p)
                print(f"入手: {p['name']}")

        elif self.idx == 1:  # 編成
            self.assembly = AssemblyScene(self.player)
            self.state = "ASSEMBLY"

        elif self.idx == 2:  # 出撃
            print("艦隊、抜錨！")

            # --- 敵の選定ロジック ---
            boss_list = ["雪風", "大和", "武蔵", "長門", "赤城"]
            # 30%の確率でボス出現、それ以外は雑魚敵
            if random.random() < 0.3:
                target_name = random.choice(boss_list)
                dummy_enemy = EnemyShip.create_boss(target_name)
            else:
                # parts.py から適当な船体を選んで雑魚敵を生成
                enemy_hull = parts.HULL_RAW["駆逐艦"][0]
                dummy_enemy = EnemyShip("深海偵察艦", enemy_hull)

            # バトルシーンの初期化
            self.battle_view = BattleScene(self.player, dummy_enemy)
            self.state = "BATTLE"

        elif self.idx == 3:  # 終了
            self.quit_game()

    def update(self):
        pass

    def draw(self):
        if self.state == "MENU":
            self.screen.fill((30, 30, 50))
            self.draw_menu()
        elif self.state == "ASSEMBLY":
            self.assembly.draw(self.screen)
        elif self.state == "BATTLE":
            self.battle_view.draw(self.screen)

        pygame.display.flip()

    def draw_menu(self):
        """メインメニューの描画"""
        title = self.font.render(
            "--- FLEET COMMANDER ---", True, (255, 215, 0))
        self.screen.blit(title, (240, 100))

        for i, opt in enumerate(self.options):
            color = (0, 255, 150) if i == self.idx else (200, 200, 200)
            prefix = "▶ " if i == self.idx else "  "
            txt = self.font.render(prefix + opt, True, color)
            self.screen.blit(txt, (300, 250 + i * 50))

        # プレイヤーの簡易ステータス表示
        hp_info = self.sub_font.render(
            f"自艦HP: {self.player.stats['hp']}", True, (255, 255, 255))
        self.screen.blit(hp_info, (50, 530))

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    GameMaster().run()
