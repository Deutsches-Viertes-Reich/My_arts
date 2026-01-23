import random
# parts.py で定義した巨大なリストを読み込む
from parts import ALL_PARTS_LIST


def spin_gacha(times=1):
    """
    ALL_PARTS_LIST から指定された回数分、パーツを抽選して返します。
    """
    results = []

    # そもそもリストが空っぽだったらエラーにならないようガード
    if not ALL_PARTS_LIST:
        print("警告: parts.py の ALL_PARTS_LIST が空っぽです！")
        return results

    for _ in range(times):
        # ランダムに一つ選ぶ
        item = random.choice(ALL_PARTS_LIST)

        # 辞書の「参照」ではなく「中身のコピー」を渡すのがポイント
        # これをしないと、同じ装備を2つ持ったときにステータス計算がおかしくなることがあります
        results.append(item.copy())

    return results


# --- テスト用コード (このファイルを直接実行した時だけ動く) ---
if __name__ == "__main__":
    print("ガチャを3回テストで回します...")
    test_results = spin_gacha(3)
    for i, res in enumerate(test_results):
        print(
            f"{i+1}回目: [{res['rarity']}] {res['name']} (カテゴリ: {res['category']})")
