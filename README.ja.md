# QQ Versions

QQ Versions は、QQ 公式インストーラーの履歴ミラーです。Windows、macOS、Linux 向けのインストーラーを GitHub Releases に整理し、過去バージョンを探しやすく、ダウンロードしやすく、検証しやすくします。

**言語**: [中文](README.md) | [English](README.en.md) | [Français](README.fr.md) | 日本語 | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md)

## 過去バージョンのダウンロード

推奨入口：

- GitHub Pages 表示ページ: <https://rodert.github.io/qq-versions/>
- GitHub Releases: <https://github.com/Rodert/qq-versions/releases>

Pages または Releases を開き、必要なバージョンを選択して、利用中の OS に合うファイルをダウンロードしてください。

- Windows: `.exe`
- macOS: `.dmg`
- Linux: `.deb`、`.rpm`、`.AppImage`

各 Release には通常、ファイルの完全性確認に使える `SHA256SUMS.txt` が含まれています。

## 使い方

1. <https://rodert.github.io/qq-versions/> を開きます。
2. Windows、macOS、Linux でパッケージを絞り込みます。
3. 必要なファイルをクリックしてダウンロードします。
4. インストーラーを実行するか、利用中のシステムの方法でインストールします。

Linux の例：

```bash
sudo dpkg -i QQ*.deb
```

```bash
sudo rpm -i QQ*.rpm
```

```bash
chmod +x QQ*.AppImage
./QQ*.AppImage
```

チェックサム確認の例：

```bash
sha256sum -c SHA256SUMS.txt
```

## リポジトリの役割

このリポジトリの目的は、QQ 公式インストーラーの履歴インデックスを整理して公開することです。次の用途に向いています。

- 古い QQ インストーラーをダウンロードする。
- 同時期の複数 OS 向けパッケージを保存する。
- SHA256 でインストーラーの完全性を確認する。
- QQ Releases を見やすいダウンロードページから閲覧する。

QQ インストーラーの著作権は Tencent に帰属します。このリポジトリは履歴インデックスとダウンロードアーカイブのみを提供します。
