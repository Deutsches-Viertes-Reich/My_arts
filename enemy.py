import random
import parts


class EnemyShip:
    def __init__(self, name, stats, is_boss=False):
        self.name = name
        # ステータス項目: atk, def, hp, spd, sp
        self.stats = stats
        self.current_hp = stats.get("hp", 100)
        self.is_boss = is_boss

    def take_damage(self, damage):
        """ダメージを受ける処理"""
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp

    def is_defeated(self):
        """撃破判定"""
        return self.current_hp <= 0

    @staticmethod
    def create_boss(boss_name):
        """
        名前を指定して、理論上最強クラスのステータスを持つボスを生成。
        プレイヤーのATK数千、HP数万というインフレ環境に対応。
        """

        # --- Tier: GOD (武蔵) - 鉄壁の移動要塞 ---
        if boss_name == "武蔵":
            return EnemyShip("重装甲戦艦・武蔵", {
                "atk": 2200, "def": 5500, "hp": 8000000, "spd": 80, "sp": 50
            }, True)

        # --- Tier: GOD (大和) - 攻防一体の究極艦 ---
        elif boss_name == "大和":
            return EnemyShip("超弩級戦艦・大和", {
                "atk": 4500, "def": 3000, "hp": 5000000, "spd": 100, "sp": 50
            }, True)

        # --- Tier: SPECIAL (雪風) - 物理法則を超えたしぶとさ ---
        elif boss_name == "雪風":
            # DEFを極端に高くし、SPD（回避）をカンスト級にする
            return EnemyShip("不沈の名駆逐艦・雪風", {
                "atk": 1500, "def": 1000, "hp": 99999999, "spd": 2500, "sp": 100
            }, True)

        # --- Tier: OVERKILL (赤城) - 触れたら終わりの超火力 ---
        elif boss_name == "赤城":
            return EnemyShip("第一航空戦隊・赤城", {
                "atk": 12000, "def": 800, "hp": 45000, "spd": 600, "sp": 80
            }, True)

        # --- Tier: LEGEND (長門) - 屈強なビッグセブン ---
        elif boss_name == "長門":
            return EnemyShip("七大戦艦・長門", {
                "atk": 3800, "def": 2500, "hp": 70000, "spd": 150, "sp": 40
            }, True)

        # --- その他：通常の強敵 ---
        else:
            # 雑魚敵もプレイヤーが強すぎるので、parts.pyの値をベースに3倍に強化
            base_hull = parts.HULL_RAW.get("駆逐艦", [{"hp": 100}])[0].copy()
            weighted_stats = {
                "atk": base_hull.get("atk", 0) * 10 + 500,
                "def": base_hull.get("def", 0) * 5 + 300,
                "hp": base_hull.get("hp", 0) * 50 + 2000,
                "spd": base_hull.get("spd", 0) * 2,
                "sp": base_hull.get("sp", 0)
            }
            return EnemyShip(f"深海{boss_name}級", weighted_stats)
