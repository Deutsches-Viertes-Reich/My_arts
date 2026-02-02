import pygame
from battle_system import BattleSystem
from assets_loading_system import AssetManager


class BattleScene:
    def __init__(self, player, enemy):
        # main.pyから渡されるデータを受け取る
        self.player = player
        self.enemy = enemy

        # プレイヤーの現在HPを一時的に保持（最大値を守るため）
        self.player_current_hp = player.stats.get("hp", 100)

        # フォント設定
        self.font = pygame.font.SysFont("msgothic", 18)
        self.log_font = pygame.font.SysFont("msgothic", 16)
        self.messages = ["戦闘開始！ 敵艦を発見！"]

        # --- サウンド管理 ---
        self.assets = AssetManager()

        # BGM再生 (ファイル名は実際の assets フォルダ内のものに合わせてください)
        self.assets.play_bgm("battle_bgm (1).wav", volume=0.3)

        # 効果音 (発射音のみ)
        self.sfx_main = self.assets.get_sfx("fire_main.wav")  # 主砲
        self.sfx_sub = self.assets.get_sfx("fire_sub.wav")   # 副砲

    def add_message(self, msg):
        """戦闘ログにメッセージを追加"""
        self.messages.append(msg)
        if len(self.messages) > 6:
            self.messages.pop(0)

    def draw(self, screen):
        """画面描画"""
        screen.fill((10, 20, 40))  # 深海の色

        # 敵のUI（上部）
        self.draw_unit_ui(screen, self.enemy, 450, 50,
                          (200, 50, 50), is_player=False)

        # プレイヤーのUI（下部）
        self.draw_unit_ui(screen, self.player, 50, 350,
                          (50, 200, 50), is_player=True)

        # 戦闘ログ枠
        log_bg = pygame.Surface((700, 140))
        log_bg.set_alpha(150)
        log_bg.fill((0, 0, 0))
        screen.blit(log_bg, (50, 190))

        for i, msg in enumerate(self.messages):
            txt = self.log_font.render(msg, True, (255, 255, 255))
            screen.blit(txt, (70, 200 + i * 20))

        # 操作ガイド (テンキー1,2にも対応)
        guide = self.font.render(
            "[1]:主砲  [2]:副砲  [ESC]:撤退", True, (255, 255, 0))
        screen.blit(guide, (250, 540))

    def draw_unit_ui(self, screen, unit, x, y, color, is_player):
        """HPバーとステータスの描画"""
        name = "味方艦隊" if is_player else getattr(unit, "name", "敵艦")
        # プレイヤーなら一時変数から、敵ならクラス内のHPから取得
        curr = self.player_current_hp if is_player else unit.current_hp
        mx = unit.stats["hp"]

        # 名前とステータス表示
        info_txt = self.font.render(
            f"{name} (ATK:{unit.stats['atk']} DEF:{unit.stats['def']})", True, (255, 255, 255))
        screen.blit(info_txt, (x, y))

        # HPバー
        pygame.draw.rect(screen, (80, 80, 80), (x, y + 30, 300, 20))  # 背景
        ratio = max(0, curr / mx) if mx > 0 else 0
        pygame.draw.rect(
            screen, color, (x, y + 30, int(300 * ratio), 20))  # 残量

        hp_txt = self.font.render(
            f"HP: {int(curr)} / {mx}", True, (255, 255, 255))
        screen.blit(hp_txt, (x + 100, y + 32))

    def handle_event(self, event):
        """入力処理"""
        if event.type == pygame.KEYDOWN:
            # --- 1: 主砲攻撃 ---
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                if self.sfx_main:
                    self.sfx_main.play()
                self.add_message("主砲、てーっ！！")

                # プレイヤーの攻撃実行
                is_dead = BattleSystem.process_turn(
                    self.player, self.enemy, "main", self)

                if is_dead:
                    self.add_message("敵艦の撃沈を確認！")
                    return "VICTORY"

                # 敵の反撃ターンへ
                return self.enemy_turn()

            # --- 2: 副砲攻撃 ---
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                if self.sfx_sub:
                    self.sfx_sub.play()
                self.add_message("副砲、斉射！")

                is_dead = BattleSystem.process_turn(
                    self.player, self.enemy, "sub", self)

                if is_dead:
                    self.add_message("目標の沈黙を確認。")
                    return "VICTORY"

                return self.enemy_turn()

            # --- ESC: 撤退 ---
            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return "ESCAPE"

        return None

    def enemy_turn(self):
        """敵側のターン処理"""
        self.add_message(f"{self.enemy.name}の反撃！")

        # 敵の攻撃（プレイヤーを防御側として計算）
        is_dead = BattleSystem.process_turn(
            self.enemy, self.player, "main", self)

        if self.player_current_hp <= 0:
            self.add_message("大破、航行不能... 撤退します！")
            pygame.mixer.music.stop()
            return "DEFEAT"

        return None
