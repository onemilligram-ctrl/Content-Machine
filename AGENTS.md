# Content Machine

This repository supports four separate role sessions: researcher, writer, editor, and publisher. Skills supply role instructions; each role runs in its own Codex session. Do not run the whole pipeline in one session.

At the start of every session, read `PIPELINE.md`, then the assigned role's `.agents/skills/content-*/SKILL.md`. If no role has been assigned, ask which role to run. Perform only that role and stop after its handoff. Do not automatically invoke another role or spawn it.

`PIPELINE.md` is the shared handoff for one active article. Preserve sections belonging to other roles. `VOICE.md` is the shared voice reference; never invent the user's examples. If there are no voice references in Voice.md continue without them. The README describes startup prompts and synchronization.

Use the existing checkout. Do not create a worktree unless the user requests one. Run only one role at a time for the active article. Separate cloud tasks have separate filesystem copies; synchronization must be explicit.

Statuses represent completed work:

- BRIEFED: researcher completed BRIEF.
- DRAFTED: writer completed DRAFT.
- EDITED: editor completed EDITS; user review is pending.
- APPROVED: user explicitly approved the exact reviewed copy in DRAFT.
- PUBLISHED: publisher completed the ready-to-paste package in READY. This workflow label does not establish external publication.

The initial template has no completed stage. Never infer approval from silence or from an EDITED status. If approved copy changes, user approval must be renewed before external publication. Completing the publishing package in READY sets the status PUBLISHED.

Commit and push only when the user authorizes a Git handoff. Publish externally only when the user explicitly authorizes the destination and action. Report blockers and completed file changes accurately.
