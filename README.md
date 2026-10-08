# Content Machine

Four separate Codex sessions share one active article through `PIPELINE.md`. Each session uses one role skill. A separate Codex Project per role is optional; the role instructions and shared handoff are what keep responsibilities clear.

## Shared files

- `PIPELINE.md`: topic, brief, draft, edits, publication package, and current stage.
- `VOICE.md`: five real examples of your existing content, read by writer and editor each session.
- `.agents/skills/`: one skill for each of the four roles.
- `AGENTS.md`: rules that apply to every role.

## First-time setup

1. Replace the NEXT UP placeholder with one topic.
2. Fill all five example slots in `VOICE.md` with your existing content.
3. Commit and push these shared files and role instructions to the Content-Machine GitHub repository when you are ready to authorize that action. They are currently local until a Git push succeeds.

Save and Publish in cloud environment settings preserves an environment snapshot. It does not push this repository to GitHub or automatically synchronize separate tasks.

## Launch one role per session

Start a separate Codex task/session against this repository for each step. Paste the corresponding prompt. If the skills are available in the session's skill picker, you can select the matching skill; otherwise, the explicit file path in the prompt supplies the instructions.

### Researcher

> Act only as Content Researcher. Read AGENTS.md and .agents/skills/content-researcher/SKILL.md, then follow that skill. Read PIPELINE.md first for the topic. Complete BRIEF, set BRIEFED, and stop at the handoff.

### Writer

> Act only as Content Writer. Read AGENTS.md and .agents/skills/content-writer/SKILL.md, then follow that skill. Read PIPELINE.md and VOICE.md. Complete DRAFT, set DRAFTED, and stop at the handoff.

### Editor

> Act only as Content Editor. Read AGENTS.md and .agents/skills/content-editor/SKILL.md, then follow that skill. Read PIPELINE.md and VOICE.md. Complete EDITS, set EDITED, and stop for my review.

### Publisher

> Act only as Content Publisher. Read AGENTS.md and .agents/skills/content-publisher/SKILL.md, then follow that skill. Read PIPELINE.md. Prepare READY from the approved copy for the platform I specify, set PUBLISHED when the package is complete, and stop after preparing it.

## Handoffs between separate cloud tasks

Run the roles sequentially. GitHub is the shared source of truth when tasks have separate checkouts. Before starting a role, ensure its checkout contains the preceding role's committed handoff. In a clean existing checkout on the shared branch, `git pull --ff-only origin main` updates it after `main` exists. If there are local changes, preserve them and resolve the handoff before continuing; do not reset or overwrite them.

After each role finishes, review its changes and authorize a commit and push to the shared branch. Do not launch the next role until the push succeeds. A local file update alone does not reach another task. If you use pull requests instead, merge each handoff before starting the next role. No automatic scheduling or synchronization is configured by these files.

## Approval and publishing

After EDITED, review the editor's feedback and verdict against DRAFT. To approve, tell the agent: “I approve the reviewed copy in DRAFT. Set the status to APPROVED.” Approval is a user decision, not a fifth agent role.

The publisher prepares a package in READY and sets PUBLISHED when it is complete. The package includes the formatted article, two title options, a two-sentence preview description, and three hashtags when the platform uses them. Specify Substack, Ghost, Medium, or LinkedIn. Here PUBLISHED is the pipeline completion label, not confirmation of external posting. Actual posting requires a separate explicit instruction and usable access to the destination.

For revisions, assign a new writer session to address the editor's feedback and return the status to DRAFTED, then run the editor again. Changed copy needs fresh approval.

## Starting the next article

After the publishing package is complete, archive the completed pipeline in a separate Markdown file before replacing the active topic or clearing its sections. Keep VOICE.md as the reusable reference. Never discard an unfinished article to start another one.
