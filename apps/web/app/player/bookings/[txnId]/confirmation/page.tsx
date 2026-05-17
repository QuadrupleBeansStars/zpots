'use client';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useBookingStore } from '@/lib/booking-store';
import { fallbackCourt } from '@/lib/mock-data';
import { PageHero } from '@/components/primitives/PageHero';
import { NumberFlip } from '@/components/primitives/NumberFlip';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';
import { formatDateShort } from '@/lib/format';

export default function ConfirmationPage() {
  const params = useParams<{ txnId: string }>();
  const booking = useBookingStore((s) => s.getByTxn(params.txnId));
  const court = booking ? fallbackCourt(booking.court_id) : undefined;

  if (!booking) {
    return (
      <div className="text-center py-10">
        <h1 className="font-geist font-bold text-title-lg text-ink-900">Booking not found</h1>
        <p className="text-body-sm text-ink-700/60 mt-2">
          This confirmation may be from a different browser session.
        </p>
        <Link href="/player/bookings" className="text-body-sm text-ink-700 underline-offset-4 hover:underline mt-4 inline-block">
          ← View my bookings
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 max-w-3xl mx-auto">
      <PageHero
        eyebrow="BOOKING CONFIRMED"
        headline={<>฿<NumberFlip value={booking.total_price} /></>}
        sub={`${booking.court_name} · ${formatDateShort(booking.date)} · ${booking.time_start} – ${booking.time_end}`}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <RevealOnScroll>
          <div className="flex flex-col gap-3">
            <Link
              href={`/player/bookings/${booking.txn_id}/checkin`}
              className="w-full text-center px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
            >
              View QR Code
            </Link>
            <button className="w-full text-center px-5 py-3 bg-surface-low text-ink-700 font-geist font-semibold text-body-sm rounded-kp-pill hover:bg-surface-med transition-colors duration-quick focus-ring">
              📅 Add to Calendar
            </button>

            <div className="mt-2">
              <div className="text-label-sm text-ink-700/60 mb-2">INVITE YOUR TEAM</div>
              <p className="text-body-sm text-ink-700/60">Share the booking details and get ready for the match.</p>
              <div className="flex gap-2 mt-3">
                {['📲 Share', '📋 Copy', '✉️ Email'].map((label) => (
                  <button
                    key={label}
                    className="px-3 py-1.5 bg-surface-low text-ink-700 text-body-sm rounded-kp-pill hover:bg-surface-med transition-colors duration-quick focus-ring"
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </RevealOnScroll>

        <RevealOnScroll delay={100}>
          <aside className="bg-white rounded-kp-card shadow-float p-5">
            <div className="text-label-sm text-ink-700/60">TRANSACTION ID</div>
            <div className="font-geist-mono font-bold text-title-md text-ink-900 mt-1">#{booking.txn_id}</div>

            {court && (
              <div
                className="rounded-kp-card mt-4 p-4 text-white"
                style={{ background: `linear-gradient(135deg, ${court.color}, ${court.color}cc)` }}
              >
                <div className="font-geist font-bold text-title-md">{court.name}</div>
              </div>
            )}

            <div className="mt-4">
              <div className="text-label-sm text-ink-700/60">TIME SLOT</div>
              <div className="font-geist font-bold text-title-lg text-ink-900 mt-1">{booking.time_start} – {booking.time_end}</div>
              <div className="text-body-sm text-ink-700/60">{formatDateShort(booking.date)}</div>
            </div>

            {court && (
              <div className="mt-4">
                <div className="text-label-sm text-ink-700/60">COURT DETAILS</div>
                <div className="font-geist font-semibold text-body-sm text-ink-900 mt-1">{court.address}</div>
                <div className="text-body-sm text-ink-700/60">{court.surface}</div>
              </div>
            )}
          </aside>
        </RevealOnScroll>
      </div>

      <RevealOnScroll delay={200}>
        <div className="bg-white rounded-kp-card shadow-float p-5">
          <div className="font-geist font-bold text-body-md text-ink-900">📒 Have questions about your booking?</div>
          <p className="text-body-sm text-ink-700/60 mt-1">Ask about directions, parking, BTS access, and more.</p>
          <div className="flex gap-2 mt-3">
            <input className="field-input flex-1" placeholder="Ask about directions, parking..." />
            <button className="px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring">
              Send
            </button>
          </div>
        </div>
      </RevealOnScroll>
    </div>
  );
}
