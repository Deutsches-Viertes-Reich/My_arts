import random


class BattleSystem:
    @staticmethod
    def calculate_damage(attacker_stats, defender_stats, attack_type="main"):
        """ダメージ計算式"""
        base_atk = attacker_stats.get("atk", 0)
        target_def = defender_stats.get("def", 0)

        # 攻撃タイプによる倍率
        multiplier = 1.2 if attack_type == "main" else 0.8

        # ダメージ計算（最低1ダメージ保障）
        damage = int((base_atk * multiplier) - (target_def / 2))
        if damage < 1:
            damage = 1

        # クリティカル判定 (10%の確率)
        is_critical = random.random() < 0.1
        if is_critical:
            damage = int(damage * 1.5)

        return max(1, damage), is_critical

    @staticmethod
    def process_turn(attacker, defender, attack_type, scene):
        """1ターン分の処理を回す"""
        # 1. 攻撃側のダメージ計算
        damage, crit = BattleSystem.calculate_damage(
            attacker.stats, defender.stats, attack_type)

        # 2. 防御側のHPを減らす
        if hasattr(defender, "current_hp"):
            defender.current_hp -= damage
        else:
            # プレイヤーのダメージはBattleScene側で管理しているのでここでは計算のみ
            pass

        # 3. ログに反映
        msg = "クリティカル！ " if crit else ""
        msg += f"{damage}のダメージを与えた！"
        scene.add_message(msg)

        # 撃破判定
        current_hp = defender.current_hp if hasattr(
            defender, "current_hp") else defender.stats["hp"]
        return current_hp <= 0
