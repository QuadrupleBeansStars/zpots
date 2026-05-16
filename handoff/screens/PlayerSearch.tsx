'use client';
import React, { useState } from 'react';
import { PlayerTopBar } from '@/components/PlayerTopBar';
import { CourtCard } from '@/components/CourtCard';
import { AITag, Chip, Eyebrow } from '@/components/Tags';
import { Button } from '@/components/Button';
import { Icon } from '@/components/Icon';
import type { Court } from '@/types';

// Replace with `useQuery(['courts', filters], () => fetch(...))` via TanStack Query
const MOCK_COURTS: Court[] = []; // import from lib/mock-data

export default function PlayerSearchPage() {
  const [query, setQuery] = useState('');
  const [sport, setSport] = useState<string>('All');
  const sports = ['All', 'Badminton', 'Football', 'Basketball', 'Padel'];
  const filtered = sport === 'All' ? MOCK_COURTS : MOCK_COURTS.filter((c) => c.sport === sport);

  async function onSearch() {
    // POST /api/ai/parse-search { query }
    // Then push filters into URL
  }

  return (
    <div style={{ background: '#fff', minHeight: '100vh' }}>
      <PlayerTopBar />
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '24px 32px' }}>
        <Eyebrow>BANGKOK PRECISION SEARCH</Eyebrow>
        <h1 className="display" style={{ fontSize: 32, marginTop: 4 }}>Find Your Court</h1>

        <div style={{ display: 'flex', gap: 10, marginTop: 18 }}>
          <div style={{ flex: 1, position: 'relative' }}>
            <Icon name="search" style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#2E6B00', fontSize: 20 }} />
            <input
              className="field-input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder='"badminton near Sukhumvit Friday evening under 400 baht"'
              style={{ paddingLeft: 44, background: '#F2F9EE', borderColor: '#E3F0DE' }}
            />
          </div>
          <Button variant="primary" onClick={onSearch}>Search</Button>
        </div>

        <div style={{ display: 'flex', gap: 8, marginTop: 16, alignItems: 'center' }}>
          <Eyebrow>SPORT</Eyebrow>
          {sports.map((s) => (
            <Chip key={s} selected={sport === s} onClick={() => setSport(s)}>{s}</Chip>
          ))}
        </div>

        <div style={{ margin: '22px 0 14px' }}>
          <Eyebrow>SHOWING {filtered.length} COURTS IN BANGKOK</Eyebrow>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 14 }}>
          {filtered.map((c) => (
            <CourtCard key={c.id} court={c} onBook={(court) => (location.href = `/courts/${court.id}/book`)} />
          ))}
        </div>
      </div>
    </div>
  );
}
