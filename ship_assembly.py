import pygame
import sys

# カラー設定
WHITE = (255, 255, 255)
BLACK = (30, 30, 35)
GREEN = (0, 255, 150)
GRAY = (100, 100, 100)
GOLD = (255, 215, 0)


class AssemblyScene:
    def __init__(self, player, assets):
        self.player = player
        self.assets = assets
        self.font = pygame.font.SysFont("msgothic", 24)
        self.categories = [
            "hull", "main_cannon", "secondary_cannon",
            "armor", "engine", "captain", "item"
        ]
        self.selected_cat_idx = 0
        self.inventory = []  # 本来は所持品リストから取得
        self.state = "SELECT_CAT"  # "SELECT_CAT" or "SELECT_PART"

    def draw(self, screen):
        screen.fill(BLACK)

        # タイトル表示
        title = self.font.render("--- 艦隊換装ドック ---", True, GOLD)
        screen.blit(title, (50, 30))

        # 現在のステータス表示
        self.draw_stats(screen)

        # カテゴリ一覧の描画
        for i, cat in enumerate(self.categories):
            color = GREEN if (
                i == self.selected_cat_idx and self.state == "SELECT_CAT") else WHITE
            prefix = "▶ " if (
                i == self.selected_cat_idx and self.state == "SELECT_CAT") else "  "

            # 現在装備中のパーツ名を取得
            equipped = self.player.equipment.get(cat)
            equipped_name = equipped["name"] if equipped else "未装備"

            text = self.font.render(
                f"{prefix}{cat.upper():<16}: {equipped_name}", True, color)
            screen.blit(text, (50, 100 + i * 40))

        # 操作ガイド
        guide = self.font.render("上下:選択 / Enter:変更 / ESC:戻る", True, GRAY)
        screen.blit(guide, (50, 530))

    def draw_stats(self, screen):
        """右側に現在の合計ステータスを表示"""
        stats_x = 500
        pygame.draw.rect(screen, GRAY, (stats_x - 20, 90, 250, 200), 1)

        y_offset = 110
        self.player.update_stats()  # 最新の値を計算
        for stat_name, value in self.player.stats.items():
            stat_text = self.font.render(
                f"{stat_name.upper()}: {value}", True, WHITE)
            screen.blit(stat_text, (stats_x, y_offset))
            y_offset += 30

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "SELECT_CAT":
                if event.key == pygame.K_UP:
                    self.selected_cat_idx = (
                        self.selected_cat_idx - 1) % len(self.categories)
                elif event.key == pygame.K_DOWN:
                    self.selected_cat_idx = (
                        self.selected_cat_idx + 1) % len(self.categories)
                elif event.key == pygame.K_RETURN:
                    # 本来はここで「所持品リスト（inventory）」を開く処理へ
                    pass
                elif event.key == pygame.K_ESCAPE:
                    return "MENU"  # メインメニューに戻る信号
        return None
