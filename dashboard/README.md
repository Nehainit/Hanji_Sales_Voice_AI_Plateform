# Dashboard (Phase 3)

The seller web app: signup, setup wizard, dashboard, calls, call script, settings.
Built with Next.js 16. Spec and tasks: `openspec/changes/add-seller-dashboard/`.

## Run it

```bash
cd dashboard
npm install
npm run dev        # open http://localhost:3000
```

## Where things are

| Path | What |
|---|---|
| `src/app/globals.css` | Colours (light and dark) and base styles, copied from the prototype |
| `src/app/layout.tsx` | Fonts: Baloo 2 (headings), Hind (text), both with Hindi support |
| `src/app/(app)/` | The screens: Dashboard (`/`), Calls, Call script, Settings |
| `src/components/AppShell.tsx` | Side menu (bottom menu on phones) and the EN / हिंदी switch |
| `src/i18n/en.ts`, `src/i18n/hi.ts` | Every label in English and Hindi. Add a label to both files. |

## Design reference

`prototype/haanji-prototype.html` is the clickable prototype. Open it in a browser.
Every screen, label and flow in it is what the real app should match.
