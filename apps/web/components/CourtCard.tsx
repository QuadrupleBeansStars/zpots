import React from 'react';
import { AITag } from './Tags';
import { Button } from './Button';
import type { Court } from '@/types';

const SPORT_ICON: Record<string, string> = {
  Badminton: '🏸', Football: '⚽', Basketball: '🏀', Padel: '🎾', Tennis: '🎾',
};

export function CourtCard({ court, onBook }: { court: Court; onBook?: (c: Court) => void }) {
  return (
    <div className="zpots-card" style={{ padding: 0, overflow: 'hidden' }}>
      <div
        style={{
          height: 150,
          background: `linear-gradient(135deg, ${court.color}, ${court.color}cc)`,
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <span style={{ fontSize: 44, color: 'rgba(255,255,255,0.9)' }}>{SPORT_ICON[court.sport] ?? '🏸'}</span>
        {court.tags?.length ? (
          <div style={{ position: 'absolute', top: 12, left: 12 }}>
            {court.tags.map((t) => (
              <AITag key={t}>{t}</AITag>
            ))}
          </div>
        ) : null}
      </div>
      <div style={{ padding: '14px 16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontWeight: 600, fontSize: 14 }}>{court.name}</span>
          <span style={{ fontSize: 13, color: '#506300' }}>⭐ {court.rating}</span>
        </div>
        <div style={{ fontSize: 12, color: '#3d4455', marginTop: 4 }}>📍 {court.location}</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginTop: 14 }}>
          <div>
            <div className="eyebrow" style={{ fontSize: 9 }}>STARTS AT</div>
            <span className="display" style={{ fontSize: 20 }}>฿{court.price_per_hour}</span>
            <span style={{ fontSize: 11, color: '#3d4455' }}> /hr</span>
          </div>
          <Button variant="primary" style={{ padding: '8px 18px', fontSize: 12 }} onClick={() => onBook?.(court)}>
            Book Now
          </Button>
        </div>
      </div>
    </div>
  );
}
