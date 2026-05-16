import Link from 'next/link';
import { KpiCard } from '@/components/KpiCard';
import { Button } from '@/components/Button';
import { Eyebrow, AITag, StatusBadge } from '@/components/Tags';
import { UtilizationBars } from '@/components/charts/UtilizationBars';
import { OWNER_VENUES, WEEKLY_UTILIZATION, TODAYS_BOOKINGS } from '@/lib/owner-mock-data';
import { currentOwner } from '@/lib/auth-stub';
import { formatPrice } from '@/lib/format';

const STATUS_VARIANT: Record<string, 'confirmed' | 'progress' | 'completed' | 'cancelled'> = {
  CONFIRMED: 'confirmed',
  'IN PROGRESS': 'progress',
  UPCOMING: 'completed',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
};

export default function OwnerDashboard() {
  // UtilizationBars expects Record<string, number> — convert the array
  const utilizationData = Object.fromEntries(
    WEEKLY_UTILIZATION.map((w) => [w.day, w.pct])
  );

  return (
    <div className="flex flex-col gap-6">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="font-display text-3xl font-bold">Venue Performance</h1>
          <p className="text-sm text-zpots-muted">
            Real-time metrics for your Bangkok sports facilities. Welcome, {currentOwner.name}.
          </p>
        </div>
        <Link href="/owner/venues/new">
          <Button variant="primary" icon="add_circle">Add Court</Button>
        </Link>
      </header>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="TOTAL BOOKINGS" value="128" delta="↗ +12%" icon="📅" />
        <KpiCard label="TOTAL REVENUE" value={`${formatPrice(64500)} THB`} delta="October 2024" icon="💰" />
        <KpiCard label="AVG UTILIZATION" value="72%" icon="📊" />
        <KpiCard label="TOP RATED COURT" value="Court 3" delta="4.8 ⭐ (142 reviews)" icon="⭐" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-4">
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Utilization Trends</h3>
          <UtilizationBars data={utilizationData} />
        </div>
        <div className="zpots-card-lime p-5">
          <AITag>AI REVENUE OPTIMIZER</AITag>
          <h3 className="font-display text-lg font-bold mt-2" style={{ color: '#1a2600' }}>
            Friday demand is up by 30%.
          </h3>
          <p className="text-sm mt-2" style={{ color: '#1a2600' }}>
            Consider raising prices for 18:00–21:00 slots to maximize revenue.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-4">
        <div>
          <h3 className="font-semibold mb-3">Today&apos;s Bookings</h3>
          <div className="flex flex-col gap-2">
            {TODAYS_BOOKINGS.map((b) => (
              <div key={b.title} className="zpots-card p-4 flex items-center gap-5">
                <div>
                  <div className="font-display text-lg font-bold">{b.time}</div>
                  <Eyebrow>{b.type}</Eyebrow>
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-sm">{b.title}</div>
                  <div className="text-xs text-zpots-muted">Customer: {b.customer} · {b.venue}</div>
                </div>
                <StatusBadge status={STATUS_VARIANT[b.status] ?? 'confirmed'}>{b.status}</StatusBadge>
              </div>
            ))}
          </div>
          <Link href="/owner/bookings" className="inline-block mt-3 text-sm text-zpots-moss">
            View All Bookings →
          </Link>
        </div>

        <div>
          <div className="flex justify-between mb-3">
            <h3 className="font-semibold">Manage Venues</h3>
            <span className="font-eyebrow text-[10px] text-zpots-muted">{OWNER_VENUES.length} LOCATIONS</span>
          </div>
          <div className="flex flex-col gap-2">
            {OWNER_VENUES.map((v) => (
              <div key={v.id} className="zpots-card flex items-stretch overflow-hidden min-h-[64px]">
                <div className="w-1.5" style={{ background: `linear-gradient(180deg,${v.color},${v.color}cc)` }} />
                <div className="flex-1 p-3">
                  <div className="text-sm font-semibold">{v.name}</div>
                  <Eyebrow>{v.location}</Eyebrow>
                  <div className="flex justify-between text-xs mt-1">
                    <span className="text-zpots-muted">{v.courts_count} courts</span>
                    <span className="font-display text-zpots-moss">{formatPrice(v.revenue_today)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
