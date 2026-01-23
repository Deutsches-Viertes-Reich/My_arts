class Player:
    def __init__(self):
        # 倉庫
        self.inventory = []
        # ここを10種類に完全固定！！
        self.equipment = {
            "hull": None,
            "main_cannon": None,
            "secondary_cannon": None,
            "anti_air": None,      # 追加
            "captain": None,       # 追加
            "armor": None,         # 追加
            "engine": None,        # 追加
            "item": None,          # 追加
            "skill": None,         # 追加
            "bridge": None         # 追加
        }
        # 初期ステータス (sp を追加)
        self.stats = {"atk": 0, "def": 0, "hp": 100, "spd": 0, "sp": 0}

    def add_to_inventory(self, part):
        self.inventory.append(part)

    def equip(self, slot_name, part):
        if slot_name in self.equipment:
            self.equipment[slot_name] = part
            self.update_stats()

    def update_stats(self):
        # spを含む合計計算
        new_stats = {"atk": 0, "def": 0, "hp": 0, "spd": 0, "sp": 0}
        for part in self.equipment.values():
            if part:
                for key in new_stats:
                    new_stats[key] += part.get(key, 0)

        if new_stats["hp"] <= 0:
            new_stats["hp"] = 10
        self.stats = new_stats
