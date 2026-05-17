'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getCourts } from '@/lib/data-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { PageHero } from '@/components/primitives/PageHero';
import { DarkHero } from '@/components/primitives/DarkHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { NumberFlip } from '@/components/primitives/NumberFlip';
import { CourtCard } from '@/components/CourtCard';

const SPORTS = [
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
    <div className="flex flex-col gap-8">
      <PageHero
        eyebrow="AI-POWERED DISCOVERY"
        headline={<>Discover & book<br />your next game.</>}
        sub="Find the best sports courts in Bangkok. Real-time AI availability, smart filtering, instant booking."
        cta={
          <div className="flex flex-wrap gap-2">
            <Link href="/player/search" className="px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring">
              Search Courts
            </Link>
            <Link href="/player/search" className="px-5 py-3 bg-white/10 text-white font-geist font-semibold text-body-sm rounded-kp-pill hover:bg-white/15 transition-colors duration-quick focus-ring">
              Explore Sports
            </Link>
          </div>
        }
      />

      <RevealOnScroll>
        <section className="flex justify-center flex-wrap gap-6">
          {SPORTS.map((s) => (
            <Link key={s.label} href={`/player/search?sport=${s.label}`} className="flex flex-col items-center gap-2 group focus-ring rounded-kp-chip p-2">
              <div className="w-14 h-14 rounded-kp-pill bg-surface-low flex items-center justify-center text-2xl group-hover:bg-surface-med transition-colors duration-quick">
                {s.emoji}
              </div>
              <span className="text-label-sm text-ink-700/70 group-hover:text-ink-900">{s.label}</span>
            </Link>
          ))}
        </section>
      </RevealOnScroll>

      <section>
        <div className="flex justify-between items-end mb-4">
          <div>
            <h2 className="font-geist font-bold text-title-lg text-ink-900">Featured Courts</h2>
            <p className="text-body-sm text-ink-700/60 mt-1">Top-rated venues chosen by the Bangkok community.</p>
          </div>
          <Link href="/player/search" className="text-body-sm text-ink-700 hover:text-ink-900 underline-offset-4 hover:underline">
            View all →
          </Link>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {featured.map((c, i) => (
            <RevealOnScroll key={c.id} delay={i * 80}>
              <CourtCard court={c} onBook={(court) => { window.location.href = `/player/courts/${court.id}`; }} />
            </RevealOnScroll>
          ))}
        </div>
      </section>

      <RevealOnScroll>
        <section>
          <h2 className="font-geist font-bold text-title-lg text-ink-900 text-center mb-6">Master your game in 3 steps</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { icon: '🔍', step: '1. Search', body: 'Browse local courts based on your sport, time, and budget.' },
              { icon: '📅', step: '2. Book', body: 'Select your preferred time and complete the booking in seconds.' },
              { icon: '🏆', step: '3. Play', body: 'Show your QR code, check in, and enjoy your time with zero hassle.' },
            ].map((s, i) => (
              <RevealOnScroll key={s.step} delay={i * 100}>
                <div className="bg-surface-low rounded-kp-card p-6 text-center">
                  <div className="text-3xl mb-3">{s.icon}</div>
                  <h3 className="font-geist font-bold text-title-md text-ink-900">{s.step}</h3>
                  <p className="text-body-sm text-ink-700/60 mt-2">{s.body}</p>
                </div>
              </RevealOnScroll>
            ))}
          </div>
        </section>
      </RevealOnScroll>

      <RevealOnScroll>
        <DarkHero glow="lime" className="p-8">
          <div className="text-label-sm text-lime/70 mb-3">AI PRECISION SUITE</div>
          <h3 className="font-geist font-bold text-display-md text-white leading-tight">
            Experience precision with <span className="text-lime">Smart Booking</span>.
          </h3>
          <ul className="mt-5 text-body-sm text-white/70 space-y-2">
            <li>→ Dynamic pricing based on real-time court demand</li>
            <li>→ AI-suggested partners matching your skill level</li>
            <li>→ Smart predictions & live availability tracking</li>
          </ul>
        </DarkHero>
      </RevealOnScroll>
    </div>
  );
}
