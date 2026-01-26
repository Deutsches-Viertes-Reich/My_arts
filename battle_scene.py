import pygame
from battle_system import BattleSystem


class BattleScene:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        # プレイヤーの現在HPを一時的に保存
        self.player_current_hp = player.stats.get("hp", 100)

        self.font = pygame.font.SysFont("msgothic", 18)
        self.log_font = pygame.font.SysFont("msgothic", 16)
        self.messages = ["戦闘開始！ 敵艦を発見！"]

    def add_message(self, msg):
        self.messages.append(msg)
        if len(self.messages) > 6:
            self.messages.pop(0)

    def draw(self, screen):
        screen.fill((10, 20, 40))
        # 敵のUI
        self.draw_unit_ui(screen, self.enemy, 450, 50,
                          (200, 50, 50), is_player=False)
        # プレイヤーのUI
        self.draw_unit_ui(screen, self.player, 50, 350,
                          (50, 200, 50), is_player=True)

        # ログ枠
        log_bg = pygame.Surface((700, 140))
        log_bg.set_alpha(150)
        log_bg.fill((0, 0, 0))
        screen.blit(log_bg, (50, 190))
        for i, msg in enumerate(self.messages):
            txt = self.log_font.render(msg, True, (255, 255, 255))
            screen.blit(txt, (70, 200 + i * 20))

        guide = self.font.render(
            "[1]:主砲  [2]:副砲  [ESC]:撤退", True, (255, 255, 0))
        screen.blit(guide, (250, 540))

    def draw_unit_ui(self, screen, unit, x, y, color, is_player):
        name = "味方艦隊" if is_player else getattr(unit, "name", "敵艦")
        curr = self.player_current_hp if is_player else unit.current_hp
        mx = unit.stats["hp"]

        txt = self.font.render(
            f"{name} (ATK:{unit.stats['atk']} DEF:{unit.stats['def']})", True, (255, 255, 255))
        screen.blit(txt, (x, y))

        # HPバー
        pygame.draw.rect(screen, (80, 80, 80), (x, y+30, 300, 20))
        ratio = max(0, curr / mx) if mx > 0 else 0
        pygame.draw.rect(screen, color, (x, y+30, int(300 * ratio), 20))
        hp_txt = self.font.render(f"HP: {curr} / {mx}", True, (255, 255, 255))
        screen.blit(hp_txt, (x + 100, y + 32))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # 1キー または テンキーの1
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                self.add_message("主砲、てーっ！！")
                is_dead = BattleSystem.process_turn(
                    self.player, self.enemy, "main", self)
                if is_dead:
                    self.add_message("敵艦の撃沈を確認！")
                    return "VICTORY"
                return self.enemy_turn()

            # 2キー または テンキーの2
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                self.add_message("副砲、斉射！")
                is_dead = BattleSystem.process_turn(
                    self.player, self.enemy, "sub", self)
                if is_dead:
                    self.add_message("目標、沈黙。")
                    return "VICTORY"
                return self.enemy_turn()

            elif event.key == pygame.K_ESCAPE:
                return "ESCAPE"
        return None

    def enemy_turn(self):
        self.add_message("敵艦の反撃！")
        damage, _ = BattleSystem.calculate_damage(
            self.enemy.stats, self.player.stats)
        self.player_current_hp -= damage
        self.add_message(f"味方艦に{damage}の被害！")
        if self.player_current_hp <= 0:
            self.add_message("大破、航行不能... 撤退します！")
            return "DEFEAT"
        return None
