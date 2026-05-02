# QQ Versions

QQ Versions 是一个 QQ 官方安装包历史版本镜像。仓库会把可用的 Windows、macOS、Linux 安装包归档到 GitHub Releases，方便查找、下载和校验不同平台的历史版本。

**语言**：中文 | [English](README.en.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md)

## 下载历史版本

推荐入口：

- GitHub Pages 展示页：<https://rodert.github.io/qq-versions/>
- GitHub Releases：<https://github.com/Rodert/qq-versions/releases>

在展示页或 Releases 页面中选择需要的版本，然后按操作系统下载对应安装包：

- Windows：`.exe`
- macOS：`.dmg`
- Linux：`.deb`、`.rpm`、`.AppImage`

每个 Release 通常会附带 `SHA256SUMS.txt`，可用于校验下载文件是否完整。

## 怎么用

1. 打开 <https://rodert.github.io/qq-versions/>。
2. 按 Windows、macOS 或 Linux 筛选安装包。
3. 点击需要的文件下载。
4. 下载完成后直接运行安装包，或按你的系统包管理方式安装。

Linux 示例：

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

校验文件示例：

```bash
sha256sum -c SHA256SUMS.txt
```

## 仓库作用

这个仓库只做一件事：整理并发布 QQ 官方安装包的历史版本索引。它适合在以下场景使用：

- 需要下载旧版 QQ 安装包。
- 需要为不同操作系统保存同一时期的安装包。
- 需要通过 SHA256 校验安装包完整性。
- 需要一个更易浏览的 QQ Releases 下载页面。

安装包版权归腾讯所有。本仓库仅做历史版本索引与下载归档。
