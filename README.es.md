# QQ Versions

QQ Versions es un espejo histórico de instaladores oficiales de QQ. Archiva paquetes disponibles para Windows, macOS y Linux en GitHub Releases para que las versiones antiguas sean más fáciles de explorar, descargar y verificar.

**Idiomas**: [中文](README.md) | [English](README.en.md) | [Français](README.fr.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | Español

## Descargar versiones antiguas

Entradas recomendadas:

- Página de GitHub Pages: <https://rodert.github.io/qq-versions/>
- GitHub Releases: <https://github.com/Rodert/qq-versions/releases>

Abre la página de GitHub Pages o GitHub Releases, elige una versión y descarga el paquete para tu sistema operativo:

- Windows: `.exe`
- macOS: `.dmg`
- Linux: `.deb`, `.rpm`, `.AppImage`

Cada Release normalmente incluye `SHA256SUMS.txt` para verificar la integridad de los archivos.

## Cómo usarlo

1. Abre <https://rodert.github.io/qq-versions/>.
2. Filtra los paquetes por Windows, macOS o Linux.
3. Haz clic en el archivo que necesitas descargar.
4. Ejecuta el instalador o instala el paquete con el método habitual de tu sistema.

Ejemplos para Linux:

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

Ejemplo de verificación:

```bash
sha256sum -c SHA256SUMS.txt
```

## Propósito del repositorio

Este repositorio tiene un único propósito: organizar y publicar un índice histórico de instaladores oficiales de QQ. Es útil para:

- Descargar un instalador antiguo de QQ.
- Conservar paquetes para varios sistemas operativos del mismo periodo.
- Verificar la integridad del instalador con SHA256.
- Explorar QQ Releases desde una página de descarga más clara.

Los instaladores de QQ son propiedad de Tencent. Este repositorio solo proporciona un índice histórico y un archivo de descargas.
