'use client';
import { useState, useEffect } from 'react';
import { getCourts } from '@/lib/data-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { Button } from '@/components/Button';
import { Eyebrow, AITag } from '@/components/Tags';
import { formatPrice } from '@/lib/format';
import { PageHero } from '@/components/primitives/PageHero';
import { NumberFlip } from '@/components/primitives/NumberFlip';
import { DarkHero } from '@/components/primitives/DarkHero';
import { PulseAccent } from '@/components/primitives/PulseAccent';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

export default function PricingPage() {
  const [standard, setStandard] = useState(450);
  const [prime, setPrime] = useState(650);
  const [courts, setCourts] = useState<Court[]>(FALLBACK_COURTS);

  useEffect(() => {
    getCourts().then(setCourts).catch(() => setCourts(FALLBACK_COURTS));
  }, []);

  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow="PRICING SETUP · 6 TIERS LIVE"
        headline={<>Revenue today: <NumberFlip value={128400} />฿</>}
        sub="+15% vs last week · Kinetic AI is watching the city demand pulse."
      />

      <RevealOnScroll delay={80}>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {courts.slice(0, 6).map((c) => (
            <div key={c.id} className="bg-white rounded-kp-card shadow-float p-3">
              <div className="font-geist text-body-sm font-semibold text-ink-900 truncate">{c.name}</div>
              <span className="text-label-sm text-lime-deep font-geist">ACTIVE</span>
              <div className="font-geist-mono tabular-nums text-title-sm text-ink-900 mt-1">{formatPrice(c.price_per_hour)}</div>
            </div>
          ))}
        </div>
      </RevealOnScroll>

      <RevealOnScroll delay={160}>
        <div className="grid grid-cols-1 lg:grid-cols-[1.6fr_1fr] gap-5">
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="font-geist font-semibold text-title-md text-ink-900">Base Hourly Rates</h3>
                <Eyebrow>MANUAL FOUNDATION</Eyebrow>
              </div>
              <span className="text-xl">💰</span>
            </div>

            <div className="mt-4">
              <div className="bg-surface-low rounded-kp-card p-3 mb-2">
                <div className="font-geist font-semibold text-body-sm text-ink-900">Standard Court</div>
                <div className="text-label-sm text-ink-700/60">Weekdays 08:00 - 17:00</div>
              </div>
              <input type="number" className="field-input" value={standard} step={50} onChange={(e) => setStandard(parseInt(e.target.value || '0', 10))} />
            </div>

            <div className="mt-4">
              <div className="bg-surface-low rounded-kp-card p-3 mb-2">
                <div className="font-geist font-semibold text-body-sm text-ink-900">Prime Time</div>
                <div className="text-label-sm text-ink-700/60">Daily 17:00 - 23:00</div>
              </div>
              <input type="number" className="field-input" value={prime} step={50} onChange={(e) => setPrime(parseInt(e.target.value || '0', 10))} />
            </div>

            <div className="grid grid-cols-2 gap-3 mt-5">
              <div className="bg-surface-low rounded-kp-card p-3">
                <Eyebrow>COMPETITOR AVERAGE</Eyebrow>
                <div className="font-geist-mono tabular-nums text-title-md text-ink-900 mt-1">{formatPrice(510)} /hr</div>
                <div className="text-label-sm text-lime-deep">Your pricing is 12% below market</div>
              </div>
              <div className="bg-surface-low rounded-kp-card p-3">
                <Eyebrow>OCCUPANCY FORECAST</Eyebrow>
                <div className="font-geist-mono tabular-nums text-title-md text-ink-900 mt-1">92%</div>
                <div className="text-label-sm text-lime-deep">HIGH DEMAND EXPECTED</div>
              </div>
            </div>
          </div>

          <DarkHero glow="lime" className="p-5">
            <AITag>LIVE AI INSIGHT</AITag>
            <h3 className="font-geist font-bold text-title-lg text-white mt-2">
              Demand Prediction<br />+30% for Friday Evening
            </h3>
            <p className="text-body-sm text-white/60 mt-2">
              Local tournaments and social events in your area are spiking demand for Friday 18:00–21:00. Our kinetic model suggests a tactical rate adjustment to maximize yield.
            </p>
            <hr className="border-white/10 my-3" />
            <Eyebrow>SUGGESTED PRICE ADJUSTMENT</Eyebrow>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-label-sm line-through text-white/40">{formatPrice(450)}</span>
              <PulseAccent>
                <span className="font-geist-mono tabular-nums text-display-sm font-bold text-white">{formatPrice(580)}</span>
              </PulseAccent>
              <span className="text-base">⚡</span>
            </div>
            <div className="text-label-sm text-lime mt-2">💰 +{formatPrice(2400)} projected daily revenue</div>
          </DarkHero>
        </div>
      </RevealOnScroll>
    </div>
  );
}
