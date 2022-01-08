[![Actions](https://github.com/konishi0125/predhinata_webapp/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/konishi0125/predhinata_webapp/actions/workflows/main.yml)
# predhinata webapp

# Require

開発前に下記ツールを準備してください

* Poetry
* npm

また、Pythonパッケージのビルド時に下記も必要になります。OSに応じてインストールしてください。

* cmake
* Python headers

例: Ubuntuの場合

```
$ sudo apt install python3-dev cmake
```


# 開発準備

```
$ poetry install
$ poetry run pre-commit install
$ npm i
```

# テストサーバーの起動

```
$ npm run build
$ poetry run poe runserver
```

# lintの実行

```
$ poetry run poe lint
$ npm run lint
```

# formatterの実行

コードの自動整形を行ってくれます

```
$ poetry run poe format
$ npm run format
```
