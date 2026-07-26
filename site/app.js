const REPOSITORY = "Rodert/qq-versions";
const RELEASES_API = `https://api.github.com/repos/${REPOSITORY}/releases`;
const RELEASES_URL = `https://github.com/${REPOSITORY}/releases`;
const grid = document.querySelector("#release-grid");
const releaseTemplate = document.querySelector("#release-template");
const assetTemplate = document.querySelector("#asset-template");
const filters = document.querySelectorAll(".filter");
let releases = [];
let activeFilter = "all";

async function loadReleases() {
  try {
    const response = await fetch(`${RELEASES_API}?per_page=30`, { headers: { Accept: "application/vnd.github+json" } });
    if (!response.ok) throw new Error(`GitHub API returned ${response.status}`);
    releases = await response.json();
    renderSummary();
    renderReleases();
  } catch (error) {
    grid.replaceChildren(errorMessage());
    console.error(error);
  }
}

function renderSummary() {
  const assets = releases.flatMap((release) => release.assets || []);
  document.querySelector("#release-count").textContent = releases.length;
  document.querySelector("#asset-count").textContent = assets.length;
  document.querySelector("#latest-version").textContent = releases[0]?.tag_name || "--";
}

function renderReleases() {
  const visible = releases.map((release) => ({ ...release, assets: release.assets.filter((asset) => assetMatchesFilter(asset, activeFilter)) })).filter((release) => activeFilter === "all" || release.assets.length);
  if (!visible.length) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = "当前筛选条件下没有可展示的安装包。";
    grid.replaceChildren(empty);
    return;
  }
  const fragment = document.createDocumentFragment();
  visible.forEach((release, index) => fragment.append(releaseCard(release, index === 0)));
  grid.replaceChildren(fragment);
}

function releaseCard(release, isLatest) {
  const node = releaseTemplate.content.firstElementChild.cloneNode(true);
  node.querySelector(".version-tag").textContent = release.name || release.tag_name;
  const badge = node.querySelector(".badge");
  badge.hidden = !isLatest;
  node.querySelector(".version-date").textContent = formatDate(release.published_at || release.created_at);
  node.querySelector(".version-info").textContent = normalizeBody(release.body);
  const packages = node.querySelector(".packages-grid");
  release.assets.forEach((asset) => packages.append(assetRow(asset)));
  return node;
}

function assetRow(asset) {
  const node = assetTemplate.content.firstElementChild.cloneNode(true);
  node.href = asset.browser_download_url;
  node.querySelector(".package-name").textContent = asset.name;
  node.querySelector(".package-size").textContent = formatSize(asset.size);
  node.querySelector(".package-type").textContent = assetType(asset.name);
  node.setAttribute("aria-label", `下载 ${asset.name}`);
  return node;
}

function errorMessage() { const node = document.createElement("div"); node.className = "error"; node.append("暂时无法读取 GitHub Releases。可直接前往 "); const link = document.createElement("a"); link.href = RELEASES_URL; link.textContent = "GitHub Releases"; node.append(link, " 下载。"); return node; }
function normalizeBody(body) { return body ? body.replaceAll("`", "").replace(/\|/g, " ").replace(/\s+/g, " ").trim() : "自动从 QQ 官方下载配置解析并归档的安装包。"; }
function assetMatchesFilter(asset, filter) { return filter === "all" || detectOS(asset.name) === filter; }
function detectOS(name) { const lower = name.toLowerCase(); if (lower.includes(".exe") || lower.includes("win")) return "windows"; if (lower.includes(".dmg") || lower.includes("mac")) return "macos"; if (lower.includes(".deb") || lower.includes(".rpm") || lower.includes("appimage") || lower.includes("linux")) return "linux"; return "all"; }
function assetType(name) { if (/sha256/i.test(name)) return "SHA256"; const extension = name.split(".").pop(); return extension ? extension.toUpperCase() : "FILE"; }
function formatDate(value) { return value ? new Intl.DateTimeFormat("zh-CN", { year:"numeric", month:"2-digit", day:"2-digit", hour:"2-digit", minute:"2-digit" }).format(new Date(value)) : "--"; }
function formatSize(size) { if (!Number.isFinite(size)) return "unknown size"; if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`; if (size > 1024 * 1024 * 1024) return `${(size / 1024 / 1024 / 1024).toFixed(2)} GB`; return `${(size / 1024 / 1024).toFixed(1)} MB`; }
filters.forEach((filter) => filter.addEventListener("click", () => { activeFilter = filter.dataset.filter; filters.forEach((item) => item.classList.toggle("is-active", item === filter)); renderReleases(); }));
loadReleases();
