const REPOSITORY = "Rodert/qq-versions";
const RELEASES_API = `https://api.github.com/repos/${REPOSITORY}/releases`;
const RELEASES_URL = `https://github.com/${REPOSITORY}/releases`;

const grid = document.querySelector("#release-grid");
const template = document.querySelector("#release-template");
const releaseCount = document.querySelector("#release-count");
const assetCount = document.querySelector("#asset-count");
const latestDate = document.querySelector("#latest-date");
const filters = document.querySelectorAll(".filter");

let releases = [];
let activeFilter = "all";

async function loadReleases() {
  try {
    const response = await fetch(`${RELEASES_API}?per_page=30`, {
      headers: { Accept: "application/vnd.github+json" },
    });

    if (!response.ok) {
      throw new Error(`GitHub API returned ${response.status}`);
    }

    releases = await response.json();
    renderSummary(releases);
    renderReleases();
  } catch (error) {
    grid.innerHTML = "";
    const message = document.createElement("div");
    message.className = "error";
    message.innerHTML = `暂时无法读取 GitHub Releases。可以直接前往 <a href="${RELEASES_URL}">GitHub Releases</a> 下载。`;
    grid.append(message);
    releaseCount.textContent = "--";
    assetCount.textContent = "--";
    latestDate.textContent = "--";
    console.error(error);
  }
}

function renderSummary(items) {
  const assets = items.flatMap((release) => release.assets || []);
  releaseCount.textContent = String(items.length);
  assetCount.textContent = String(assets.length);
  latestDate.textContent = items[0] ? formatDate(items[0].published_at || items[0].created_at) : "--";
}

function renderReleases() {
  grid.innerHTML = "";

  const visible = releases
    .map((release) => ({
      ...release,
      assets: (release.assets || []).filter((asset) => assetMatchesFilter(asset, activeFilter)),
    }))
    .filter((release) => activeFilter === "all" || release.assets.length > 0);

  if (!visible.length) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = "当前筛选条件下没有可展示的安装包。";
    grid.append(empty);
    return;
  }

  for (const release of visible) {
    const node = template.content.firstElementChild.cloneNode(true);
    const title = node.querySelector("h3");
    const date = node.querySelector(".release-card__date");
    const tag = node.querySelector(".release-card__tag");
    const body = node.querySelector(".release-card__body");
    const assetList = node.querySelector(".asset-list");

    title.textContent = release.name || release.tag_name;
    date.textContent = formatDate(release.published_at || release.created_at);
    tag.textContent = release.tag_name;
    tag.href = release.html_url;
    body.textContent = normalizeBody(release.body);

    for (const asset of release.assets || []) {
      const link = document.createElement("a");
      const os = detectOS(asset.name);
      link.className = "asset";
      link.dataset.os = os;
      link.href = asset.browser_download_url;
      link.textContent = formatAssetName(asset.name);
      link.title = `${asset.name} - ${formatSize(asset.size)}`;
      link.setAttribute("aria-label", `下载 ${asset.name}`);
      assetList.append(link);
    }

    grid.append(node);
  }
}

function normalizeBody(body) {
  if (!body) {
    return "自动从 QQ 官方下载配置解析并归档的安装包。";
  }
  return body
    .replaceAll("`", "")
    .replace(/\|/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function assetMatchesFilter(asset, filter) {
  return filter === "all" || detectOS(asset.name) === filter;
}

function detectOS(name) {
  const lower = name.toLowerCase();
  if (lower.includes(".exe") || lower.includes("win") || lower.includes("windows")) {
    return "windows";
  }
  if (lower.includes(".dmg") || lower.includes("mac")) {
    return "macos";
  }
  if (
    lower.includes(".deb") ||
    lower.includes(".rpm") ||
    lower.includes("appimage") ||
    lower.includes("linux")
  ) {
    return "linux";
  }
  return "all";
}

function formatAssetName(name) {
  if (name === "SHA256SUMS.txt") {
    return "SHA256SUMS";
  }
  return name.replace(/^QQ_?/i, "").replace(/_/g, " ");
}

function formatDate(value) {
  if (!value) {
    return "--";
  }
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date(value));
}

function formatSize(size) {
  if (!Number.isFinite(size)) {
    return "unknown size";
  }
  if (size > 1024 * 1024 * 1024) {
    return `${(size / 1024 / 1024 / 1024).toFixed(2)} GB`;
  }
  return `${(size / 1024 / 1024).toFixed(1)} MB`;
}

for (const filter of filters) {
  filter.addEventListener("click", () => {
    activeFilter = filter.dataset.filter;
    filters.forEach((item) => item.classList.toggle("is-active", item === filter));
    renderReleases();
  });
}

loadReleases();
