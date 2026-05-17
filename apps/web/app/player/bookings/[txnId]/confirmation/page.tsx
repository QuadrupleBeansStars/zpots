'use client';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useBookingStore } from '@/lib/booking-store';
import { fallbackCourt } from '@/lib/mock-data';
import { Button } from '@/components/Button';
import { AITag, Eyebrow } from '@/components/Tags';
import { formatDateShort } from '@/lib/format';

export default function ConfirmationPage() {
  const params = useParams<{ txnId: string }>();
  const booking = useBookingStore((s) => s.getByTxn(params.txnId));
  const court = booking ? fallbackCourt(booking.court_id) : undefined;

  if (!booking) {
    return (
      <div className="text-center py-10">
        <h1 className="font-display text-xl">Booking not found</h1>
        <p className="text-zpots-muted text-sm mt-2">
          This confirmation may be from a different browser session.
        </p>
        <Link href="/player/bookings" className="text-zpots-moss mt-4 inline-block">
          ← View my bookings
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="text-center">
        <div className="w-14 h-14 rounded-full bg-zpots-lime mx-auto flex items-center justify-center text-3xl">✓</div>
        <h1 className="font-display text-4xl font-bold mt-3">Booking<br />Confirmed!</h1>
        <p className="text-zpots-muted mt-2 text-sm">
          You're all set for <strong>{booking.court_name}</strong>. Your court is waiting.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-8">
        <div>
          <Link href={`/player/bookings/${booking.txn_id}/checkin`}>
            <Button variant="primary" className="w-full justify-center">View My Bookings</Button>
          </Link>
          <Button variant="secondary" className="w-full justify-center mt-2">📅 Add to Calendar</Button>

          <div className="mt-4">
            <Eyebrow>Invite your team</Eyebrow>
            <p className="text-sm text-zpots-muted mt-1">Share the booking details and get ready for the match.</p>
            <div className="flex gap-2 mt-2">
              <Button variant="ghost">📲 Share</Button>
              <Button variant="ghost">📋 Copy</Button>
              <Button variant="ghost">✉️ Email</Button>
            </div>
          </div>
        </div>

        <aside className="zpots-card p-4">
          <Eyebrow>TRANSACTION ID</Eyebrow>
          <div className="font-display text-2xl font-bold mt-1">#{booking.txn_id}</div>

          {court && (
            <div
              className="rounded-card mt-3 p-4 text-white"
              style={{ background: `linear-gradient(135deg, ${court.color}, ${court.color}cc)` }}
            >
              {court.name}
            </div>
          )}

          <div className="mt-3">
            <Eyebrow>TIME SLOT</Eyebrow>
            <div className="font-display text-2xl font-bold mt-1">{booking.time_start} – {booking.time_end}</div>
            <div className="text-sm text-zpots-muted">{formatDateShort(booking.date)}</div>
          </div>

          {court && (
            <div className="mt-3">
              <Eyebrow>COURT DETAILS</Eyebrow>
              <div className="font-semibold mt-1">{court.address}</div>
              <div className="text-sm text-zpots-muted">{court.surface}</div>
            </div>
          )}
        </aside>
      </div>

      <div className="zpots-card p-4 mt-6">
        <div className="font-semibold">📒 Have questions about your booking?</div>
        <p className="text-sm text-zpots-muted mt-1">Ask about directions, parking, BTS access, and more.</p>
        <div className="flex gap-2 mt-2">
          <input className="field-input flex-1" placeholder="Ask about directions, parking..." />
          <Button variant="primary">Send</Button>
        </div>
      </div>
    </div>
  );
}
