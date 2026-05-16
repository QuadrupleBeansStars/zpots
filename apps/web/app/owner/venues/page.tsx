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
                  <span className="absolute top-3 left-3"><StatusBadge status="confirmed">● {c.status}</StatusBadge></span>
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
