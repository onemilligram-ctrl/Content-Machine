# Daily four-role content run

Requested schedule: every day at 7:00 a.m. America/Los_Angeles, including daylight saving changes. No scheduler has been activated.

## Inputs required before scheduling

Supply the topic and common-question list, fill the five examples in VOICE.md, and specify the publishing platform (Substack, Ghost, Medium, or LinkedIn). Do not invent missing inputs.

Upload plain text with one question per line, or a CSV with a `question` column. Import it with:

```sh
python scripts/question_queue.py import /path/to/questions.txt --topic "Your topic"
```

QUESTIONS.json records IDs, topics, state, and selection timestamps. Duplicates within a topic are ignored and reimports preserve usage. Supply questions in frequency order; importing does not independently verify how common they are.

## Scheduled coordinator prompt

> Act as the Content Machine daily coordinator. Read PIPELINE.md, AGENTS.md, and DAILY_RUN.md. Coordinate four separate role agents sequentially using the skills under .agents/skills; do not do their content work yourself. Select or resume one question, delegate the researcher, writer, editor, and publisher, and continue through their handoffs rather than stopping after a brief. Route REVISE feedback to a separate writer revision session and run the editor again. Under this user-authorized automated workflow, set APPROVED only after an explicit editor APPROVE verdict for the current draft. Run the publisher for the configured platform. Set Current stage: PUBLISH only after all four roles have completed their work and READY contains the complete publishing package. Mark the matching question used and report the result. Preserve completed content and never post externally without a separate explicit instruction.

## Execution and recovery

1. Before selecting a new question, check required inputs. If the previous package is at PUBLISH, mark its selected question used if needed, archive the entire pipeline under a unique filename in archive/, and reset the active pipeline to its original placeholders. Keep the latest completed package visible until a later run starts the next article.
2. Run `python scripts/question_queue.py select`. Exhaustion ends the run without recycling questions. A reserved question resumes instead of consuming another. If an unrelated article occupies the pipeline, report the conflict without replacing it.
3. Delegate Content Researcher using `.agents/skills/content-researcher/SKILL.md` for a new question lacking a brief. Require BRIEFED and a complete BRIEF before continuing.
4. Delegate Content Writer using `.agents/skills/content-writer/SKILL.md`. Require DRAFTED and a complete DRAFT before continuing. Resume existing completed stages rather than repeating them unnecessarily.
5. Delegate Content Editor using `.agents/skills/content-editor/SKILL.md`. Require EDITED and a verdict for the current draft. On REVISE, delegate a writer revision, then another editor review. Continue until APPROVE; if repeated attempts make no progress or a factual/input blocker remains, preserve the work and report the blocker rather than claiming completion.
6. On the editor's explicit APPROVE verdict, set APPROVED. This automated approval of the draft is authorized for preparing a package, not for external posting. Any subsequent substantive change requires another editor review.
7. Delegate Content Publisher using `.agents/skills/content-publisher/SKILL.md`. Require formatted copy, both titles, the two-sentence preview description, and three hashtags where applicable under READY. Successful completion sets `Current stage: PUBLISH`.
8. Run `python scripts/question_queue.py complete` to mark the question used. Leave READY and PUBLISH visible. Report all four role outcomes and the final package location.

Do not mark PUBLISH on a partial run. Missing questions, voice examples, platform, research access, or execution capabilities are blockers; preserve the current stage and explain what is needed. A coordinator needs a runner that supports separate agent sessions. Merely reading four skills in one agent does not meet the role separation requirement.

## Persistence and scheduling

Serialize daily runs. Within a shared checkout, each role reads the previous role's saved output. Across separate cloud checkouts, each successful handoff must be committed and pushed, and the next role must read the latest shared state. Persist queue, pipeline, and any archives together through an explicitly authorized Git handoff. Do not reset local changes or overwrite a rejected push.

The queue helper uses Python's standard library and locks commands in one checkout. It does not serialize independent machines. After an interrupted command, inspect a stale .question-queue.lock before removing it.

No scheduling capability is exposed to this chat. Configure your scheduler for the requested local time with the coordinator prompt above, separate-agent execution, and repository persistence. These instructions do not activate scheduling or launch agents by themselves. PUBLISH means the publishing package is ready to paste, not that it has been posted externally.
