# Frontend Instructions

The project-wide instructions in `../AGENTS.md` apply here.

- Use plain React, TypeScript, and Vite. Do not introduce Next.js, SSR, or another meta-framework.
- Use React Router for navigation and TanStack Query for server state.
- Keep TypeScript in strict mode and define typed API boundaries.
- Prefer semantic HTML, native controls, accessible interactions, and a lightweight documented styling approach.
- Keep feature-specific components and hooks colocated. Use shared UI components only for genuinely reusable presentation.
- Use React Hook Form and Zod only for forms complex enough to benefit from them.
- Do not add a global state library unless demonstrated cross-feature client state requires one.
- Treat API and externally sourced content as untrusted. Render text safely and never inject untrusted HTML.
- Provide responsive loading, empty, and error states and keyboard-accessible workflows.
- Add or update Vitest tests alongside each implementation slice.
- Do not install dependencies without the user's explicit approval; report the required install command and wait for the user to run it.

