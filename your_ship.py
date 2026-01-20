import json
import os


class Player:
    def __init__(self):
        # 初期装備（空の状態やデフォルト値）
        self.equipment = {
            "hull": None,
            "main_cannon": None,
            "secondary_cannon": None,
            "anti_air": None,
            "bridge": None,
            "captain": None,
            "armor": None,
            "engine": None,
            "item": None,
            "skill": None
        }
        # 最終的な合計ステータス
        self.stats = {"atk": 0, "def": 0, "hp": 0, "spd": 0, "sp": 0}

    def equip(self, category, part_data):
        """パーツを装備する"""
        if category in self.equipment:
            self.equipment[category] = part_data
            self.update_stats()

    def update_stats(self):
        """全装備から合計ステータスを再計算する"""
        # ステータスをリセット
        new_stats = {"atk": 0, "def": 0, "hp": 0, "spd": 0, "sp": 0}

        for category, part in self.equipment.items():
            if part:
                for stat in new_stats.keys():
                    # 各パーツの数値を加算
                    new_stats[stat] += part.get(stat, 0)

        self.stats = new_stats

    def save_data(self, filename="save_player.json"):
        """現在の装備状態を保存する"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.equipment, f, ensure_ascii=False, indent=4)

    def load_data(self, filename="save_player.json"):
        """保存された装備状態を読み込む"""
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                self.equipment = json.load(f)
                self.update_stats()
