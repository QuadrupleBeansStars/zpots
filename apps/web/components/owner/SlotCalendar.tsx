import type { SlotBlock } from '@/lib/owner-mock-data';

const DAYS = [
  { name: 'MON', date: 12 },
  { name: 'TUE', date: 13 },
  { name: 'WED', date: 14, today: true },
  { name: 'THU', date: 15 },
  { name: 'FRI', date: 16 },
  { name: 'SAT', date: 17 },
  { name: 'SUN', date: 18 },
];

export function SlotCalendar({ calendar }: { calendar: Record<number, SlotBlock[]> }) {
  return (
    <div className="grid grid-cols-7 gap-2">
      {DAYS.map((d, i) => (
        <div key={d.name} className="flex flex-col gap-2">
          <div className={`text-center text-xs uppercase font-geist py-2 rounded-kp-card ${d.today ? 'bg-lime text-ink-900 font-bold' : 'bg-surface-low text-ink-700/60'}`}>
            {d.name}<br />{d.date}
          </div>
          {(calendar[i] ?? []).map((slot, j) => (
            <div
              key={`${slot.time}-${j}`}
              className="rounded-kp-card p-2 transition-shadow duration-quick hover:shadow-lift cursor-pointer"
              style={{ background: slot.color }}
            >
              <div className="font-geist font-semibold text-xs text-ink-900">{slot.label}</div>
              <div className="text-[10px] text-ink-700/60">{slot.time}</div>
            </div>
          ))}
          {(calendar[i] ?? []).length === 0 && (
            <div className="rounded-kp-card p-3 bg-surface-low text-center text-ink-700/60 text-xs cursor-pointer hover:shadow-lift transition-shadow duration-quick">+</div>
          )}
        </div>
      ))}
    </div>
  );
}
