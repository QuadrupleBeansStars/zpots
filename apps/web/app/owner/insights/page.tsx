'use client';
import { useEffect, useState } from 'react';
import Markdown from 'react-markdown';

import { PageHero } from '@/components/primitives/PageHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { AITag, Eyebrow, StatusBadge } from '@/components/Tags';
import { DemandHeatmap } from '@/components/owner/DemandHeatmap';
import {
  DEMAND_FORECAST, DISTRICT_DEMAND, PEAK_UTILIZATION_BARS,
  WEEKLY_UTILIZATION, OWNER_BOOKINGS,
} from '@/lib/owner-mock-data';
import { aiInsights, mlDemandForecast } from '@/lib/api-client';
import type { DemandCell } from '@/lib/owner-mock-data';

const LEVEL_TO_STATUS: Record<string, 'confirmed' | 'progress' | 'cancelled'> = {
  Peak: 'confirmed', Moderate: 'progress', Saturated: 'cancelled',
};

export default function InsightsPage() {
  const [summary, setSummary] = useState('');
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [heatmap, setHeatmap] = useState<DemandCell[]>(DEMAND_FORECAST);
  const [heatmapFromApi, setHeatmapFromApi] = useState(false);

  useEffect(() => {
    mlDemandForecast()
      .then((res) => {
        if (res.cells.length > 0) {
          setHeatmap(res.cells);
          setHeatmapFromApi(true);
        }
      })
      .catch(() => { /* keep mock fallback */ });
  }, []);

  async function generate() {
    setSummaryLoading(true);
    setSummaryError(null);
    try {
      const weekly_utilization = Object.fromEntries(
        WEEKLY_UTILIZATION.map((w) => [w.day, w.pct]),
      );
      const res = await aiInsights({
        weekly_utilization,
        district_demand: DISTRICT_DEMAND,
        owner_bookings: OWNER_BOOKINGS.map((b) => ({
          customer: b.customer, sport: b.sport, status: b.status,
        })),
      });
      setSummary(res.markdown);
    } catch (e) {
      setSummaryError('Could not generate summary. Is the API running?');
    } finally {
      setSummaryLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-5">
      <PageHero
        eyebrow="AI INSIGHTS · 7-DAY FORECAST"
        headline="Bangkok demand intelligence."
        sub="Live signals from your venues + our models, fused. Generate the summary on demand or browse the heatmap below."
        cta={
          <div className="flex gap-2">
            <button
              type="button"
              onClick={generate}
              disabled={summaryLoading}
              className="px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring disabled:opacity-60"
            >
              {summaryLoading ? 'Generating…' : 'Generate AI Summary'}
            </button>
            <button
              type="button"
              onClick={() => setSummary('')}
              className="px-5 py-3 bg-white/10 text-white font-geist font-semibold text-body-sm rounded-kp-pill hover:bg-white/15 transition-colors duration-quick focus-ring"
            >
              Clear
            </button>
          </div>
        }
      />

      {summaryError && (
        <div className="bg-white rounded-kp-card shadow-float p-3 text-body-sm text-red-700">
          {summaryError}
        </div>
      )}

      {summary && (
        <RevealOnScroll>
          <div className="bg-surface-low rounded-kp-card p-5">
            <AITag>AI GENERATED SUMMARY</AITag>
            <div className="mt-2 text-body-sm leading-relaxed prose prose-sm max-w-none">
              <Markdown>{summary}</Markdown>
            </div>
          </div>
        </RevealOnScroll>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <RevealOnScroll>
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">Bangkok Demand Heatmap</h3>
            <Eyebrow>
              {heatmapFromApi ? '7-DAY FORECAST · LIVE FROM MODEL' : '7-DAY FORECAST · CACHED'}
            </Eyebrow>
            <div className="mt-3">
              <DemandHeatmap data={heatmap} />
            </div>
          </div>
        </RevealOnScroll>
        <RevealOnScroll delay={80}>
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">Peak Utilization</h3>
            <Eyebrow>HOURLY DISTRIBUTION</Eyebrow>
            <div className="flex items-end gap-[3px] h-24 mt-3">
              {PEAK_UTILIZATION_BARS.map((v, i) => (
                <div
                  key={i}
                  className="flex-1 rounded-t"
                  style={{
                    height: `${v}%`,
                    background: v > 80 ? '#cffc00' : v > 50 ? '#506300' : '#A5D6A7',
                  }}
                />
              ))}
            </div>
            <div className="mt-3 bg-surface-low rounded-kp-card p-3 flex justify-between items-center">
              <div className="text-body-sm">
                <span className="text-lime">⚡</span> <strong>Golden Slot</strong>
              </div>
              <span className="font-geist-mono text-lime-deep font-bold">฿2,400/hr</span>
            </div>
          </div>
        </RevealOnScroll>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {DISTRICT_DEMAND.map((d, i) => (
          <RevealOnScroll key={d.name} delay={i * 60}>
            <div className="bg-surface-low rounded-kp-card p-4 text-center">
              <Eyebrow>{d.name}</Eyebrow>
              <div className="font-geist-mono font-bold text-display-md text-ink-900 my-1 tabular-nums">
                {d.demand}%
              </div>
              <StatusBadge status={LEVEL_TO_STATUS[d.level]}>{d.level}</StatusBadge>
            </div>
          </RevealOnScroll>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <RevealOnScroll>
          <div className="bg-white rounded-kp-card shadow-float p-5 min-h-[260px] flex flex-col">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">No-Show Risk Analysis ⚠️</h3>
            <span className="text-label-sm text-red-700 mt-1">
              PRIORITY: HIGH INTERVENTION
            </span>
            <div className="bg-surface-low rounded-kp-card mt-3 p-3 flex justify-between items-center">
              <span className="text-body-sm">Probable No-Shows</span>
              <span className="font-geist-mono text-body-md text-ink-900">
                12% <span className="text-body-sm text-red-700">(+4% WoW)</span>
              </span>
            </div>
            <div className="bg-surface-low rounded-kp-card mt-2 p-3 flex-1">
              <Eyebrow>PRIMARY ROOT CAUSE</Eyebrow>
              <div className="text-body-sm text-ink-700 mt-1">
                Traffic delays on Rama IV during rain predicted (70% probability).
              </div>
            </div>
          </div>
        </RevealOnScroll>
        <RevealOnScroll delay={80}>
          <div className="bg-surface-low rounded-kp-card p-5 min-h-[260px] flex flex-col">
            <h3 className="font-geist font-semibold text-title-md text-ink-900">AI Mitigation Strategies</h3>
            <div className="flex gap-3 flex-1 mt-3">
              <div className="bg-white rounded-kp-card shadow-float p-3 flex-1">
                <h4 className="text-body-sm font-geist font-bold">Smart Reschedule</h4>
                <p className="text-body-sm text-ink-700/60 leading-snug mt-1">
                  Auto-offer 15-min delay window to users in high-traffic zones.
                </p>
                <span className="text-label-sm text-lime-deep mt-2 inline-block">+23% RETENTION</span>
              </div>
              <div className="bg-white rounded-kp-card shadow-float p-3 flex-1">
                <h4 className="text-body-sm font-geist font-bold">Pre-Check Deposit</h4>
                <p className="text-body-sm text-ink-700/60 leading-snug mt-1">
                  20% commitment fee for high-demand Saturday slots.
                </p>
                <span className="text-label-sm text-lime-deep mt-2 inline-block">-60% NO-SHOWS</span>
              </div>
            </div>
            <button
              type="button"
              className="w-full mt-3 px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
            >
              Execute All
            </button>
          </div>
        </RevealOnScroll>
      </div>
    </div>
  );
}
