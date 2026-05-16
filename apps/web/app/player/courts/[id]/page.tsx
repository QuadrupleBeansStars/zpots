'use client';
import { useState } from 'react';
import { notFound, useParams } from 'next/navigation';
import { getCourt, getFreeSlotStarts, SEEDED_BOOKINGS } from '@/lib/mock-data';
import { useBookingStore } from '@/lib/booking-store';
import { SlotGrid } from '@/components/player/SlotGrid';
import { BookingSummaryCard } from '@/components/player/BookingSummaryCard';
import { AITag, Eyebrow } from '@/components/Tags';

function isoOffset(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

export default function CourtDetailsPage() {
  const params = useParams<{ id: string }>();
  const court = getCourt(params.id);
  if (!court) notFound();

  const upcoming = Array.from({ length: 7 }, (_, i) => isoOffset(i));
  const [date, setDate] = useState(upcoming[0]);
  const [duration, setDuration] = useState<number>(1);
  const [timeStart, setTimeStart] = useState<string | null>(null);

  const storeBookings = useBookingStore((s) => s.bookings);
  const allBookings = [...SEEDED_BOOKINGS, ...storeBookings];
  const freeStarts = getFreeSlotStarts(court.id, date, allBookings);

  return (
    <div>
      <a href="/player/search" className="text-sm text-zpots-moss">← Back to Search</a>

      {/* Hero */}
      <div
        className="w-full h-48 rounded-card mt-3 flex items-center justify-center"
        style={{ background: `linear-gradient(135deg, ${court.color}, ${court.color}cc)` }}
      >
        <span style={{ fontSize: 60, color: 'rgba(255,255,255,0.9)' }}>
          {court.sport === 'Badminton' ? '🏸' : court.sport === 'Football' ? '⚽' : court.sport === 'Basketball' ? '🏀' : court.sport === 'Padel' || court.sport === 'Tennis' ? '🎾' : '🏐'}
        </span>
      </div>

      <div className="mt-4 flex items-center gap-3">
        <AITag>LIVE AVAILABILITY</AITag>
        <span className="text-sm text-zpots-muted">⭐ {court.rating} ({court.reviews} reviews)</span>
      </div>

      <h1 className="font-display text-3xl font-bold uppercase mt-2">{court.name}</h1>
      <p className="text-zpots-muted">📍 {court.district}</p>

      {/* Amenities — responsive grid */}
      <div className="grid gap-3 mt-4" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))' }}>
        {court.amenities.map((a) => (
          <div key={a.label} className="zpots-card-surface p-4 text-center min-w-0">
            <span className="material-symbols-rounded text-zpots-moss" style={{ fontSize: 24 }}>{a.icon}</span>
            <div className="font-eyebrow text-[9px] uppercase mt-1">{a.label}</div>
            <div className="font-semibold text-sm text-zpots-ink mt-0.5">{a.value}</div>
          </div>
        ))}
      </div>

      {/* Main grid: slot selector + booking summary */}
      <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6 mt-6">
        <div className="zpots-card-surface p-5">
          <Eyebrow>SELECT YOUR SLOT</Eyebrow>

          {/* Date row */}
          <div className="flex gap-2 mt-3 overflow-x-auto">
            {upcoming.map((d, i) => (
              <button
                key={d}
                onClick={() => { setDate(d); setTimeStart(null); }}
                className={`chip ${date === d ? 'chip-selected' : 'chip-default'} whitespace-nowrap`}
              >
                {i === 0 ? 'Today' : new Date(d + 'T00:00').toLocaleDateString('en-GB', { weekday: 'short', day: '2-digit' }).toUpperCase()}
              </button>
            ))}
          </div>

          {/* Duration radios */}
          <div className="flex gap-3 mt-4 items-center">
            <Eyebrow>DURATION</Eyebrow>
            {[1, 2, 3].map((d) => (
              <label key={d} className="text-sm flex items-center gap-1 cursor-pointer">
                <input
                  type="radio"
                  name="duration"
                  checked={duration === d}
                  onChange={() => { setDuration(d); setTimeStart(null); }}
                />
                {d} hr{d > 1 ? 's' : ''}
              </label>
            ))}
          </div>

          {/* Slot grid */}
          <div className="mt-4">
            <SlotGrid
              freeStarts={freeStarts}
              selectedStart={timeStart}
              duration={duration}
              onSelect={(h) => setTimeStart(h)}
            />
          </div>
        </div>

        <BookingSummaryCard
          courtId={court.id}
          date={date}
          timeStart={timeStart}
          duration={duration}
          pricePerHour={court.price_per_hour}
        />
      </div>
    </div>
  );
}
