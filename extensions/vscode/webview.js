"use strict";

function matchesWorkspaceFolder(cwd, workspaceFolders) {
  if (!cwd || !Array.isArray(workspaceFolders) || workspaceFolders.length === 0) return false;
  return workspaceFolders.some((folder) => {
    if (!folder) return false;
    return cwd === folder || cwd.startsWith(folder.endsWith("/") ? folder : folder + "/");
  });
}

function formatQuotaBucket(bucket) {
  if (!bucket || typeof bucket.usedPercent !== "number") return null;
  return `${bucket.usedPercent}% used`;
}

function statusLabel(status) {
  if (status === "completed") return "done";
  if (status === "in_progress") return "active";
  return "pending";
}

function renderTodoList(todos) {
  if (!Array.isArray(todos) || todos.length === 0) return "<p class=\"empty\">No todos</p>";
  return "<ul class=\"todo-list\">" + todos.map((t) => {
    const label = t.status === "in_progress" && t.activeForm ? t.activeForm : t.content;
    return `<li class="todo todo-${statusLabel(t.status)}">${escapeHtml(label)}</li>`;
  }).join("") + "</ul>";
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderUsage(session) {
  const parts = [];
  const claude = session.claudeQuota;
  if (claude && claude.claudeFiveHour) parts.push(`5h: ${formatQuotaBucket(claude.claudeFiveHour)}`);
  if (claude && claude.claudeWeekly) parts.push(`weekly: ${formatQuotaBucket(claude.claudeWeekly)}`);
  const antigravity = session.antigravityQuota;
  if (antigravity) {
    for (const key of Object.keys(antigravity)) {
      const formatted = formatQuotaBucket(antigravity[key]);
      if (formatted) parts.push(`${key}: ${formatted}`);
    }
  }
  const ctx = session.contextUsage;
  if (ctx && typeof ctx.percent === "number") parts.push(`context: ${ctx.percent}%`);
  return parts.length ? `<div class="usage">${parts.map(escapeHtml).join(" &middot; ")}</div>` : "";
}

function renderSessionRow(session, workspaceFolders, pendingPermissionIds) {
  const highlighted = matchesWorkspaceFolder(session.cwd, workspaceFolders);
  const pending = pendingPermissionIds instanceof Set && pendingPermissionIds.has(session.id);
  const actions = pending
    ? `<div class="actions">
         <button data-action="allow" data-session="${escapeHtml(session.id)}">Allow</button>
         <button data-action="deny" data-session="${escapeHtml(session.id)}">Deny</button>
       </div>`
    : "";
  return `<div class="session-row${highlighted ? " session-row-highlight" : ""}" data-session-id="${escapeHtml(session.id)}">
    <div class="session-title">${escapeHtml(session.displayTitle || session.id)}</div>
    <div class="session-badge session-badge-${escapeHtml(session.badge || "idle")}">${escapeHtml(session.badge || "idle")}</div>
    ${renderUsage(session)}
    ${renderTodoList(session.todos)}
    ${actions}
  </div>`;
}

function renderDashboard(snapshot, workspaceFolders, pendingPermissionIds) {
  const sessions = (snapshot && Array.isArray(snapshot.sessions)) ? snapshot.sessions : [];
  if (sessions.length === 0) return "<p class=\"empty\">No live sessions</p>";
  const sorted = sessions.slice().sort((a, b) => {
    const aHi = matchesWorkspaceFolder(a.cwd, workspaceFolders) ? 1 : 0;
    const bHi = matchesWorkspaceFolder(b.cwd, workspaceFolders) ? 1 : 0;
    return bHi - aHi;
  });
  return sorted.map((s) => renderSessionRow(s, workspaceFolders, pendingPermissionIds)).join("");
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    matchesWorkspaceFolder,
    formatQuotaBucket,
    renderTodoList,
    renderUsage,
    renderSessionRow,
    renderDashboard,
    escapeHtml,
  };
}

if (typeof window !== "undefined" && typeof document !== "undefined") {
  (function () {
    const vscodeApi = acquireVsCodeApi();
    const root = document.getElementById("dashboard-root");
    const banner = document.getElementById("status-banner");
    let ws = null;
    let latestSnapshot = { sessions: [] };
    const workspaceFolders = window.__DESKBUDDY_WORKSPACE_FOLDERS__ || [];

    function pendingPermissionIds(snapshot) {
      const ids = new Set();
      const sessions = (snapshot && snapshot.sessions) || [];
      for (const s of sessions) if (s.badge === "notification") ids.add(s.id);
      return ids;
    }

    function render() {
      root.innerHTML = renderDashboard(latestSnapshot, workspaceFolders, pendingPermissionIds(latestSnapshot));
    }

    function connect(port) {
      if (!port) {
        banner.textContent = "DeskBuddy not running";
        return;
      }
      banner.textContent = "";
      ws = new WebSocket("ws://127.0.0.1:" + port + "/ws");
      ws.addEventListener("message", (event) => {
        let msg;
        try { msg = JSON.parse(event.data); } catch { return; }
        if (msg.type === "snapshot") {
          latestSnapshot = msg.snapshot;
          render();
        }
      });
      ws.addEventListener("close", () => { banner.textContent = "Disconnected from DeskBuddy"; });
    }

    root.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button || !ws) return;
      ws.send(JSON.stringify({
        action: "resolve-permission",
        entryId: button.getAttribute("data-session"),
        decision: button.getAttribute("data-action"),
      }));
    });

    window.addEventListener("message", (event) => {
      const msg = event.data;
      if (msg && msg.type === "bridge-port") {
        if (ws) ws.close();
        connect(msg.port);
      }
    });

    connect(window.__DESKBUDDY_BRIDGE_PORT__);
    vscodeApi.postMessage({ type: "ready" });
  })();
}
