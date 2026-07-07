"use strict";

const { describe, it } = require("node:test");
const assert = require("node:assert");
const {
  matchesWorkspaceFolder,
  formatQuotaBucket,
} = require("../extensions/vscode/webview.js");

describe("matchesWorkspaceFolder", () => {
  it("matches when cwd is inside a workspace folder", () => {
    assert.strictEqual(matchesWorkspaceFolder("/home/user/project/src", ["/home/user/project"]), true);
  });

  it("does not match an unrelated cwd", () => {
    assert.strictEqual(matchesWorkspaceFolder("/home/user/other", ["/home/user/project"]), false);
  });

  it("returns false for empty inputs", () => {
    assert.strictEqual(matchesWorkspaceFolder("", ["/home/user/project"]), false);
    assert.strictEqual(matchesWorkspaceFolder("/home/user/project", []), false);
  });
});

describe("formatQuotaBucket", () => {
  it("formats a used percentage", () => {
    assert.strictEqual(formatQuotaBucket({ usedPercent: 42 }), "42% used");
  });

  it("returns null for a missing bucket", () => {
    assert.strictEqual(formatQuotaBucket(null), null);
  });
});
