'use client';
import { ALL_HOURS } from '@/lib/mock-data';

type SlotGridProps = {
  freeStarts: string[];
  selectedStart: string | null;
  duration: number;
  onSelect: (start: string) => void;
};

export function SlotGrid({ freeStarts, selectedStart, duration, onSelect }: SlotGridProps) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
      {ALL_HOURS.map((h) => {
        const startH = parseInt(h.slice(0, 2), 10);
        const blockHours = Array.from({ length: duration }, (_, i) => `${String(startH + i).padStart(2, '0')}:00`);
        const fits = blockHours.every((b) => freeStarts.includes(b));
        const isSelected = selectedStart === h;
        return (
          <button
            key={h}
            disabled={!fits}
            onClick={() => onSelect(h)}
            className={[
              'rounded-card p-3 text-sm border',
              isSelected
                ? 'bg-zpots-lime border-zpots-moss text-zpots-forest font-semibold'
                : fits
                ? 'bg-white border-zpots-mint hover:border-zpots-moss'
                : 'bg-zpots-surface border-zpots-mint text-zpots-muted cursor-not-allowed opacity-60',
            ].join(' ')}
          >
            <div className="font-display">{h}</div>
            <div className="text-[11px] text-zpots-muted">
              {fits ? 'Available' : '—'}
            </div>
          </button>
        );
      })}
    </div>
  );
}
