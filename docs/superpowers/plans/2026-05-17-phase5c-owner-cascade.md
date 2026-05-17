# Phase 5c — Owner Cascade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Autonomous execution per [[feedback-design-revamp-autonomy]].

**Goal:** Apply the KP+Motion language to the remaining 6 owner pages + 3 supporting components, then delete the now-orphaned `OwnerSidebar`.

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase5c-owner-cascade-design.md` (read the transformation-rules table — every task here is "apply those rules to file X")
**Branch:** `feat/nextjs-phase5c` off main

---

## Task 0: Branch + baseline

- [ ] `git checkout main && git pull && git checkout -b feat/nextjs-phase5c`
- [ ] `cd apps/web && pnpm test:unit` → **43 passed**
- [ ] `pnpm build` → clean

---

## Task 1: `/owner/venues` page

**File:** `apps/web/app/owner/venues/page.tsx`

Apply spec's transformation rules. Headline copy:
- eyebrow: `MANAGE COURTS · ${courts.length} LOCATIONS`
- headline: `Your court portfolio.`
- sub: `Real-time performance metrics and availability control across your elite sports facilities.`
- CTA: `+ Register Venue` (Link to `/owner/venues/new`, same lime pill button style as 5b dashboard CTA)

Replace GRID/LIST chip buttons with new style:
```tsx
<button
  className={[
    'px-4 py-2 rounded-kp-pill text-label-sm font-geist transition-colors duration-quick ease-precision focus-ring',
    view === 'grid' ? 'bg-lime text-ink-900 font-semibold' : 'bg-surface-low text-ink-700 hover:bg-surface-med',
  ].join(' ')}
>GRID</button>
```

Court cards (grid view): keep image header with `<DiagonalDivider>` between hero and body if it improves visual rhythm — implementer's call. Body uses `bg-white rounded-kp-card shadow-float`. Status pill is already inline-styled fine (kept the user's prior fix).

Court card body typography: `font-geist font-semibold text-body-md` for court name, `text-label-sm text-ink-700/60` for location, `font-geist-mono text-title-md tabular-nums text-ink-900` for the utilization/peak numbers.

List view: `bg-white rounded-kp-card shadow-float overflow-hidden` outer, rows separated by `bg-surface-low` band on row hover or every-other-row. Drop the `border-t border-zpots-mint`.

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): venues page → KP+Motion (PageHero, new chips, glass cards)`

---

## Task 2: `CourtForm` + `/owner/venues/new` + `/owner/venues/[id]/edit`

**Files:**
- Modify: `apps/web/components/owner/CourtForm.tsx`
- Modify: `apps/web/app/owner/venues/new/page.tsx`
- Modify: `apps/web/app/owner/venues/[id]/edit/page.tsx`

`CourtForm` is reused by both pages. Apply transformation rules to the form internals: card style swaps, font-display → font-geist, field-label / field-input stay (already styled).

Wrapper pages (`new/page.tsx` and `[id]/edit/page.tsx`):

**new page:**
- PageHero: eyebrow `REGISTER VENUE · ELITE PARTNER`, headline `Add a new court.`, sub `Fill in the details — the AI will surface pricing recommendations once you publish.`
- No CTA (form has its own submit)

**edit page:**
- PageHero: eyebrow `EDIT VENUE`, headline `Update court details.`, sub `Changes go live immediately. Past bookings are unaffected.`

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): CourtForm + new/edit venue wrappers → KP+Motion`

---

## Task 3: `/owner/slots` + `SlotCalendar`

**Files:**
- Modify: `apps/web/app/owner/slots/page.tsx`
- Modify: `apps/web/components/owner/SlotCalendar.tsx`

Page:
- PageHero: eyebrow `SLOT CONTROL · MAY 12–18`, headline `Precision schedule.`, sub `AI is forecasting 97% occupancy for weekend prime slots. Tune the inventory below.`, CTA `+ Add New Slot`
- AI tag (LIVE AI OPTIMIZATION ON) sits inline directly under hero
- KpiCard grid below the calendar — no change to KpiCard itself (already upgraded)

SlotCalendar internals: apply card swap rules. Day cells: subtle hover lift via `hover:shadow-lift` transition. Booked slots: `bg-lime/20 text-ink-900` instead of legacy moss green.

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): slots page + SlotCalendar → KP+Motion`

---

## Task 4: `/owner/pricing`

**File:** `apps/web/app/owner/pricing/page.tsx`

- PageHero: eyebrow `PRICING SETUP · 6 TIERS LIVE`, headline:
```tsx
<>Revenue today: <NumberFlip value={128400} />฿</>
```
sub: `+15% vs last week · Kinetic AI is watching the city demand pulse.`
No CTA (page is form-based)

- Drop the standalone `.zpots-card-dark` revenue banner — its content moved into the hero

- Court tier strip (6 court chips): `bg-white rounded-kp-card shadow-float p-3` each, font-geist typography

- Base Hourly Rates panel: `bg-white rounded-kp-card shadow-float p-5`; inline sub-cards become `bg-surface-low rounded-kp-card p-3`

- AI card: convert `.zpots-card-lime` → `<DarkHero glow="lime" className="p-5">` with white text inside; wrap the SUGGESTED PRICE adjust block's number in subtle PulseAccent. The "+฿2,400 projected daily revenue" line in `text-lime` (the brighter lime on dark bg).

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): pricing page → KP+Motion (hero NumberFlip, dark AI card)`

---

## Task 5: `/owner/optimization` + `OpportunityCard`

**Files:**
- Modify: `apps/web/app/owner/optimization/page.tsx`
- Modify: `apps/web/components/owner/OpportunityCard.tsx`

Page:
- PageHero: eyebrow `AI OPS · PRIORITY INSIGHT`, headline `Optimization engine.`, sub `Surfaced opportunities your venues should act on this week.` No CTA (cards have their own actions).

OpportunityCard: apply token swaps. The opportunity hero should be a `<DarkHero glow="lime">` since it's the most attention-worthy element on the page. Outcome numbers use `<CountUp>` or `<NumberFlip>`.

Three benchmark cards below: `bg-white rounded-kp-card shadow-float p-4` with `font-geist font-semibold` titles and `text-label-sm text-ink-700/60` eyebrows; values use `font-geist-mono tabular-nums`.

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): optimization page + OpportunityCard → KP+Motion`

---

## Task 6: Delete `OwnerSidebar`

**File:** delete `apps/web/components/OwnerSidebar.tsx`

After tasks 1-5, no consumer imports it. Verify:
```bash
grep -rln "OwnerSidebar" apps/web/
```
Expected: 0 matches (besides the file itself).

If clean:
```bash
rm apps/web/components/OwnerSidebar.tsx
git add apps/web/components/OwnerSidebar.tsx
git commit -m "chore(web): delete OwnerSidebar (replaced by TopNav in 5a)"
```

- [ ] Verify zero consumers
- [ ] Delete
- [ ] Commit per above

---

## Task 7: Playwright owner-flow

**File:** `apps/web/tests/owner-flow.spec.ts`

The 5c heading text changed on every owner page. Update selectors that target old `<h1>` text ("Manage Courts" → "Your court portfolio", "Slot Control" → "Precision schedule", "Pricing Setup" → "Revenue today: …", "Optimization Engine" → "Optimization engine"). Prefer URL-based assertions (`toHaveURL(/\/owner\/venues$/)`) where possible — they're stable across copy changes.

Also: the venues page section headings inside cards changed. If the test asserts on specific card content, adapt.

- [ ] Read the spec, identify broken selectors
- [ ] Update minimum-viable
- [ ] `cd apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test 2>&1 | tail -10` → expect **2 passed**
- [ ] Commit: `test(web): owner-flow selectors for 5c heading copy`

---

## Task 8: Final smoke + open PR + merge

- [ ] All suites:
```bash
cd /Users/nchawanp/Desktop/ZPOTS && conda run -n MADT pytest tests/ -q
cd apps/api && conda run -n MADT pytest -q && cd ..
cd apps/web && pnpm test:unit && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```
Expected: Streamlit 29 · FastAPI 53 · Vitest 43 · build clean

- [ ] PR body to `/tmp/pr5c-body.md`:
```markdown
## Summary

Phase 5c — owner cascade. The remaining 6 owner pages (Venues + Add/Edit · Slots · Pricing · Optimization) now use the KP+Motion language locked in 5b. Plus: legacy `OwnerSidebar` deleted (replaced by `TopNav` since 5a).

- Spec: `docs/superpowers/specs/2026-05-17-phase5c-owner-cascade-design.md`
- Plan: `docs/superpowers/plans/2026-05-17-phase5c-owner-cascade.md`

## What ships

- 6 pages migrated: `/owner/venues` · `/owner/venues/new` · `/owner/venues/[id]/edit` · `/owner/slots` · `/owner/pricing` · `/owner/optimization`
- 3 supporting components upgraded: `CourtForm` · `SlotCalendar` · `OpportunityCard`
- `OwnerSidebar.tsx` deleted (no consumers)
- Every owner-side page now uses `<PageHero>` + new glass cards + Geist + lime/ink/surface ramps

## Tests

| Suite | Result |
|---|---|
| Streamlit | 29 / 29 ✅ |
| FastAPI | 53 / 53 ✅ |
| Vitest | 43 / 43 ✅ |
| Playwright | 2 / 3 ⚠️ (player-flow pre-existing, unrelated) |
| `pnpm build` | clean ✅ |

## What's NOT in this PR

- Player pages — Phase 5d
- Chat widget polish — Phase 5e
- Backend changes — none

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

- [ ] Push + create PR + auto-merge:
```bash
git push -u origin feat/nextjs-phase5c
gh pr create --base main --title "Phase 5c: owner cascade (venues, slots, pricing, optimization)" --body-file /tmp/pr5c-body.md
gh pr merge --merge --delete-branch
git checkout main && git pull
```

Report PR URL + merge confirmation.
