import React from 'react';
import type { Court } from '@/types';

const SPORT_ICON: Record<string, string> = {
  Badminton: '🏸', Football: '⚽', Basketball: '🏀', Padel: '🎾', Tennis: '🎾', Volleyball: '🏐',
};

export function CourtCard({ court, onBook }: { court: Court; onBook?: (c: Court) => void }) {
  return (
    <div className="bg-white rounded-kp-card shadow-float overflow-hidden">
      <div
        className="relative flex items-center justify-center"
        style={{
          height: 150,
          background: `linear-gradient(135deg, ${court.color}, ${court.color}cc)`,
        }}
      >
        <span style={{ fontSize: 44, color: 'rgba(255,255,255,0.9)' }}>{SPORT_ICON[court.sport] ?? '🏸'}</span>
        {court.tags?.length ? (
          <div className="absolute top-3 left-3 flex flex-wrap gap-1">
            {court.tags.map((t) => (
              <span key={t} className="px-2 py-0.5 bg-lime text-ink-900 text-label-sm font-geist font-semibold rounded-kp-pill">
                {t}
              </span>
            ))}
          </div>
        ) : null}
      </div>
      <div className="p-4">
        <div className="flex justify-between items-center">
          <span className="font-geist font-semibold text-body-md text-ink-900">{court.name}</span>
          <span className="text-body-sm text-ink-700/70">⭐ {court.rating}</span>
        </div>
        <div className="text-body-sm text-ink-700/60 mt-1">📍 {court.location}</div>
        <div className="flex justify-between items-end mt-4">
          <div>
            <div className="text-label-sm text-ink-700/50">STARTS AT</div>
            <span className="font-geist font-bold text-title-md text-ink-900">฿{court.price_per_hour}</span>
            <span className="text-body-sm text-ink-700/60"> /hr</span>
          </div>
          <button
            onClick={() => onBook?.(court)}
            className="px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
          >
            Book Now
          </button>
        </div>
      </div>
    </div>
  );
}
