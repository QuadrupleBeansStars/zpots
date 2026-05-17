'use client';
import Link from 'next/link';
import { useBookingStore } from '@/lib/booking-store';
import { currentUser } from '@/lib/auth-stub';
import { PageHero } from '@/components/primitives/PageHero';
import { NumberFlip } from '@/components/primitives/NumberFlip';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { formatDateShort } from '@/lib/format';

export default function MyBookingsPage() {
  const storeBookings = useBookingStore((s) => s.bookings);
  const all = [...storeBookings].sort((a, b) => b.date.localeCompare(a.date));

  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow="MY GAMES"
        headline={<><NumberFlip value={all.length} /> bookings.</>}
        sub={`${currentUser.name}, here are your upcoming and past sessions.`}
      />

      {all.length === 0 ? (
        <div className="bg-surface-low rounded-kp-card p-16 text-center">
          <div className="text-5xl">🎾</div>
          <h2 className="font-geist font-bold text-title-lg text-ink-900 mt-3">No bookings yet</h2>
          <p className="text-body-sm text-ink-700/60 mt-1">Start by searching for a court.</p>
          <Link
            href="/player/search"
            className="inline-block mt-4 px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
          >
            Find a Court
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-3">
          {all.map((bk, i) => (
            <RevealOnScroll key={bk.txn_id} delay={i * 60}>
              <div className="bg-white rounded-kp-card shadow-float p-4 flex gap-5 items-center">
                <div
                  className="w-32 h-20 rounded-kp-card flex items-center justify-center flex-shrink-0"
                  style={{ background: 'linear-gradient(135deg, #1a3a2a, #1a3a2acc)' }}
                >
                  <span className="text-2xl">🏸</span>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-geist font-bold text-body-md text-ink-900 truncate">{bk.court_name}</div>
                  <div className="text-body-sm text-ink-700/60 mt-1">
                    📅 {formatDateShort(bk.date)} &nbsp; 🕐 {bk.time_start} – {bk.time_end}
                  </div>
                  <div className="mt-2 flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded-kp-pill text-label-sm font-geist font-semibold ${
                      bk.status === 'CONFIRMED'
                        ? 'bg-lime text-ink-900'
                        : 'bg-surface-med text-ink-700'
                    }`}>
                      {bk.status}
                    </span>
                    <span className="text-body-sm text-ink-700/50">#{bk.txn_id}</span>
                  </div>
                </div>
                <Link
                  href={`/player/bookings/${bk.txn_id}/checkin`}
                  className="flex-shrink-0 px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
                >
                  🎫 View QR
                </Link>
              </div>
            </RevealOnScroll>
          ))}
        </div>
      )}
    </div>
  );
}
