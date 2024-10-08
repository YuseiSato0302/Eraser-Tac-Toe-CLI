# Tic-Tac-Toe Game

## 概要

このプロジェクトは、Pythonで開発されたCLI（コマンドライン）ベースの**三目並べ（Tic-Tac-Toe）ゲーム**です。ユーザーは交互にコマを打ち、先に縦、横、または斜めに3つのコマを並べたプレイヤーが勝利します。また、4手目以降は古いコマが消えるという追加ルールが実装されています。将来的には、CPU対戦やオンライン対戦の機能を追加する予定です。

### 主な機能

- **2人プレイモード**: 同じマシンで交互にプレイできます。
- **コマの削除機能**: 4手目以降は、最も古いコマが消えます。
- **BGM再生機能**: ゲーム中にはBGMが流れ、タイトル画面とゲーム画面で異なる曲が再生されます。


## インストール方法

このプロジェクトをローカルで実行するには、以下の手順に従ってください。

### 1. リポジトリのクローン

まず、GitHubリポジトリをクローンします。

```bash
git clone https://github.com/YuseiSato0302/Eraser-Tac-Toe-CLI
cd Eraser-Tac-Toe-CLI
```

### 2. 仮想環境のセットアップ

Pythonの仮想環境を作成し、依存パッケージをインストールします。

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
```

### 3. 依存パッケージのインストール

`requirements.txt` に基づいて、依存関係をインストールします。

```bash
pip install -r requirements.txt
```


## 使い方
### ゲームの起動

以下のコマンドを実行してゲームを起動します。

```bash
python main.py
```

### ゲームの操作方法

- プレイヤーは、`a1` や `b2` のように、**行と列を指定**してコマを置きます。
- プレイヤーが3手目以降になると、**最も古いコマが消える**特殊ルールがあります。
- タイトル画面では「2人プレイ」「CPU対戦」「オンライン対戦」を選択可能ですが、CPU対戦とオンライン対戦は現在開発中です。


### 今後の拡張予定

- **AI対戦機能**: コンピュータと対戦できるモードを実装予定です。
- **オンライン対戦機能**: 他のプレイヤーとネットワークを介して対戦できるようにします。
- **UI改善**: コマの配置や削除のアニメーションを追加予定です。


## 必要な環境

このゲームを実行するために、以下の環境が必要です。

- **Python 3.8** 以上
- `mpg123`: BGMを再生するために必要です。インストールは以下のコマンドで行えます。
- `figlet`: タイトルの装飾を出力ために必要です。インストールは以下のコマンドで行えます。

```bash
# macOS
brew install mpg123
brew install figlet

# Ubuntu/Debian
sudo apt install mpg123
sudo apt install figlet
```


## 開発者向け情報

### テストの実行

以下のコマンドでテストを実行できます。

```bash
python -m unittest discover tests
```
