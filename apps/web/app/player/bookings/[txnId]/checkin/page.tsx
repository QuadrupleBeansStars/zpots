'use client';
import { useParams } from 'next/navigation';
import { QRCodeSVG } from 'qrcode.react';
import { useBookingStore } from '@/lib/booking-store';
import { fallbackCourt } from '@/lib/mock-data';
import Link from 'next/link';
import { formatDateFull, formatTimeRange } from '@/lib/format';
import { DarkHero } from '@/components/primitives/DarkHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

export default function CheckinPage() {
  const params = useParams<{ txnId: string }>();
  const storeBookings = useBookingStore((s) => s.bookings);
  const booking = storeBookings.find((b) => b.txn_id === params.txnId);
  const court = booking ? fallbackCourt(booking.court_id) : undefined;
  const today = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();

  if (!booking) {
    return (
      <div className="text-center py-10">
        <h1 className="font-geist font-bold text-title-lg text-ink-900">Booking not found</h1>
        <Link href="/player/bookings" className="text-body-sm text-ink-700 underline-offset-4 hover:underline mt-2 inline-block">
          ← My bookings
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 max-w-2xl mx-auto">
      <DarkHero glow="lime" className="p-8 text-center">
        <div className="text-label-sm text-lime/70 mb-3">CHECK-IN · TODAY {today}</div>
        <h1 className="font-geist font-bold text-display-md text-white leading-none tracking-tight">
          READY TO<br />PLAY?
        </h1>
        <p className="text-body-md text-white/60 mt-3">
          Show this QR code at the venue front desk to confirm your slot.
        </p>
      </DarkHero>

      <RevealOnScroll>
        <div className="bg-lime rounded-kp-card p-8 flex flex-col items-center gap-4">
          <QRCodeSVG value={`zpots:${booking.txn_id}`} size={220} />
          <div className="text-label-sm text-ink-900/70 font-geist-mono">#{booking.txn_id}</div>
        </div>
      </RevealOnScroll>

      <RevealOnScroll>
        <div className="bg-white rounded-kp-card shadow-float p-5 text-left">
          <div className="text-label-sm text-ink-700/60 mb-3">BOOKING DETAILS</div>
          <div className="font-geist font-bold text-title-md text-ink-900">{booking.court_name}</div>
          <div className="text-body-sm text-ink-700/60 mt-1">{formatDateFull(booking.date)}</div>
          <div className="text-body-sm text-ink-700/60">{formatTimeRange(booking.time_start, booking.time_end)}</div>
          {court && (
            <>
              <div className="border-t border-surface-med mt-4 pt-4">
                <div className="text-label-sm text-ink-700/60 mb-1">VENUE</div>
                <div className="text-body-sm text-ink-900">{court.address}</div>
                <div className="text-body-sm text-ink-700/60">{court.district}</div>
              </div>
            </>
          )}
          <div className="border-t border-surface-med mt-4 pt-4">
            <div className="text-label-sm text-ink-700/60 mb-1">TRANSACTION</div>
            <div className="font-geist-mono text-body-sm text-ink-900">{booking.txn_id}</div>
          </div>
        </div>
      </RevealOnScroll>

      <Link
        href={`/player/bookings/${booking.txn_id}/feedback`}
        className="text-body-sm text-ink-700 hover:text-ink-900 underline-offset-4 hover:underline text-center"
      >
        Leave feedback after your session →
      </Link>
    </div>
  );
}
