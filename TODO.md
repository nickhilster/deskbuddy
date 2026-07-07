# TODO

This file tracks high-leverage product work for DeskBuddy.

## P0 — Flagship: Context-aware session resume across devices

### Product thesis

DeskBuddy should not only notify the user that an AI coding session needs attention or has completed. It should help the user quickly regain context when returning to a session from another device, another machine, or after switching between multiple concurrent agent/project sessions.

The real user problem is not just awareness. It is **session re-entry**.

A user may have:

- more than one coding device
- multiple AI agents running at the same time
- 4+ active or recent sessions per device
- separate projects/repositories in motion
- long-running outputs that are easy to lose inside terminals or agent panes
- a need to know what they asked, what the agent did, what changed, and what needs attention next

Current notification behavior answers: **Did something happen?**

This feature should answer: **What was I doing, what happened, and what should I do now?**

### Core user story

As a user working across several devices and AI coding agents, I want DeskBuddy to show a compact, trusted context brief for each active/recent session so I can resume the right work without scrolling back through terminal history or reconstructing the previous prompt manually.

### Context Brief should answer

1. Which machine/device is this from?
2. Which repo/project is this session working in?
3. Which agent produced the update?
4. What was the last meaningful user prompt/request?
5. What did the agent do or attempt?
6. What changed, if anything?
7. What is the current status?
8. What does the user need to do next?

### Proposed UX

#### Session Context Cards

Add a context card in the Dashboard/HUD/Mobile Companion view for each active or recent session.

Each card should include:

- machine name / device label
- repo name and local path
- branch, if available
- agent source
- session status: active, waiting, completed, failed, stale, crashed, or needs review
- last user prompt excerpt
- latest agent summary or output summary
- changed files count and key file names, where available
- last event timestamp
- one clear next action

#### Context Brief Drawer

Clicking/tapping a card opens a richer drawer with:

- session timeline summary
- last prompt
- latest meaningful response/output summary
- files touched
- errors/warnings
- permission request context
- suggested resume action
- same-machine button to jump/focus the original terminal

#### Cross-device re-entry

For mobile or another machine, the context should remain read-oriented by default:

- show session context from paired machines
- show enough information to understand what happened
- do not require the original terminal to be visible
- keep write/approval actions out of scope unless intentionally designed later

### Suggested implementation path

#### Phase 1 — Local session context cards

- Add a normalized session context snapshot model.
- Populate machine, agent, repo, path, branch, status, and last event timestamp.
- Add context cards to Dashboard/HUD.
- Add simple next-action labels.

#### Phase 2 — Last prompt + output context

- Extract last user prompt where supported.
- Extract latest agent output excerpt or event summary.
- Add the context drawer.
- Add basic context retention and privacy controls.

#### Phase 3 — Cross-device context bridge

- Extend the existing multi-machine/mobile dashboard payload with context snapshots.
- Show grouped cards by machine and project.
- Preserve read-only behavior.
- Support stale/offline machine context where safe.

#### Phase 4 — Intelligent summaries

- Optional local or user-configured summarization.
- Summarize long outputs into resume briefs.
- Identify likely next action.
- Highlight failed commands, permission blockers, changed files, and review needs.

### Privacy and safety constraints

- Prefer local-first storage.
- Keep mobile/multi-machine context read-only by default.
- Avoid requiring cloud sync for v1.
- Store useful excerpts/summaries rather than unlimited raw logs.
- Allow users to limit or disable context capture per agent.

### Acceptance criteria

- A user with multiple active sessions can see which session belongs to which project/device/agent.
- A user can understand the last meaningful prompt without scrolling through terminal history.
- A user can see the latest status and what needs attention next.
- A user can distinguish completed sessions from waiting/failed/stale sessions.
- Mobile/multi-machine view shows context, not just notification state.
- Context capture can be limited or disabled.
- The feature does not require cloud sync for v1.
