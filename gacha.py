import sys
import os
import random
from parts import ALL_PARTS

# WindowsでもUnix系でもどっちでもいいぞ！
try:
    import msvcrt

    def get_key():
        # Windows用
        ch = msvcrt.getch()
        if ch == b'\xe0':  # windows用やぞ
            ch = msvcrt.getch()
            return {b'H': 'up', b'P': 'down'}.get(ch, None)
        elif ch == b'\r':
            return 'enter'
        return None
except ImportError:
    import tty
    import termios

    def get_key():
        # マックとかリナックス用やぞ
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch = sys.stdin.read(2)
                return {'[A': 'up', '[B': 'down'}.get(ch, None)
            elif ch == '\r' or ch == '\n':
                return 'enter'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

# ガチャ本体
RARITY_WEIGHTS = {"N": 40, "R": 30, "SR": 15, "SSR": 10, "LEGEND": 5}


def get_parts_by_rarity(rarity):
    pool = []
    for ship_type in ALL_PARTS["hull"]:
        for item in ALL_PARTS["hull"][ship_type]:
            if item["rarity"] == rarity:
                pool.append(item)
    other_categories = ["main_cannon", "secondary_cannon", "anti_air",
                        "bridge", "captain", "armor", "engine", "item", "skill"]
    for cat in other_categories:
        for item in ALL_PARTS[cat]:
            if item["rarity"] == rarity:
                pool.append(item)
    return pool


def spin_gacha(times=1):
    results = []
    rarities = list(RARITY_WEIGHTS.keys())
    weights = list(RARITY_WEIGHTS.values())
    for _ in range(times):
        chosen_rarity = random.choices(rarities, weights=weights, k=1)[0]
        pool = get_parts_by_rarity(chosen_rarity)
        results.append(random.choice(pool) if pool else random.choice(
            get_parts_by_rarity("N")))
    return results

# メニュー


def print_menu(selected_index):
    os.system('cls' if os.name == 'nt' else 'clear')  # 画面更新
    options = ["1: 単発ガチャを引く", "2: 10連ガチャを引く", "3: 終了する"]
    print("=== ガチャメニュー (矢印キーで選択 / Enterで決定) ===")
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"> \033[92m{option}\033[0m")  # 選択箇所をハイライト
        else:
            print(f"  {option}")


def display_results(results):
    print("\n" + "="*40)
    print(f"--- ガチャ結果 ({len(results)}連) ---")
    print("="*40)
    for i, item in enumerate(results, 1):
        rarity_str = f"[{item['rarity']}]"
        if item['rarity'] == "LEGEND":
            rarity_str = f"✨{rarity_str}✨"
        print(f"{i:2d}: {rarity_str:10} {item['name']}")
    print("="*40)
    print("\n何かキーを押すとメニューに戻ります...")
    get_key()

# ガチャを回すぞ！


def main():
    selected_index = 0
    while True:
        print_menu(selected_index)
        key = get_key()

        if key == 'up':
            selected_index = (selected_index - 1) % 3
        elif key == 'down':
            selected_index = (selected_index + 1) % 3
        elif key == 'enter':
            if selected_index == 0:
                display_results(spin_gacha(1))
            elif selected_index == 1:
                display_results(spin_gacha(10))
            elif selected_index == 2:
                print("終了します。")
                break


if __name__ == "__main__":
    main()
