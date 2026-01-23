import pygame


class BattleScene:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.font = pygame.font.SysFont("msgothic", 18)
        self.log_font = pygame.font.SysFont("msgothic", 16)
        self.messages = ["戦闘開始！ 敵艦を発見！"]

    def add_message(self, msg):
        self.messages.append(msg)
        if len(self.messages) > 5:  # ログは最新5件まで
            self.messages.pop(0)

    def draw(self, screen):
        # 背景（海戦をイメージした暗い青）
        screen.fill((10, 20, 40))

        # --- 敵の情報 (上部) ---
        self.draw_unit_ui(screen, self.enemy, 450, 50, (200, 50, 50))

        # --- プレイヤーの情報 (下部) ---
        self.draw_unit_ui(screen, self.player, 50, 350, (50, 200, 50))

        # --- 戦闘ログの表示 ---
        log_bg = pygame.Surface((700, 120))
        log_bg.set_alpha(150)
        log_bg.fill((0, 0, 0))
        screen.blit(log_bg, (50, 200))

        for i, msg in enumerate(self.messages):
            txt = self.log_font.render(msg, True, (255, 255, 255))
            screen.blit(txt, (70, 210 + i * 20))

        # --- 操作ガイド ---
        guide = self.font.render(
            " [1]:主砲攻撃  [2]:副砲攻撃  [ESC]:撤退 ", True, (255, 255, 0))
        screen.blit(guide, (250, 530))

    def draw_unit_ui(self, screen, unit, x, y, color):
        """HPバーと名前を描画"""
        name = getattr(unit, "name", "味方艦隊")
        # PlayerかEnemyかでHPの持ち方が違う場合に対応
        current_hp = unit.current_hp if hasattr(
            unit, "current_hp") else unit.stats["hp"]
        max_hp = unit.stats["hp"]

        # 名前表示
        name_txt = self.font.render(f"NAME: {name}", True, (255, 255, 255))
        screen.blit(name_txt, (x, y))

        # HPバーの枠
        pygame.draw.rect(screen, (100, 100, 100), (x, y + 30, 300, 20))
        # HPバーの中身
        hp_ratio = max(0, current_hp / max_hp) if max_hp > 0 else 0
        pygame.draw.rect(screen, color, (x, y + 30, int(300 * hp_ratio), 20))
        # 数値表示
        hp_txt = self.font.render(
            f"HP: {current_hp} / {max_hp}", True, (255, 255, 255))
        screen.blit(hp_txt, (x + 100, y + 32))

    def handle_event(self, event):
        """戦闘中のキー入力を受け付ける"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return "ATTACK_MAIN"
            if event.key == pygame.K_2:
                return "ATTACK_SUB"
            if event.key == pygame.K_ESCAPE:
                return "ESCAPE"
        return None
