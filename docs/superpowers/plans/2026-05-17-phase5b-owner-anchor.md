# Phase 5b — Owner Dashboard Anchor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Autonomous execution per [[feedback-design-revamp-autonomy]] — proceed without per-task user approval; ship and continue.

**Goal:** Transform `/owner`, `/owner/insights`, `/owner/bookings` into the KP+Motion anchor surfaces using the 5a primitives.

**Architecture:** Three new composite components (`PageHero`, `KpiPill`, `TabStrip`) plus targeted page rewrites. Existing supporting components (KpiCard, UtilizationBars, RevenueBanner) upgrade in place — keep their APIs so 5c pages stay green.

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase5b-owner-anchor-design.md`
**Branch:** `feat/nextjs-phase5b` off main

---

## Task 0: Branch + baseline

- [ ] `git checkout main && git pull && git checkout -b feat/nextjs-phase5b`
- [ ] Vitest baseline from `apps/web`: `pnpm test:unit` → **39 passed**
- [ ] `pnpm build` → clean

---

## Task 1: PageHero + KpiPill + TabStrip primitives

**Files:**
- Create: `apps/web/components/primitives/PageHero.tsx`
- Create: `apps/web/components/primitives/KpiPill.tsx`
- Create: `apps/web/components/primitives/TabStrip.tsx`
- Create: `apps/web/tests/PageHero.test.tsx`
- Create: `apps/web/tests/TabStrip.test.tsx`

- [ ] **Step 1: Write tests** at `apps/web/tests/PageHero.test.tsx`:

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { PageHero } from '@/components/primitives/PageHero';

describe('PageHero', () => {
  it('renders eyebrow + headline + sub', () => {
    render(
      <PageHero eyebrow="LIVE" headline="128 bookings" sub="great day" />
    );
    expect(screen.getByText('LIVE')).toBeInTheDocument();
    expect(screen.getByText('128 bookings')).toBeInTheDocument();
    expect(screen.getByText('great day')).toBeInTheDocument();
  });

  it('renders the optional CTA slot', () => {
    render(
      <PageHero
        eyebrow="x"
        headline="y"
        sub="z"
        cta={<button>Add Court</button>}
      />
    );
    expect(screen.getByText('Add Court')).toBeInTheDocument();
  });
});
```

and `apps/web/tests/TabStrip.test.tsx`:

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TabStrip } from '@/components/primitives/TabStrip';

describe('TabStrip', () => {
  it('renders all tabs and marks active with aria-selected', () => {
    render(
      <TabStrip
        active="utilization"
        onChange={() => {}}
        tabs={[
          { key: 'utilization', label: 'UTILIZATION ↗' },
          { key: 'revenue', label: 'REVENUE' },
        ]}
      />
    );
    const active = screen.getByText('UTILIZATION ↗').closest('button');
    expect(active).toHaveAttribute('aria-selected', 'true');
  });

  it('calls onChange when a tab is clicked', () => {
    const onChange = vi.fn();
    render(
      <TabStrip
        active="a"
        onChange={onChange}
        tabs={[
          { key: 'a', label: 'A' },
          { key: 'b', label: 'B' },
        ]}
      />
    );
    fireEvent.click(screen.getByText('B'));
    expect(onChange).toHaveBeenCalledWith('b');
  });
});
```

- [ ] **Step 2: Create `apps/web/components/primitives/PageHero.tsx`:**

```tsx
import React from 'react';
import { DarkHero } from './DarkHero';

type Props = {
  eyebrow: React.ReactNode;
  headline: React.ReactNode;
  sub?: React.ReactNode;
  cta?: React.ReactNode;
  className?: string;
};

/**
 * Page-level hero with KP-style structure: eyebrow date stamp, big headline,
 * optional sub-line, optional right-aligned CTA. Wraps DarkHero.
 */
export function PageHero({ eyebrow, headline, sub, cta, className = '' }: Props) {
  return (
    <DarkHero glow="lime" className={`px-6 md:px-8 py-8 md:py-10 ${className}`}>
      <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
        <div className="flex-1 min-w-0">
          <div className="text-label-sm text-lime/70 mb-2">{eyebrow}</div>
          <h1 className="font-geist font-bold text-display-md md:text-display-lg text-white leading-none tracking-tight">
            {headline}
          </h1>
          {sub && (
            <p className="mt-3 text-body-sm md:text-body-md text-white/60 max-w-2xl">
              {sub}
            </p>
          )}
        </div>
        {cta && <div className="flex-shrink-0">{cta}</div>}
      </div>
    </DarkHero>
  );
}
```

- [ ] **Step 3: Create `apps/web/components/primitives/KpiPill.tsx`:**

```tsx
import React from 'react';

type Props = {
  label: string;
  value: React.ReactNode;
  className?: string;
};

/**
 * Compact KPI for the dark hero's right side or anywhere a small lime-on-ink
 * data chip is needed.
 */
export function KpiPill({ label, value, className = '' }: Props) {
  return (
    <div className={`inline-flex flex-col gap-0.5 px-3 py-2 bg-ink-800 rounded-kp-chip ${className}`}>
      <span className="text-label-sm text-white/50">{label}</span>
      <span className="font-geist-mono text-body-md text-lime tabular-nums">{value}</span>
    </div>
  );
}
```

- [ ] **Step 4: Create `apps/web/components/primitives/TabStrip.tsx`:**

```tsx
'use client';
import React from 'react';

type Tab = { key: string; label: React.ReactNode };

type Props = {
  active: string;
  tabs: Tab[];
  onChange: (key: string) => void;
  className?: string;
};

/**
 * Pill-tab strip — lime fill on active, neutral text on inactive.
 * Used by the dashboard's UTIL / REVENUE / NO-SHOW selector.
 */
export function TabStrip({ active, tabs, onChange, className = '' }: Props) {
  return (
    <div role="tablist" className={`flex flex-wrap gap-2 ${className}`}>
      {tabs.map((t) => {
        const isActive = t.key === active;
        return (
          <button
            key={t.key}
            type="button"
            role="tab"
            aria-selected={isActive}
            onClick={() => onChange(t.key)}
            className={[
              'px-4 py-2 rounded-kp-pill text-label-sm font-geist transition-colors duration-quick ease-precision focus-ring',
              isActive
                ? 'bg-lime text-ink-900 font-semibold'
                : 'bg-surface-low text-ink-700 hover:bg-surface-med',
            ].join(' ')}
          >
            {t.label}
          </button>
        );
      })}
    </div>
  );
}
```

- [ ] **Step 5:** `pnpm test:unit` → **43 passed** (39 + 4 new)
- [ ] **Step 6:** Commit:
```
git add apps/web/components/primitives/PageHero.tsx apps/web/components/primitives/KpiPill.tsx apps/web/components/primitives/TabStrip.tsx apps/web/tests/PageHero.test.tsx apps/web/tests/TabStrip.test.tsx
git commit -m "feat(web): PageHero + KpiPill + TabStrip primitives"
```

---

## Task 2: Transform `/owner` dashboard

**Files:**
- Modify: `apps/web/app/owner/page.tsx`

- [ ] **Step 1: Replace `apps/web/app/owner/page.tsx`:**

```tsx
'use client';
import { useState } from 'react';
import Link from 'next/link';

import { PageHero } from '@/components/primitives/PageHero';
import { TabStrip } from '@/components/primitives/TabStrip';
import { NumberFlip } from '@/components/primitives/NumberFlip';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { PulseAccent } from '@/components/primitives/PulseAccent';
import { DarkHero } from '@/components/primitives/DarkHero';
import { UtilizationBars } from '@/components/charts/UtilizationBars';
import { StatusBadge } from '@/components/Tags';
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

const TODAY_LABEL = new Date().toLocaleDateString('en-US', {
  weekday: 'short',
  month: 'short',
  day: 'numeric',
}).toUpperCase();

export default function OwnerDashboard() {
  const [tab, setTab] = useState('utilization');

  const utilizationData = Object.fromEntries(
    WEEKLY_UTILIZATION.map((w) => [w.day, w.pct])
  );

  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow={`LIVE · ${TODAY_LABEL}`}
        headline={
          <>
            <NumberFlip value={128} /> bookings.<br />
            <span className="text-lime"><NumberFlip value={64500} className="!font-geist font-bold" />฿</span>
          </>
        }
        sub={`Welcome back, ${currentOwner.name}. Court 3 is your top performer — 92% utilization this week.`}
        cta={
          <Link
            href="/owner/venues/new"
            className="inline-flex items-center gap-2 px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
          >
            + Add Court
          </Link>
        }
      />

      <TabStrip
        active={tab}
        onChange={setTab}
        tabs={[
          { key: 'utilization', label: 'UTILIZATION ↗ +12%' },
          { key: 'revenue', label: 'REVENUE' },
          { key: 'noshow', label: 'NO-SHOW RISK' },
        ]}
      />

      <RevealOnScroll>
        <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-5">
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">Utilization Trends</h3>
            <p className="text-label-sm text-ink-700/60 mt-1">Past 7 days · hourly rollup</p>
            <div className="mt-4">
              <UtilizationBars data={utilizationData} />
            </div>
          </div>

          <DarkHero glow="lime" className="p-5 flex flex-col gap-3">
            <span className="text-label-sm text-lime/70">AI REVENUE OPTIMIZER</span>
            <h3 className="font-geist font-bold text-title-lg text-white leading-tight">
              ▲ Raise Friday 18–21h pricing by 18%
            </h3>
            <p className="text-body-sm text-white/60">
              Expected impact: <span className="text-lime font-geist-mono">+฿2,400/wk</span>
            </p>
            <PulseAccent className="mt-auto self-start">
              <button className="px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring">
                Approve →
              </button>
            </PulseAccent>
          </DarkHero>
        </div>
      </RevealOnScroll>

      <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-5">
        <div>
          <h3 className="font-geist font-semibold text-title-md text-ink-900 mb-3">Today&apos;s Bookings</h3>
          <div className="flex flex-col gap-2">
            {TODAYS_BOOKINGS.map((b, i) => (
              <RevealOnScroll key={b.title} delay={i * 80}>
                <div className="bg-white rounded-kp-card shadow-float p-4 flex items-center gap-5">
                  <div className="w-20 flex-shrink-0">
                    <div className="font-geist-mono text-display-md text-ink-900 tabular-nums leading-none">
                      {b.time}
                    </div>
                    <div className="text-label-sm text-ink-700/60 mt-1">{b.type}</div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-geist font-semibold text-body-md text-ink-900 truncate">{b.title}</div>
                    <div className="text-body-sm text-ink-700/60 truncate">
                      {b.customer} · {b.venue}
                    </div>
                  </div>
                  <StatusBadge status={STATUS_VARIANT[b.status] ?? 'confirmed'}>{b.status}</StatusBadge>
                </div>
              </RevealOnScroll>
            ))}
          </div>
          <Link
            href="/owner/bookings"
            className="inline-block mt-4 text-body-sm text-ink-700 hover:text-ink-900 underline-offset-4 hover:underline"
          >
            View all bookings →
          </Link>
        </div>

        <div>
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">Manage Venues</h3>
            <span className="text-label-sm text-ink-700/60">{OWNER_VENUES.length} LOCATIONS</span>
          </div>
          <div className="flex flex-col gap-2">
            {OWNER_VENUES.map((v, i) => (
              <RevealOnScroll key={v.id} delay={i * 60}>
                <div className="bg-white rounded-kp-card shadow-float flex items-stretch overflow-hidden min-h-[68px]">
                  <div className="w-1.5" style={{ background: `linear-gradient(180deg,${v.color},${v.color}cc)` }} />
                  <div className="flex-1 p-3">
                    <div className="text-body-sm font-geist font-semibold text-ink-900">{v.name}</div>
                    <div className="text-label-sm text-ink-700/60 mt-0.5">{v.location}</div>
                    <div className="flex justify-between items-baseline text-body-sm mt-2">
                      <span className="text-ink-700/60">{v.courts_count} courts</span>
                      <span className="font-geist-mono text-lime-deep tabular-nums">
                        {formatPrice(v.revenue_today)}
                      </span>
                    </div>
                  </div>
                </div>
              </RevealOnScroll>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2:** `pnpm build` → clean
- [ ] **Step 3:** Commit: `feat(web): transform owner dashboard with KP+Motion (DarkHero, NumberFlip, PulseAccent, RevealOnScroll)`

---

## Task 3: Transform `/owner/insights`

**Files:**
- Modify: `apps/web/app/owner/insights/page.tsx`

- [ ] **Step 1: Replace the file. Keep all data-fetching logic; rewrite the JSX to use PageHero + new card style.** Final code:

```tsx
'use client';
import { useEffect, useState } from 'react';
import Markdown from 'react-markdown';

import { PageHero } from '@/components/primitives/PageHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { AITag, Eyebrow, StatusBadge } from '@/components/Tags';
import { DemandHeatmap } from '@/components/owner/DemandHeatmap';
import {
  DEMAND_FORECAST, DISTRICT_DEMAND, PEAK_UTILIZATION_BARS,
  WEEKLY_UTILIZATION, OWNER_BOOKINGS,
} from '@/lib/owner-mock-data';
import { aiInsights, mlDemandForecast } from '@/lib/api-client';
import type { DemandCell } from '@/lib/owner-mock-data';

const LEVEL_TO_STATUS: Record<string, 'confirmed' | 'progress' | 'cancelled'> = {
  Peak: 'confirmed', Moderate: 'progress', Saturated: 'cancelled',
};

export default function InsightsPage() {
  const [summary, setSummary] = useState('');
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [heatmap, setHeatmap] = useState<DemandCell[]>(DEMAND_FORECAST);
  const [heatmapFromApi, setHeatmapFromApi] = useState(false);

  useEffect(() => {
    mlDemandForecast()
      .then((res) => {
        if (res.cells.length > 0) {
          setHeatmap(res.cells);
          setHeatmapFromApi(true);
        }
      })
      .catch(() => { /* keep mock fallback */ });
  }, []);

  async function generate() {
    setSummaryLoading(true);
    setSummaryError(null);
    try {
      const weekly_utilization = Object.fromEntries(
        WEEKLY_UTILIZATION.map((w) => [w.day, w.pct]),
      );
      const res = await aiInsights({
        weekly_utilization,
        district_demand: DISTRICT_DEMAND,
        owner_bookings: OWNER_BOOKINGS.map((b) => ({
          customer: b.customer, sport: b.sport, status: b.status,
        })),
      });
      setSummary(res.markdown);
    } catch (e) {
      setSummaryError('Could not generate summary. Is the API running?');
    } finally {
      setSummaryLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-5">
      <PageHero
        eyebrow="AI INSIGHTS · 7-DAY FORECAST"
        headline="Bangkok demand intelligence."
        sub="Live signals from your venues + our models, fused. Generate the summary on demand or browse the heatmap below."
        cta={
          <div className="flex gap-2">
            <button
              type="button"
              onClick={generate}
              disabled={summaryLoading}
              className="px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring disabled:opacity-60"
            >
              {summaryLoading ? 'Generating…' : 'Generate AI Summary'}
            </button>
            <button
              type="button"
              onClick={() => setSummary('')}
              className="px-5 py-3 bg-white/10 text-white font-geist font-semibold text-body-sm rounded-kp-pill hover:bg-white/15 transition-colors duration-quick focus-ring"
            >
              Clear
            </button>
          </div>
        }
      />

      {summaryError && (
        <div className="bg-white rounded-kp-card shadow-float p-3 text-body-sm text-red-700">
          {summaryError}
        </div>
      )}

      {summary && (
        <RevealOnScroll>
          <div className="bg-surface-low rounded-kp-card p-5">
            <AITag>AI GENERATED SUMMARY</AITag>
            <div className="mt-2 text-body-sm leading-relaxed prose prose-sm max-w-none">
              <Markdown>{summary}</Markdown>
            </div>
          </div>
        </RevealOnScroll>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <RevealOnScroll>
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">Bangkok Demand Heatmap</h3>
            <Eyebrow>
              {heatmapFromApi ? '7-DAY FORECAST · LIVE FROM MODEL' : '7-DAY FORECAST · CACHED'}
            </Eyebrow>
            <div className="mt-3">
              <DemandHeatmap data={heatmap} />
            </div>
          </div>
        </RevealOnScroll>
        <RevealOnScroll delay={80}>
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">Peak Utilization</h3>
            <Eyebrow>HOURLY DISTRIBUTION</Eyebrow>
            <div className="flex items-end gap-[3px] h-24 mt-3">
              {PEAK_UTILIZATION_BARS.map((v, i) => (
                <div
                  key={i}
                  className="flex-1 rounded-t"
                  style={{
                    height: `${v}%`,
                    background: v > 80 ? '#cffc00' : v > 50 ? '#506300' : '#A5D6A7',
                  }}
                />
              ))}
            </div>
            <div className="mt-3 bg-surface-low rounded-kp-card p-3 flex justify-between items-center">
              <div className="text-body-sm">
                <span className="text-lime">⚡</span> <strong>Golden Slot</strong>
              </div>
              <span className="font-geist-mono text-lime-deep font-bold">฿2,400/hr</span>
            </div>
          </div>
        </RevealOnScroll>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {DISTRICT_DEMAND.map((d, i) => (
          <RevealOnScroll key={d.name} delay={i * 60}>
            <div className="bg-surface-low rounded-kp-card p-4 text-center">
              <Eyebrow>{d.name}</Eyebrow>
              <div className="font-geist-mono font-bold text-display-md text-ink-900 my-1 tabular-nums">
                {d.demand}%
              </div>
              <StatusBadge status={LEVEL_TO_STATUS[d.level]}>{d.level}</StatusBadge>
            </div>
          </RevealOnScroll>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <RevealOnScroll>
          <div className="bg-white rounded-kp-card shadow-float p-5 min-h-[260px] flex flex-col">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">No-Show Risk Analysis ⚠️</h3>
            <span className="text-label-sm text-red-700 mt-1">
              PRIORITY: HIGH INTERVENTION
            </span>
            <div className="bg-surface-low rounded-kp-card mt-3 p-3 flex justify-between items-center">
              <span className="text-body-sm">Probable No-Shows</span>
              <span className="font-geist-mono text-body-md text-ink-900">
                12% <span className="text-body-sm text-red-700">(+4% WoW)</span>
              </span>
            </div>
            <div className="bg-surface-low rounded-kp-card mt-2 p-3 flex-1">
              <Eyebrow>PRIMARY ROOT CAUSE</Eyebrow>
              <div className="text-body-sm text-ink-700 mt-1">
                Traffic delays on Rama IV during rain predicted (70% probability).
              </div>
            </div>
          </div>
        </RevealOnScroll>
        <RevealOnScroll delay={80}>
          <div className="bg-surface-low rounded-kp-card p-5 min-h-[260px] flex flex-col">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">AI Mitigation Strategies</h3>
            <div className="flex gap-3 flex-1 mt-3">
              <div className="bg-white rounded-kp-card shadow-float p-3 flex-1">
                <h4 className="text-body-sm font-geist font-bold">Smart Reschedule</h4>
                <p className="text-body-sm text-ink-700/60 leading-snug mt-1">
                  Auto-offer 15-min delay window to users in high-traffic zones.
                </p>
                <span className="text-label-sm text-lime-deep mt-2 inline-block">+23% RETENTION</span>
              </div>
              <div className="bg-white rounded-kp-card shadow-float p-3 flex-1">
                <h4 className="text-body-sm font-geist font-bold">Pre-Check Deposit</h4>
                <p className="text-body-sm text-ink-700/60 leading-snug mt-1">
                  20% commitment fee for high-demand Saturday slots.
                </p>
                <span className="text-label-sm text-lime-deep mt-2 inline-block">-60% NO-SHOWS</span>
              </div>
            </div>
            <button
              type="button"
              className="w-full mt-3 px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
            >
              Execute All
            </button>
          </div>
        </RevealOnScroll>
      </div>
    </div>
  );
}
```

- [ ] **Step 2:** `pnpm build` → clean
- [ ] **Step 3:** Commit: `feat(web): transform owner insights with PageHero + new card style`

---

## Task 4: Transform `/owner/bookings`

**Files:**
- Modify: `apps/web/app/owner/bookings/page.tsx`

- [ ] **Step 1: Replace the file:**

```tsx
'use client';
import { useEffect, useState } from 'react';

import { PageHero } from '@/components/primitives/PageHero';
import { NumberFlip } from '@/components/primitives/NumberFlip';
import { KpiPill } from '@/components/primitives/KpiPill';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { TabStrip } from '@/components/primitives/TabStrip';
import { StatusBadge, Eyebrow } from '@/components/Tags';
import { OWNER_BOOKINGS } from '@/lib/owner-mock-data';
import { mlNoshowRiskBatch } from '@/lib/api-client';
import type { NoShowRiskResult } from '@/lib/api-types';

const STATUS_TO_VARIANT: Record<string, 'confirmed' | 'completed' | 'cancelled'> = {
  BOOKED: 'confirmed',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
};

const TIER_TO_VARIANT: Record<string, 'confirmed' | 'progress' | 'cancelled'> = {
  Low: 'confirmed', Medium: 'progress', High: 'cancelled',
};

const SPORT_TO_DISTRICT: Record<string, string> = {
  Padel: 'Sukhumvit', Tennis: 'Pathumwan', Soccer: 'Thong Lor', Yoga: 'Ari',
};

function parseHour(time: string): number {
  const m = /^(\d{2}):/.exec(time);
  return m ? parseInt(m[1], 10) : 18;
}

const TODAY_LABEL = new Date().toLocaleDateString('en-US', {
  weekday: 'short',
  month: 'short',
  day: 'numeric',
}).toUpperCase();

export default function BookingDashboardPage() {
  const [risks, setRisks] = useState<NoShowRiskResult[] | null>(null);
  const [range, setRange] = useState('today');

  useEffect(() => {
    mlNoshowRiskBatch({
      items: OWNER_BOOKINGS.map((b) => ({
        sport: b.sport,
        district: SPORT_TO_DISTRICT[b.sport] ?? 'Sukhumvit',
        hour: parseHour(b.time),
      })),
    })
      .then((res) => setRisks(res.results))
      .catch(() => setRisks(null));
  }, []);

  return (
    <div className="flex flex-col gap-5">
      <PageHero
        eyebrow={`TODAY · ${TODAY_LABEL}`}
        headline={
          <>
            <span className="text-lime">฿</span>
            <NumberFlip value={4280} />
          </>
        }
        sub="+15.6% from yesterday · 12 upcoming sessions"
        cta={
          <div className="flex flex-wrap gap-2">
            <KpiPill label="MAIN ARENA" value="฿1,240" />
            <KpiPill label="PADEL POD 2" value="฿890" />
            <KpiPill label="INDOOR TURF" value="฿2,150" />
          </div>
        }
      />

      <TabStrip
        active={range}
        onChange={setRange}
        tabs={[
          { key: 'today', label: 'Today' },
          { key: 'week',  label: 'This Week' },
          { key: 'cal',   label: 'Calendar' },
        ]}
      />

      <div className="grid grid-cols-2 gap-3">
        <select className="field-input">
          <option>All Venues</option>
          <option>Main Arena</option>
          <option>Padel Pod 2</option>
          <option>Indoor Turf</option>
        </select>
        <select className="field-input">
          <option>Time Descending</option>
          <option>Time Ascending</option>
          <option>Status</option>
        </select>
      </div>

      <div className="grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 px-4">
        <Eyebrow>Customer</Eyebrow>
        <Eyebrow>Session info</Eyebrow>
        <Eyebrow>Status</Eyebrow>
        <Eyebrow>Risk</Eyebrow>
      </div>

      <div className="flex flex-col gap-2">
        {OWNER_BOOKINGS.map((b, i) => {
          const risk = risks?.[i];
          return (
            <RevealOnScroll key={b.member_id} delay={i * 40}>
              <div className="bg-white rounded-kp-card shadow-float grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 items-center p-3">
                <div className="flex items-center gap-3 min-w-0">
                  <div
                    className="w-9 h-9 rounded-kp-pill text-white flex items-center justify-center font-geist font-semibold flex-shrink-0"
                    style={{ background: b.avatar_color }}
                  >
                    {b.customer[0]}
                  </div>
                  <div className="min-w-0">
                    <div className="font-geist font-semibold text-body-md text-ink-900 truncate">{b.customer}</div>
                    <div className="text-label-sm text-ink-700/60">ID: {b.member_id}</div>
                  </div>
                </div>
                <div className="min-w-0">
                  <div className="text-body-md text-ink-900 truncate">🏟 {b.court} • {b.sport}</div>
                  <div className="text-body-sm text-ink-700/60">🕐 {b.time}</div>
                </div>
                <StatusBadge status={STATUS_TO_VARIANT[b.status] ?? 'confirmed'}>{b.status}</StatusBadge>
                {risk ? (
                  <StatusBadge status={TIER_TO_VARIANT[risk.tier]}>
                    {risk.tier} ({(risk.probability * 100).toFixed(0)}%)
                  </StatusBadge>
                ) : (
                  <span className="text-body-sm text-ink-700/60">—</span>
                )}
              </div>
            </RevealOnScroll>
          );
        })}
      </div>

      <div className="text-label-sm text-ink-700/60 text-center">
        SHOWING {OWNER_BOOKINGS.length} BOOKINGS · seeded demo data
      </div>
    </div>
  );
}
```

- [ ] **Step 2:** `pnpm build` → clean
- [ ] **Step 3:** Commit: `feat(web): transform owner bookings page (PageHero + NumberFlip + KpiPill)`

---

## Task 5: Upgrade UtilizationBars to lime gradient

**Files:**
- Modify: `apps/web/components/charts/UtilizationBars.tsx`

The dashboard's chart card needs gradient bars instead of flat color, and a subtle on-mount reveal.

- [ ] **Step 1: Read the existing file** — it's small. The change: bars get `bg-gradient-to-t from-lime-press to-lime` and a CSS scale-y reveal on mount.

```bash
cat /Users/nchawanp/Desktop/ZPOTS/apps/web/components/charts/UtilizationBars.tsx
```

- [ ] **Step 2: Update the bars' className and style.** Wherever the bar `<div>` is rendered, change the background to:
```ts
background: 'linear-gradient(180deg, #cffc00 0%, #b8e600 100%)'
```
and add a CSS keyframe `bar-rise` that does `transform: scaleY(0)` → `scaleY(1)` over 360ms with `transform-origin: bottom`. Stagger via `animation-delay: ${i * 40}ms`.

The implementer should make this judgment based on the actual file structure. Keep the component API unchanged.

- [ ] **Step 3:** `pnpm build` → clean
- [ ] **Step 4:** Commit: `feat(web): UtilizationBars lime-gradient + staggered scale-y reveal`

---

## Task 6: Update Playwright owner-flow selectors

**Files:**
- Modify: `apps/web/tests/owner-flow.spec.ts`

The dashboard DOM changed (no more `font-display text-3xl` heading; now a `<PageHero>` with the date eyebrow). Selectors that target the old heading text need updates.

- [ ] **Step 1: Read** `apps/web/tests/owner-flow.spec.ts`
- [ ] **Step 2: Update any selector that targeted dashboard header content.** The new dashboard headline includes "bookings" via NumberFlip — selector strategy: use `page.getByText(/bookings\./)` or target a stable element like the "Manage Venues" h3. Avoid asserting on animated numbers (NumberFlip).
- [ ] **Step 3:** `cd apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test 2>&1 | tail -10` → expect **2 passed** (player-flow still pre-existing fail; not our concern in this PR)
- [ ] **Step 4:** Commit: `test(web): update Playwright owner-flow selectors for new dashboard DOM`

---

## Task 7: Final smoke + open PR

- [ ] **Step 1: Run all suites:**
```bash
cd /Users/nchawanp/Desktop/ZPOTS && conda run -n MADT pytest tests/ -q
cd apps/api && conda run -n MADT pytest -q && cd ..
cd apps/web && pnpm test:unit && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```
Expected: Streamlit 29 · FastAPI 53 · Vitest 43 · build clean

- [ ] **Step 2: Manual browser smoke (mental note, not blocking):**
  - `/owner` shows the dark hero with NumberFlip-animated numbers
  - PulseAccent halo on the AI approve button
  - RevealOnScroll fades stagger as you scroll down
  - `/owner/insights` and `/owner/bookings` also have dark heroes
  - All previous pages (player, owner venues/slots/pricing) still render — they still use legacy zpots tokens, that's intended (5c migrates them)

- [ ] **Step 3: Push + PR.**
```bash
git push -u origin feat/nextjs-phase5b
gh pr create --base main --title "Phase 5b: owner anchor (dashboard + insights + bookings)" --body-file /tmp/pr5b-body.md
```

PR body content (write to `/tmp/pr5b-body.md` first):
```markdown
## Summary

Phase 5b — the visual "wow" moment. Owner dashboard, AI insights, and bookings pages transformed to KP+Motion. Each page now opens with a dark hero card (NumberFlip-animated numbers, lime radial glow, noise texture), tabbed pill strips, glass cards with shadow-float, RevealOnScroll staggered entries, and a PulseAccent halo on AI CTAs.

- Spec: `docs/superpowers/specs/2026-05-17-phase5b-owner-anchor-design.md`
- Plan: `docs/superpowers/plans/2026-05-17-phase5b-owner-anchor.md`

## What ships

**New composite primitives:** `PageHero` · `KpiPill` · `TabStrip`

**Three pages transformed:**
- `/owner` — dashboard with DarkHero, NumberFlip on bookings/revenue, lime-gradient chart bars, PulseAccent on AI CTA
- `/owner/insights` — PageHero header, restyled cards using new tokens, RevealOnScroll stagger
- `/owner/bookings` — revenue hero with KpiPill breakdown, TabStrip range selector, restyled table rows

**One supporting component upgraded:** `UtilizationBars` — lime gradient + scale-y reveal.

## Tests

| Suite | Result |
|---|---|
| Streamlit | 29 / 29 ✅ |
| FastAPI | 53 / 53 ✅ |
| Vitest | 43 / 43 ✅ (+4 for PageHero + TabStrip) |
| Playwright | 2 / 3 ⚠️ (player-flow pre-existing fail from 4a, unrelated) |
| `pnpm build` | clean ✅ |

## What's NOT in this PR

- Other owner pages (venues / slots / pricing / optimization) — Phase 5c
- Player pages — Phase 5d
- Chat widget polish — Phase 5e
- Backend changes — none

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

- [ ] **Step 4: Auto-merge per autonomy grant.**
```bash
gh pr merge --merge --delete-branch
git checkout main && git pull
```
