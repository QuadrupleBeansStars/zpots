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
          <div className={`text-center text-xs uppercase font-eyebrow py-2 rounded-card ${d.today ? 'bg-zpots-lime text-zpots-forest font-bold' : 'bg-zpots-surface text-zpots-muted'}`}>
            {d.name}<br />{d.date}
          </div>
          {(calendar[i] ?? []).map((slot, j) => (
            <div key={`${slot.time}-${j}`} className="rounded-card p-2" style={{ background: slot.color }}>
              <div className="font-semibold text-xs text-zpots-ink">{slot.label}</div>
              <div className="text-[10px] text-zpots-muted">{slot.time}</div>
            </div>
          ))}
          {(calendar[i] ?? []).length === 0 && (
            <div className="rounded-card p-3 bg-zpots-surface text-center text-zpots-muted text-xs cursor-pointer">+</div>
          )}
        </div>
      ))}
    </div>
  );
}
