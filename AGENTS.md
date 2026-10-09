# Content Machine

This repository supports four separate role sessions: researcher, writer, editor, and publisher. Skills supply role instructions; each role runs in its own Codex session. Each role must execute in its own agent session. A daily coordinator may orchestrate these sessions under DAILY_RUN.md but must not perform their content work itself.

At the start of every session, read `PIPELINE.md`, then the assigned role's `.agents/skills/content-*/SKILL.md`. If no role has been assigned, ask which role to run. Perform only that role and stop after its handoff. Role agents do not invoke the next role. The daily coordinator is authorized to delegate each role sequentially and manage handoffs.

`PIPELINE.md` is the shared handoff for one active article. Preserve sections belonging to other roles. `VOICE.md` is the shared voice reference; never invent the user's examples. If there are no voice references in Voice.md continue without them. The README describes startup prompts and synchronization.

Use the existing checkout. Do not create a worktree unless the user requests one. Run only one role at a time for the active article. Separate cloud tasks have separate filesystem copies; synchronization must be explicit.

Statuses represent completed work:

- BRIEFED: researcher completed BRIEF.
- DRAFTED: writer completed DRAFT.
- EDITED: editor completed EDITS with an APPROVE or REVISE verdict.
- APPROVED: user explicitly approved the reviewed DRAFT, or the daily coordinator recorded the editor’s APPROVE verdict under the user-authorized automated workflow.
- PUBLISH: publisher completed the ready-to-paste package in READY. This workflow label does not establish external publication.

The initial template has no completed stage. Never infer approval from silence or from an EDITED status alone. Daily automation may proceed only on an explicit editor APPROVE verdict for the current draft. If approved copy changes, user approval must be renewed before external publication. Completing the publishing package in READY sets the status PUBLISH.

Commit and push only when the user authorizes a Git handoff. Publish externally only when the user explicitly authorizes the destination and action. Report blockers and completed file changes accurately.
