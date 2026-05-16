'use client';
import Link from 'next/link';
import { useBookingStore } from '@/lib/booking-store';
import { SEEDED_BOOKINGS } from '@/lib/mock-data';
import { currentUser } from '@/lib/auth-stub';
import { StatusBadge } from '@/components/Tags';
import { Button } from '@/components/Button';
import { formatDateShort } from '@/lib/format';

export default function MyBookingsPage() {
  const storeBookings = useBookingStore((s) => s.bookings);
  const all = [...storeBookings, ...SEEDED_BOOKINGS].sort((a, b) =>
    b.date.localeCompare(a.date),
  );

  return (
    <div>
      <h1 className="font-display text-3xl font-bold">My Bookings</h1>
      <p className="text-sm text-zpots-muted">
        Welcome back, {currentUser.name}. Here are your upcoming and past sessions.
      </p>

      {all.length === 0 ? (
        <div className="zpots-card-surface text-center p-16 mt-6 rounded-card">
          <div className="text-5xl">🎾</div>
          <h2 className="font-display text-xl font-bold mt-3">No bookings yet</h2>
          <p className="text-sm text-zpots-muted mt-1">Start by searching for a court.</p>
          <Link href="/player/search" className="inline-block mt-3">
            <Button variant="primary">Find a Court</Button>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-3 mt-6">
          {all.map((bk) => (
            <div key={bk.txn_id} className="zpots-card p-4 flex gap-5 items-center">
              <div
                className="w-32 h-20 rounded-card flex items-center justify-center"
                style={{ background: `linear-gradient(135deg, #1a3a2a, #1a3a2acc)` }}
              >
                <span className="text-2xl">🏸</span>
              </div>
              <div className="flex-1">
                <div className="font-bold">{bk.court_name}</div>
                <div className="text-sm text-zpots-muted mt-1">
                  📅 {formatDateShort(bk.date)} &nbsp; 🕐 {bk.time_start} – {bk.time_end}
                </div>
                <div className="mt-2 flex items-center gap-2">
                  <StatusBadge status={bk.status === 'CONFIRMED' ? 'confirmed' : 'cancelled'}>
                    {bk.status}
                  </StatusBadge>
                  <span className="text-xs text-zpots-muted">Booking #{bk.txn_id}</span>
                </div>
              </div>
              <Link href={`/player/bookings/${bk.txn_id}/checkin`}>
                <Button variant="primary">🎫 View QR</Button>
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
