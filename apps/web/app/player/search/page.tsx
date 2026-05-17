'use client';
import { useRouter, useSearchParams } from 'next/navigation';
import { useState, Suspense } from 'react';
import { COURTS } from '@/lib/mock-data';
import { aiParseSearch } from '@/lib/api-client';
import { CourtCard } from '@/components/CourtCard';
import { Button } from '@/components/Button';
import { Eyebrow } from '@/components/Tags';
import { Icon } from '@/components/Icon';

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

  const filtered = COURTS.filter((c) => {
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
    <div>
      <Eyebrow>BANGKOK PRECISION SEARCH</Eyebrow>
      <h1 className="font-display text-3xl font-bold mt-1">Find Your Court</h1>

      <div className="flex gap-3 mt-4">
        <div className="flex-1 relative">
          <Icon name="search" className="absolute left-4 top-1/2 -translate-y-1/2 text-zpots-moss" style={{ fontSize: 20 }} />
          <input
            className="field-input pl-12 bg-zpots-surface"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder='e.g. "badminton near Sukhumvit Friday evening under 400 baht"'
          />
        </div>
        <Button variant="primary" disabled={searchLoading} onClick={async () => {
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
        }}>{searchLoading ? 'Parsing…' : 'Search'}</Button>
      </div>

      <div className="flex gap-2 mt-4 items-center flex-wrap">
        <Eyebrow>SPORT</Eyebrow>
        {SPORTS.map((s) => (
          <button
            key={s}
            onClick={() => setSport(s)}
            className={`chip ${sport === s ? 'chip-selected' : 'chip-default'}`}
          >
            {s}
          </button>
        ))}
      </div>

      <div className="mt-6 mb-3">
        <Eyebrow>SHOWING {filtered.length} COURTS IN BANGKOK</Eyebrow>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((c) => (
          <CourtCard
            key={c.id}
            court={c}
            onBook={(court) => router.push(`/player/courts/${court.id}`)}
          />
        ))}
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
