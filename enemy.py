import random


class EnemyShip:
    def __init__(self, name, hull_data, main_cannon=None, secondary_cannon=None, anti_air=None):
        self.name = name
        self.hull = hull_data
        self.main_cannon = main_cannon
        self.secondary_cannon = secondary_cannon
        self.anti_air = anti_air

        self.current_hp = self.calculate_total_hp()
        self.stats = self.calculate_total_stats()

    def calculate_total_hp(self):
        """船体と装備から合計HPを計算"""
        total_hp = self.hull["hp"]
        if self.main_cannon:
            total_hp += self.main_cannon.get("hp", 0)
        if self.secondary_cannon:
            total_hp += self.secondary_cannon.get("hp", 0)
        if self.anti_air:
            total_hp += self.anti_air.get("hp", 0)
        # 他のパーツ（bridge, captain, armor, engine, item, skill）もHPを持つ可能性があれば追加
        return total_hp

    def calculate_total_stats(self):
        """船体と装備から合計ステータスを計算"""
        stats = {"atk": 0, "def": 0, "hp": 0, "spd": 0, "sp": 0}

        # 船体ステータスを初期値とする
        for key in stats:
            stats[key] = self.hull.get(key, 0)

        # 各装備のステータスを加算
        if self.main_cannon:
            for key in stats:
                stats[key] += self.main_cannon.get(key, 0)
        if self.secondary_cannon:
            for key in stats:
                stats[key] += self.secondary_cannon.get(key, 0)
        if self.anti_air:
            for key in stats:
                stats[key] += self.anti_air.get(key, 0)
        # 必要であれば、他のパーツもここで加算するロジックを追加

        return stats

    def take_damage(self, damage):
        """ダメージを受ける処理"""
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        return self.current_hp

    def is_defeated(self):
        """撃破されたか判定"""
        return self.current_hp <= 0

    def choose_action(self, player_ship_stats):
        """
        敵の行動を決定する簡易AI。
        プレイヤーのステータス（HPなど）を考慮に入れる。
        """
        # --- 簡易AIロジックの例 ---
        # 1. 自身のHPが低い場合、防御を優先
        if self.current_hp < self.calculate_total_hp() * 0.3 and self.stats["def"] > 0:
            return "defend"  # 防御を選択（例：ダメージを軽減する）

        # 2. プレイヤーのHPが高い場合、強力な攻撃を狙う
        elif player_ship_stats["hp"] > 500 and self.main_cannon:
            return "main_cannon_attack"  # 主砲攻撃

        # 3. それ以外はランダムに攻撃（副砲や対空砲も選択肢に）
        else:
            actions = []
            if self.main_cannon:
                actions.append("main_cannon_attack")
            if self.secondary_cannon:
                actions.append("secondary_cannon_attack")
            if self.anti_air:
                actions.append("anti_air_attack")  # 対空攻撃は敵が空母の場合など

            if actions:
                return random.choice(actions)
            else:
                return "do_nothing"  # 何もできない場合
