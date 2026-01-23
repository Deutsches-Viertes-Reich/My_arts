import pygame


class AssemblyScene:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont("msgothic", 20)
        self.slots = list(self.player.equipment.keys())
        self.current_slot_idx = 0
        self.selected_part_idx = 0
        self.state = "SELECT_SLOT"

    def get_filtered_inventory(self):
        target_cat = self.slots[self.current_slot_idx]
        return [p for p in self.player.inventory if p.get("category") == target_cat]

    def draw(self, screen):
        screen.fill((20, 30, 60))  # 少し深みのある青（ドックっぽさ）

        # --- 左側：スロット選択 (2列表示) ---
        self.draw_text(screen, "=== 装備編成ドック (全10スロット) ===",
                       50, 20, (255, 255, 0))

        for i, slot in enumerate(self.slots):
            # 2列に分ける計算 (x座標をiによって変える)
            col = i // 5  # 0か1
            row = i % 5   # 0～4
            x = 50 + (col * 300)
            y = 80 + (row * 70)

            is_active = (self.state == "SELECT_SLOT" and i ==
                         self.current_slot_idx)
            color = (0, 255, 255) if is_active else (200, 200, 200)

            # スロット名と装備品名
            equipped = self.player.equipment[slot]
            part_name = equipped["name"] if equipped else "--- 未装備 ---"
            rarity = f"[{equipped['rarity']}]" if equipped else ""

            pygame.draw.rect(screen, color, (x-5, y-5, 280, 60),
                             2 if is_active else 1)
            self.draw_text(screen, f"{slot.upper()}:", x, y, (150, 150, 150))
            self.draw_text(screen, f"{rarity} {part_name}", x, y + 25, color)

        # --- 右側：ステータス詳細 ---
        self.draw_stats(screen)

        # --- パーツ選択モード時のオーバーレイ ---
        if self.state == "SELECT_PART":
            self.draw_part_selector(screen)

    def draw_stats(self, screen):
        # 画面下部に合計ステータスを表示
        s = self.player.stats
        stat_str = f"HP: {s['hp']}  ATK: {s['atk']}  DEF: {s['def']}  SPD: {s['spd']}  SP: {s['sp']}"
        self.draw_text(screen, "【現在の艦隊性能】", 50, 450, (255, 215, 0))
        self.draw_text(screen, stat_str, 50, 480, (255, 255, 255))
        self.draw_text(screen, "ESC: メニューへ  矢印キー: 選択  ENTER: 決定",
                       50, 550, (100, 100, 100))

    def draw_part_selector(self, screen):
        # パーツ選択ウィンドウを画面中央に
        overlay = pygame.Surface((400, 400))
        overlay.set_alpha(230)
        overlay.fill((10, 10, 20))
        screen.blit(overlay, (200, 100))

        target_cat = self.slots[self.current_slot_idx]
        parts = self.get_filtered_inventory()

        self.draw_text(screen, f"倉庫: {target_cat}", 220, 120, (255, 255, 0))

        if not parts:
            self.draw_text(screen, "対象パーツがありません", 220, 200, (255, 0, 0))
        else:
            for i, p in enumerate(parts):
                color = (255, 255, 255)
                if i == self.selected_part_idx:
                    color = (255, 100, 255)
                    pygame.draw.rect(
                        screen, color, (215, 155 + i*30, 370, 28), 1)

                txt = f"[{p['rarity']}] {p['name']} (ATK:{p.get('atk', 0)}/DEF:{p.get('def', 0)})"
                self.draw_text(screen, txt, 220, 160 + i*30, color)

    def draw_text(self, screen, text, x, y, color):
        surf = self.font.render(text, True, color)
        screen.blit(surf, (x, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "SELECT_SLOT":
                if event.key == pygame.K_UP:
                    self.current_slot_idx = (
                        self.current_slot_idx - 1) % len(self.slots)
                if event.key == pygame.K_DOWN:
                    self.current_slot_idx = (
                        self.current_slot_idx + 1) % len(self.slots)
                # 左右キーで列移動
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if self.current_slot_idx < 5:
                        self.current_slot_idx += 5
                    else:
                        self.current_slot_idx -= 5
                    self.current_slot_idx %= len(self.slots)

                if event.key == pygame.K_RETURN:  # 決定キーでパーツ選択へ
                    if self.get_filtered_inventory():
                        self.state = "SELECT_PART"
                        self.selected_part_idx = 0
                if event.key == pygame.K_ESCAPE:
                    return "MENU"

            elif self.state == "SELECT_PART":
                parts = self.get_filtered_inventory()
                if event.key == pygame.K_UP:
                    self.selected_part_idx = (
                        self.selected_part_idx - 1) % len(parts)
                if event.key == pygame.K_DOWN:
                    self.selected_part_idx = (
                        self.selected_part_idx + 1) % len(parts)
                if event.key == pygame.K_ESCAPE:
                    self.state = "SELECT_SLOT"
                if event.key == pygame.K_RETURN:
                    self.player.equip(
                        self.slots[self.current_slot_idx], parts[self.selected_part_idx])
                    self.state = "SELECT_SLOT"
        return None
