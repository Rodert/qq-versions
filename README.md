# qq-versions

自动扫描 QQ 官网下载配置，并把新的 QQ 安装包上传到 GitHub Releases。

## 工作方式

仓库内的 GitHub Action 会在每次提交推送后运行，也会每天定时运行一次：

1. 读取 QQ 官网使用的桌面端下载配置。
2. 同时检查官方 CDN 地址和官网代理地址，并选择版本/更新日期更新的安装包。
3. 根据安装包版本生成 Release tag。
4. 如果这个 tag 已经存在，则跳过下载和发布。
5. 如果发现新版本，则下载安装包、生成 `SHA256SUMS.txt`，并创建 GitHub Release。

默认同步所有已支持的 Windows、macOS、Linux 安装包。可以在 GitHub Actions 页面手动运行 workflow，并通过 `targets` 参数指定其中一部分安装包。

## 自动运行规则

Workflow: `.github/workflows/sync-qq-release.yml`

每次 push 后都会运行：

```yaml
push:
```

默认 cron 为每天北京时间 02:20：

```yaml
schedule:
  - cron: "20 18 * * *"
```

GitHub Actions 的 cron 使用 UTC 时间，所以 `18:20 UTC` 对应北京时间第二天 `02:20`。

## 支持的 targets

多个 target 用英文逗号分隔，例如：

```text
windows-x64,windows-x86,windows-arm64,macos
```

当前支持：

- `windows-x64`
- `windows-x86`
- `windows-arm64`
- `windows-classic`
- `macos`
- `linux-amd64-deb`
- `linux-amd64-rpm`
- `linux-amd64-appimage`
- `linux-arm64-deb`
- `linux-arm64-rpm`
- `linux-arm64-appimage`
- `linux-loongarch64-deb`
- `linux-mips64el-deb`

## 本地测试

只解析官网配置，不下载大文件：

```bash
QQ_DRY_RUN=1 python3 scripts/sync_qq_release.py
```

指定多个安装包：

```bash
QQ_DRY_RUN=1 QQ_RELEASE_TARGETS=windows-x64,macos python3 scripts/sync_qq_release.py
```

默认解析全部支持的安装包：

```bash
QQ_DRY_RUN=1 python3 scripts/sync_qq_release.py
```

实际下载到 `dist/qq-release`：

```bash
python3 scripts/sync_qq_release.py --output-dir dist/qq-release
```
