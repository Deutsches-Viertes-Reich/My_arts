import pygame


class AssemblyScene:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont("msgothic", 18)
        # ここでPlayerからスロット名（10個）を吸い出す
        self.slots = list(self.player.equipment.keys())
        self.current_slot_idx = 0
        self.selected_part_idx = 0
        self.state = "SELECT_SLOT"

    def get_filtered_inventory(self):
        target_cat = self.slots[self.current_slot_idx]
        return [p for p in self.player.inventory if p.get("category") == target_cat]

    def draw(self, screen):
        screen.fill((20, 25, 40))
        self.draw_text(screen, "=== 艦隊編成ドック (10 SLOT SYSTEM) ===",
                       50, 20, (255, 215, 0))

        # 10個のスロットを2列に並べる
        for i, slot in enumerate(self.slots):
            col = i // 5  # 0か1
            row = i % 5   # 0〜4
            x = 40 + (col * 380)
            y = 70 + (row * 80)

            is_active = (self.state == "SELECT_SLOT" and i ==
                         self.current_slot_idx)
            color = (0, 255, 255) if is_active else (150, 150, 150)

            # 枠を描く
            pygame.draw.rect(screen, color, (x, y, 350, 65),
                             2 if is_active else 1)

            equipped = self.player.equipment[slot]
            name_text = equipped["name"] if equipped else "---"
            rarity = f"[{equipped['rarity']}]" if equipped else ""

            self.draw_text(screen, f"{slot.upper()}:",
                           x + 10, y + 10, (100, 100, 100))
            self.draw_text(
                screen, f"{rarity} {name_text}", x + 10, y + 35, color)

        # ステータス表示
        self.draw_stats(screen)

        if self.state == "SELECT_PART":
            self.draw_part_selector(screen)

    def draw_stats(self, screen):
        s = self.player.stats
        # 安全に数値を取り出す
        hp, atk, df, spd, sp = s.get("hp", 0), s.get("atk", 0), s.get(
            "def", 0), s.get("spd", 0), s.get("sp", 0)
        stat_line = f"HP: {hp}  ATK: {atk}  DEF: {df}  SPD: {spd}  SP: {sp}"
        self.draw_text(screen, "【艦隊総合性能】", 50, 480, (255, 255, 0))
        self.draw_text(screen, stat_line, 50, 510, (255, 255, 255))

    def draw_part_selector(self, screen):
        overlay = pygame.Surface((500, 400))
        overlay.set_alpha(235)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (150, 100))

        parts = self.get_filtered_inventory()
        target_cat = self.slots[self.current_slot_idx]
        self.draw_text(screen, f"倉庫: {target_cat}", 170, 120, (0, 255, 255))

        for i, p in enumerate(parts):
            color = (255, 255, 255)
            if i == self.selected_part_idx:
                color = (255, 255, 0)
                pygame.draw.rect(screen, color, (165, 155 + i*30, 470, 25), 1)
            self.draw_text(
                screen, f"[{p['rarity']}] {p['name']}", 170, 160 + i*30, color)

    def draw_text(self, screen, text, x, y, color):
        surf = self.font.render(text, True, color)
        screen.blit(surf, (x, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "SELECT_SLOT":
                # 10スロット間の移動
                if event.key == pygame.K_UP:
                    self.current_slot_idx = (self.current_slot_idx - 1) % 10
                if event.key == pygame.K_DOWN:
                    self.current_slot_idx = (self.current_slot_idx + 1) % 10
                if event.key == pygame.K_LEFT:
                    self.current_slot_idx = (self.current_slot_idx - 5) % 10
                if event.key == pygame.K_RIGHT:
                    self.current_slot_idx = (self.current_slot_idx + 5) % 10

                if event.key == pygame.K_RETURN:
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
