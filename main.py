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
        # 画面設定（800x600）
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("艦隊RPG：10スロット・バトル実装版")
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
        """メインループ：ここがゲームの心臓部です"""
        while True:
            # 1. 入力の受付
            self.handle_input()

            # 2. 画面のクリア
            self.screen.fill((20, 20, 25))

            # 3. 状態に応じた描画
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "ASSEMBLY":
                if self.assembly:
                    self.assembly.draw(self.screen)
            elif self.state == "BATTLE":
                if self.battle_view:
                    self.battle_view.draw(self.screen)

            # 4. 画面更新
            pygame.display.flip()
            self.clock.tick(30)

    def handle_input(self):
        """イベントを各シーンへ適切に振り分ける"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            # --- バトル中：最優先でbattle_viewにイベントを渡す ---
            if self.state == "BATTLE":
                if self.battle_view:
                    res = self.battle_view.handle_event(event)
                    # バトル終了判定
                    if res in ["ESCAPE", "VICTORY", "DEFEAT"]:
                        print(f"戦闘結果: {res}")
                        self.state = "MENU"
                continue  # バトル中は以降のメニュー処理をスキップ

            # --- 編成中 ---
            elif self.state == "ASSEMBLY":
                if self.assembly:
                    res = self.assembly.handle_event(event)
                    if res == "MENU":
                        self.state = "MENU"
                continue

            # --- メニュー中 ---
            elif self.state == "MENU":
                self.handle_menu_input(event)

    def handle_menu_input(self, event):
        """メインメニューでのキー操作"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.idx = (self.idx - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.idx = (self.idx + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.execute_menu()

    def execute_menu(self):
        """メニュー項目の実行"""
        if self.idx == 0:  # ガチャ
            new_items = spin_gacha(1)
            for item in new_items:
                self.player.add_to_inventory(item)
                print(f"【獲得】: {item['name']}")

        elif self.idx == 1:  # 編成
            self.assembly = AssemblyScene(self.player)
            self.state = "ASSEMBLY"

        elif self.idx == 2:  # 出撃
            print("艦隊、抜錨！")
            # 敵データの生成（parts.pyに依存）
            enemy_hull = parts.HULL_RAW["駆須玖"][0] if "駆須玖" in parts.HULL_RAW else parts.HULL_RAW["駆逐艦"][0]
            dummy_enemy = EnemyShip("深海偵察艦", enemy_hull)

            # バトルシーンの初期化
            self.battle_view = BattleScene(self.player, dummy_enemy)
            self.state = "BATTLE"

        elif self.idx == 3:  # 終了
            self.quit_game()

    def draw_menu(self):
        """メインメニューの画面描画"""
        title = self.font.render(
            "--- FLEET COMMANDER ---", True, (255, 215, 0))
        self.screen.blit(title, (240, 100))

        for i, opt in enumerate(self.options):
            color = (0, 255, 150) if i == self.idx else (200, 200, 200)
            prefix = "▶ " if i == self.idx else "  "
            txt = self.font.render(prefix + opt, True, color)
            self.screen.blit(txt, (320, 220 + i * 60))

        # 現在のステータスを画面下に表示
        s = self.player.stats
        status_line = f"旗艦ステータス: HP {s['hp']} / ATK {s['atk']} / DEF {s['def']}"
        status_txt = self.sub_font.render(status_line, True, (150, 150, 150))
        self.screen.blit(status_txt, (50, 550))

    def quit_game(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    GameMaster().run()
