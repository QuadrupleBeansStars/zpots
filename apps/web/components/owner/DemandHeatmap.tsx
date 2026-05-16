import type { DemandCell } from '@/lib/owner-mock-data';
import { lerpHex } from '@/lib/heatmap-color';

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const HOURS = Array.from({ length: 16 }, (_, i) => i + 7);

export function DemandHeatmap({ data }: { data: DemandCell[] }) {
  const max = data.reduce((m, c) => Math.max(m, c.predicted_bookings), 0) || 1;
  const cellByKey = new Map(data.map((c) => [`${c.day_of_week}-${c.hour}`, c]));

  return (
    <div>
      <div className="grid" style={{ gridTemplateColumns: '40px repeat(16, 1fr)', gap: 2 }}>
        <div></div>
        {HOURS.map((h) => (
          <div key={h} className="text-[9px] text-zpots-muted text-center">{h}</div>
        ))}
        {DAYS.map((day, dow) => (
          <FragmentRow key={day} day={day} cells={HOURS.map((h) => cellByKey.get(`${dow}-${h}`)!)} max={max} />
        ))}
      </div>
      <div className="flex items-center gap-2 mt-2 text-[10px] text-zpots-muted">
        <span>Low</span>
        <div className="flex-1 h-2 rounded-pill" style={{ background: `linear-gradient(90deg, ${lerpHex('#F2F9EE', '#1E4A00', 0)}, ${lerpHex('#F2F9EE', '#1E4A00', 1)})` }} />
        <span>High</span>
      </div>
    </div>
  );
}

function FragmentRow({ day, cells, max }: { day: string; cells: DemandCell[]; max: number }) {
  return (
    <>
      <div className="text-[10px] font-eyebrow text-zpots-muted self-center">{day}</div>
      {cells.map((c, i) => (
        <div
          key={i}
          title={c ? `${c.predicted_bookings.toFixed(2)} bookings` : ''}
          style={{
            aspectRatio: '1',
            background: c ? lerpHex('#F2F9EE', '#1E4A00', c.predicted_bookings / max) : '#fff',
            borderRadius: 3,
          }}
        />
      ))}
    </>
  );
}
