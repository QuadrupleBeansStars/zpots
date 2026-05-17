# Phase 5d — Player Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Autonomous execution per [[feedback-design-revamp-autonomy]].

**Goal:** Apply KP+Motion to every player page (11 pages) + ship real mobile menu + delete `PlayerTopBar`.

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase5d-player-revamp-design.md`
**Branch:** `feat/nextjs-phase5d` off main

---

## Task 0: Branch + baseline

- [ ] `git checkout main && git pull && git checkout -b feat/nextjs-phase5d`
- [ ] `cd apps/web && pnpm test:unit` → **43 passed**

---

## Task 1: SplitHero primitive + MobileMenu (TDD)

**Files:**
- Create: `apps/web/components/primitives/SplitHero.tsx`
- Create: `apps/web/components/nav/MobileMenu.tsx`
- Create: `apps/web/tests/SplitHero.test.tsx`
- Create: `apps/web/tests/MobileMenu.test.tsx`
- Modify: `apps/web/components/nav/TopNav.tsx` (wire MobileMenu)

### SplitHero tests
```tsx
// apps/web/tests/SplitHero.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { SplitHero } from '@/components/primitives/SplitHero';

describe('SplitHero', () => {
  it('renders eyebrow, headline, sub, and children', () => {
    render(
      <SplitHero eyebrow="LOGIN" headline="Welcome" sub="Click to enter">
        <p data-testid="form">form here</p>
      </SplitHero>
    );
    expect(screen.getByText('LOGIN')).toBeInTheDocument();
    expect(screen.getByText('Welcome')).toBeInTheDocument();
    expect(screen.getByText('Click to enter')).toBeInTheDocument();
    expect(screen.getByTestId('form')).toBeInTheDocument();
  });
});
```

### SplitHero component
```tsx
// apps/web/components/primitives/SplitHero.tsx
import React from 'react';
import { DarkHero } from './DarkHero';

type Props = {
  eyebrow: React.ReactNode;
  headline: React.ReactNode;
  sub?: React.ReactNode;
  children?: React.ReactNode;
  className?: string;
};

/**
 * Split full-page hero. Used by landing, login pages.
 * Left panel: dark hero (eyebrow + headline + sub). Right panel: children (form/cards).
 * Stacks vertically on mobile.
 */
export function SplitHero({ eyebrow, headline, sub, children, className = '' }: Props) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-[1.2fr_1fr] min-h-screen ${className}`}>
      <DarkHero glow="lime" className="p-8 md:p-13 flex items-center">
        <div>
          <div className="text-label-sm text-lime/70 mb-3">{eyebrow}</div>
          <h1 className="font-geist font-bold text-display-md md:text-display-lg text-white leading-none tracking-tight">
            {headline}
          </h1>
          {sub && (
            <p className="mt-4 text-body-md text-white/60 max-w-md">{sub}</p>
          )}
        </div>
      </DarkHero>
      <div className="bg-surface-low p-8 md:p-13 flex items-center">
        <div className="w-full max-w-md mx-auto">{children}</div>
      </div>
    </div>
  );
}
```

### MobileMenu tests
```tsx
// apps/web/tests/MobileMenu.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

vi.mock('next/navigation', () => ({
  usePathname: () => '/player',
}));

import { MobileMenu } from '@/components/nav/MobileMenu';

describe('MobileMenu', () => {
  it('renders nav links when open', () => {
    render(
      <MobileMenu
        open={true}
        onClose={() => {}}
        items={[{ href: '/a', label: 'A' }, { href: '/b', label: 'B' }]}
      />
    );
    expect(screen.getByText('A')).toBeInTheDocument();
    expect(screen.getByText('B')).toBeInTheDocument();
  });
  it('does not render when closed', () => {
    render(
      <MobileMenu
        open={false}
        onClose={() => {}}
        items={[{ href: '/a', label: 'A' }]}
      />
    );
    expect(screen.queryByText('A')).toBeNull();
  });
  it('calls onClose when close button clicked', () => {
    const onClose = vi.fn();
    render(
      <MobileMenu open={true} onClose={onClose} items={[]} />
    );
    fireEvent.click(screen.getByLabelText('Close menu'));
    expect(onClose).toHaveBeenCalled();
  });
});
```

### MobileMenu component
```tsx
// apps/web/components/nav/MobileMenu.tsx
'use client';
import Link from 'next/link';
import React from 'react';
import { Icon } from '@/components/Icon';

type Item = { href: string; label: string };

type Props = {
  open: boolean;
  onClose: () => void;
  items: Item[];
  cta?: { href: string; label: string };
};

export function MobileMenu({ open, onClose, items, cta }: Props) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 bg-ink-900/95 backdrop-blur-2xl flex flex-col p-8">
      <div className="flex justify-end">
        <button
          type="button"
          onClick={onClose}
          aria-label="Close menu"
          className="p-2 focus-ring rounded-kp-chip text-white"
        >
          <Icon name="close" style={{ fontSize: 28 }} />
        </button>
      </div>
      <nav className="flex-1 flex flex-col justify-center gap-6">
        {items.map((it) => (
          <Link
            key={it.href}
            href={it.href}
            onClick={onClose}
            className="text-display-md font-geist font-bold text-white hover:text-lime transition-colors duration-quick ease-precision focus-ring"
          >
            {it.label}
          </Link>
        ))}
      </nav>
      {cta && (
        <Link
          href={cta.href}
          onClick={onClose}
          className="block w-full text-center px-5 py-4 bg-lime text-ink-900 font-geist font-semibold rounded-kp-pill focus-ring"
        >
          {cta.label}
        </Link>
      )}
    </div>
  );
}
```

### Wire MobileMenu into TopNav

Modify `apps/web/components/nav/TopNav.tsx`. Replace the placeholder hamburger button with stateful open/close:

```tsx
// at top of TopNav.tsx
import { useState } from 'react';
import { MobileMenu } from './MobileMenu';

// inside TopNav function:
const [mobileOpen, setMobileOpen] = useState(false);
const mobileItems = nav.map((it) => ({ href: it.href, label: it.label }));

// replace the placeholder button with:
<button
  type="button"
  onClick={() => setMobileOpen(true)}
  className="md:hidden ml-auto p-2 focus-ring rounded-kp-chip"
  aria-label="Open menu"
>
  <Icon name="menu" style={{ fontSize: 22, color: '#272e42' }} />
</button>

// before the closing </GlassPanel>:
<MobileMenu
  open={mobileOpen}
  onClose={() => setMobileOpen(false)}
  items={mobileItems}
  cta={{ href: ctaHref, label: ctaLabel }}
/>
```

- [ ] Implement + tests pass (`pnpm test:unit` → **47 passed**: 43 + 1 SplitHero + 3 MobileMenu)
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): SplitHero + MobileMenu primitives, wire mobile menu into TopNav`

---

## Task 2: Landing page `/`

**File:** `apps/web/app/page.tsx`

Replace with split-hero composition. Left: dark hero with ZPOTS wordmark + tagline. Right: two role cards stacked or side-by-side.

```tsx
import Link from 'next/link';
import { SplitHero } from '@/components/primitives/SplitHero';
import { Ticker } from '@/components/primitives/Ticker';

export default function LandingPage() {
  return (
    <SplitHero
      eyebrow="KINETIC PRECISION ENGINEERED"
      headline={<>ZPOTS. <span className="text-lime">Book your next game.</span></>}
      sub="AI-powered sports court booking for Bangkok athletes. Real-time availability, smart pricing, instant confirmation."
    >
      <div className="flex flex-col gap-4">
        <RoleCard
          icon="🏸"
          title="I'm a Player"
          description="Discover courts, book sessions, and track your games."
          href="/player/login"
          cta="Enter as Player"
        />
        <RoleCard
          icon="🏟"
          title="I'm a Court Owner"
          description="Manage venues, optimize pricing, grow your business."
          href="/owner-login"
          cta="Enter as Owner"
        />
        <div className="mt-3">
          <Ticker speed={50} className="text-label-sm text-ink-700/60">
            BANGKOK · 247 COURTS · 18 DISTRICTS · 6 SPORTS · AI-MATCHED
          </Ticker>
        </div>
      </div>
    </SplitHero>
  );
}

function RoleCard({ icon, title, description, href, cta }: {
  icon: string; title: string; description: string; href: string; cta: string;
}) {
  return (
    <Link
      href={href}
      className="group block bg-white rounded-kp-card shadow-float p-5 hover:shadow-lift transition-shadow duration-quick ease-precision focus-ring"
    >
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-kp-pill bg-surface-low flex items-center justify-center text-2xl flex-shrink-0">
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="font-geist font-bold text-title-md text-ink-900">{title}</h2>
          <p className="mt-1 text-body-sm text-ink-700/60">{description}</p>
          <span className="inline-flex items-center gap-1 mt-3 text-label-sm font-geist font-semibold text-lime-deep group-hover:text-ink-900">
            {cta} →
          </span>
        </div>
      </div>
    </Link>
  );
}
```

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): landing → SplitHero with role cards + ticker`

---

## Task 3: Both login pages

**Files:**
- Modify: `apps/web/app/player/login/page.tsx`
- Modify: `apps/web/app/owner-login/page.tsx`

Both wrap the existing form in `<SplitHero>`. Form gets the new field-input/button style.

Player login:
```tsx
'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { SplitHero } from '@/components/primitives/SplitHero';

export default function PlayerLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('player@zpots.ai');
  const [password, setPassword] = useState('demo123');

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email.trim() && password.trim()) router.push('/player');
  }

  return (
    <SplitHero
      eyebrow="ATHLETE LOGIN"
      headline={<>Welcome back,<br />Athlete.</>}
      sub="Your next session is one click away."
    >
      <form onSubmit={onSubmit} className="flex flex-col gap-4">
        <div>
          <label className="text-label-sm text-ink-700/60 block mb-2">EMAIL</label>
          <input type="email" className="field-input" value={email}
            onChange={(e) => setEmail(e.target.value)} placeholder="athlete@zpots.ai" />
        </div>
        <div>
          <label className="text-label-sm text-ink-700/60 block mb-2">PASSWORD</label>
          <input type="password" className="field-input" value={password}
            onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
        </div>
        <button
          type="submit"
          className="w-full px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring mt-2"
        >
          LOG IN
        </button>
        <p className="text-body-sm text-ink-700/60 text-center mt-2">
          Demo: <code className="font-geist-mono text-ink-900">player@zpots.ai</code> / <code className="font-geist-mono text-ink-900">demo123</code>
        </p>
      </form>
    </SplitHero>
  );
}
```

Owner login: same pattern, eyebrow `BUSINESS LOGIN`, headline `Manage your courts.`, sub `Welcome back to the dashboard.`, push to `/owner` on submit.

- [ ] Implement both
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): both login pages → SplitHero pattern`

---

## Task 4: Player home `/player`

**File:** `apps/web/app/player/page.tsx`

Multiple sections, all using new primitives. Apply rules:

```tsx
'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getCourts } from '@/lib/data-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { PageHero } from '@/components/primitives/PageHero';
import { DarkHero } from '@/components/primitives/DarkHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { NumberFlip } from '@/components/primitives/NumberFlip';
import { CourtCard } from '@/components/CourtCard';

const SPORTS = [
  { emoji: '🏸', label: 'Badminton' },
  { emoji: '⚽', label: 'Football' },
  { emoji: '🏀', label: 'Basketball' },
  { emoji: '🎾', label: 'Tennis' },
  { emoji: '🏐', label: 'Volleyball' },
  { emoji: '🎾', label: 'Padel' },
];

export default function PlayerHomePage() {
  const [courts, setCourts] = useState<Court[]>(FALLBACK_COURTS);
  useEffect(() => {
    getCourts().then(setCourts).catch(() => setCourts(FALLBACK_COURTS));
  }, []);
  const featured = courts.slice(0, 4);

  return (
    <div className="flex flex-col gap-8">
      <PageHero
        eyebrow="AI-POWERED DISCOVERY"
        headline={<>Discover & book<br />your next game.</>}
        sub="Find the best sports courts in Bangkok. Real-time AI availability, smart filtering, instant booking."
        cta={
          <div className="flex flex-wrap gap-2">
            <Link href="/player/search" className="px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring">
              Search Courts
            </Link>
            <Link href="/player/search" className="px-5 py-3 bg-white/10 text-white font-geist font-semibold text-body-sm rounded-kp-pill hover:bg-white/15 transition-colors duration-quick focus-ring">
              Explore Sports
            </Link>
          </div>
        }
      />

      <RevealOnScroll>
        <section className="flex justify-center flex-wrap gap-6">
          {SPORTS.map((s) => (
            <Link key={s.label} href={`/player/search?sport=${s.label}`} className="flex flex-col items-center gap-2 group focus-ring rounded-kp-chip p-2">
              <div className="w-14 h-14 rounded-kp-pill bg-surface-low flex items-center justify-center text-2xl group-hover:bg-surface-med transition-colors duration-quick">
                {s.emoji}
              </div>
              <span className="text-label-sm text-ink-700/70 group-hover:text-ink-900">{s.label}</span>
            </Link>
          ))}
        </section>
      </RevealOnScroll>

      <section>
        <div className="flex justify-between items-end mb-4">
          <div>
            <h2 className="font-geist font-bold text-title-lg text-ink-900">Featured Courts</h2>
            <p className="text-body-sm text-ink-700/60 mt-1">Top-rated venues chosen by the Bangkok community.</p>
          </div>
          <Link href="/player/search" className="text-body-sm text-ink-700 hover:text-ink-900 underline-offset-4 hover:underline">
            View all →
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {featured.map((c, i) => (
            <RevealOnScroll key={c.id} delay={i * 80}>
              <CourtCard court={c} onBook={(court) => { window.location.href = `/player/courts/${court.id}`; }} />
            </RevealOnScroll>
          ))}
        </div>
      </section>

      <RevealOnScroll>
        <section>
          <h2 className="font-geist font-bold text-title-lg text-ink-900 text-center mb-6">Master your game in 3 steps</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { icon: '🔍', step: '1. Search', body: 'Browse local courts based on your sport, time, and budget.' },
              { icon: '📅', step: '2. Book', body: 'Select your preferred time and complete the booking in seconds.' },
              { icon: '🏆', step: '3. Play', body: 'Show your QR code, check in, and enjoy your time with zero hassle.' },
            ].map((s, i) => (
              <RevealOnScroll key={s.step} delay={i * 100}>
                <div className="bg-surface-low rounded-kp-card p-6 text-center">
                  <div className="text-3xl mb-3">{s.icon}</div>
                  <h3 className="font-geist font-bold text-title-md text-ink-900">{s.step}</h3>
                  <p className="text-body-sm text-ink-700/60 mt-2">{s.body}</p>
                </div>
              </RevealOnScroll>
            ))}
          </div>
        </section>
      </RevealOnScroll>

      <RevealOnScroll>
        <DarkHero glow="lime" className="p-8">
          <div className="text-label-sm text-lime/70 mb-3">AI PRECISION SUITE</div>
          <h3 className="font-geist font-bold text-display-md text-white leading-tight">
            Experience precision with <span className="text-lime">Smart Booking</span>.
          </h3>
          <ul className="mt-5 text-body-sm text-white/70 space-y-2">
            <li>→ Dynamic pricing based on real-time court demand</li>
            <li>→ AI-suggested partners matching your skill level</li>
            <li>→ Smart predictions & live availability tracking</li>
          </ul>
        </DarkHero>
      </RevealOnScroll>
    </div>
  );
}
```

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): player home → PageHero + DarkHero + RevealOnScroll`

---

## Task 5: Search `/player/search`

**File:** `apps/web/app/player/search/page.tsx`

PageHero with AI search input below, sport chips, court grid. Apply transformation rules. The search input stays as the existing `.field-input` with the icon — but the surrounding card gets new tokens.

Full code follows the same pattern as Task 4 — read the existing page, apply: `font-display` → `font-geist`, `.chip` styles → new TabStrip-style buttons, `.zpots-card-surface` → `bg-surface-low rounded-kp-card`. PageHero eyebrow `BANGKOK PRECISION SEARCH · ${courts.length} COURTS`, headline `Find your court.`, sub describes the AI search.

The search row (input + Search button) sits in a `bg-white rounded-kp-card shadow-float p-3` below the hero.

- [ ] Implement
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): search page → PageHero + glass search input`

---

## Task 6: Court detail `/player/courts/[id]` + CourtCard

**Files:**
- Modify: `apps/web/app/player/courts/[id]/page.tsx`
- Modify: `apps/web/components/CourtCard.tsx`

The court page leads with a court-specific dark hero (image background, lime overlay). Below: amenities grid, sub-courts list, sticky/sub-CTA to book.

**CourtCard** is consumed by player home + search + this page indirectly. Apply token swap: outer becomes `bg-white rounded-kp-card shadow-float overflow-hidden`, body typography uses font-geist, sport pill uses lime-on-ink.

- [ ] Read existing court detail page (132 lines) and CourtCard, apply transformation rules consistent with home + search
- [ ] Court hero: `<DarkHero glow="lime">` with the existing background image/gradient style overlaid, court name in display-md, sport pill + rating + price chip below
- [ ] Amenities grid: `bg-surface-low rounded-kp-card p-3` cards
- [ ] Book button: lime pill, full width on mobile, anchored to hero
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): court detail page + CourtCard → KP+Motion`

---

## Task 7: Booking checkout `/player/courts/[id]/book`

**File:** `apps/web/app/player/courts/[id]/book/page.tsx`

Same dark hero pattern. Below: date picker, time-slot grid (`bg-white rounded-kp-card shadow-float`, each slot button `bg-surface-low` default, `bg-lime text-ink-900` when selected), confirm CTA wrapped in `<PulseAccent>`.

- [ ] Read existing (142 lines), apply transformation rules
- [ ] PulseAccent on the final Confirm button only after a valid slot is selected
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): booking checkout → KP+Motion, PulseAccent confirm`

---

## Task 8: My bookings, checkin, confirmation, feedback

**Files:**
- Modify: `apps/web/app/player/bookings/page.tsx`
- Modify: `apps/web/app/player/bookings/[txnId]/checkin/page.tsx`
- Modify: `apps/web/app/player/bookings/[txnId]/confirmation/page.tsx`
- Modify: `apps/web/app/player/bookings/[txnId]/feedback/page.tsx`

Apply rules to each:

**My bookings:** PageHero eyebrow `MY GAMES`, headline `<NumberFlip value={bookings.length} /> bookings.`, sub `${userName}, here are your upcoming and past sessions.` Booking cards: `bg-white rounded-kp-card shadow-float p-4`.

**Checkin (QR):** Smaller page. `<DarkHero glow="lime" className="p-8">` with QR card centered on lime accent background inside. Eyebrow `CHECK-IN · TODAY ${date}`, the booking summary + QR scaled big.

**Confirmation:** Celebratory. PageHero with `<NumberFlip>` showing the total price, eyebrow `BOOKING CONFIRMED`, sub showing court+time. RevealOnScroll on summary cards.

**Feedback:** PageHero `LEAVE FEEDBACK · ${court_name}`, headline `How was your game?`, rating form below in `bg-white rounded-kp-card shadow-float p-6`.

- [ ] Implement all 4
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): bookings + checkin + confirmation + feedback pages → KP+Motion`

---

## Task 9: Delete PlayerTopBar

```bash
grep -rln "PlayerTopBar" apps/web/
```
Expected: 0 matches. If clean:
```bash
rm apps/web/components/PlayerTopBar.tsx
git add apps/web/components/PlayerTopBar.tsx
git commit -m "chore(web): delete PlayerTopBar (replaced by TopNav in 5a)"
```

- [ ] Verify zero consumers
- [ ] Delete + commit

---

## Task 10: Playwright player-flow selectors

**File:** `apps/web/tests/player-flow.spec.ts`

The player home, search, court detail, booking pages all changed text/heading. Update selectors:
- Prefer URL-based assertions and stable text (e.g. court names which don't change)
- Avoid asserting on animated content (NumberFlip)

The pre-existing FastAPI-dependence failure is NOT fixed in this task — that's a separate concern.

- [ ] Update selectors
- [ ] `cd apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test 2>&1 | tail -10` — Expected: 2 passed (landing + owner-flow). player-flow still pre-existing fail.
- [ ] Commit: `test(web): player-flow selectors for 5d copy changes`

---

## Task 11: Final smoke + PR + merge

```bash
cd /Users/nchawanp/Desktop/ZPOTS && conda run -n MADT pytest tests/ -q
cd apps/api && conda run -n MADT pytest -q && cd ..
cd apps/web && pnpm test:unit && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```
Expected: Streamlit 29 · FastAPI 53 · Vitest 47 · build clean

PR body → `/tmp/pr5d-body.md`:
```markdown
## Summary

Phase 5d — player revamp. All 11 player-facing pages now use KP+Motion. Plus: real mobile menu (was placeholder hamburger), legacy `PlayerTopBar` deleted.

- Spec: `docs/superpowers/specs/2026-05-17-phase5d-player-revamp-design.md`
- Plan: `docs/superpowers/plans/2026-05-17-phase5d-player-revamp.md`

## What ships

**New primitives:** `SplitHero` (landing + logins) · `MobileMenu` (full-screen overlay)

**11 pages transformed:** `/` · `/player/login` · `/owner-login` · `/player` · `/player/search` · `/player/courts/[id]` · `/player/courts/[id]/book` · `/player/bookings` · `/player/bookings/[txnId]/checkin` · `/player/bookings/[txnId]/confirmation` · `/player/bookings/[txnId]/feedback`

**Supporting components upgraded:** `CourtCard`, `Tags`

**Deleted:** `PlayerTopBar.tsx`

**Mobile menu:** Hamburger in TopNav now opens full-screen ink-900 overlay with display-md nav links + lime CTA.

## Tests

| Suite | Result |
|---|---|
| Streamlit | 29 / 29 ✅ |
| FastAPI | 53 / 53 ✅ |
| Vitest | 47 / 47 ✅ (+4 for SplitHero + MobileMenu) |
| Playwright | 2 / 3 ⚠️ (player-flow pre-existing fail, separate issue) |
| `pnpm build` | clean ✅ |

## What's NOT in this PR

- Chat widget polish — Phase 5e
- Playwright player-flow fix (needs Playwright `webServer` to launch FastAPI — out of scope for design work)
- Backend changes — none

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

```bash
git push -u origin feat/nextjs-phase5d
gh pr create --base main --title "Phase 5d: player revamp + mobile menu" --body-file /tmp/pr5d-body.md
gh pr merge --merge --delete-branch
git checkout main && git pull
```
