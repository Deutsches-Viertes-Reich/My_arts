import pygame


class AssemblyScene:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont("msgothic", 22)
        self.slots = list(self.player.equipment.keys())
        self.current_slot_idx = 0
        self.selected_part_idx = 0
        self.state = "SELECT_SLOT"  # "SELECT_SLOT" or "SELECT_PART"

    def get_filtered_inventory(self):
        """現在のスロット属性と一致する所持パーツのみを抽出"""
        target_cat = self.slots[self.current_slot_idx]
        return [p for p in self.player.inventory if p.get("category") == target_cat]

    def draw(self, screen):
        screen.fill((30, 30, 45))
        # 左側：スロット選択
        self.draw_text(screen, "--- 装備スロット ---", 50, 50, (255, 215, 0))
        for i, slot in enumerate(self.slots):
            is_active = (self.state == "SELECT_SLOT" and i ==
                         self.current_slot_idx)
            color = (0, 255, 150) if is_active else (255, 255, 255)

            equipped = self.player.equipment[slot]
            part_name = equipped["name"] if equipped else "未装備"
            txt = f"{slot.upper()}: {part_name}"
            screen.blit(self.font.render(txt, True, color), (50, 100 + i * 45))

        # 右側：適合する所持パーツリスト
        pygame.draw.line(screen, (80, 80, 80), (400, 50), (400, 550), 2)
        parts = self.get_filtered_inventory()
        self.draw_text(screen, "--- 適合パーツ一覧 ---", 430, 50, (255, 215, 0))

        if not parts:
            self.draw_text(screen, "対象パーツなし", 430, 100, (150, 150, 150))
        else:
            for i, part in enumerate(parts):
                is_active = (self.state == "SELECT_PART" and i ==
                             self.selected_part_idx)
                color = (0, 255, 255) if is_active else (200, 200, 200)
                txt = f"[{part['rarity']}] {part['name']}"
                screen.blit(self.font.render(
                    txt, True, color), (430, 100 + i * 35))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "SELECT_SLOT":
                if event.key == pygame.K_UP:
                    self.current_slot_idx = (
                        self.current_slot_idx - 1) % len(self.slots)
                if event.key == pygame.K_DOWN:
                    self.current_slot_idx = (
                        self.current_slot_idx + 1) % len(self.slots)
                if event.key == pygame.K_RIGHT:
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
                if event.key == pygame.K_LEFT:
                    self.state = "SELECT_SLOT"
                if event.key == pygame.K_RETURN:
                    self.player.equip(
                        self.slots[self.current_slot_idx], parts[self.selected_part_idx])
                    self.state = "SELECT_SLOT"
        return None

    def draw_text(self, screen, text, x, y, color):
        screen.blit(self.font.render(text, True, color), (x, y))
