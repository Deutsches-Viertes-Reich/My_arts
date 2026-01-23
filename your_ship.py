class Player:
    def __init__(self):
        # ガチャで引いた全パーツを保管する倉庫
        self.inventory = []
        # 現在装備しているパーツのスロット
        self.equipment = {
            "hull": None,
            "main_cannon": None,
            "secondary_cannon": None,
            "armor": None,
            "engine": None
        }
        # 合計ステータス
        self.stats = {"atk": 0, "def": 0, "hp": 100, "spd": 0}

    def add_to_inventory(self, part):
        """ガチャ結果を倉庫に放り込む"""
        self.inventory.append(part)

    def equip(self, slot_name, part):
        """スロットに装備してステータスを更新"""
        self.equipment[slot_name] = part
        self.update_stats()

    def update_stats(self):
        """全装備の数値を合計する"""
        new_stats = {"atk": 0, "def": 0, "hp": 0, "spd": 0}
        for part in self.equipment.values():
            if part:
                for key in new_stats:
                    new_stats[key] += part.get(key, 0)

        if new_stats["hp"] <= 0:
            new_stats["hp"] = 10
        self.stats = new_stats
