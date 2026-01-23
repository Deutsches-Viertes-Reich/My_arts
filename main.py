import pygame
import sys
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
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("艦隊RPG：リファイン版")
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.player = Player()
        self.assembly = AssemblyScene(self.player)
        # 戦闘画面用変数を初期化
        self.battle_view = None

        self.state = "MENU"
        self.options = ["ガチャを引く", "編成ドック", "出撃", "終了"]
        self.idx = 0
        self.font = pygame.font.SysFont("msgothic", 30)

    def run(self):
        while True:
            self.screen.fill((20, 20, 25))
            self.handle_input()

            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "ASSEMBLY":
                self.assembly.draw(self.screen)
            elif self.state == "BATTLE":
                if self.battle_view:
                    self.battle_view.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(30)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- 編成画面の入力 ---
            if self.state == "ASSEMBLY":
                if self.assembly.handle_event(event) == "MENU":
                    self.state = "MENU"

            # --- 戦闘画面の入力 ---
            elif self.state == "BATTLE":
                res = self.battle_view.handle_event(event)
                if res == "ESCAPE":
                    self.state = "MENU"
                elif res == "ATTACK_MAIN":
                    self.battle_view.add_message("主砲、てーっ！！")
                elif res == "ATTACK_SUB":
                    self.battle_view.add_message("副砲、斉射！")

            # --- メニュー画面の入力 ---
            elif self.state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.idx = (self.idx - 1) % len(self.options)
                if event.key == pygame.K_DOWN:
                    self.idx = (self.idx + 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    self.execute_menu()

    def execute_menu(self):
        if self.idx == 0:  # ガチャ
            new_items = spin_gacha(1)
            for item in new_items:
                self.player.add_to_inventory(item)
                print(f"【獲得】: {item['name']}")

        elif self.idx == 1:  # 編成
            self.assembly = AssemblyScene(self.player)
            self.state = "ASSEMBLY"

        elif self.idx == 2:  # 出撃
            print("艦隊、抜錨します！")
            # 敵を生成してバトルシーンをセットアップ
            dummy_enemy = EnemyShip("深海棲艦", parts.HULL_RAW["駆逐艦"][0])
            self.battle_view = BattleScene(self.player, dummy_enemy)
            self.state = "BATTLE"

        elif self.idx == 3:  # 終了
            pygame.quit()
            sys.exit()

    def draw_menu(self):
        for i, opt in enumerate(self.options):
            color = (0, 255, 100) if i == self.idx else (255, 255, 255)
            txt = self.font.render(opt, True, color)
            self.screen.blit(txt, (300, 200 + i * 60))

    def draw_text(self, text, x, y, color):
        surf = self.font.render(text, True, color)
        self.screen.blit(surf, (x, y))


if __name__ == "__main__":
    GameMaster().run()
