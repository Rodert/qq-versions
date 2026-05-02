# QQ Versions

QQ Versions는 공식 QQ 설치 파일의 과거 버전 미러입니다. Windows, macOS, Linux용 설치 파일을 GitHub Releases에 정리해 이전 버전을 쉽게 찾고, 다운로드하고, 검증할 수 있게 합니다.

**언어**: [中文](README.md) | [English](README.en.md) | [Français](README.fr.md) | [日本語](README.ja.md) | 한국어 | [Русский](README.ru.md) | [Español](README.es.md)

## 과거 버전 다운로드

권장 링크:

- GitHub Pages 브라우저: <https://rodert.github.io/qq-versions/>
- GitHub Releases: <https://github.com/Rodert/qq-versions/releases>

Pages 또는 Releases 페이지를 열고 필요한 버전을 선택한 뒤 운영체제에 맞는 파일을 다운로드하세요.

- Windows: `.exe`
- macOS: `.dmg`
- Linux: `.deb`, `.rpm`, `.AppImage`

각 Release에는 보통 파일 무결성 확인용 `SHA256SUMS.txt`가 포함됩니다.

## 사용 방법

1. <https://rodert.github.io/qq-versions/> 를 엽니다.
2. Windows, macOS, Linux 중에서 패키지를 필터링합니다.
3. 필요한 파일을 클릭해 다운로드합니다.
4. 설치 파일을 실행하거나 시스템 패키지 방식에 따라 설치합니다.

Linux 예시:

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

체크섬 확인 예시:

```bash
sha256sum -c SHA256SUMS.txt
```

## 저장소 역할

이 저장소의 목적은 공식 QQ 설치 파일의 과거 버전 인덱스를 정리하고 배포하는 것입니다. 다음 상황에 유용합니다.

- 이전 QQ 설치 파일을 다운로드해야 할 때.
- 같은 시기의 여러 운영체제용 패키지를 보관해야 할 때.
- SHA256으로 설치 파일 무결성을 확인해야 할 때.
- 더 보기 쉬운 다운로드 페이지에서 QQ Releases를 탐색하고 싶을 때.

QQ 설치 파일의 저작권은 Tencent에 있습니다. 이 저장소는 과거 버전 인덱스와 다운로드 아카이브만 제공합니다.
