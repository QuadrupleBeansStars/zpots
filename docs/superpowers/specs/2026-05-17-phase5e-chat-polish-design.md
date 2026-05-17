# Phase 5e — Chat Polish Design

**Status:** approved 2026-05-17 (autonomous per [[feedback-design-revamp-autonomy]])
**Sub-phase of:** Phase 5 — **final** sub-phase. After this, the whole app uses KP+Motion.

## Goal

Apply KP+Motion to the floating chat widget — launcher, panel, message bubbles, confirm draft. The widget appears on every player + owner page, so its visual feel impacts every screen.

## Components in scope

- `apps/web/components/chat/ChatWidget.tsx` (178 lines) — launcher + panel chrome
- `apps/web/components/chat/ChatBubble.tsx` (30 lines) — message bubble
- `apps/web/components/chat/ConfirmDraft.tsx` (38 lines) — booking/cancel confirmation

## Visual changes

### Launcher (💬 button)

Current: 64px circle, flat `bg-zpots-lime`, bottom-right at `bottom-6 right-6`.

New: 64px circle, `bg-lime` (same color, new token), continuous subtle `<PulseAccent>` halo at idle (paused when chat is open), inline 1.05× scale on hover. Drop shadow upgrades from `shadow-card-lift` to `shadow-lift`. Icon stays as the bolt emoji or upgrades to Material Symbols `chat`.

### Panel

Current: 400×600, white background, `rounded-card`, `shadow-card-lift`, hard `border-zpots-mint`.

New: same dimensions, wrap in `<GlassPanel>` (`bg-white/95 backdrop-blur-2xl shadow-lift`), `rounded-kp-card`, **no border**, ink-900-tinted backdrop overlay on the rest of the page when open (subtle, ~10% opacity) for focus.

Open/close animation: scale `0.94 → 1` + opacity `0 → 1` over `dur-smooth` with `ease-precision`. Origin: bottom-right.

### Header

Current: small icon + bold name in `font-display`.

New: same icon + name in `font-geist font-semibold text-title-md text-ink-900`. Add a small lime status dot (●) on the left to indicate "live AI". Close button gets new focus-ring.

### Message bubbles (ChatBubble)

| Role | Old | New |
|---|---|---|
| user | `bg-zpots-lime text-zpots-forest rounded-card` | `bg-lime text-ink-900 rounded-kp-card` |
| assistant | `bg-white border border-zpots-mint text-zpots-ink rounded-card` | `bg-white shadow-float text-ink-900 rounded-kp-card` (drop border) |

Both: max-w-[85%], `text-body-sm`. New: subtle `transition-all duration-quick` fade-up on mount (CSS-driven).

### ConfirmDraft

Current: `zpots-card-surface` background, basic Confirm/Cancel buttons.

New: `bg-surface-low rounded-kp-card p-4`, lime/ink button pair matching the new pill style. **Confirm button wrapped in `<PulseAccent>`** since it's an active decision. Cancel button: ghost style (`bg-white/60 text-ink-700 hover:bg-white`).

### Input row

Current: `.field-input` (already preserved) + `<Button variant="primary">`.

New: `field-input` stays; Send button becomes the standard lime pill matching every other CTA in the app.

### "Thinking…" indicator

Current: italic text "Thinking…".

New: same text + a subtle 3-dot bouncing animation (CSS keyframe). Honors `prefers-reduced-motion`.

### Welcome bubble

First-time welcome message bubble gets a subtle fade-up reveal on mount (already accomplished by the general message animation).

## Code structure (no API changes)

`ChatWidget` keeps its current props (`role`) and state shape. The `bookings`/`addBooking`/`cancelBooking` integration from 4a stays exactly as-is. This is a pure visual update.

`ChatBubble` and `ConfirmDraft` keep their existing prop signatures.

## Backdrop overlay

When the panel is open on mobile (<md), render a `bg-ink-900/30 backdrop-blur-sm` overlay behind the panel that closes the chat on click. On desktop, no backdrop (the panel is small and side-floats).

## Tests

| Suite | Expected |
|---|---|
| Streamlit | 29 / 29 ✅ |
| FastAPI | 53 / 53 ✅ |
| Vitest | 47 / 47 ✅ (no new tests; pure visual update) |
| Playwright | 2 / 3 (player-flow pre-existing, unchanged) |
| `pnpm build` | clean |

## Out of scope

- Streaming responses
- Persistent chat history
- Backend changes
- Mobile-only redesign of the chat panel (the panel stays at 400×600 fixed positioning even on mobile, with backdrop)
- Voice / multimodal

## Open questions

None — final sub-phase, ship and close out Phase 5.
