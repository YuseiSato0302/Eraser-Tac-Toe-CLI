import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

import unittest
from utils import validate_input, play_bgm
import subprocess

class TestUtils(unittest.TestCase):
    def test_validate_input(self):
        """入力の検証をテスト"""
        self.assertTrue(validate_input('a1'))
        self.assertTrue(validate_input('B2'))
        self.assertFalse(validate_input('d4'))
        self.assertFalse(validate_input('1a'))
        self.assertFalse(validate_input('ab'))

    def test_play_bgm_file_not_found(self):
        """BGMファイルが存在しない場合の処理をテスト"""
        process = play_bgm('nonexistent.mp3')
        self.assertIsNone(process)

    def test_play_bgm_mpg123_not_installed(self):
        """mpg123が未インストールの場合の処理をテスト"""
        original_popen = subprocess.Popen

        def mock_popen(*args, **kwargs):
            raise FileNotFoundError

        subprocess.Popen = mock_popen
        process = play_bgm('assets/title_bgm.mp3')
        self.assertIsNone(process)
        subprocess.Popen = original_popen

if __name__ == '__main__':
    unittest.main()
