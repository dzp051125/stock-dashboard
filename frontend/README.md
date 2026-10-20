# Frontend learning scaffold

Prepared by the teacher for stage 3.4. The learner wrote the core components and connections with guidance. The teacher prepared the environment and demo metadata.

## Files

- `index.html`: the HTML entry and app container.
- `src/main.js`: loads Vue and mounts `App.vue`.
- `src/App.vue`: parent account data, selection state, component composition and event handlers.
- `src/DashboardHeader.vue`: account heading.
- `src/account summary.vue`: account overview and rename event.
- `src/AccountSelector.vue`: account selection events.
- `src/HoldingsList.vue`: holding rows.
- `src/StatusMessage.vue`: global demo notice.
- `vite.config.js`: enables Vue file processing.
- `package.json`: records tools and commands.

## Development

From this directory, run `pnpm dev` if pnpm is available in the terminal.
Keep the terminal running, then visit http://127.0.0.1:5173/.

The current stage 3.4 application displays local demo content. It does not request the Python backend.
The original dashboard remains in the parent directory for comparison; it has not been migrated yet.

## Build check

Run `pnpm build` to check that the source can be processed into browser files.
This check does not verify actual browser interactions or layout.
