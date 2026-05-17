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
