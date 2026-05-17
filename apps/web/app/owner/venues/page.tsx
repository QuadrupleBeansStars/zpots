'use client';
import { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { getCourts } from '@/lib/data-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';
import { PageHero } from '@/components/primitives/PageHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

const SPORT_ICON: Record<string, string> = {
  Badminton: '🏸', Football: '⚽', Padel: '🎾', Basketball: '🏀', Tennis: '🎾', Volleyball: '🏐',
};

function VenuesPageInner() {
  const router = useRouter();
  const params = useSearchParams();
  const view = (params.get('view') ?? 'grid').toLowerCase() === 'list' ? 'list' : 'grid';
  const [courts, setCourts] = useState<Court[]>(FALLBACK_COURTS);

  useEffect(() => {
    getCourts().then(setCourts).catch(() => setCourts(FALLBACK_COURTS));
  }, []);

  function setView(v: 'grid' | 'list') {
    const next = new URLSearchParams(params.toString());
    if (v === 'grid') next.delete('view'); else next.set('view', 'list');
    router.push(`/owner/venues?${next.toString()}`);
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow={`MANAGE COURTS · ${courts.length} LOCATIONS`}
        headline="Your court portfolio."
        sub="Real-time performance metrics and availability control across your elite sports facilities."
        cta={
          <Link
            href="/owner/venues/new"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-kp-pill bg-lime text-ink-900 font-geist font-semibold text-label-sm transition-colors duration-quick ease-precision hover:bg-lime/90 focus-ring"
          >
            + Register Venue
          </Link>
        }
      />

      <RevealOnScroll>
        <div className="flex gap-2">
          <button
            onClick={() => setView('grid')}
            className={[
              'px-4 py-2 rounded-kp-pill text-label-sm font-geist transition-colors duration-quick ease-precision focus-ring',
              view === 'grid' ? 'bg-lime text-ink-900 font-semibold' : 'bg-surface-low text-ink-700 hover:bg-surface-med',
            ].join(' ')}
          >GRID</button>
          <button
            onClick={() => setView('list')}
            className={[
              'px-4 py-2 rounded-kp-pill text-label-sm font-geist transition-colors duration-quick ease-precision focus-ring',
              view === 'list' ? 'bg-lime text-ink-900 font-semibold' : 'bg-surface-low text-ink-700 hover:bg-surface-med',
            ].join(' ')}
          >LIST</button>
        </div>
      </RevealOnScroll>

      <RevealOnScroll delay={80}>
        {view === 'grid' ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {courts.map((c) => (
              <div key={c.id} className="bg-white rounded-kp-card shadow-float overflow-hidden">
                <div className="h-40 flex items-center justify-center relative" style={{ background: `linear-gradient(135deg,${c.color},${c.color}cc)` }}>
                  <span className="text-5xl">{SPORT_ICON[c.sport] ?? '🏟'}</span>
                  {/* Inline pill — full-strength lime for readability on dark court hero */}
                  <span
                    className="absolute top-3 left-3 px-3 py-1 rounded-kp-pill font-geist text-[10px] uppercase tracking-wider font-semibold"
                    style={{ background: '#CFFC00', color: '#1E4A00' }}
                  >
                    ● {c.status}
                  </span>
                </div>
                <div className="p-4">
                  <div className="font-geist font-semibold text-body-md text-ink-900">{c.name}</div>
                  <div className="text-label-sm text-ink-700/60">📍 {c.district}, Bangkok</div>
                  <div className="flex gap-6 mt-3">
                    <div>
                      <Eyebrow>Utilization</Eyebrow>
                      <div className="font-geist-mono text-title-md tabular-nums text-ink-900">{c.utilization}%</div>
                    </div>
                    <div>
                      <Eyebrow>Peak hours</Eyebrow>
                      <div className="font-geist-mono text-title-md tabular-nums text-ink-900">{c.peak_hours}</div>
                    </div>
                    <div>
                      <Eyebrow>AI efficiency</Eyebrow>
                      <div className="font-geist-mono text-title-md tabular-nums text-ink-900 italic">{c.ai_efficiency}</div>
                    </div>
                  </div>
                  <Link
                    href={`/owner/venues/${c.id}/edit`}
                    className="block mt-4 w-full text-center px-4 py-2 rounded-kp-pill bg-surface-low text-ink-700 font-geist text-label-sm font-semibold hover:bg-surface-med transition-colors duration-quick ease-precision focus-ring"
                  >
                    Edit Court
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-kp-card shadow-float overflow-hidden">
            <div className="grid grid-cols-[48px_2fr_1fr_1fr_1fr_100px] gap-3 p-3 bg-surface-low">
              <div></div>
              <Eyebrow>Court</Eyebrow>
              <Eyebrow>District</Eyebrow>
              <Eyebrow>Utilization</Eyebrow>
              <Eyebrow>Peak hours</Eyebrow>
              <Eyebrow>Price/hr</Eyebrow>
            </div>
            {courts.map((c, idx) => (
              <div
                key={c.id}
                className={[
                  'grid grid-cols-[48px_2fr_1fr_1fr_1fr_100px] gap-3 p-3 items-center transition-colors duration-quick',
                  idx % 2 === 1 ? 'bg-surface-low/50' : '',
                  'hover:bg-surface-low',
                ].join(' ')}
              >
                <div className="w-9 h-9 rounded-lg flex items-center justify-center text-lg" style={{ background: `linear-gradient(135deg,${c.color},${c.color}cc)` }}>
                  {SPORT_ICON[c.sport] ?? '🏟'}
                </div>
                <div>
                  <div className="font-geist font-semibold text-body-sm text-ink-900">{c.name}</div>
                  <div className="text-label-sm text-ink-700/60">{c.sport}</div>
                </div>
                <div className="text-body-sm text-ink-900">{c.district}</div>
                <div className="font-geist-mono tabular-nums text-title-sm text-ink-900">{c.utilization}%</div>
                <div className="text-body-sm text-ink-900">{c.peak_hours}</div>
                <div className="font-geist-mono tabular-nums text-title-sm text-lime-deep">{formatPrice(c.price_per_hour)}</div>
              </div>
            ))}
          </div>
        )}
      </RevealOnScroll>
    </div>
  );
}

export default function VenuesPage() {
  return <Suspense fallback={null}><VenuesPageInner /></Suspense>;
}
