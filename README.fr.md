# QQ Versions

QQ Versions est un miroir historique des installateurs officiels de QQ. Il archive les paquets disponibles pour Windows, macOS et Linux dans GitHub Releases afin de faciliter la consultation, le téléchargement et la vérification des anciennes versions.

**Langues** : [中文](README.md) | [English](README.en.md) | Français | [日本語](README.ja.md) | [한국어](README.ko.md) | [Русский](README.ru.md) | [Español](README.es.md)

## Télécharger les anciennes versions

Entrées recommandées :

- Page GitHub Pages : <https://rodert.github.io/qq-versions/>
- GitHub Releases : <https://github.com/Rodert/qq-versions/releases>

Ouvrez la page GitHub Pages ou GitHub Releases, choisissez une version, puis téléchargez le paquet correspondant à votre système :

- Windows : `.exe`
- macOS : `.dmg`
- Linux : `.deb`, `.rpm`, `.AppImage`

Chaque Release inclut généralement `SHA256SUMS.txt` pour vérifier l'intégrité des fichiers.

## Utilisation

1. Ouvrez <https://rodert.github.io/qq-versions/>.
2. Filtrez les paquets par Windows, macOS ou Linux.
3. Cliquez sur le fichier à télécharger.
4. Lancez l'installateur ou installez le paquet selon la méthode habituelle de votre système.

Exemples Linux :

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

Exemple de vérification :

```bash
sha256sum -c SHA256SUMS.txt
```

## Rôle du dépôt

Ce dépôt a un seul objectif : organiser et publier un index historique des installateurs officiels de QQ. Il est utile pour :

- Télécharger un ancien installateur QQ.
- Conserver des paquets pour plusieurs systèmes d'exploitation sur une même période.
- Vérifier l'intégrité des installateurs avec SHA256.
- Parcourir les Releases QQ depuis une page de téléchargement plus lisible.

Les installateurs QQ sont protégés par les droits de Tencent. Ce dépôt fournit uniquement un index historique et une archive de téléchargement.
