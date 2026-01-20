import pygame
import os


class AssetLoader:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = assets_dir
        self.images = {}
        self.bgms = {}
        self.sfx = {}  # 効果音も将来的に追加可能

        pygame.mixer.init()  # サウンドを初期化

    def load_image(self, filename, scale=1.0):
        """画像を読み込み、必要であればスケーリングする"""
        if filename not in self.images:
            path = os.path.join(self.assets_dir, filename)
            if not os.path.exists(path):
                print(f"Warning: Image file not found: {path}")
                # ファイルが見つからない場合はダミーのサーフェスを返す
                # これにより、プログラムがクラッシュするのを防ぎます
                dummy_surface = pygame.Surface((100, 100))
                dummy_surface.fill((255, 0, 255))  # マゼンタ色で存在しないことを示す
                self.images[filename] = dummy_surface
                return dummy_surface

            try:
                image = pygame.image.load(path).convert_alpha()  # 透明度を保持
                if scale != 1.0:
                    size = (int(image.get_width() * scale),
                            int(image.get_height() * scale))
                    image = pygame.transform.scale(image, size)
                self.images[filename] = image
            except pygame.error as e:
                print(f"Error loading image {filename}: {e}")
                dummy_surface = pygame.Surface((100, 100))
                dummy_surface.fill((255, 0, 255))
                self.images[filename] = dummy_surface
                return dummy_surface
        return self.images[filename]

    def load_bgm(self, filename):
        """BGMファイルを読み込む (再生は別途行う)"""
        if filename not in self.bgms:
            path = os.path.join(self.assets_dir, filename)
            if not os.path.exists(path):
                print(f"Warning: BGM file not found: {path}")
                self.bgms[filename] = None  # ファイルがない場合はNoneを格納
                return None

            try:
                # BGMはパスを保存し、pygame.mixer.music.loadでロード
                self.bgms[filename] = path
            except pygame.error as e:
                print(f"Error loading BGM {filename}: {e}")
                self.bgms[filename] = None
                return None
        return self.bgms[filename]

    def play_bgm(self, filename, loop=-1, volume=0.5):
        """BGMを再生する"""
        bgm_path = self.load_bgm(filename)
        if bgm_path:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop)
        else:
            print(f"Cannot play BGM: {filename} (file not loaded or found)")

    def stop_bgm(self):
        """BGMを停止する"""
        pygame.mixer.music.stop()

    def get_image(self, filename):
        """読み込んだ画像を返す"""
        return self.images.get(filename)
