import { RevenueBanner } from '@/components/owner/RevenueBanner';
import { StatusBadge, Eyebrow } from '@/components/Tags';
import { OWNER_BOOKINGS } from '@/lib/owner-mock-data';

const STATUS_TO_VARIANT: Record<string, 'confirmed' | 'completed' | 'cancelled'> = {
  BOOKED: 'confirmed',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
};

const RISK_BY_SPORT: Record<string, { tier: string; cls: 'confirmed' | 'progress' | 'cancelled' }> = {
  Padel:  { tier: 'Low',    cls: 'confirmed' },
  Tennis: { tier: 'Medium', cls: 'progress' },
  Soccer: { tier: 'High',   cls: 'cancelled' },
  Yoga:   { tier: 'Low',    cls: 'confirmed' },
};

export default function BookingDashboardPage() {
  return (
    <div className="flex flex-col gap-5">
      <h1 className="font-display text-3xl font-bold">Bookings</h1>

      <RevenueBanner
        total={4280}
        delta="+15.6% from yesterday · Upcoming"
        breakdown={[
          { label: 'MAIN ARENA',  amount: 1240 },
          { label: 'PADEL POD 2', amount:  890 },
          { label: 'INDOOR TURF', amount: 2150, highlight: true },
        ]}
      />

      <div className="flex gap-2">
        <button className="chip chip-selected">Today</button>
        <button className="chip chip-default">This Week</button>
        <button className="chip chip-default">Calendar</button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <select className="field-input"><option>All Venues</option><option>Main Arena</option><option>Padel Pod 2</option><option>Indoor Turf</option></select>
        <select className="field-input"><option>Time Descending</option><option>Time Ascending</option><option>Status</option></select>
      </div>

      <div className="grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 px-4 py-3">
        <Eyebrow>Customer</Eyebrow>
        <Eyebrow>Session info</Eyebrow>
        <Eyebrow>Status</Eyebrow>
        <Eyebrow>Risk</Eyebrow>
      </div>

      <div className="flex flex-col gap-2">
        {OWNER_BOOKINGS.map((b) => {
          const risk = RISK_BY_SPORT[b.sport] ?? { tier: 'Medium', cls: 'progress' as const };
          return (
            <div key={b.member_id} className="zpots-card grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 items-center p-3">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full text-white flex items-center justify-center font-semibold" style={{ background: b.avatar_color }}>{b.customer[0]}</div>
                <div>
                  <div className="font-semibold text-sm">{b.customer}</div>
                  <div className="text-xs text-zpots-muted">Member ID: {b.member_id}</div>
                </div>
              </div>
              <div>
                <div className="text-sm">🏟 {b.court} • {b.sport}</div>
                <div className="text-xs text-zpots-muted">🕐 {b.time}</div>
              </div>
              <StatusBadge status={STATUS_TO_VARIANT[b.status] ?? 'confirmed'}>{b.status}</StatusBadge>
              <StatusBadge status={risk.cls}>{risk.tier}</StatusBadge>
            </div>
          );
        })}
      </div>

      <div className="text-xs text-zpots-muted">SHOWING {OWNER_BOOKINGS.length} BOOKINGS · seeded demo data</div>
    </div>
  );
}
