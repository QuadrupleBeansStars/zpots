'use client';
import { useState, useEffect } from 'react';
import { notFound, useParams } from 'next/navigation';
import Link from 'next/link';
import { getCourt } from '@/lib/data-client';
import { fallbackCourt, getFreeSlotStarts } from '@/lib/mock-data';
import { useBookingStore } from '@/lib/booking-store';
import type { Court } from '@/lib/types';
import { SlotGrid } from '@/components/player/SlotGrid';
import { BookingSummaryCard } from '@/components/player/BookingSummaryCard';
import { DarkHero } from '@/components/primitives/DarkHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

function isoOffset(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0, 10);
}

const SPORT_ICON: Record<string, string> = {
  Badminton: '🏸', Football: '⚽', Basketball: '🏀', Padel: '🎾', Tennis: '🎾', Volleyball: '🏐',
};

export default function CourtDetailsPage() {
  const params = useParams<{ id: string }>();
  const [court, setCourt] = useState<Court | undefined>(undefined);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCourt(params.id)
      .then(setCourt)
      .catch(() => setCourt(fallbackCourt(params.id)))
      .finally(() => setLoading(false));
  }, [params.id]);

  const upcoming = Array.from({ length: 7 }, (_, i) => isoOffset(i));
  const [date, setDate] = useState(upcoming[0]);
  const [duration, setDuration] = useState<number>(1);
  const [timeStart, setTimeStart] = useState<string | null>(null);

  const storeBookings = useBookingStore((s) => s.bookings);
  const freeStarts = court ? getFreeSlotStarts(court.id, date, storeBookings) : [];

  if (loading) {
    return <div className="text-ink-700/60 text-body-sm py-10 text-center">Loading court…</div>;
  }

  if (!court) return notFound();

  return (
    <div className="flex flex-col gap-6">
      <Link href="/player/search" className="text-body-sm text-ink-700 hover:text-ink-900 underline-offset-4 hover:underline">
        ← Back to Search
      </Link>

      <DarkHero glow="lime" className="p-8">
        <div className="flex flex-col items-start gap-4">
          <div className="text-5xl">{SPORT_ICON[court.sport] ?? '🏸'}</div>
          <div>
            <div className="text-label-sm text-lime/70 mb-2">LIVE AVAILABILITY</div>
            <h1 className="font-geist font-bold text-display-md text-white leading-none tracking-tight uppercase">
              {court.name}
            </h1>
            <p className="mt-2 text-body-md text-white/60">📍 {court.district}</p>
            <div className="flex gap-3 mt-3 flex-wrap">
              <span className="px-3 py-1 bg-lime text-ink-900 font-geist font-semibold text-label-sm rounded-kp-pill">
                {court.sport}
              </span>
              <span className="px-3 py-1 bg-white/10 text-white font-geist text-label-sm rounded-kp-pill">
                ⭐ {court.rating} ({court.reviews} reviews)
              </span>
              <span className="px-3 py-1 bg-white/10 text-white font-geist text-label-sm rounded-kp-pill">
                ฿{court.price_per_hour}/hr
              </span>
            </div>
          </div>
        </div>
      </DarkHero>

      <RevealOnScroll>
        <div className="grid gap-3" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))' }}>
          {court.amenities.map((a) => (
            <div key={a.label} className="bg-surface-low rounded-kp-card p-4 text-center">
              <span className="material-symbols-rounded text-ink-700/60" style={{ fontSize: 24 }}>{a.icon}</span>
              <div className="text-label-sm text-ink-700/50 mt-1">{a.label}</div>
              <div className="font-geist font-semibold text-body-sm text-ink-900 mt-0.5">{a.value}</div>
            </div>
          ))}
        </div>
      </RevealOnScroll>

      <RevealOnScroll>
        <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <div className="text-label-sm text-ink-700/60 mb-3">SELECT YOUR SLOT</div>

            <div className="flex gap-2 overflow-x-auto">
              {upcoming.map((d, i) => (
                <button
                  key={d}
                  onClick={() => { setDate(d); setTimeStart(null); }}
                  className={`px-3 py-1.5 rounded-kp-pill text-label-sm font-geist font-semibold whitespace-nowrap transition-colors duration-quick focus-ring ${
                    date === d
                      ? 'bg-lime text-ink-900'
                      : 'bg-surface-low text-ink-700 hover:bg-surface-med'
                  }`}
                >
                  {i === 0 ? 'Today' : new Date(d + 'T00:00').toLocaleDateString('en-GB', { weekday: 'short', day: '2-digit' }).toUpperCase()}
                </button>
              ))}
            </div>

            <div className="flex gap-3 mt-4 items-center">
              <span className="text-label-sm text-ink-700/60">DURATION</span>
              {[1, 2, 3].map((d) => (
                <label key={d} className="text-body-sm text-ink-700 flex items-center gap-1 cursor-pointer">
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
      </RevealOnScroll>
    </div>
  );
}
