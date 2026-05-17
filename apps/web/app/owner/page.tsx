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
