'use client';
import { useRouter, useSearchParams } from 'next/navigation';
import { useState, useEffect, Suspense } from 'react';
import { getCourts } from '@/lib/data-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { aiParseSearch } from '@/lib/api-client';
import { CourtCard } from '@/components/CourtCard';
import { Icon } from '@/components/Icon';
import { PageHero } from '@/components/primitives/PageHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

const SPORTS = ['All', 'Badminton', 'Football', 'Basketball', 'Padel', 'Tennis', 'Volleyball'];

function SearchPageInner() {
  const router = useRouter();
  const params = useSearchParams();
  const sport = params.get('sport') ?? 'All';
  const district = params.get('district') ?? '';
  const maxPriceStr = params.get('max_price') ?? '';
  const maxPrice = maxPriceStr ? parseInt(maxPriceStr, 10) : null;
  const [query, setQuery] = useState(params.get('q') ?? '');
  const [searchLoading, setSearchLoading] = useState(false);
  const [courts, setCourts] = useState<Court[]>(FALLBACK_COURTS);

  useEffect(() => {
    getCourts().then(setCourts).catch(() => setCourts(FALLBACK_COURTS));
  }, []);

  const filtered = courts.filter((c) => {
    if (sport !== 'All' && c.sport !== sport) return false;
    if (district && !c.district.toLowerCase().includes(district.toLowerCase())) return false;
    if (maxPrice !== null && c.price_per_hour > maxPrice) return false;
    return true;
  });

  function setSport(s: string) {
    const next = new URLSearchParams(params.toString());
    if (s === 'All') next.delete('sport'); else next.set('sport', s);
    router.push(`/player/search?${next.toString()}`);
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow={`BANGKOK PRECISION SEARCH · ${courts.length} COURTS`}
        headline="Find your court."
        sub="Describe what you need — sport, time, district, budget — and AI will narrow it down instantly."
      />

      <div className="bg-white rounded-kp-card shadow-float p-3 flex gap-3">
        <div className="flex-1 relative">
          <Icon name="search" className="absolute left-4 top-1/2 -translate-y-1/2 text-ink-700/50" style={{ fontSize: 20 }} />
          <input
            className="field-input pl-12"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder='e.g. "badminton near Sukhumvit Friday evening under 400 baht"'
          />
        </div>
        <button
          disabled={searchLoading}
          onClick={async () => {
            if (!query.trim()) return;
            setSearchLoading(true);
            try {
              const parsed = await aiParseSearch({ query });
              const next = new URLSearchParams(params.toString());
              if (parsed.sport) next.set('sport', parsed.sport); else next.delete('sport');
              if (parsed.district) next.set('district', parsed.district); else next.delete('district');
              if (parsed.max_price !== null) next.set('max_price', String(parsed.max_price)); else next.delete('max_price');
              router.push(`/player/search?${next.toString()}`);
            } catch {
              // silent — user can still type and filter manually
            } finally {
              setSearchLoading(false);
            }
          }}
          className="px-5 py-2.5 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring disabled:opacity-60"
        >
          {searchLoading ? 'Parsing…' : 'Search'}
        </button>
      </div>

      <div className="flex gap-2 flex-wrap items-center">
        <span className="text-label-sm text-ink-700/60">SPORT</span>
        {SPORTS.map((s) => (
          <button
            key={s}
            onClick={() => setSport(s)}
            className={`px-3 py-1.5 rounded-kp-pill text-label-sm font-geist font-semibold transition-colors duration-quick focus-ring ${
              sport === s
                ? 'bg-lime text-ink-900'
                : 'bg-surface-low text-ink-700 hover:bg-surface-med'
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      <div>
        <div className="text-label-sm text-ink-700/60 mb-4">SHOWING {filtered.length} COURTS IN BANGKOK</div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((c, i) => (
            <RevealOnScroll key={c.id} delay={i * 60}>
              <CourtCard
                court={c}
                onBook={(court) => router.push(`/player/courts/${court.id}`)}
              />
            </RevealOnScroll>
          ))}
        </div>
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={null}>
      <SearchPageInner />
    </Suspense>
  );
}
