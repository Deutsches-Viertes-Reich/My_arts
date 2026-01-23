import pygame
import os


class AssetManager:
    def __init__(self):
        self.base_path = "assets"
        self.images = {}  # 画像キャッシュ用
        self.sounds = {}  # 効果音キャッシュ用

        # 初期化時にmixerが準備されているか確認
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    # --- 画像・スプライト関連 ---
    def get_image(self, filename, scale=None):
        """画像を読み込み、キャッシュから返す（スケーリング対応）"""
        if filename not in self.images:
            path = os.path.join(self.base_path, filename)
            try:
                # convert_alpha()で透明度を最適化して読み込み
                img = pygame.image.load(path).convert_alpha()
                if scale:
                    # scale=(width, height) のタプルでサイズ変更
                    img = pygame.transform.scale(img, scale)
                self.images[filename] = img
            except Exception as e:
                print(f"Error loading image {filename}: {e}")
                # エラー時は目立つ色のダミーを生成
                dummy = pygame.Surface((64, 64))
                dummy.fill((255, 0, 255))
                return dummy

        return self.images[filename]

    # --- サウンド・BGM関連 ---
    def play_bgm(self, filename, volume=0.5):
        """BGM(.wav)をループ再生する"""
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  # -1は無限ループ
        else:
            print(f"BGM not found: {path}")

    def get_sfx(self, filename):
        """効果音(.wav)をロードしてSoundオブジェクトを返す"""
        if filename not in self.sounds:
            path = os.path.join(self.base_path, filename)
            if os.path.exists(path):
                self.sounds[filename] = pygame.mixer.Sound(path)
            else:
                print(f"SFX not found: {path}")
                return None
        return self.sounds[filename]

# --- スプライトクラスのベース (RPG風のキャラ表示用) ---


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
