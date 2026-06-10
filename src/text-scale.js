"use strict";

// Global text-window zoom (settings key: textScale).
//
// Chromium registers zoom per scheme+host inside a storage partition. Every
// loadFile window shares the empty file:// host, so zoom set on any text
// window propagates to all of them — that propagation is how one setting
// covers every text window, including future ones. Windows that must NOT
// scale (pet render/hit, animation poster capture) opt out by living in this
// dedicated in-memory partition instead. See docs/plans/plan-text-scale.md.
const NO_ZOOM_PARTITION = "clawd-no-zoom";

const TEXT_SCALE_MIN = 0.8;
const TEXT_SCALE_MAX = 1.6;
const TEXT_SCALE_DEFAULT = 1;
const TEXT_SCALE_STEP = 0.05;

function isValidTextScale(value) {
  return typeof value === "number"
    && Number.isFinite(value)
    && value >= TEXT_SCALE_MIN
    && value <= TEXT_SCALE_MAX;
}

function clampTextScale(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return TEXT_SCALE_DEFAULT;
  if (n < TEXT_SCALE_MIN) return TEXT_SCALE_MIN;
  if (n > TEXT_SCALE_MAX) return TEXT_SCALE_MAX;
  return n;
}

// CSS px → DIP. Widths round: bubble base widths are multiples of 20, so every
// 5% step lands on an integer and the CSS viewport width stays exact — cached
// renderer-side heights survive scale changes. Heights ceil so a rounded-down
// window can never clip scaled content.
function scaleWidth(cssPx, scale) {
  return Math.round(cssPx * clampTextScale(scale));
}

function scaleHeight(cssPx, scale) {
  return Math.ceil(cssPx * clampTextScale(scale));
}

function applyZoomToWindow(win, scale) {
  if (!win || typeof win.isDestroyed !== "function" || win.isDestroyed()) return false;
  const wc = win.webContents;
  if (!wc || typeof wc.setZoomFactor !== "function") return false;
  try {
    // Always set explicitly, even at 1.0: Chromium persists per-origin zoom in
    // the partition across restarts, so skipping the "default" call would let
    // a stale persisted factor survive a prefs reset.
    wc.setZoomFactor(clampTextScale(scale));
    return true;
  } catch {
    return false;
  }
}

// Settings slider mapping (UI works in whole percent: 80–160, step 5).
function textScaleToUiPercent(scale) {
  return Math.round(clampTextScale(scale) * 100);
}

function uiPercentToTextScale(percent) {
  const n = Number(percent);
  if (!Number.isFinite(n)) return TEXT_SCALE_DEFAULT;
  return clampTextScale(n / 100);
}

module.exports = {
  NO_ZOOM_PARTITION,
  TEXT_SCALE_MIN,
  TEXT_SCALE_MAX,
  TEXT_SCALE_DEFAULT,
  TEXT_SCALE_STEP,
  isValidTextScale,
  clampTextScale,
  scaleWidth,
  scaleHeight,
  applyZoomToWindow,
  textScaleToUiPercent,
  uiPercentToTextScale,
};
