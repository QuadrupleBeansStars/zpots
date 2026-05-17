'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getCourts } from '@/lib/data-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { Button } from '@/components/Button';
import { CourtCard } from '@/components/CourtCard';
import { AITag, Eyebrow } from '@/components/Tags';

const SPORTS: { emoji: string; label: string }[] = [
  { emoji: '🏸', label: 'Badminton' },
  { emoji: '⚽', label: 'Football' },
  { emoji: '🏀', label: 'Basketball' },
  { emoji: '🎾', label: 'Tennis' },
  { emoji: '🏐', label: 'Volleyball' },
  { emoji: '🎾', label: 'Padel' },
];

export default function PlayerHomePage() {
  const [courts, setCourts] = useState<Court[]>(FALLBACK_COURTS);

  useEffect(() => {
    getCourts().then(setCourts).catch(() => setCourts(FALLBACK_COURTS));
  }, []);

  const featured = courts.slice(0, 4);
  return (
    <div className="flex flex-col gap-10">
      {/* Hero */}
      <section className="text-center pt-6">
        <AITag>AI-POWERED DISCOVERY</AITag>
        <h1 className="font-display text-4xl font-bold mt-4">
          Discover &amp; Book<br />Your Next Game
        </h1>
        <p className="text-zpots-muted mt-2 max-w-xl mx-auto">
          Find the best sports courts, choose your time, and join the action
          with real-time AI availability.
        </p>
        <div className="flex gap-3 justify-center mt-6">
          <Link href="/player/search">
            <Button variant="primary" icon="search">Search Courts</Button>
          </Link>
          <Link href="/player/search">
            <Button variant="secondary" icon="explore">Explore Sports</Button>
          </Link>
        </div>
      </section>

      {/* Sport row */}
      <section className="flex justify-center gap-8">
        {SPORTS.map((s) => (
          <div key={s.label} className="flex flex-col items-center gap-2">
            <div className="w-12 h-12 rounded-full bg-zpots-surface flex items-center justify-center text-xl">
              {s.emoji}
            </div>
            <span className="font-eyebrow text-[9px] uppercase tracking-wider text-zpots-muted">
              {s.label}
            </span>
          </div>
        ))}
      </section>

      {/* Featured courts */}
      <section>
        <div className="flex justify-between items-end mb-4">
          <div>
            <h2 className="font-display text-2xl font-bold">Featured Courts</h2>
            <p className="text-sm text-zpots-muted">Top-rated venues chosen by the Bangkok community.</p>
          </div>
          <Link href="/player/search" className="text-sm text-zpots-moss font-medium">
            View all →
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {featured.map((c) => (
            <CourtCard key={c.id} court={c} onBook={(court) => { window.location.href = `/player/courts/${court.id}`; }} />
          ))}
        </div>
      </section>

      {/* 3-step explainer */}
      <section className="text-center">
        <h2 className="font-display text-2xl font-bold mb-6">Master Your Game in 3 Steps</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {[
            { icon: 'search', step: '1. Search', body: 'Browse local courts based on your sport, time, and budget preferences.' },
            { icon: 'calendar_month', step: '2. Book', body: 'Select your preferred time and complete the booking in seconds.' },
            { icon: 'sports', step: '3. Play', body: 'Show your QR code, check in, and enjoy your time with zero hassle.' },
          ].map((s) => (
            <div key={s.step} className="zpots-card-surface p-6 text-center">
              <span className="material-symbols-rounded text-zpots-moss" style={{ fontSize: 32 }}>{s.icon}</span>
              <h3 className="font-display font-bold mt-2">{s.step}</h3>
              <p className="text-sm text-zpots-muted mt-2">{s.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Smart Booking call-out */}
      <section>
        <div className="zpots-card-dark p-8">
          <AITag onDark>AI PRECISION SUITE</AITag>
          <h3 className="font-display text-2xl font-bold mt-3">
            Experience Precision<br />with <span className="text-zpots-lime">Smart Booking</span>
          </h3>
          <ul className="mt-4 text-sm text-white/80 space-y-1">
            <li>• Dynamic pricing based on real-time court demand</li>
            <li>• AI-suggested partners matching your skill level</li>
            <li>• Smart predictions &amp; live availability tracking</li>
          </ul>
        </div>
      </section>
    </div>
  );
}
