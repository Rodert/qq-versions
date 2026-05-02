#!/usr/bin/env python3
"""Create release metadata and download current QQ installers.

The script reads QQ's official desktop download config, decides whether the
corresponding GitHub release already exists, and downloads selected installer
assets only when a release should be created.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


OFFICIAL_SITE_URL = "https://im.qq.com/index/"
PC_CONFIG_URLS = [
    "https://im.qq.com/proxy/domain/cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json",
    "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/pcConfig.json",
]
DEFAULT_TARGETS = "windows-x64"
USER_AGENT = (
    "Mozilla/5.0 (compatible; qq-versions-release-bot/1.0; "
    "+https://github.com/${GITHUB_REPOSITORY:-unknown})"
)


@dataclass(frozen=True)
class ConfigCandidate:
    url: str
    data: dict


@dataclass(frozen=True)
class Package:
    target: str
    platform: str
    arch: str
    version: str
    update_date: str
    url: str

    @property
    def filename(self) -> str:
        parsed = urllib.parse.urlparse(self.url)
        name = Path(urllib.parse.unquote(parsed.path)).name
        if not name:
            raise ValueError(f"Cannot derive filename from URL: {self.url}")
        return name


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y", "on"}


def request(url: str, timeout: int = 30) -> urllib.request.Request:
    return urllib.request.Request(url, headers={"User-Agent": USER_AGENT})


def fetch_json(url: str, timeout: int = 30) -> dict:
    with urllib.request.urlopen(request(url), timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw.decode("utf-8"))


def fetch_configs() -> list[ConfigCandidate]:
    candidates: list[ConfigCandidate] = []
    errors: list[str] = []
    for url in PC_CONFIG_URLS:
        try:
            candidates.append(ConfigCandidate(url=url, data=fetch_json(url)))
        except Exception as exc:  # noqa: BLE001 - emit all URL failures clearly
            errors.append(f"{url}: {exc}")

    if not candidates:
        raise RuntimeError("Could not fetch any official QQ config:\n" + "\n".join(errors))

    if errors:
        print("Some config URLs failed; continuing with successful configs:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
    return candidates


def version_key(version: str) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", version or "")
    return tuple(int(item) for item in numbers)


def date_key(update_date: str) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", update_date or "")
    return tuple(int(item) for item in numbers[:3])


def package_key(package: Package) -> tuple[tuple[int, ...], tuple[int, ...], str]:
    return (date_key(package.update_date), version_key(package.version), package.url)


def normalize_date(update_date: str) -> str:
    match = re.search(r"(\d{4})\D?(\d{2})\D?(\d{2})", update_date or "")
    if not match:
        return "unknown-date"
    return "-".join(match.groups())


def compact_date(update_date: str) -> str:
    normalized = normalize_date(update_date)
    return normalized.replace("-", "") if normalized != "unknown-date" else normalized


def package_from_config(target: str, candidate: ConfigCandidate) -> Package:
    data = candidate.data
    windows = data.get("Windows") or {}
    linux = data.get("Linux") or {}
    macos = data.get("macOS") or {}

    if target == "windows-x64":
        return Package(target, "Windows", "x64", windows["version"], windows["updateDate"], windows["ntDownloadX64Url"])
    if target == "windows-x86":
        return Package(target, "Windows", "x86", windows["version"], windows["updateDate"], windows["ntDownloadUrl"])
    if target == "windows-arm64":
        return Package(target, "Windows", "arm64", windows["version"], windows["updateDate"], windows["ntDownloadARMUrl"])
    if target == "windows-classic":
        return Package(target, "Windows", "classic", "9.7.25", "legacy", windows["downloadUrl"])
    if target == "macos":
        return Package(target, "macOS", "universal", macos["version"], macos["updateDate"], macos["downloadUrl"])
    if target == "linux-amd64-deb":
        return Package(target, "Linux", "amd64-deb", linux["version"], linux["updateDate"], linux["x64DownloadUrl"]["deb"])
    if target == "linux-amd64-rpm":
        return Package(target, "Linux", "amd64-rpm", linux["version"], linux["updateDate"], linux["x64DownloadUrl"]["rpm"])
    if target == "linux-amd64-appimage":
        return Package(target, "Linux", "amd64-appimage", linux["version"], linux["updateDate"], linux["x64DownloadUrl"]["appimage"])
    if target == "linux-arm64-deb":
        return Package(target, "Linux", "arm64-deb", linux["version"], linux["updateDate"], linux["armDownloadUrl"]["deb"])
    if target == "linux-arm64-rpm":
        return Package(target, "Linux", "arm64-rpm", linux["version"], linux["updateDate"], linux["armDownloadUrl"]["rpm"])
    if target == "linux-arm64-appimage":
        return Package(target, "Linux", "arm64-appimage", linux["version"], linux["updateDate"], linux["armDownloadUrl"]["appimage"])
    if target == "linux-loongarch64-deb":
        return Package(target, "Linux", "loongarch64-deb", linux["version"], linux["updateDate"], linux["loongarchDownloadUrl"])
    if target == "linux-mips64el-deb":
        return Package(target, "Linux", "mips64el-deb", linux["version"], linux["updateDate"], linux["mipsDownloadUrl"])

    raise ValueError(f"Unknown target: {target}")


def parse_targets(value: str) -> list[str]:
    targets = [item.strip() for item in value.split(",") if item.strip()]
    if not targets:
        raise ValueError("At least one target is required")
    return targets


def select_packages(targets: Iterable[str], candidates: list[ConfigCandidate]) -> list[Package]:
    packages: list[Package] = []
    for target in targets:
        target_packages = [package_from_config(target, candidate) for candidate in candidates]
        packages.append(max(target_packages, key=package_key))
    return packages


def release_identity(packages: list[Package]) -> tuple[str, str]:
    if len(packages) == 1:
        package = packages[0]
        date = compact_date(package.update_date)
        target = package.target.replace("_", "-")
        tag = f"qq-{target}-{package.version}-{date}"
        title = f"QQ {package.platform} {package.arch} {package.version} ({normalize_date(package.update_date)})"
        return sanitize_tag(tag), title

    latest = max(packages, key=package_key)
    digest_input = "\n".join(sorted(package.url for package in packages)).encode("utf-8")
    digest = hashlib.sha256(digest_input).hexdigest()[:8]
    date = compact_date(latest.update_date)
    tag = f"qq-packages-{date}-{digest}"
    title = f"QQ installer packages {date}"
    return sanitize_tag(tag), title


def sanitize_tag(tag: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "-", tag)
    return cleaned.strip("-")


def github_release_exists(tag: str) -> bool:
    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repository:
        return False

    url = f"https://api.github.com/repos/{repository}/releases/tags/{urllib.parse.quote(tag, safe='')}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status == 200
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        raise


def download(url: str, destination: Path, timeout: int = 60) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = destination.with_suffix(destination.suffix + ".tmp")
    digest = hashlib.sha256()

    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(request(url), timeout=timeout) as response:
                with tmp.open("wb") as handle:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        handle.write(chunk)
                        digest.update(chunk)
            tmp.replace(destination)
            return digest.hexdigest()
        except Exception:
            tmp.unlink(missing_ok=True)
            if attempt == 3:
                raise
            time.sleep(2 * attempt)
            digest = hashlib.sha256()

    raise RuntimeError(f"Failed to download {url}")


def write_release_body(path: Path, packages: list[Package], checksums: dict[str, str]) -> None:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "Automated QQ installer mirror from the official QQ download configuration.",
        "",
        f"- Official site: {OFFICIAL_SITE_URL}",
        f"- Generated at: {now}",
        "",
        "| Target | Platform | Version | Update date | File | SHA256 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for package in packages:
        filename = package.filename
        sha256 = checksums.get(filename, "not downloaded")
        lines.append(
            f"| `{package.target}` | {package.platform} {package.arch} | "
            f"{package.version} | {package.update_date} | `{filename}` | `{sha256}` |"
        )

    lines.extend(["", "Source URLs:"])
    for package in packages:
        lines.append(f"- `{package.target}`: {package.url}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_checksum_file(path: Path, checksums: dict[str, str]) -> None:
    lines = [f"{sha256}  {filename}" for filename, sha256 in sorted(checksums.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_output(name: str, value: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return

    with open(output_file, "a", encoding="utf-8") as handle:
        if "\n" in value:
            delimiter = f"EOF_{hashlib.sha256(value.encode('utf-8')).hexdigest()}"
            handle.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
        else:
            handle.write(f"{name}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync QQ installers into a GitHub Release.")
    parser.add_argument(
        "--targets",
        default=os.environ.get("QQ_RELEASE_TARGETS", DEFAULT_TARGETS),
        help="Comma-separated target list. Default: %(default)s",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("QQ_RELEASE_OUTPUT_DIR", "dist/qq-release"),
        help="Directory for downloaded assets and release notes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=truthy(os.environ.get("QQ_DRY_RUN")),
        help="Resolve metadata but do not download installers.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=truthy(os.environ.get("QQ_FORCE_RELEASE")),
        help="Download and publish even when the tag already exists.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    targets = parse_targets(args.targets)
    candidates = fetch_configs()
    packages = select_packages(targets, candidates)
    tag, title = release_identity(packages)
    body_path = output_dir / "release_body.md"
    asset_list_path = output_dir / "assets.txt"
    checksum_path = output_dir / "SHA256SUMS.txt"

    exists = github_release_exists(tag)
    should_release = args.force or not exists
    checksums: dict[str, str] = {}
    asset_paths: list[str] = []

    print(f"Resolved release tag: {tag}")
    print(f"Resolved release title: {title}")
    for package in packages:
        print(f"Selected {package.target}: {package.url}")

    if should_release and not args.dry_run:
        for package in packages:
            destination = output_dir / package.filename
            print(f"Downloading {package.url} -> {destination}")
            checksums[package.filename] = download(package.url, destination)
            asset_paths.append(str(destination))

        write_checksum_file(checksum_path, checksums)
        asset_paths.append(str(checksum_path))
    else:
        reason = "dry run" if args.dry_run else "release already exists"
        print(f"Skipping downloads: {reason}")

    write_release_body(body_path, packages, checksums)
    asset_list_path.write_text("\n".join(asset_paths) + ("\n" if asset_paths else ""), encoding="utf-8")

    write_output("should_release", "true" if should_release and not args.dry_run else "false")
    write_output("tag", tag)
    write_output("title", title)
    write_output("body_path", str(body_path))
    write_output("asset_list_path", str(asset_list_path))
    write_output("asset_paths", "\n".join(asset_paths))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
