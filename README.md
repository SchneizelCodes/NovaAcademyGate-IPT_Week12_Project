# Nova Academy Gate

A Week 12 pilot-validation lab implemented in Next.js, React, TypeScript, Node.js and Three.js. This is the requested web-stack adaptation of a C# ASP.NET MVC worksheet; no Visual Basic, Razor or ASP.NET project is claimed.

## Run

Node.js 22.18+ is needed for the native TypeScript unit tests (developed with Node 26). Use an active supported Node release with Next.js support.

```powershell
cd C:\Users\joshu\Documents\GitHub\Apps\NovaAcademyGate
npm ci
npm run dev
```

Open http://localhost:3212. Installed dependencies already exist on this PC. Production: `npm run build`, then `npm start`. These commands run the Node.js API too; a static file server cannot replace it.

## What works

- `/`: responsive Academy registration with a real Three.js planet/orbits and a CSS fallback.
- `/api/pilots`: same-origin JSON POST; server-side validation; HTTP 422 for invalid values and a welcome message on success.
- `/lab`: exercise overview; `/lab/model`, `/lab/controller`, `/lab/view` show actual numbered source.
- Exact worksheet error messages, plus a clear blank-age message. Invalid fields retain their values; success clears them.
- Optional launch date accepts today/future and rejects a past date, using Asia/Manila on client/server.
- No account, database, emails, real registrations or persistent personal data. PilotId is not needed without persistence; a server would assign it if persistence were added.

## Verification and submission

```powershell
npm test
npm run typecheck
npm run build
# Start npm start in another terminal, then:
npm run test:e2e
```

The browser script needs Playwright Chromium. If unavailable: `npx playwright install chromium`.

`deliverables/COMPLETED_WEEK_12_LAB.docx` contains answers and screenshots. `deliverables/TEST_RESULTS.json` records executed browser/API cases. Full-resolution checkpoints are in `deliverables/screenshots/`. The break-it tests mutate only an ignored test copy or isolated harness. The real app retains its validation guard.

The original worksheet remains untouched. Fill in your own name and section. The worksheet gives conflicting optional bonus totals (+8 in Step 6, +10 in rubric), so no grade is claimed. Since the course explicitly asks for MVC artifacts, this implementation honestly labels equivalents; confirm your teacher accepts the alternate stack.

## Design and sources

Original Academy layout: warm paper, midnight-blue mission panel, copper planet, serif display and quiet technical labels. It reuses general responsive/focus/feedback/motion principles from the owner's vault and portfolio, without copying private app records or other projects' branding. Three.js uses procedural geometry, not external images. Geist's regular font is served locally with its included licence.

Implementation references: [Next.js Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers), [MDN aria-invalid](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid). Package versions are pinned and package-lock.json supports npm ci. No publishing or Git commits were performed.


## Worksheet format correction

The current answer document follows the supplied worksheet format: original title/metadata, Mission Brief, numbered Steps 1–6, exact questions, checkpoint locations, all eight test-table columns, reflections and rubric. Answers and actual screenshots appear within the relevant step. The original malformed pseudo-tables and fractional page dimensions were repaired; the source itself is unchanged. Eleven rendered pages were checked. `deliverables/COMPLETED_WEEK_12_LAB_WORKSHEET_FORMAT.docx` is the primary file; `COMPLETED_WEEK_12_LAB.docx` is an identical current alias. The earlier separate report and source ZIP are preserved in `deliverables/_previous/`. Application code and existing functional test evidence are unchanged. Use build-worksheet-format.py for this format; build-answers.py is the historical report generator.
