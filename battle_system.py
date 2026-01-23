import pygame
import random


class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.log = []  # 戦闘履歴
        self.turn = 1

    def player_attack(self, type="main"):
        """プレイヤーの攻撃処理"""
        if type == "main":
            damage = max(0, self.player.stats["atk"] - self.enemy.stats["def"])
            msg = f"主砲発射！ {self.enemy.name}に {damage} のダメージ！"
        else:
            damage = max(
                0, (self.player.stats["atk"] // 2) - self.enemy.stats["def"])
            msg = f"副砲掃射！ {self.enemy.name}に {damage} のダメージ！"

        self.enemy.take_damage(damage)
        self.log.append(msg)
        return damage

    def enemy_turn(self):
        """敵の疑似AIによる行動決定"""
        # enemy.pyで定義したAIロジックを呼び出す
        action = self.enemy.choose_action(self.player.stats)

        damage = 0
        if action == "main_cannon_attack":
            damage = max(0, self.enemy.stats["atk"] - self.player.stats["def"])
            msg = f"敵の主砲攻撃！ {damage} のダメージを受けた！"
        elif action == "defend":
            msg = f"{self.enemy.name}は防御を固めている！"
        else:
            msg = f"{self.enemy.name}は様子をうかがっている。"

        self.player.stats["hp"] -= damage
        self.log.append(msg)
        self.turn += 1
        return action
