# Phase 3a — Owner UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship all 7 owner pages plus login and add/edit-court form in `apps/web/app/owner/`, fed by a mock data layer at `apps/web/lib/owner-mock-data.ts`. No real backend yet — FastAPI lands in Phase 3b, chat in Phase 3c.

**Architecture:** All owner pages live at `apps/web/app/owner/*` (literal path, not a route group — same reasoning as `/player` from Phase 2). The OwnerSidebar from `apps/web/components/OwnerSidebar.tsx` is reused, with its NAV hrefs rewritten to point to `/owner/...`. Pages are React server components where possible, client components where they need state or `useSearchParams`. Four new page-local components live under `apps/web/components/owner/`.

**Tech Stack:** Next.js 16 App Router · TypeScript · Tailwind v3 · Recharts (for UtilizationBars only; demand heatmap is pure CSS-grid) · Vitest · Playwright

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase3a-owner-ui-design.md`
**Branch:** create `feat/nextjs-phase3a` off main

---

## Pre-task setup

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git checkout main && git pull
git checkout -b feat/nextjs-phase3a
```

---

## File structure (end of Phase 3a)

```
apps/web/app/owner/
├── layout.tsx                          # OwnerSidebar + content container (NEW)
├── login/page.tsx                      # form UI only (NEW)
├── page.tsx                            # dashboard (NEW)
├── venues/
│   ├── page.tsx                        # manage courts grid/list (NEW)
│   ├── new/page.tsx                    # add court form (NEW)
│   └── [id]/edit/page.tsx              # edit court form (NEW)
├── slots/page.tsx                      # NEW
├── pricing/page.tsx                    # NEW
├── bookings/page.tsx                   # NEW
├── insights/page.tsx                   # NEW
└── optimization/page.tsx               # NEW

apps/web/components/
├── OwnerSidebar.tsx                    # MODIFIED — hrefs prefixed with /owner
└── owner/                              # NEW directory
    ├── DemandHeatmap.tsx
    ├── SlotCalendar.tsx
    ├── RevenueBanner.tsx
    └── OpportunityCard.tsx

apps/web/lib/
├── owner-mock-data.ts                  # NEW — OWNER_VENUES, WEEKLY_UTILIZATION,
│                                       # DISTRICT_DEMAND, TODAYS_BOOKINGS,
│                                       # OWNER_BOOKINGS, SLOT_CALENDAR, DEMAND_FORECAST,
│                                       # PEAK_UTILIZATION_BARS
├── owner-mock-data.test.ts             # NEW — Vitest sanity
├── heatmap-color.ts                    # NEW — helper for DemandHeatmap
├── heatmap-color.test.ts               # NEW
└── auth-stub.ts                        # MODIFIED — exports currentOwner

apps/web/tests/
└── owner-flow.spec.ts                  # NEW
```

---

## Task 1: owner mock data + auth stub update + heatmap color helper

**Files:**
- Create: `apps/web/lib/owner-mock-data.ts`
- Create: `apps/web/lib/owner-mock-data.test.ts`
- Create: `apps/web/lib/heatmap-color.ts`
- Create: `apps/web/lib/heatmap-color.test.ts`
- Modify: `apps/web/lib/auth-stub.ts`

- [ ] **Step 1: Append to `apps/web/lib/auth-stub.ts`** (keep `currentUser` untouched):

```ts
/**
 * Hardcoded current owner for Phase 3a. Mirrors the seed user
 * `owner@zpots.ai` in `data/database.py:_seed`. Replaced by NextAuth in Phase 4.
 */
export const currentOwner = {
  id: 3,
  name: 'Venue Admin',
  email: 'owner@zpots.ai',
};
```

- [ ] **Step 2: Create `apps/web/lib/heatmap-color.ts`** — interpolates between two ZPOTS palette colours for the demand heatmap.

```ts
/**
 * Interpolates between `from` and `to` hex colors based on `t` in [0, 1].
 * Returns "#RRGGBB". Used by DemandHeatmap to color cells based on predicted bookings.
 */
export function lerpHex(from: string, to: string, t: number): string {
  const clamp = Math.max(0, Math.min(1, t));
  const f = parseInt(from.slice(1), 16);
  const g = parseInt(to.slice(1), 16);
  const fr = (f >> 16) & 0xff;
  const fg = (f >> 8) & 0xff;
  const fb = f & 0xff;
  const gr = (g >> 16) & 0xff;
  const gg = (g >> 8) & 0xff;
  const gb = g & 0xff;
  const r = Math.round(fr + (gr - fr) * clamp);
  const gC = Math.round(fg + (gg - fg) * clamp);
  const b = Math.round(fb + (gb - fb) * clamp);
  return `#${((r << 16) | (gC << 8) | b).toString(16).padStart(6, '0')}`;
}
```

- [ ] **Step 3: Write `apps/web/lib/heatmap-color.test.ts`:**

```ts
import { describe, it, expect } from 'vitest';
import { lerpHex } from './heatmap-color';

describe('lerpHex', () => {
  it('returns from at t=0', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', 0)).toBe('#f2f9ee');
  });
  it('returns to at t=1', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', 1)).toBe('#1e4a00');
  });
  it('returns a midpoint at t=0.5', () => {
    const mid = lerpHex('#000000', '#ffffff', 0.5);
    expect(mid).toBe('#808080');
  });
  it('clamps below 0', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', -1)).toBe('#f2f9ee');
  });
  it('clamps above 1', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', 2)).toBe('#1e4a00');
  });
});
```

- [ ] **Step 4: Create `apps/web/lib/owner-mock-data.ts`** with the verbatim data copied from `data/dummy_data.py` (the Streamlit file at the repo root is the source of truth):

```ts
import type { Booking } from './types';

export type OwnerVenue = {
  id: string;
  name: string;
  location: string;
  courts_count: number;
  revenue_today: number;
  color: string;
};

export type DistrictDemand = {
  name: string;
  demand: number;
  level: 'Peak' | 'Moderate' | 'Saturated';
};

export type TodaysBookingRow = {
  time: string;
  type: string;
  title: string;
  customer: string;
  venue: string;
  status: 'CONFIRMED' | 'IN PROGRESS' | 'UPCOMING' | 'COMPLETED' | 'CANCELLED';
};

export type OwnerBookingRow = {
  customer: string;
  member_id: string;
  court: string;
  sport: string;
  time: string;
  status: 'BOOKED' | 'COMPLETED' | 'CANCELLED';
  avatar_color: string;
};

export type SlotBlock = {
  time: string;
  label: string;
  type: 'booking' | 'maintenance' | 'open';
  color: string;
};

export type DemandCell = {
  day_of_week: number;     // 0=Mon..6=Sun
  hour: number;            // 7..22
  predicted_bookings: number;
};

export const OWNER_VENUES: OwnerVenue[] = [
  { id: 'venue-01', name: 'Main Arena',         location: 'BANGKOK CENTRAL',      courts_count: 6, revenue_today: 1240, color: '#1a3a2a' },
  { id: 'venue-02', name: 'Ari Sports Center',  location: 'PHAYA THAI, BANGKOK',  courts_count: 4, revenue_today:  890, color: '#1a2a3a' },
  { id: 'venue-03', name: 'Sukhumvit Padel',    location: 'KLONG TOEY, BANGKOK',  courts_count: 3, revenue_today: 2150, color: '#2a1a2a' },
];

export const WEEKLY_UTILIZATION: { day: string; pct: number }[] = [
  { day: 'Mon', pct: 65 },
  { day: 'Tue', pct: 72 },
  { day: 'Wed', pct: 58 },
  { day: 'Thu', pct: 80 },
  { day: 'Fri', pct: 91 },
  { day: 'Sat', pct: 88 },
  { day: 'Sun', pct: 45 },
];

export const DISTRICT_DEMAND: DistrictDemand[] = [
  { name: 'Sukhumvit',    demand: 94, level: 'Peak' },
  { name: 'Ari District', demand: 62, level: 'Moderate' },
  { name: 'Thong Lor',    demand: 98, level: 'Saturated' },
];

export const TODAYS_BOOKINGS: TodaysBookingRow[] = [
  { time: '17:00', type: 'PM', title: 'Padel Championship Practice', customer: 'Amanda S.', venue: 'Sukhumvit Padel',    status: 'CONFIRMED' },
  { time: '18:30', type: 'PM', title: 'Casual Tennis Session',       customer: 'Michael W.', venue: 'Ari Sports Center',  status: 'IN PROGRESS' },
  { time: '20:00', type: 'PM', title: 'Late Night Badminton',        customer: 'Sarah L.',   venue: 'Ari Sports Center',  status: 'UPCOMING' },
];

export const OWNER_BOOKINGS: OwnerBookingRow[] = [
  { customer: 'Marcus Sterling',  member_id: '#ZP-2940', court: 'Center Court',     sport: 'Padel',  time: '14:00 - 15:30 (90 min)',  status: 'BOOKED',    avatar_color: '#506300' },
  { customer: 'Elena Rodriguez',  member_id: '#ZP-5811', court: 'Practice Wall 2',  sport: 'Tennis', time: '10:00 - 11:00 (60 min)',  status: 'COMPLETED', avatar_color: '#615e00' },
  { customer: 'Jonathan Wu',      member_id: '#ZP-1087', court: 'West Pitch',       sport: 'Soccer', time: '16:00 - 20:00 (240 min)', status: 'CANCELLED', avatar_color: '#b02500' },
  { customer: 'Sarah Connor',     member_id: '#ZP-0622', court: 'High-Perf Studio', sport: 'Yoga',   time: '18:00 - 19:00 (60 min)',  status: 'BOOKED',    avatar_color: '#3a506b' },
];

export const SLOT_CALENDAR: Record<number, SlotBlock[]> = {
  0: [
    { time: '08:00-10:00', label: 'Advanced Padel', type: 'booking',     color: '#e2e7ff' },
    { time: '14:00-15:00', label: 'Maintenance',    type: 'maintenance', color: '#ffddcc' },
  ],
  1: [
    { time: '10:00-12:00', label: 'Open Booking',   type: 'open',        color: '#f0ffc0' },
  ],
  2: [
    { time: '09:00-11:00', label: 'Maintenance',    type: 'maintenance', color: '#ffddcc' },
    { time: '16:00-18:00', label: 'Open Booking',   type: 'open',        color: '#f0ffc0' },
    { time: '19:00-21:00', label: 'Pickleball Slam',type: 'booking',     color: '#e2e7ff' },
  ],
  3: [],
  4: [],
  5: [
    { time: '08:00-12:00', label: 'Tournament',     type: 'booking',     color: '#e2e7ff' },
  ],
  6: [],
};

/** Demand heatmap: 7 days × 16 hours (07–22). Deterministic pseudo-random
 *  values that look like a real weekly demand pattern (peak Friday evening). */
export const DEMAND_FORECAST: DemandCell[] = (() => {
  const out: DemandCell[] = [];
  for (let dow = 0; dow < 7; dow++) {
    for (let h = 7; h <= 22; h++) {
      // Higher predicted bookings in evening + on Friday/Saturday.
      const eveningBoost = h >= 17 && h <= 21 ? 1.6 : 1.0;
      const weekendBoost = dow === 4 || dow === 5 ? 1.4 : 1.0;
      const base = 0.3 + 0.5 * Math.sin((h - 7) / 8);
      out.push({
        day_of_week: dow,
        hour: h,
        predicted_bookings: Math.round(base * eveningBoost * weekendBoost * 100) / 100,
      });
    }
  }
  return out;
})();

/** 16 hourly bars (07-22). Used on /owner/insights "Peak Utilization". */
export const PEAK_UTILIZATION_BARS: number[] = [30, 35, 38, 42, 50, 58, 62, 68, 75, 85, 92, 95, 88, 70, 50, 30];
```

(Note: the `Booking` import is just to share the type system — we don't actually use it in this file, but keeping the import lets future fields reference it without restructuring. If TS complains about unused import, drop it.)

- [ ] **Step 5: Write `apps/web/lib/owner-mock-data.test.ts`:**

```ts
import { describe, it, expect } from 'vitest';
import { OWNER_VENUES, WEEKLY_UTILIZATION, DISTRICT_DEMAND, TODAYS_BOOKINGS, OWNER_BOOKINGS, SLOT_CALENDAR, DEMAND_FORECAST, PEAK_UTILIZATION_BARS } from './owner-mock-data';

describe('owner-mock-data', () => {
  it('has 3 venues', () => {
    expect(OWNER_VENUES).toHaveLength(3);
    expect(OWNER_VENUES[0].name).toBe('Main Arena');
  });
  it('has weekly utilization for all 7 days', () => {
    expect(WEEKLY_UTILIZATION).toHaveLength(7);
    expect(WEEKLY_UTILIZATION.map((w) => w.day)).toEqual(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
  });
  it('has 3 district demand entries', () => {
    expect(DISTRICT_DEMAND).toHaveLength(3);
    expect(DISTRICT_DEMAND.find((d) => d.name === 'Sukhumvit')?.demand).toBe(94);
  });
  it('has 3 today\'s bookings', () => {
    expect(TODAYS_BOOKINGS).toHaveLength(3);
  });
  it('has 4 owner bookings', () => {
    expect(OWNER_BOOKINGS).toHaveLength(4);
  });
  it('slot calendar has 7 day keys', () => {
    expect(Object.keys(SLOT_CALENDAR)).toHaveLength(7);
    expect(SLOT_CALENDAR[2]).toHaveLength(3);  // Wednesday has 3 events
  });
  it('demand forecast covers 7 days × 16 hours', () => {
    expect(DEMAND_FORECAST).toHaveLength(7 * 16);
  });
  it('peak utilization bars cover 16 hours', () => {
    expect(PEAK_UTILIZATION_BARS).toHaveLength(16);
  });
});
```

- [ ] **Step 6: Run, expect all tests pass.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit
```

Expected: 18 (Phase 2) + 5 (heatmap-color) + 8 (owner-mock-data) = 31 passed.

- [ ] **Step 7: Commit.**

```bash
git add apps/web/lib/owner-mock-data.ts apps/web/lib/owner-mock-data.test.ts apps/web/lib/heatmap-color.ts apps/web/lib/heatmap-color.test.ts apps/web/lib/auth-stub.ts
git commit -m "feat(web): owner mock data + auth stub + heatmap color helper

Phase 3a foundation. owner-mock-data.ts copies OWNER_VENUES,
WEEKLY_UTILIZATION, DISTRICT_DEMAND, TODAYS_BOOKINGS, OWNER_BOOKINGS,
SLOT_CALENDAR verbatim from data/dummy_data.py. DEMAND_FORECAST and
PEAK_UTILIZATION_BARS generated deterministically — Phase 3b will swap
the demand forecast for the live ml/models/demand_predictions.parquet
artifact via the FastAPI endpoint. auth-stub adds currentOwner.
heatmap-color.lerpHex powers the upcoming DemandHeatmap colour scale."
```

---

## Task 2: Fix OwnerSidebar hrefs and wrap "Add New Court"

**Files:**
- Modify: `apps/web/components/OwnerSidebar.tsx`

The current `OwnerSidebar` has NAV hrefs like `/`, `/venues`, `/slots`, etc. These need the `/owner` prefix or the sidebar links go to nonexistent paths. The "Add New Court" Button has no onClick — wrap it in a Link to `/owner/venues/new`.

- [ ] **Step 1: Replace the relevant parts of `apps/web/components/OwnerSidebar.tsx`.** Open the file. Replace the `NAV` array:

```ts
const NAV = [
  { key: 'dashboard', icon: 'dashboard',       label: 'Dashboard',     href: '/owner' },
  { key: 'courts',    icon: 'stadium',         label: 'Venue Manager', href: '/owner/venues' },
  { key: 'slots',     icon: 'calendar_month',  label: 'Slot Control',  href: '/owner/slots' },
  { key: 'pricing',   icon: 'payments',        label: 'Pricing',       href: '/owner/pricing' },
  { key: 'bookings',  icon: 'list_alt',        label: 'Bookings',      href: '/owner/bookings' },
  { key: 'insights',  icon: 'smart_toy',       label: 'AI Insights',   href: '/owner/insights' },
  { key: 'opt',       icon: 'bolt',            label: 'Optimization',  href: '/owner/optimization' },
];
```

- [ ] **Step 2: Fix the active-link detection** in the `NAV.map((it) => { const active = ... })` line. The current detection (`pathname === it.href || (it.href !== '/' && pathname.startsWith(it.href))`) treats `/owner` as a prefix of `/owner/venues`, so Dashboard is always active. Tighten it:

```ts
const active =
  pathname === it.href ||
  (it.href !== '/owner' && pathname.startsWith(it.href));
```

- [ ] **Step 3: Wrap "Add New Court" Button in a Link.** Replace the existing line:

```tsx
<Button variant="primary" icon="add_circle" style={{ justifyContent: 'center', padding: '10px 14px' }}>
  Add New Court
</Button>
```

with:

```tsx
<Link href="/owner/venues/new" style={{ textDecoration: 'none' }}>
  <Button variant="primary" icon="add_circle" style={{ justifyContent: 'center', padding: '10px 14px', width: '100%' }}>
    Add New Court
  </Button>
</Link>
```

- [ ] **Step 4: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Expected: exit 0. (The sidebar isn't yet rendered anywhere since the owner layout doesn't exist; build passes because nothing imports it yet.)

- [ ] **Step 5: Commit.**

```bash
git add apps/web/components/OwnerSidebar.tsx
git commit -m "fix(web): OwnerSidebar hrefs use /owner prefix + Add New Court is now a Link

Sidebar nav was originally written with bare /venues, /slots, etc.
Prefixed each with /owner so the sidebar works inside app/owner/layout.tsx.
Tightened active-link detection so /owner is no longer treated as a prefix
of /owner/venues (was making Dashboard always look active). 'Add New Court'
button now navigates to /owner/venues/new."
```

---

## Task 3: Owner layout

**Files:**
- Create: `apps/web/app/owner/layout.tsx`

- [ ] **Step 1: Create the layout.** Owner uses a side-by-side layout: sidebar on the left, content on the right.

```tsx
import { OwnerSidebar } from '@/components/OwnerSidebar';

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-zpots-surface">
      <OwnerSidebar />
      <main className="flex-1 px-8 py-6 max-w-[1400px]">{children}</main>
    </div>
  );
}
```

- [ ] **Step 2: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 3: Commit.**

```bash
git add apps/web/app/owner/layout.tsx
git commit -m "feat(web): owner layout — OwnerSidebar + content container"
```

---

## Task 4: Owner login

**Files:**
- Create: `apps/web/app/owner/login/page.tsx`

Mirror the player login but on a dark navy background. The owner layout's sidebar should NOT show on the login page — Next.js layouts apply to all children, so we need a different layout for `/owner/login`. The simplest fix: render the login page with `position: fixed; inset: 0` to cover the sidebar, OR keep it simple and ship the login page WITHOUT the sidebar by placing it at `/owner-login` instead of `/owner/login`.

Cleanest: keep the route at `/owner/login` and override the layout via a per-route layout. We can put `apps/web/app/owner/login/layout.tsx` that returns just `<>{children}</>` to bypass the parent owner layout. But Next.js layouts compose — so `/owner/login` would still get the OwnerLayout. The proper escape is `app/owner/login/route.tsx`... actually the simplest pattern is to move login out of `/owner/login` to `/owner-login` (top-level route). Per the spec/migration brief, the route was `/owner/login`, but `/owner-login` (no slash) keeps it close enough and avoids the layout conflict.

Decision: use `/owner-login` (top-level), not `/owner/login`. Update the landing's RoleCard href accordingly (already points to `/owner/login` from Phase 1 — need to update). Also update the OwnerSidebar logout link (currently `/`) — fine, that's the landing.

- [ ] **Step 1: Create `apps/web/app/owner-login/page.tsx`** (note: NOT `app/owner/login/`):

```tsx
'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Button } from '@/components/Button';
import { AITag } from '@/components/Tags';

export default function OwnerLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('owner@zpots.ai');
  const [password, setPassword] = useState('owner123');

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email.trim() && password.trim()) {
      router.push('/owner');
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6"
         style={{ background: 'linear-gradient(160deg,#060e20 0%,#0d1b2e 40%,#162d3e 70%,#1a3040 100%)' }}>
      <div className="w-full max-w-md">
        <div className="bg-white rounded-card p-10 shadow-2xl">
          <div className="flex items-center gap-2 mb-4">
            <span className="font-display text-lg font-bold text-zpots-ink">⚡ ZPOTS Admin</span>
          </div>
          <AITag>ELITE VENUE PARTNER</AITag>
          <h1 className="font-display text-3xl font-bold mt-3 text-zpots-ink">
            Venue Control,<br />Supercharged.
          </h1>
          <p className="text-sm text-zpots-ink mt-2 opacity-75">
            Sign in to manage your Bangkok sports facilities.
          </p>

          <form onSubmit={onSubmit} className="mt-6 flex flex-col gap-4">
            <div>
              <label className="field-label">EMAIL</label>
              <input
                type="email" className="field-input" value={email}
                onChange={(e) => setEmail(e.target.value)} placeholder="owner@zpots.ai"
              />
            </div>
            <div>
              <label className="field-label">PASSWORD</label>
              <input
                type="password" className="field-input" value={password}
                onChange={(e) => setPassword(e.target.value)} placeholder="••••••••"
              />
            </div>
            <Button variant="primary" type="submit" className="w-full justify-center mt-2">
              ENTER CONSOLE →
            </Button>
          </form>
        </div>

        <p className="text-center text-xs text-white/75 mt-4">
          New operator?{' '}
          <strong className="text-zpots-lime cursor-pointer">Contact us to register your venue.</strong>
          <br />
          <small className="text-white/60">Demo: owner@zpots.ai / owner123</small>
        </p>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Update the landing's "Enter as Owner" RoleCard href** from `/owner/login` to `/owner-login`. Open `apps/web/app/page.tsx` and replace `href="/owner/login"` with `href="/owner-login"`.

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 4: Commit.**

```bash
git add apps/web/app/owner-login apps/web/app/page.tsx
git commit -m "feat(web): owner login page at /owner-login

Top-level route (not /owner/login) so the OwnerSidebar layout doesn't
wrap it. Dark navy background + glass card + lime CTA matching the legacy
Streamlit owner login. Updates landing's Enter as Owner button to point
here. Form is UI only — any non-empty submit redirects to /owner."
```

---

## Task 5: Owner dashboard

**Files:**
- Create: `apps/web/app/owner/page.tsx`

- [ ] **Step 1: Create `apps/web/app/owner/page.tsx`:**

```tsx
import Link from 'next/link';
import { KpiCard } from '@/components/KpiCard';
import { Button } from '@/components/Button';
import { Eyebrow, AITag, StatusBadge } from '@/components/Tags';
import { UtilizationBars } from '@/components/charts/UtilizationBars';
import { OWNER_VENUES, WEEKLY_UTILIZATION, TODAYS_BOOKINGS } from '@/lib/owner-mock-data';
import { currentOwner } from '@/lib/auth-stub';
import { formatPrice } from '@/lib/format';

const STATUS_VARIANT: Record<string, 'confirmed' | 'progress' | 'completed' | 'cancelled'> = {
  CONFIRMED: 'confirmed',
  'IN PROGRESS': 'progress',
  UPCOMING: 'completed',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
};

export default function OwnerDashboard() {
  return (
    <div className="flex flex-col gap-6">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="font-display text-3xl font-bold">Venue Performance</h1>
          <p className="text-sm text-zpots-muted">
            Real-time metrics for your Bangkok sports facilities. Welcome, {currentOwner.name}.
          </p>
        </div>
        <Link href="/owner/venues/new">
          <Button variant="primary" icon="add_circle">Add Court</Button>
        </Link>
      </header>

      {/* KPIs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="TOTAL BOOKINGS" value="128" delta="↗ +12%" icon="📅" />
        <KpiCard label="TOTAL REVENUE" value={`${formatPrice(64500)} THB`} delta="October 2024" icon="💰" />
        <KpiCard label="AVG UTILIZATION" value="72%" icon="📊" />
        <KpiCard label="TOP RATED COURT" value="Court 3" delta="4.8 ⭐ (142 reviews)" icon="⭐" />
      </div>

      {/* Chart + AI optimizer */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-4">
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Utilization Trends</h3>
          <UtilizationBars data={WEEKLY_UTILIZATION.map((w) => ({ label: w.day, value: w.pct }))} />
        </div>
        <div className="zpots-card-lime p-5">
          <AITag>AI REVENUE OPTIMIZER</AITag>
          <h3 className="font-display text-lg font-bold mt-2" style={{ color: '#1a2600' }}>
            Friday demand is up by 30%.
          </h3>
          <p className="text-sm mt-2" style={{ color: '#1a2600' }}>
            Consider raising prices for 18:00–21:00 slots to maximize revenue.
          </p>
        </div>
      </div>

      {/* Today's bookings + manage venues */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-4">
        <div>
          <h3 className="font-semibold mb-3">Today's Bookings</h3>
          <div className="flex flex-col gap-2">
            {TODAYS_BOOKINGS.map((b) => (
              <div key={b.title} className="zpots-card p-4 flex items-center gap-5">
                <div>
                  <div className="font-display text-lg font-bold">{b.time}</div>
                  <Eyebrow>{b.type}</Eyebrow>
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-sm">{b.title}</div>
                  <div className="text-xs text-zpots-muted">Customer: {b.customer} · {b.venue}</div>
                </div>
                <StatusBadge status={STATUS_VARIANT[b.status] ?? 'confirmed'}>{b.status}</StatusBadge>
              </div>
            ))}
          </div>
          <Link href="/owner/bookings" className="inline-block mt-3 text-sm text-zpots-moss">
            View All Bookings →
          </Link>
        </div>

        <div>
          <div className="flex justify-between mb-3">
            <h3 className="font-semibold">Manage Venues</h3>
            <span className="font-eyebrow text-[10px] text-zpots-muted">{OWNER_VENUES.length} LOCATIONS</span>
          </div>
          <div className="flex flex-col gap-2">
            {OWNER_VENUES.map((v) => (
              <div key={v.id} className="zpots-card flex items-stretch overflow-hidden min-h-[64px]">
                <div className="w-1.5" style={{ background: `linear-gradient(180deg,${v.color},${v.color}cc)` }} />
                <div className="flex-1 p-3">
                  <div className="text-sm font-semibold">{v.name}</div>
                  <Eyebrow>{v.location}</Eyebrow>
                  <div className="flex justify-between text-xs mt-1">
                    <span className="text-zpots-muted">{v.courts_count} courts</span>
                    <span className="font-display text-zpots-moss">{formatPrice(v.revenue_today)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
```

NOTE: `UtilizationBars` may take a different prop shape than `{label, value}[]`. Open `apps/web/components/charts/UtilizationBars.tsx` and adapt the prop name if it differs (e.g., it might want `days: WeeklyUtilization[]` instead). Don't rewrite the component.

`KpiCard` and `StatusBadge` props (per Phase 2 lessons): `KpiCard` takes `{label, value, delta?, icon?}`. `StatusBadge` takes `status` prop, not `variant`.

- [ ] **Step 2: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

If `UtilizationBars` props don't match, adapt to its actual interface. If anything else fails to type-check, fix MINIMALLY and report concerns.

- [ ] **Step 3: Smoke.** `pnpm dev` then open `http://localhost:3000/owner`. Verify sidebar + KPIs + chart + bookings + venue cards render.

- [ ] **Step 4: Commit.**

```bash
git add apps/web/app/owner/page.tsx
git commit -m "feat(web): owner dashboard — KPIs, utilization, today's bookings, venues"
```

---

## Task 6: Manage Courts (Venues) — GRID/LIST with URL param

**Files:**
- Create: `apps/web/app/owner/venues/page.tsx`

- [ ] **Step 1: Create `apps/web/app/owner/venues/page.tsx`:**

```tsx
'use client';
import { Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { COURTS } from '@/lib/mock-data';
import { Button } from '@/components/Button';
import { Eyebrow, StatusBadge } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

const SPORT_ICON: Record<string, string> = {
  Badminton: '🏸', Football: '⚽', Padel: '🎾', Basketball: '🏀', Tennis: '🎾', Volleyball: '🏐',
};

function VenuesPageInner() {
  const router = useRouter();
  const params = useSearchParams();
  const view = (params.get('view') ?? 'grid').toLowerCase() === 'list' ? 'list' : 'grid';

  function setView(v: 'grid' | 'list') {
    const next = new URLSearchParams(params.toString());
    if (v === 'grid') next.delete('view'); else next.set('view', 'list');
    router.push(`/owner/venues?${next.toString()}`);
  }

  return (
    <div>
      <div className="flex justify-between items-end">
        <div>
          <h1 className="font-display text-3xl font-bold">Manage Courts</h1>
          <p className="text-sm text-zpots-muted">Real-time performance metrics and availability control for your elite sports facilities.</p>
        </div>
        <Link href="/owner/venues/new">
          <Button variant="primary" icon="add_circle">Register Venue</Button>
        </Link>
      </div>

      <div className="flex gap-2 mt-4">
        <button onClick={() => setView('grid')} className={`chip ${view === 'grid' ? 'chip-selected' : 'chip-default'}`}>GRID</button>
        <button onClick={() => setView('list')} className={`chip ${view === 'list' ? 'chip-selected' : 'chip-default'}`}>LIST</button>
      </div>

      <div className="mt-6">
        {view === 'grid' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {COURTS.map((c) => (
              <div key={c.id} className="zpots-card overflow-hidden">
                <div className="h-40 flex items-center justify-center relative" style={{ background: `linear-gradient(135deg,${c.color},${c.color}cc)` }}>
                  <span className="text-5xl">{SPORT_ICON[c.sport] ?? '🏟'}</span>
                  <StatusBadge status="confirmed" className="absolute top-3 left-3">● {c.status}</StatusBadge>
                </div>
                <div className="p-4">
                  <div className="font-bold">{c.name}</div>
                  <div className="text-xs text-zpots-muted">📍 {c.district}, Bangkok</div>
                  <div className="flex gap-6 mt-3 text-xs">
                    <div><Eyebrow>Utilization</Eyebrow><div className="font-display font-bold text-base">{c.utilization}%</div></div>
                    <div><Eyebrow>Peak hours</Eyebrow><div className="font-display font-bold text-base">{c.peak_hours}</div></div>
                    <div><Eyebrow>AI efficiency</Eyebrow><div className="font-display font-bold text-base italic">{c.ai_efficiency}</div></div>
                  </div>
                  <Link href={`/owner/venues/${c.id}/edit`} className="block mt-4">
                    <Button variant="secondary" className="w-full justify-center">Edit Court</Button>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="zpots-card overflow-hidden">
            <div className="grid grid-cols-[48px_2fr_1fr_1fr_1fr_100px] gap-3 p-3 bg-zpots-surface">
              <div></div>
              <Eyebrow>Court</Eyebrow>
              <Eyebrow>District</Eyebrow>
              <Eyebrow>Utilization</Eyebrow>
              <Eyebrow>Peak hours</Eyebrow>
              <Eyebrow>Price/hr</Eyebrow>
            </div>
            {COURTS.map((c) => (
              <div key={c.id} className="grid grid-cols-[48px_2fr_1fr_1fr_1fr_100px] gap-3 p-3 border-t border-zpots-mint items-center">
                <div className="w-9 h-9 rounded-lg flex items-center justify-center text-lg" style={{ background: `linear-gradient(135deg,${c.color},${c.color}cc)` }}>
                  {SPORT_ICON[c.sport] ?? '🏟'}
                </div>
                <div>
                  <div className="font-semibold text-sm">{c.name}</div>
                  <div className="text-xs text-zpots-muted">{c.sport}</div>
                </div>
                <div className="text-sm">{c.district}</div>
                <div className="font-display font-bold">{c.utilization}%</div>
                <div className="text-sm">{c.peak_hours}</div>
                <div className="text-sm font-display font-bold text-zpots-moss">{formatPrice(c.price_per_hour)}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function VenuesPage() {
  return <Suspense fallback={null}><VenuesPageInner /></Suspense>;
}
```

If `StatusBadge` doesn't accept `className`, drop it and wrap the badge in a styled span.

- [ ] **Step 2: Build + smoke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Open `http://localhost:3000/owner/venues`. Click GRID/LIST chips, URL updates to `?view=list` and layout swaps.

- [ ] **Step 3: Commit.**

```bash
git add apps/web/app/owner/venues/page.tsx
git commit -m "feat(web): manage courts page with URL-param GRID/LIST toggle

Reads COURTS from the player mock-data layer (same set) and renders
either a 2-column card grid or a compact table. The chip-style toggle
pushes ?view=list into the URL so the choice is linkable."
```

---

## Task 7: Add/Edit Court form

**Files:**
- Create: `apps/web/components/owner/CourtForm.tsx`
- Create: `apps/web/app/owner/venues/new/page.tsx`
- Create: `apps/web/app/owner/venues/[id]/edit/page.tsx`

Both pages render the same `CourtForm` component, just with different `mode` and (for edit) the court id.

- [ ] **Step 1: Create `apps/web/app/owner/venues/new/page.tsx`:**

```tsx
import { CourtForm } from '@/components/owner/CourtForm';

export default function NewCourtPage() {
  return <CourtForm mode="new" />;
}
```

- [ ] **Step 2: Create `apps/web/components/owner/CourtForm.tsx`:**

```tsx
'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/Button';
import { Eyebrow, AITag } from '@/components/Tags';
import { COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';

const SPORTS = ['Badminton', 'Football', 'Basketball', 'Padel', 'Tennis', 'Volleyball'];
const SURFACES = ['Professional Mat', 'Premium Synthetic', 'Hardwood', 'Artificial Turf', 'Glass Panels', 'Clay', 'Sprung Floor'];
const AMENITY_OPTIONS = ['AC Units', 'Pro Lighting', 'Locker Rooms', 'Water Station', 'AV Video', 'Showers', 'Cafe', 'Parking'];

export function CourtForm({ mode, courtId }: { mode: 'new' | 'edit'; courtId?: string }) {
  const existing: Court | undefined = courtId ? COURTS.find((c) => c.id === courtId) : undefined;
  const [name, setName] = useState(existing?.name ?? '');
  const [sport, setSport] = useState(existing?.sport ?? 'Badminton');
  const [surface, setSurface] = useState(existing?.surface ?? 'Premium Synthetic');
  const [location, setLocation] = useState(existing?.location ?? '');
  const [description, setDescription] = useState('');
  const [amenities, setAmenities] = useState<string[]>(
    existing ? existing.amenities.map((a) => a.label) : [],
  );

  function toggleAmenity(a: string) {
    setAmenities((s) => (s.includes(a) ? s.filter((x) => x !== a) : [...s, a]));
  }

  return (
    <div>
      <Link href="/owner/venues" className="text-sm text-zpots-moss">← Back to courts</Link>
      <h1 className="font-display text-3xl font-bold mt-3">
        {mode === 'new' ? 'Add New Court' : `Edit ${existing?.name ?? 'Court'}`}
      </h1>
      <p className="text-sm text-zpots-muted">
        Configure high-performance court settings. Changes reflect across all booking channels instantly via Sync. <em>(In Phase 3a, nothing is saved — Phase 4 wires the real backend.)</em>
      </p>

      <div className="zpots-card p-6 mt-5 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <Eyebrow>COURT FUNDAMENTALS</Eyebrow>

          <div className="mt-3">
            <label className="field-label">COURT NAME</label>
            <input className="field-input" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Center Court" />
          </div>

          <div className="grid grid-cols-2 gap-3 mt-3">
            <div>
              <label className="field-label">SPORT CATEGORY</label>
              <select className="field-input" value={sport} onChange={(e) => setSport(e.target.value)}>
                {SPORTS.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="field-label">SURFACE TYPE</label>
              <select className="field-input" value={surface} onChange={(e) => setSurface(e.target.value)}>
                {SURFACES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
          </div>

          <div className="mt-3">
            <label className="field-label">LOCATION / FULL ADDRESS</label>
            <input className="field-input" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Sukhumvit Soi 39, Bangkok 10110" />
          </div>

          <div className="mt-3">
            <label className="field-label">COURT DESCRIPTION</label>
            <textarea className="field-input" rows={4} value={description} onChange={(e) => setDescription(e.target.value)}
                      placeholder="Write a description so users discover & connect with your court..." />
            <Button variant="primary" className="mt-2" type="button"
                    onClick={() => setDescription('A premium climate-controlled venue with elite-grade equipment, located in the heart of Bangkok. Open daily 06:00–23:00.')}>
              <AITag>AI</AITag> Generate Description
            </Button>
          </div>

          <div className="mt-4">
            <Eyebrow>KINETIC AMENITIES</Eyebrow>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2">
              {AMENITY_OPTIONS.map((a) => (
                <label key={a} className="flex items-center gap-2 text-sm">
                  <input type="checkbox" checked={amenities.includes(a)} onChange={() => toggleAmenity(a)} />
                  {a}
                </label>
              ))}
            </div>
          </div>
        </div>

        <div>
          <Eyebrow>VISUAL & BRANDING</Eyebrow>
          <div className="zpots-card-surface mt-3 h-48 flex items-center justify-center text-zpots-muted text-sm">
            Drag and drop file here<br />Limit 200MB · JPG, PNG, MP4
          </div>
          <Button variant="secondary" className="mt-3 w-full justify-center" type="button">Browse files</Button>

          <div className="mt-6">
            <Eyebrow>MICROLOCATION</Eyebrow>
            <div className="zpots-card-surface h-40 mt-2 flex items-center justify-center text-zpots-muted text-sm">
              (Map placeholder — real map lands in Phase 4)
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-2 mt-5">
        <Link href="/owner/venues"><Button variant="secondary">Discard Changes</Button></Link>
        <Button variant="primary" type="button" onClick={() => alert('Saved (demo). Real backend lands in Phase 4.')}>
          Save & Continue →
        </Button>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Create `apps/web/app/owner/venues/[id]/edit/page.tsx`:**

```tsx
'use client';
import { useParams } from 'next/navigation';
import { CourtForm } from '@/components/owner/CourtForm';

export default function EditCourtPage() {
  const params = useParams<{ id: string }>();
  return <CourtForm mode="edit" courtId={params.id} />;
}
```

- [ ] **Step 4: Build + smoke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Open `/owner/venues/new` and `/owner/venues/bbc-01/edit`. Form fields render. Generate Description button fills the textarea.

- [ ] **Step 5: Commit.**

```bash
git add "apps/web/app/owner/venues/new" "apps/web/app/owner/venues/[id]/edit"
git commit -m "feat(web): add/edit court form (shared CourtForm component)

Both /owner/venues/new and /owner/venues/[id]/edit render the same
form. Edit prefills from COURTS by id. AI Generate Description shows
a hardcoded blurb in Phase 3a; Phase 3b will call /api/ai/court-description."
```

---

## Task 8: Slot Control + SlotCalendar component

**Files:**
- Create: `apps/web/components/owner/SlotCalendar.tsx`
- Create: `apps/web/app/owner/slots/page.tsx`

- [ ] **Step 1: Create `apps/web/components/owner/SlotCalendar.tsx`:**

```tsx
import type { SlotBlock } from '@/lib/owner-mock-data';

const DAYS = [
  { name: 'MON', date: 12 },
  { name: 'TUE', date: 13 },
  { name: 'WED', date: 14, today: true },
  { name: 'THU', date: 15 },
  { name: 'FRI', date: 16 },
  { name: 'SAT', date: 17 },
  { name: 'SUN', date: 18 },
];

export function SlotCalendar({ calendar }: { calendar: Record<number, SlotBlock[]> }) {
  return (
    <div className="grid grid-cols-7 gap-2">
      {DAYS.map((d, i) => (
        <div key={d.name} className="flex flex-col gap-2">
          <div className={`text-center text-xs uppercase font-eyebrow py-2 rounded-card ${d.today ? 'bg-zpots-lime text-zpots-forest font-bold' : 'bg-zpots-surface text-zpots-muted'}`}>
            {d.name}<br />{d.date}
          </div>
          {(calendar[i] ?? []).map((slot, j) => (
            <div key={`${slot.time}-${j}`} className="rounded-card p-2" style={{ background: slot.color }}>
              <div className="font-semibold text-xs text-zpots-ink">{slot.label}</div>
              <div className="text-[10px] text-zpots-muted">{slot.time}</div>
            </div>
          ))}
          {(calendar[i] ?? []).length === 0 && (
            <div className="rounded-card p-3 bg-zpots-surface text-center text-zpots-muted text-xs cursor-pointer">+</div>
          )}
        </div>
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Create `apps/web/app/owner/slots/page.tsx`:**

```tsx
import { Button } from '@/components/Button';
import { KpiCard } from '@/components/KpiCard';
import { AITag } from '@/components/Tags';
import { SlotCalendar } from '@/components/owner/SlotCalendar';
import { SLOT_CALENDAR } from '@/lib/owner-mock-data';

export default function SlotsPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="font-display text-3xl font-bold">Slot Control</h1>
          <p className="text-sm text-zpots-muted">Precision management of court inventory. AI is currently forecasting 97% occupancy for weekend prime slots.</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-zpots-muted">May 12–18</span>
          <Button variant="primary" icon="add_circle">Add New Slot</Button>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <AITag>LIVE AI OPTIMIZATION ON</AITag>
      </div>

      <SlotCalendar calendar={SLOT_CALENDAR} />

      <h2 className="font-semibold mt-4">🤖 AI Performance Prediction</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="PREDICTED REVENUE" value="฿4,280" delta="↗ +10% vs LW" icon="💰" />
        <KpiCard label="PEAK HOURS"        value="18:00–20:00" delta="Fri, Sat, Sun" icon="🕐" />
        <KpiCard label="OCCUPANCY"         value="88.4%" icon="📊" />
        <KpiCard label="ACTIVE SLOTS"      value="24 Active" delta="View Rewards" icon="📅" />
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Build + smoke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Open `/owner/slots`. 7 day columns, Wed highlighted, slot blocks visible (Padel/Maintenance/Open Booking/Tournament), 4 KPI cards below.

- [ ] **Step 4: Commit.**

```bash
git add apps/web/components/owner/SlotCalendar.tsx apps/web/app/owner/slots/page.tsx
git commit -m "feat(web): slot control page + SlotCalendar component

Week-grid calendar with seeded slot blocks from owner-mock-data."
```

---

## Task 9: Pricing page

**Files:**
- Create: `apps/web/app/owner/pricing/page.tsx`

- [ ] **Step 1: Create `apps/web/app/owner/pricing/page.tsx`:**

```tsx
'use client';
import { useState } from 'react';
import { COURTS } from '@/lib/mock-data';
import { Button } from '@/components/Button';
import { Eyebrow, AITag } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

export default function PricingPage() {
  const [standard, setStandard] = useState(450);
  const [prime, setPrime] = useState(650);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-3xl font-bold">Pricing Setup</h1>
        <p className="text-sm text-zpots-muted">Precision control for your revenue. Leverage our proprietary Kinetic AI to optimize hourly rates based on real-time city demand.</p>
      </div>

      <div className="zpots-card-dark p-6">
        <Eyebrow>REVENUE TODAY</Eyebrow>
        <div className="font-display text-4xl font-bold text-white mt-1">{formatPrice(128400)}</div>
        <div className="text-xs text-white/70">+15% vs last week · 6 pricing tiers live</div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
        {COURTS.slice(0, 6).map((c) => (
          <div key={c.id} className="zpots-card p-3">
            <div className="text-xs font-semibold truncate">{c.name}</div>
            <span className="font-eyebrow text-[9px] text-zpots-moss">ACTIVE</span>
            <div className="font-display text-base font-bold mt-1">{formatPrice(c.price_per_hour)}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1.6fr_1fr] gap-5">
        {/* Editable rates */}
        <div className="zpots-card p-5">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-semibold">Base Hourly Rates</h3>
              <Eyebrow>MANUAL FOUNDATION</Eyebrow>
            </div>
            <span className="text-xl">💰</span>
          </div>

          <div className="mt-4">
            <div className="zpots-card-surface p-3 mb-2">
              <div className="font-semibold text-sm">Standard Court</div>
              <div className="text-xs text-zpots-muted">Weekdays 08:00 - 17:00</div>
            </div>
            <input type="number" className="field-input" value={standard} step={50} onChange={(e) => setStandard(parseInt(e.target.value || '0', 10))} />
          </div>

          <div className="mt-4">
            <div className="zpots-card-surface p-3 mb-2">
              <div className="font-semibold text-sm">Prime Time</div>
              <div className="text-xs text-zpots-muted">Daily 17:00 - 23:00</div>
            </div>
            <input type="number" className="field-input" value={prime} step={50} onChange={(e) => setPrime(parseInt(e.target.value || '0', 10))} />
          </div>

          <div className="grid grid-cols-2 gap-3 mt-5">
            <div className="zpots-card-surface p-3">
              <Eyebrow>COMPETITOR AVERAGE</Eyebrow>
              <div className="font-display text-xl font-bold mt-1">{formatPrice(510)} /hr</div>
              <div className="text-xs text-zpots-moss">Your pricing is 12% below market</div>
            </div>
            <div className="zpots-card-surface p-3">
              <Eyebrow>OCCUPANCY FORECAST</Eyebrow>
              <div className="font-display text-xl font-bold mt-1">92%</div>
              <div className="text-xs text-zpots-moss">HIGH DEMAND EXPECTED</div>
            </div>
          </div>
        </div>

        {/* AI insight + elasticity */}
        <div className="zpots-card-lime p-5">
          <AITag>LIVE AI INSIGHT</AITag>
          <h3 className="font-display text-lg font-bold mt-2" style={{ color: '#1a2600' }}>
            Demand Prediction<br />+30% for Friday Evening
          </h3>
          <p className="text-xs mt-2" style={{ color: '#1a2600' }}>
            Local tournaments and social events in your area are spiking demand for Friday 18:00–21:00. Our kinetic model suggests a tactical rate adjustment to maximize yield.
          </p>
          <hr className="border-black/10 my-3" />
          <Eyebrow>SUGGESTED PRICE ADJUSTMENT</Eyebrow>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-xs line-through text-zpots-muted">{formatPrice(450)}</span>
            <span className="font-display text-2xl font-bold" style={{ color: '#1a2600' }}>{formatPrice(580)}</span>
            <span className="text-base">⚡</span>
          </div>
          <div className="text-xs mt-2" style={{ color: '#1a2600' }}>💰 +{formatPrice(2400)} projected daily revenue</div>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Build + smoke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Open `/owner/pricing`. Revenue banner + 6 court price tiles + 2-column layout with editable Standard/Prime inputs + AI insight card.

- [ ] **Step 3: Commit.**

```bash
git add apps/web/app/owner/pricing/page.tsx
git commit -m "feat(web): pricing page — revenue banner, editable base rates, AI insight card"
```

---

## Task 10: Booking Dashboard + RevenueBanner

**Files:**
- Create: `apps/web/components/owner/RevenueBanner.tsx`
- Create: `apps/web/app/owner/bookings/page.tsx`

- [ ] **Step 1: Create `apps/web/components/owner/RevenueBanner.tsx`:**

```tsx
import { Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

type Props = {
  total: number;
  delta: string;
  breakdown: { label: string; amount: number; highlight?: boolean }[];
};

export function RevenueBanner({ total, delta, breakdown }: Props) {
  return (
    <div className="rounded-card p-6 text-white" style={{ background: 'linear-gradient(135deg, #1a3a2a, #2E6B00)' }}>
      <div className="flex justify-between items-start">
        <div>
          <Eyebrow style={{ color: 'rgba(255,255,255,0.7)' }}>TOTAL REVENUE TODAY</Eyebrow>
          <div className="font-display text-5xl font-bold mt-1">{formatPrice(total)}</div>
          <div className="text-xs mt-1 opacity-80">📈 {delta}</div>
        </div>
      </div>
      <div className="flex gap-3 mt-5 flex-wrap">
        {breakdown.map((b) => (
          <div
            key={b.label}
            className="rounded-card px-4 py-2"
            style={{ background: b.highlight ? 'rgba(207,252,0,0.3)' : 'rgba(255,255,255,0.15)' }}
          >
            <div className="text-[10px] opacity-70">{b.label}</div>
            <div className="font-display font-bold">{formatPrice(b.amount)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

Note: `Eyebrow style={{...}}` won't work if Eyebrow doesn't accept `style`. If TypeScript complains, replace with a raw `<span className="font-eyebrow text-[10px] uppercase tracking-wider" style={{color: 'rgba(255,255,255,0.7)'}}>TOTAL REVENUE TODAY</span>`.

- [ ] **Step 2: Create `apps/web/app/owner/bookings/page.tsx`:**

```tsx
import { RevenueBanner } from '@/components/owner/RevenueBanner';
import { StatusBadge, Eyebrow } from '@/components/Tags';
import { OWNER_BOOKINGS } from '@/lib/owner-mock-data';

const STATUS_TO_VARIANT: Record<string, 'confirmed' | 'completed' | 'cancelled'> = {
  BOOKED: 'confirmed',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
};

const RISK_BY_SPORT: Record<string, { tier: string; cls: 'confirmed' | 'progress' | 'cancelled' }> = {
  Padel:  { tier: 'Low',    cls: 'confirmed' },
  Tennis: { tier: 'Medium', cls: 'progress' },
  Soccer: { tier: 'High',   cls: 'cancelled' },
  Yoga:   { tier: 'Low',    cls: 'confirmed' },
};

export default function BookingDashboardPage() {
  return (
    <div className="flex flex-col gap-5">
      <h1 className="font-display text-3xl font-bold">Bookings</h1>

      <RevenueBanner
        total={4280}
        delta="+15.6% from yesterday · Upcoming"
        breakdown={[
          { label: 'MAIN ARENA',  amount: 1240 },
          { label: 'PADEL POD 2', amount:  890 },
          { label: 'INDOOR TURF', amount: 2150, highlight: true },
        ]}
      />

      {/* Today / This Week / Calendar — visual tabs only in 3a */}
      <div className="flex gap-2">
        <button className="chip chip-selected">Today</button>
        <button className="chip chip-default">This Week</button>
        <button className="chip chip-default">Calendar</button>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-2 gap-3">
        <select className="field-input"><option>All Venues</option><option>Main Arena</option><option>Padel Pod 2</option><option>Indoor Turf</option></select>
        <select className="field-input"><option>Time Descending</option><option>Time Ascending</option><option>Status</option></select>
      </div>

      {/* Header */}
      <div className="grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 px-4 py-3">
        <Eyebrow>Customer</Eyebrow>
        <Eyebrow>Session info</Eyebrow>
        <Eyebrow>Status</Eyebrow>
        <Eyebrow>Risk</Eyebrow>
      </div>

      {/* Rows */}
      <div className="flex flex-col gap-2">
        {OWNER_BOOKINGS.map((b) => {
          const risk = RISK_BY_SPORT[b.sport] ?? { tier: 'Medium', cls: 'progress' as const };
          return (
            <div key={b.member_id} className="zpots-card grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 items-center p-3">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full text-white flex items-center justify-center font-semibold" style={{ background: b.avatar_color }}>{b.customer[0]}</div>
                <div>
                  <div className="font-semibold text-sm">{b.customer}</div>
                  <div className="text-xs text-zpots-muted">Member ID: {b.member_id}</div>
                </div>
              </div>
              <div>
                <div className="text-sm">🏟 {b.court} • {b.sport}</div>
                <div className="text-xs text-zpots-muted">🕐 {b.time}</div>
              </div>
              <StatusBadge status={STATUS_TO_VARIANT[b.status] ?? 'confirmed'}>{b.status}</StatusBadge>
              <StatusBadge status={risk.cls}>{risk.tier}</StatusBadge>
            </div>
          );
        })}
      </div>

      <div className="text-xs text-zpots-muted">SHOWING {OWNER_BOOKINGS.length} BOOKINGS · seeded demo data</div>
    </div>
  );
}
```

- [ ] **Step 3: Build + smoke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Open `/owner/bookings`. Revenue banner + tabs + filters + booking rows with avatar bubble + status/risk badges.

- [ ] **Step 4: Commit.**

```bash
git add apps/web/components/owner/RevenueBanner.tsx apps/web/app/owner/bookings/page.tsx
git commit -m "feat(web): booking dashboard + RevenueBanner component

Revenue banner with venue breakdown, Today/This Week/Calendar tabs
(visual only), venue+sort filters, booking rows with avatar bubble,
status and no-show risk pills. Risk tier derived from sport in Phase
3a; real ML inference call lands in Phase 3b."
```

---

## Task 11: AI Insights + DemandHeatmap

**Files:**
- Create: `apps/web/components/owner/DemandHeatmap.tsx`
- Create: `apps/web/app/owner/insights/page.tsx`

- [ ] **Step 1: Create `apps/web/components/owner/DemandHeatmap.tsx`:**

```tsx
import type { DemandCell } from '@/lib/owner-mock-data';
import { lerpHex } from '@/lib/heatmap-color';

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const HOURS = Array.from({ length: 16 }, (_, i) => i + 7);  // 7..22

export function DemandHeatmap({ data }: { data: DemandCell[] }) {
  const max = data.reduce((m, c) => Math.max(m, c.predicted_bookings), 0) || 1;
  const cellByKey = new Map(data.map((c) => [`${c.day_of_week}-${c.hour}`, c]));

  return (
    <div>
      <div className="grid" style={{ gridTemplateColumns: '40px repeat(16, 1fr)', gap: 2 }}>
        <div></div>
        {HOURS.map((h) => (
          <div key={h} className="text-[9px] text-zpots-muted text-center">{h}</div>
        ))}
        {DAYS.map((day, dow) => (
          <FragmentRow key={day} day={day} cells={HOURS.map((h) => cellByKey.get(`${dow}-${h}`)!)} max={max} />
        ))}
      </div>
      <div className="flex items-center gap-2 mt-2 text-[10px] text-zpots-muted">
        <span>Low</span>
        <div className="flex-1 h-2 rounded-pill" style={{ background: `linear-gradient(90deg, ${lerpHex('#F2F9EE', '#1E4A00', 0)}, ${lerpHex('#F2F9EE', '#1E4A00', 1)})` }} />
        <span>High</span>
      </div>
    </div>
  );
}

function FragmentRow({ day, cells, max }: { day: string; cells: DemandCell[]; max: number }) {
  return (
    <>
      <div className="text-[10px] font-eyebrow text-zpots-muted self-center">{day}</div>
      {cells.map((c, i) => (
        <div
          key={i}
          title={c ? `${c.predicted_bookings.toFixed(2)} bookings` : ''}
          style={{
            aspectRatio: '1',
            background: c ? lerpHex('#F2F9EE', '#1E4A00', c.predicted_bookings / max) : '#fff',
            borderRadius: 3,
          }}
        />
      ))}
    </>
  );
}
```

- [ ] **Step 2: Create `apps/web/app/owner/insights/page.tsx`:**

```tsx
'use client';
import { useState } from 'react';
import { Button } from '@/components/Button';
import { AITag, Eyebrow, StatusBadge } from '@/components/Tags';
import { DemandHeatmap } from '@/components/owner/DemandHeatmap';
import { DEMAND_FORECAST, DISTRICT_DEMAND, PEAK_UTILIZATION_BARS } from '@/lib/owner-mock-data';

const MOCK_SUMMARY =
  'Your Friday evening slots (18:00–21:00) continue to dominate revenue, ' +
  'driving 41% of weekly bookings. Sukhumvit demand is saturated — consider ' +
  'opening Court 4 for tournament-rate pricing. Thong Lor traffic predicted ' +
  'to intensify Saturday after 16:00 due to weather; auto-rescheduling ' +
  'recommended for 12% of bookings.';

const LEVEL_TO_STATUS: Record<string, 'confirmed' | 'progress' | 'cancelled'> = {
  Peak: 'confirmed', Moderate: 'progress', Saturated: 'cancelled',
};

export default function InsightsPage() {
  const [summary, setSummary] = useState('');

  return (
    <div className="flex flex-col gap-5">
      <div className="flex justify-between items-end">
        <div className="flex items-center gap-3">
          <h1 className="font-display text-3xl font-bold">AI Insights</h1>
          <AITag>ELITE VENUE PARTNER</AITag>
        </div>
        <div className="flex gap-2">
          <Button variant="primary" icon="smart_toy" onClick={() => setSummary(MOCK_SUMMARY)}>
            Generate AI Summary
          </Button>
          <Button variant="secondary" onClick={() => setSummary('')}>Regenerate</Button>
        </div>
      </div>

      {summary && (
        <div className="zpots-card-surface p-4">
          <AITag>AI GENERATED SUMMARY</AITag>
          <p className="mt-2 text-sm leading-relaxed">{summary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Bangkok Demand Heatmap</h3>
          <Eyebrow>7-DAY FORECAST · MODEL: RANDOM FOREST</Eyebrow>
          <div className="mt-3">
            <DemandHeatmap data={DEMAND_FORECAST} />
          </div>
        </div>
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Peak Utilization</h3>
          <Eyebrow>HOURLY DISTRIBUTION</Eyebrow>
          <div className="flex items-end gap-[3px] h-24 mt-3">
            {PEAK_UTILIZATION_BARS.map((v, i) => (
              <div key={i} className="flex-1 rounded-t" style={{
                height: `${v}%`,
                background: v > 80 ? '#CFFC00' : v > 50 ? '#2E6B00' : '#A5D6A7',
              }} />
            ))}
          </div>
          <div className="mt-3 zpots-card-surface p-3 flex justify-between">
            <div><span className="text-zpots-lime">⚡</span> <strong>Golden Slot</strong></div>
            <span className="font-display font-bold text-zpots-moss">฿2,400/hr</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {DISTRICT_DEMAND.map((d) => (
          <div key={d.name} className="zpots-card-surface p-4 text-center">
            <Eyebrow>{d.name}</Eyebrow>
            <div className="font-display text-2xl font-bold my-1">{d.demand}%</div>
            <StatusBadge status={LEVEL_TO_STATUS[d.level]}>{d.level}</StatusBadge>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="zpots-card p-5 min-h-[260px] flex flex-col">
          <h3 className="font-semibold">No-Show Risk Analysis ⚠️</h3>
          <Eyebrow style={{ color: '#b02500' }}>PRIORITY: HIGH INTERVENTION</Eyebrow>
          <div className="zpots-card-surface mt-3 p-3 flex justify-between">
            <span>Probable No-Shows</span>
            <span className="font-display text-base">12% <span className="text-xs text-red-700">(+4% WoW)</span></span>
          </div>
          <div className="zpots-card-surface mt-2 p-3 flex-1">
            <Eyebrow>PRIMARY ROOT CAUSE</Eyebrow>
            <div className="text-sm mt-1">Traffic delays on Rama IV during rain predicted (70% probability).</div>
          </div>
        </div>
        <div className="zpots-card-surface p-5 min-h-[260px] flex flex-col">
          <h3 className="font-semibold">AI Mitigation Strategies</h3>
          <div className="flex gap-3 flex-1 mt-3">
            <div className="zpots-card p-3 flex-1">
              <h4 className="text-sm font-bold">Smart Reschedule</h4>
              <p className="text-xs text-zpots-muted leading-snug mt-1">Auto-offer 15-min delay window to users in high-traffic zones.</p>
              <Eyebrow style={{ color: '#506300' }}>+23% RETENTION</Eyebrow>
            </div>
            <div className="zpots-card p-3 flex-1">
              <h4 className="text-sm font-bold">Pre-Check Deposit</h4>
              <p className="text-xs text-zpots-muted leading-snug mt-1">20% commitment fee for high-demand Saturday slots.</p>
              <Eyebrow style={{ color: '#506300' }}>-60% NO-SHOWS</Eyebrow>
            </div>
          </div>
          <Button variant="primary" className="w-full justify-center mt-3">Execute All</Button>
        </div>
      </div>
    </div>
  );
}
```

If `Eyebrow style={{...}}` doesn't compile, swap those two lines for raw `<span className="font-eyebrow ..." style={{color: ...}}>...</span>` like in Task 10.

- [ ] **Step 3: Build + smoke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Open `/owner/insights`. Click Generate AI Summary — mock text appears. Heatmap renders as a 7×16 colored grid. Three district cards show. No-show + mitigation cards equal height.

- [ ] **Step 4: Commit.**

```bash
git add apps/web/components/owner/DemandHeatmap.tsx apps/web/app/owner/insights/page.tsx
git commit -m "feat(web): AI insights page + DemandHeatmap component

Pure CSS-grid 7×16 heatmap (no chart library). Generate AI Summary
shows seeded mock text — real call lands in Phase 3b. Peak utilization
bars + 3 district cards + no-show risk + mitigation strategies."
```

---

## Task 12: Optimization + OpportunityCard

**Files:**
- Create: `apps/web/components/owner/OpportunityCard.tsx`
- Create: `apps/web/app/owner/optimization/page.tsx`

- [ ] **Step 1: Create `apps/web/components/owner/OpportunityCard.tsx`:**

```tsx
import { Button } from '@/components/Button';
import { AITag, Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

type Props = {
  headlineHtml: string;
  body: string;
  revenueLift: string;
  outcomes: { weeklyEarnings: number; delta: number; occupancyRate: number; occupancyDelta: number };
};

export function OpportunityCard({ headlineHtml, body, revenueLift, outcomes }: Props) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-5">
      <div className="zpots-card p-6">
        <AITag>LIVE OPPORTUNITY</AITag>
        <h2 className="font-display text-3xl font-bold mt-2" dangerouslySetInnerHTML={{ __html: headlineHtml }} />
        <div className="font-display text-5xl font-bold text-zpots-moss mt-3">{revenueLift}</div>
        <Eyebrow>REVENUE LIFT</Eyebrow>

        <div className="zpots-card-surface p-3 mt-4">
          <p className="text-sm">{body}</p>
        </div>
        <div className="flex gap-2 mt-4">
          <Button variant="primary" icon="check_circle">Adjust Slots Now</Button>
          <Button variant="secondary">Dismiss Insight</Button>
        </div>
      </div>

      <div className="zpots-card-lime p-5">
        <Eyebrow style={{ color: '#1a2600' }}>PREDICTED OUTCOMES</Eyebrow>
        <div className="mt-3">
          <div className="text-xs" style={{ color: '#1a2600' }}>WEEKLY EARNINGS</div>
          <div className="font-display text-3xl font-bold flex items-baseline gap-2" style={{ color: '#1a2600' }}>
            {formatPrice(outcomes.weeklyEarnings)}
            <span className="text-xs">+{formatPrice(outcomes.delta)}</span>
          </div>
        </div>
        <div className="mt-4">
          <div className="text-xs" style={{ color: '#1a2600' }}>OCCUPANCY RATE</div>
          <div className="font-display text-3xl font-bold flex items-baseline gap-2" style={{ color: '#1a2600' }}>
            {outcomes.occupancyRate}%
            <span className="text-xs">↑ {outcomes.occupancyDelta}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create `apps/web/app/owner/optimization/page.tsx`:**

```tsx
import { OpportunityCard } from '@/components/owner/OpportunityCard';
import { Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

export default function OptimizationPage() {
  return (
    <div className="flex flex-col gap-5">
      <div>
        <h1 className="font-display text-3xl font-bold">Optimization Engine</h1>
        <Eyebrow>AI OPS · PRIORITY INSIGHT</Eyebrow>
      </div>

      <OpportunityCard
        headlineHtml='Open up <em>Friday 21:00</em> to capture <strong>+80% demand</strong>.'
        body='Data from the last 4 weeks shows a consistent search spike for Sunday 8:00 AM – 11:00 AM. Currently, your slots are locked for club training. Releasing 3 courts will likely fill within 12 hours.'
        revenueLift='+80%'
        outcomes={{ weeklyEarnings: 1420, delta: 204, occupancyRate: 92, occupancyDelta: 8 }}
      />

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="zpots-card p-4">
          <Eyebrow>MARKET BENCHMARK</Eyebrow>
          <p className="text-sm text-zpots-muted mt-2">
            Similar venues in your area are pricing Sunday mornings at <strong>{formatPrice(45)}/hr</strong>.
          </p>
          <div className="text-sm mt-1">Your: <strong>{formatPrice(38)}/hr</strong></div>
        </div>
        <div className="zpots-card p-4">
          <Eyebrow>USER LOYALTY</Eyebrow>
          <p className="text-sm text-zpots-muted mt-2">
            Weekend users are <strong>3.5x</strong> more likely to book a recurring monthly slot.
          </p>
          <div className="text-sm mt-1">High LTV potential</div>
        </div>
        <div className="zpots-card p-4">
          <Eyebrow>LEAD TIME</Eyebrow>
          <p className="text-sm text-zpots-muted mt-2">
            Users are searching for Sunday slots as early as <strong>Wednesday evening</strong>.
          </p>
          <div className="text-sm mt-1 text-zpots-moss">Optimize now →</div>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Build + smoke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Open `/owner/optimization`. Opportunity card with lime predicted-outcomes side card. 3 benchmark cards below.

- [ ] **Step 4: Commit.**

```bash
git add apps/web/components/owner/OpportunityCard.tsx apps/web/app/owner/optimization/page.tsx
git commit -m "feat(web): optimization page + OpportunityCard component"
```

---

## Task 13: Playwright owner-flow E2E

**Files:**
- Create: `apps/web/tests/owner-flow.spec.ts`

- [ ] **Step 1: Create `apps/web/tests/owner-flow.spec.ts`:**

```ts
import { test, expect } from '@playwright/test';

test('owner can sign in and navigate the sidebar', async ({ page }) => {
  // Landing → Enter as Owner
  await page.goto('/');
  await page.getByRole('button', { name: /Enter as Owner/i }).click();
  await expect(page).toHaveURL(/\/owner-login$/);

  // Submit login (prefilled creds)
  await page.getByRole('button', { name: /ENTER CONSOLE/i }).click();
  await expect(page).toHaveURL(/\/owner$/);

  // Dashboard heading
  await expect(page.getByRole('heading', { name: /Venue Performance/i })).toBeVisible();

  // Sidebar items
  for (const [linkLabel, expectedHeading] of [
    ['Venue Manager', /Manage Courts/i],
    ['Slot Control',  /Slot Control/i],
    ['Pricing',       /Pricing Setup/i],
    ['Bookings',      /^Bookings$/i],
    ['AI Insights',   /AI Insights/i],
    ['Optimization',  /Optimization Engine/i],
  ] as const) {
    await page.getByRole('link', { name: linkLabel }).click();
    await expect(page.getByRole('heading', { name: expectedHeading })).toBeVisible();
  }
});
```

- [ ] **Step 2: Run all Playwright tests.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web
lsof -ti :3000 | xargs kill -9 2>/dev/null || true
pnpm test
```

Expected: 3 passed (`landing.spec.ts`, `player-flow.spec.ts`, `owner-flow.spec.ts`).

- [ ] **Step 3: Commit.**

```bash
git add apps/web/tests/owner-flow.spec.ts
git commit -m "test(web): Playwright E2E for owner flow

Landing -> owner login -> dashboard -> click each sidebar item and
assert the destination page's heading renders. ~7 assertions."
```

---

## Task 14: Final smoke + PR open

- [ ] **Step 1: All automated checks.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
conda run -n MADT pytest tests/ -q

cd apps/web
pnpm test:unit
pnpm build
lsof -ti :3000 | xargs kill -9 2>/dev/null || true
pnpm test
```

Expected: Streamlit 29 passed, Vitest 31+ passed, Next.js build clean (~22 routes), Playwright 3 passed.

- [ ] **Step 2: Manual browser smoke.**

```bash
cd apps/web && pnpm dev
```

Walk through in Chrome:
1. `http://localhost:3000` → Enter as Owner → owner-login → ENTER CONSOLE → /owner
2. Click each sidebar item: Dashboard / Venue Manager / Slot Control / Pricing / Bookings / AI Insights / Optimization
3. On /owner/venues, switch GRID ↔ LIST via the chips
4. On /owner/insights, click Generate AI Summary — mock text appears
5. On /owner/venues, click Edit Court on bbc-01 → land on `/owner/venues/bbc-01/edit` → form prefilled
6. Click "Add New Court" in sidebar → `/owner/venues/new` → empty form
7. Logout (Back to home in sidebar) → land on /

- [ ] **Step 3: Confirm Streamlit at the root still runs.**

```bash
# Another terminal
cd /Users/nchawanp/Desktop/ZPOTS
conda run -n MADT streamlit run app.py
```

Open http://localhost:8501 — original Streamlit landing renders.

- [ ] **Step 4: Push + PR.**

```bash
git push -u origin feat/nextjs-phase3a
gh pr create --base main --title "Phase 3a: owner UI with mock data" --body-file ...
```

PR body must include:
- Link to spec and this plan
- Test counts (Streamlit 29, Vitest 31+, Playwright 3)
- Note that 3b (FastAPI + AI endpoints) and 3c (chat) follow
- Confirmation that Streamlit still runs unchanged

---

## Out of scope for Phase 3a (do NOT add)

- FastAPI scaffold or any real API call — Phase 3b
- Live AI calls — Phase 3b
- Chat widget — Phase 3c
- Real CRUD writes from any owner form — Phase 4
- NextAuth — Phase 4
- Postgres — Phase 4
- Mobile responsive polish beyond Tailwind defaults
- Replacing emoji placeholders with real photography
- Cancel-from-bookings or owner-side player-booking edits
