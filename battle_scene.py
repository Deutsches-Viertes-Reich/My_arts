import random


class BattleScene:
    @staticmethod
    def calculate_damage(attacker_stats, defender_stats, defender_name="", attack_type="main"):
        """
        隊長指定の計算式: ダメージ = 攻撃力 * (100 / (100 + 防御力))
        """
        # ステータス取得（最低値1を保証して0除算エラーを防止）
        atk = max(1, attacker_stats.get("atk", 1))
        defn = max(0, defender_stats.get("def", 0))

        # --- 1. 雪風専用の特殊回避ロジック ---
        # 物理法則を超えたしぶとさを再現（30%の確率で強制1ダメージ）
        if "雪風" in defender_name:
            if random.random() < 0.3:
                return 1, False

        # --- 2. 攻撃タイプによる倍率補正 ---
        # 主砲は一撃が重く、副砲は手数が多いため軽く設定
        multiplier = 1.2 if attack_type == "main" else 0.8
        modified_atk = atk * multiplier

        # --- 3. メイン計算式 (防御減衰) ---
        # ダメージ = 攻撃力 * (100 / (100 + 防御力))
        damage_ratio = 100 / (100 + defn)
        base_damage = modified_atk * damage_ratio

        # --- 4. クリティカル判定 (10%の確率でダメージ1.5倍) ---
        is_critical = random.random() < 0.1
        if is_critical:
            base_damage *= 1.5

        # --- 5. 最終調整 (乱数によるゆらぎ ±10%) ---
        final_damage = int(base_damage * random.uniform(0.9, 1.1))

        # 最低でも1ダメージは与える
        return max(1, final_damage), is_critical

    @staticmethod
    def process_turn(attacker, defender, attack_type, scene):
        """
        1ターン分の戦闘計算と反映を行う
        """
        # 名前を取得（ログ表示用）
        def_name = getattr(defender, "name", "敵艦")

        # ダメージ計算実行
        damage, crit = BattleSystem.calculate_damage(
            attacker.stats,
            defender.stats,
            def_name,
            attack_type
        )

        # 防御側のHPを減らす
        # EnemyShipクラスならtake_damageメソッドを使用、Playerなら直接減らす
        if hasattr(defender, "take_damage"):
            defender.take_damage(damage)
        elif hasattr(scene, "player_current_hp") and defender == scene.player:
            scene.player_current_hp -= damage
        else:
            # どちらでもない場合は直接 stats を操作（フォールバック）
            if hasattr(defender, "current_hp"):
                defender.current_hp -= damage

        # 戦闘ログにメッセージを追加
        msg = ""
        if crit:
            msg += "★会心の一撃！ "

        # 攻撃側がプレイヤーか敵かでログの書き方を変える
        if defender == scene.player:
            msg += f"味方艦は {damage} の被害を受けた！"
        else:
            msg += f"{def_name} に {damage} のダメージを与えた！"

        scene.add_message(msg)

        # 撃破判定（HPが0以下になったらTrueを返す）
        curr_hp = getattr(defender, "current_hp", 0)
        if defender == scene.player:
            curr_hp = scene.player_current_hp

        return curr_hp <= 0
