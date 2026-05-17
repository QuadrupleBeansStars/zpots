'use client';
import { useState, useEffect } from 'react';
import { getCourts } from '@/lib/data-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { Button } from '@/components/Button';
import { Eyebrow, AITag } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

export default function PricingPage() {
  const [standard, setStandard] = useState(450);
  const [prime, setPrime] = useState(650);
  const [courts, setCourts] = useState<Court[]>(FALLBACK_COURTS);

  useEffect(() => {
    getCourts().then(setCourts).catch(() => setCourts(FALLBACK_COURTS));
  }, []);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-3xl font-bold">Pricing Setup</h1>
        <p className="text-sm text-zpots-muted">Precision control for your revenue. Leverage our proprietary Kinetic AI to optimize hourly rates based on real-time city demand.</p>
      </div>

      <div className="zpots-card-dark p-6">
        <Eyebrow>REVENUE TODAY</Eyebrow>
        <div className="font-display text-4xl font-bold text-white mt-1">{formatPrice(128400)}</div>
        <div className="text-xs text-white/70">+15% vs last week · 6 pricing tiers live</div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
        {courts.slice(0, 6).map((c) => (
          <div key={c.id} className="zpots-card p-3">
            <div className="text-xs font-semibold truncate">{c.name}</div>
            <span className="font-eyebrow text-[9px] text-zpots-moss">ACTIVE</span>
            <div className="font-display text-base font-bold mt-1">{formatPrice(c.price_per_hour)}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1.6fr_1fr] gap-5">
        <div className="zpots-card p-5">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-semibold">Base Hourly Rates</h3>
              <Eyebrow>MANUAL FOUNDATION</Eyebrow>
            </div>
            <span className="text-xl">💰</span>
          </div>

          <div className="mt-4">
            <div className="zpots-card-surface p-3 mb-2">
              <div className="font-semibold text-sm">Standard Court</div>
              <div className="text-xs text-zpots-muted">Weekdays 08:00 - 17:00</div>
            </div>
            <input type="number" className="field-input" value={standard} step={50} onChange={(e) => setStandard(parseInt(e.target.value || '0', 10))} />
          </div>

          <div className="mt-4">
            <div className="zpots-card-surface p-3 mb-2">
              <div className="font-semibold text-sm">Prime Time</div>
              <div className="text-xs text-zpots-muted">Daily 17:00 - 23:00</div>
            </div>
            <input type="number" className="field-input" value={prime} step={50} onChange={(e) => setPrime(parseInt(e.target.value || '0', 10))} />
          </div>

          <div className="grid grid-cols-2 gap-3 mt-5">
            <div className="zpots-card-surface p-3">
              <Eyebrow>COMPETITOR AVERAGE</Eyebrow>
              <div className="font-display text-xl font-bold mt-1">{formatPrice(510)} /hr</div>
              <div className="text-xs text-zpots-moss">Your pricing is 12% below market</div>
            </div>
            <div className="zpots-card-surface p-3">
              <Eyebrow>OCCUPANCY FORECAST</Eyebrow>
              <div className="font-display text-xl font-bold mt-1">92%</div>
              <div className="text-xs text-zpots-moss">HIGH DEMAND EXPECTED</div>
            </div>
          </div>
        </div>

        <div className="zpots-card-lime p-5">
          <AITag>LIVE AI INSIGHT</AITag>
          <h3 className="font-display text-lg font-bold mt-2" style={{ color: '#1a2600' }}>
            Demand Prediction<br />+30% for Friday Evening
          </h3>
          <p className="text-xs mt-2" style={{ color: '#1a2600' }}>
            Local tournaments and social events in your area are spiking demand for Friday 18:00–21:00. Our kinetic model suggests a tactical rate adjustment to maximize yield.
          </p>
          <hr className="border-black/10 my-3" />
          <Eyebrow>SUGGESTED PRICE ADJUSTMENT</Eyebrow>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-xs line-through text-zpots-muted">{formatPrice(450)}</span>
            <span className="font-display text-2xl font-bold" style={{ color: '#1a2600' }}>{formatPrice(580)}</span>
            <span className="text-base">⚡</span>
          </div>
          <div className="text-xs mt-2" style={{ color: '#1a2600' }}>💰 +{formatPrice(2400)} projected daily revenue</div>
        </div>
      </div>
    </div>
  );
}
