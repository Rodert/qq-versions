# QQ Versions

QQ Versions is a historical mirror for official QQ installers. It archives available Windows, macOS, and Linux packages in GitHub Releases so older versions are easier to browse, download, and verify.

**Languages**: [中文](README.md) | English | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md)

## Download Historical Versions

Recommended entry points:

- GitHub Pages browser: <https://rodert.github.io/qq-versions/>
- GitHub Releases: <https://github.com/Rodert/qq-versions/releases>

Open the Pages browser or Releases page, choose a version, then download the package for your operating system:

- Windows: `.exe`
- macOS: `.dmg`
- Linux: `.deb`, `.rpm`, `.AppImage`

Each Release usually includes `SHA256SUMS.txt` for file integrity verification.

## How To Use

1. Open <https://rodert.github.io/qq-versions/>.
2. Filter packages by Windows, macOS, or Linux.
3. Click the file you need to download.
4. Run the installer, or install it using your system package tools.

Linux examples:

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

Checksum example:

```bash
sha256sum -c SHA256SUMS.txt
```

## Repository Purpose

This repository has one purpose: organize and publish a historical index of official QQ installers. It is useful when you need to:

- Download an older QQ installer.
- Keep packages for multiple operating systems from the same release period.
- Verify installer integrity with SHA256 checksums.
- Browse QQ Releases through a cleaner download page.

QQ installers are copyrighted by Tencent. This repository only provides a historical index and download archive.
