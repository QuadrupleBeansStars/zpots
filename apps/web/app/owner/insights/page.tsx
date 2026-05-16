'use client';
import { useState } from 'react';
import { Button } from '@/components/Button';
import { AITag, Eyebrow, StatusBadge } from '@/components/Tags';
import { DemandHeatmap } from '@/components/owner/DemandHeatmap';
import { DEMAND_FORECAST, DISTRICT_DEMAND, PEAK_UTILIZATION_BARS } from '@/lib/owner-mock-data';

const MOCK_SUMMARY =
  'Your Friday evening slots (18:00–21:00) continue to dominate revenue, ' +
  'driving 41% of weekly bookings. Sukhumvit demand is saturated — consider ' +
  'opening Court 4 for tournament-rate pricing. Thong Lor traffic predicted ' +
  'to intensify Saturday after 16:00 due to weather; auto-rescheduling ' +
  'recommended for 12% of bookings.';

const LEVEL_TO_STATUS: Record<string, 'confirmed' | 'progress' | 'cancelled'> = {
  Peak: 'confirmed', Moderate: 'progress', Saturated: 'cancelled',
};

export default function InsightsPage() {
  const [summary, setSummary] = useState('');

  return (
    <div className="flex flex-col gap-5">
      <div className="flex justify-between items-end">
        <div className="flex items-center gap-3">
          <h1 className="font-display text-3xl font-bold">AI Insights</h1>
          <AITag>ELITE VENUE PARTNER</AITag>
        </div>
        <div className="flex gap-2">
          <Button variant="primary" icon="smart_toy" onClick={() => setSummary(MOCK_SUMMARY)}>
            Generate AI Summary
          </Button>
          <Button variant="secondary" onClick={() => setSummary('')}>Regenerate</Button>
        </div>
      </div>

      {summary && (
        <div className="zpots-card-surface p-4">
          <AITag>AI GENERATED SUMMARY</AITag>
          <p className="mt-2 text-sm leading-relaxed">{summary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Bangkok Demand Heatmap</h3>
          <Eyebrow>7-DAY FORECAST · MODEL: RANDOM FOREST</Eyebrow>
          <div className="mt-3">
            <DemandHeatmap data={DEMAND_FORECAST} />
          </div>
        </div>
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Peak Utilization</h3>
          <Eyebrow>HOURLY DISTRIBUTION</Eyebrow>
          <div className="flex items-end gap-[3px] h-24 mt-3">
            {PEAK_UTILIZATION_BARS.map((v, i) => (
              <div key={i} className="flex-1 rounded-t" style={{
                height: `${v}%`,
                background: v > 80 ? '#CFFC00' : v > 50 ? '#2E6B00' : '#A5D6A7',
              }} />
            ))}
          </div>
          <div className="mt-3 zpots-card-surface p-3 flex justify-between">
            <div><span className="text-zpots-lime">⚡</span> <strong>Golden Slot</strong></div>
            <span className="font-display font-bold text-zpots-moss">฿2,400/hr</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {DISTRICT_DEMAND.map((d) => (
          <div key={d.name} className="zpots-card-surface p-4 text-center">
            <Eyebrow>{d.name}</Eyebrow>
            <div className="font-display text-2xl font-bold my-1">{d.demand}%</div>
            <StatusBadge status={LEVEL_TO_STATUS[d.level]}>{d.level}</StatusBadge>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="zpots-card p-5 min-h-[260px] flex flex-col">
          <h3 className="font-semibold">No-Show Risk Analysis ⚠️</h3>
          <span className="font-eyebrow text-[10px] uppercase tracking-wider mt-1" style={{ color: '#b02500' }}>
            PRIORITY: HIGH INTERVENTION
          </span>
          <div className="zpots-card-surface mt-3 p-3 flex justify-between">
            <span>Probable No-Shows</span>
            <span className="font-display text-base">12% <span className="text-xs text-red-700">(+4% WoW)</span></span>
          </div>
          <div className="zpots-card-surface mt-2 p-3 flex-1">
            <Eyebrow>PRIMARY ROOT CAUSE</Eyebrow>
            <div className="text-sm mt-1">Traffic delays on Rama IV during rain predicted (70% probability).</div>
          </div>
        </div>
        <div className="zpots-card-surface p-5 min-h-[260px] flex flex-col">
          <h3 className="font-semibold">AI Mitigation Strategies</h3>
          <div className="flex gap-3 flex-1 mt-3">
            <div className="zpots-card p-3 flex-1">
              <h4 className="text-sm font-bold">Smart Reschedule</h4>
              <p className="text-xs text-zpots-muted leading-snug mt-1">Auto-offer 15-min delay window to users in high-traffic zones.</p>
              <span className="font-eyebrow text-[10px] uppercase tracking-wider" style={{ color: '#506300' }}>+23% RETENTION</span>
            </div>
            <div className="zpots-card p-3 flex-1">
              <h4 className="text-sm font-bold">Pre-Check Deposit</h4>
              <p className="text-xs text-zpots-muted leading-snug mt-1">20% commitment fee for high-demand Saturday slots.</p>
              <span className="font-eyebrow text-[10px] uppercase tracking-wider" style={{ color: '#506300' }}>-60% NO-SHOWS</span>
            </div>
          </div>
          <Button variant="primary" className="w-full justify-center mt-3">Execute All</Button>
        </div>
      </div>
    </div>
  );
}
