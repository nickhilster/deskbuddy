"use strict";

const { describe, it } = require("node:test");
const assert = require("node:assert");
const {
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
} = require("../src/text-scale");

describe("text-scale clamp and validation", () => {
  it("accepts the full supported range", () => {
    assert.strictEqual(isValidTextScale(0.8), true);
    assert.strictEqual(isValidTextScale(1), true);
    assert.strictEqual(isValidTextScale(1.6), true);
  });

  it("rejects out-of-range and non-numeric values", () => {
    assert.strictEqual(isValidTextScale(0.79), false);
    assert.strictEqual(isValidTextScale(1.61), false);
    assert.strictEqual(isValidTextScale(NaN), false);
    assert.strictEqual(isValidTextScale("1.2"), false);
    assert.strictEqual(isValidTextScale(null), false);
  });

  it("clamps to bounds and falls back to default on garbage", () => {
    assert.strictEqual(clampTextScale(0.5), TEXT_SCALE_MIN);
    assert.strictEqual(clampTextScale(3), TEXT_SCALE_MAX);
    assert.strictEqual(clampTextScale(1.25), 1.25);
    assert.strictEqual(clampTextScale(NaN), TEXT_SCALE_DEFAULT);
    assert.strictEqual(clampTextScale(undefined), TEXT_SCALE_DEFAULT);
    assert.strictEqual(clampTextScale("not a number"), TEXT_SCALE_DEFAULT);
  });
});

describe("text-scale DIP conversion", () => {
  it("is the identity at 100%", () => {
    assert.strictEqual(scaleWidth(340, 1), 340);
    assert.strictEqual(scaleHeight(212, 1), 212);
  });

  it("keeps the 340 bubble base width integral at every 5% step", () => {
    // CSS viewport width must stay exactly 340 at every slider stop so cached
    // renderer-side measurements survive scale changes without re-measuring.
    for (let pct = 80; pct <= 160; pct += 5) {
      const scale = pct / 100;
      const exact = (340 * pct) / 100;
      // 340 × pct is divisible by 100 at every 5% stop, so the rounded DIP
      // width is mathematically exact (IEEE754 noise stays far below 1e-6).
      assert.ok(
        Math.abs(340 * scale - exact) < 1e-6,
        `340 × ${pct}% must be integral up to float noise`,
      );
      assert.strictEqual(scaleWidth(340, scale), exact);
    }
  });

  it("ceils heights so scaled content is never clipped", () => {
    assert.strictEqual(scaleHeight(201, 1.05), Math.ceil(201 * 1.05));
    assert.strictEqual(scaleHeight(333, 0.85), Math.ceil(333 * 0.85));
  });

  it("clamps the scale before converting", () => {
    assert.strictEqual(scaleWidth(340, 99), 340 * TEXT_SCALE_MAX);
    assert.strictEqual(scaleHeight(100, NaN), 100);
  });
});

describe("text-scale slider mapping", () => {
  it("round-trips every slider stop", () => {
    for (let pct = 80; pct <= 160; pct += 5) {
      assert.strictEqual(textScaleToUiPercent(uiPercentToTextScale(pct)), pct);
    }
  });

  it("normalizes invalid percent input to the default", () => {
    assert.strictEqual(uiPercentToTextScale("abc"), TEXT_SCALE_DEFAULT);
    assert.strictEqual(uiPercentToTextScale(NaN), TEXT_SCALE_DEFAULT);
  });

  it("exposes step and partition constants", () => {
    assert.strictEqual(TEXT_SCALE_STEP, 0.05);
    assert.strictEqual(typeof NO_ZOOM_PARTITION, "string");
    assert.ok(NO_ZOOM_PARTITION.length > 0);
    assert.ok(!NO_ZOOM_PARTITION.startsWith("persist:"), "must stay in-memory");
  });
});

describe("applyZoomToWindow", () => {
  function makeWindow({ destroyed = false, throws = false } = {}) {
    const calls = [];
    return {
      calls,
      isDestroyed: () => destroyed,
      webContents: {
        setZoomFactor(factor) {
          if (throws) throw new Error("boom");
          calls.push(factor);
        },
      },
    };
  }

  it("sets the clamped factor on a live window", () => {
    const win = makeWindow();
    assert.strictEqual(applyZoomToWindow(win, 1.25), true);
    assert.deepStrictEqual(win.calls, [1.25]);
  });

  it("still sets explicitly at the default scale", () => {
    const win = makeWindow();
    assert.strictEqual(applyZoomToWindow(win, 1), true);
    assert.deepStrictEqual(win.calls, [1]);
  });

  it("is safe on destroyed/missing windows and swallows setter errors", () => {
    assert.strictEqual(applyZoomToWindow(null, 1.2), false);
    assert.strictEqual(applyZoomToWindow(makeWindow({ destroyed: true }), 1.2), false);
    assert.strictEqual(applyZoomToWindow({ isDestroyed: () => false }, 1.2), false);
    assert.strictEqual(applyZoomToWindow(makeWindow({ throws: true }), 1.2), false);
  });
});
