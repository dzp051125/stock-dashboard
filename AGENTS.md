# Project and teaching instructions

## Project

- The current Vue application is in `frontend/`; root `main.py` serves its demo backend on port 8001 via the Vite development proxy. Root `index.html` is the prior reference page.
- Read `learning/STATUS.md` before teaching. Use `learning/PLAN.md` for the route and the latest daily report for recent evidence.
- Application identifiers, comments and UI strings are English. Teaching and learning documents may be Chinese.
- Use fictional data. Keep credentials, real account exports, databases, backups and dependencies out of Git.

## Teaching

- Explain why each change is needed, where the data originates, intermediate values and the expected visible result.
- Explain new terms and APIs before assigning work. Distinguish language keywords, framework APIs and names chosen by the learner.
- Explain new syntax with complete local examples, preferably using different content from the current task. For familiar patterns, give the goal and observable acceptance criteria first and let the learner choose the implementation before showing code.
- Allow old code and documentation as references. If the learner gets stuck, increase help from reasoning/location to API names to a complete local example as needed. Do not reveal assignment operands or line-by-line solutions upfront, impose a silent timer, or replace the main project with repeated quizzes.
- Teach one coherent goal at a time. Batch familiar patterns when appropriate.
- A message containing `1` means inspect saved work or continue; it is not evidence of understanding.
- Record outcomes, assistance and verification separately. Never report a browser test when only a build or script check was performed.
- About 40 minutes is a reference block, not an automatic stop. Respect the learner's request to wrap up and keep stage boundaries explicit.

## End-of-session GitHub workflow

The learner has requested ongoing lesson-end uploads of code and learning records to an agreed GitHub repository.

1. Check the saved source and perform verification appropriate to the actual change.
2. Update `learning/STATUS.md`, including the next two or three study sessions.
3. Append to `learning/daily/YYYY-MM-DD.md`, using the Shanghai end date; list actual start/end dates for sessions crossing midnight. Preserve earlier sessions in the same daily file.
4. State who wrote the core code, what required hints, what remains uncertain and what checks were performed.
5. Inspect the diff and candidate files, then commit and push to the agreed repository/branch using normal Git history. Never force-push or overwrite unrelated remote work.
6. Report the actual push result and commit link. If the remote or authorization is missing, prepare the local content and state what is pending; do not claim an upload.

This is a workflow during an active lesson wrap-up, not a scheduled background job. The remote is https://github.com/dzp051125/stock-dashboard.git, branch main, visibility private. The learner delegated the first upload and authorized ordinary future lesson-end updates. Keep that destination and visibility unless the learner requests a change.

Muse can review the repository through its own access. Preparing review notes does not authorize sending external messages or assuming Muse has read them.
