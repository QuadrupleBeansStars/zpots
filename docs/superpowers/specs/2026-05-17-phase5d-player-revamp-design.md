# Phase 5d — Player Revamp Design

**Status:** approved 2026-05-17 (autonomous per [[feedback-design-revamp-autonomy]])
**Sub-phase of:** Phase 5.

## Goal

Apply KP+Motion to every player-facing surface — landing, both login pages, player home, search, court detail, booking flow, my bookings, check-in, confirmation, feedback. Plus: ship the real mobile menu (placeholder in 5a). Delete the now-orphaned `PlayerTopBar`. After 5d, only the chat widget retains legacy styling (handled in 5e).

## Pages in scope

| Page | Path | Treatment |
|---|---|---|
| Landing | `/` (`app/page.tsx`) | Full magazine-style hero, role picker becomes hero+cards, AI tag becomes ticker tagline |
| Player login | `/player/login` | Dark hero left, glass form card right (side-by-side on desktop, stacked on mobile) |
| Owner login | `/owner-login` | Same split-hero pattern |
| Player home | `/player` | Multi-section: dark hero with NumberFlip stats, sport pills, featured courts grid, 3-step explainer, smart-booking dark callout |
| Search | `/player/search` | PageHero with AI search input embedded, sport chips, court grid |
| Court detail | `/player/courts/[id]` | DarkHero with court photo+gradient, amenities/court-list cards, Book CTA |
| Booking checkout | `/player/courts/[id]/book` | DarkHero with court ID/date, time picker grid, PulseAccent confirm |
| My bookings | `/player/bookings` | PageHero with booking count NumberFlip, booking cards |
| Check-in QR | `/player/bookings/[txnId]/checkin` | Full-screen-ish dark hero, QR code on lime card |
| Confirmation | `/player/bookings/[txnId]/confirmation` | Celebratory dark hero with NumberFlip, summary cards |
| Feedback | `/player/bookings/[txnId]/feedback` | Calm PageHero, star-rating form |

## Layout-aware notes

- `/` and `/player/login` and `/owner-login` are **outside the player/owner layouts** — they don't get `PageShell` (no TopNav). They render as their own full-page composition. Pattern: dark hero left, content right, no global nav.
- All `/player/*` pages get the shared `<PageShell role="player">` already in place from 5a.

## New patterns introduced in 5d

### `<SplitHero>` primitive

Used by both login pages and the landing page. Dark hero panel left (with brand/eyebrow/sub), content panel right (form or role picker).

```tsx
<SplitHero
  eyebrow="ATHLETE LOGIN"
  headline="Welcome back."
  sub="Your next session is one click away."
>
  <LoginForm />
</SplitHero>
```

Renders as `grid grid-cols-1 md:grid-cols-[1.2fr_1fr]` with min-height-screen; left is `<DarkHero>` styled, right is the children.

### Mobile menu

`TopNav`'s placeholder hamburger now opens a full-screen overlay:
- `bg-ink-900/95 backdrop-blur-2xl` full-screen
- Stack nav links as `display-md` text
- CTA at the bottom
- Close button top-right
- Closes on link click

Lives as `<MobileMenu>` component in `components/nav/`.

### `<CourtHero>` (court detail page)

Composes `<DarkHero>` with a court image + gradient overlay. Displays court name + sport pill + price + rating. Used by `/player/courts/[id]` and the booking checkout.

## Transformation rules

Same as 5c spec — re-read the table there. Plus:

- For **emoji icons currently sitting in pills/circles** (sport row, court placeholders), keep them but the container becomes `bg-surface-low` or `bg-ink-800` depending on context, with `rounded-kp-pill`.
- For **`zpots-card-dark`** sections, convert to `<DarkHero glow="lime">`.
- For **chat-like CTAs**, wrap in `<PulseAccent>` only if it represents an active recommendation; not every CTA needs it.

## Components to upgrade in-place

- `components/CourtCard.tsx` — restyle internally with new tokens
- `components/Button.tsx` — already used; small update to default variants to use lime/ink ramps (don't break existing API; the legacy zpots-* fallback values stay until last consumer migrates, but most consumers will be migrated after 5d)
- `components/Tags.tsx` — `AITag`, `Eyebrow`, `StatusBadge` minor token shifts
- `components/KpiCard.tsx` — already upgraded in 5b; just used here too

## Delete after 5d

- `components/PlayerTopBar.tsx` — no consumer left
- Possibly `components/Button.tsx` legacy gradient variants → only if all callers migrated. If any zpots-* button class is still used anywhere, defer the cleanup.

## Mobile-first considerations

- Landing + login: stacks vertically on mobile (`md:grid-cols-[1.2fr_1fr]` collapses)
- Player home: hero stays full-width; featured courts grid goes 1-col on `sm:`, 2-col on `md:`, 4-col on `lg:`
- Search: sport chips wrap; grid 1/2/3 cols
- Court detail: image hero shrinks; amenities stack; sticky bottom CTA on mobile
- Booking checkout: time picker becomes 3-col on mobile (was 6-col on desktop)
- Mobile menu finally functional — TopNav hamburger opens it

## Tests

| Suite | Expected |
|---|---|
| Streamlit | 29 / 29 ✅ |
| FastAPI | 53 / 53 ✅ |
| Vitest | 46 / 46 ✅ (+3 for SplitHero + MobileMenu) |
| Playwright | 2 / 3 (player-flow may need updates; the pre-existing FastAPI-needed failure remains until a follow-up wires uvicorn into the Playwright webServer config) |
| `pnpm build` | clean |

## Out of scope

- Chat widget → 5e
- Backend changes
- Visual regression tooling
- Fix the pre-existing Playwright player-flow regression (needs `playwright.config.ts` webServer for FastAPI — out of scope for design work)

## Open questions

None.
