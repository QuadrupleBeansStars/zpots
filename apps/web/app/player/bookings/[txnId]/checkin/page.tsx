'use client';
import { useParams } from 'next/navigation';
import { QRCodeSVG } from 'qrcode.react';
import { useBookingStore } from '@/lib/booking-store';
import { fallbackCourt } from '@/lib/mock-data';
import { Eyebrow } from '@/components/Tags';
import Link from 'next/link';
import { formatDateFull, formatTimeRange } from '@/lib/format';

export default function CheckinPage() {
  const params = useParams<{ txnId: string }>();
  const storeBookings = useBookingStore((s) => s.bookings);
  const booking = storeBookings.find((b) => b.txn_id === params.txnId);
  const court = booking ? fallbackCourt(booking.court_id) : undefined;

  if (!booking) {
    return (
      <div className="text-center py-10">
        <h1 className="font-display text-xl">Booking not found</h1>
        <Link href="/player/bookings" className="text-zpots-moss text-sm mt-2 inline-block">← My bookings</Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto text-center">
      <Eyebrow>CHECK IN AT VENUE</Eyebrow>
      <h1 className="font-display text-4xl font-bold mt-3">READY TO<br />PLAY?</h1>
      <p className="text-sm text-zpots-muted mt-2">
        Show this QR code at the venue front desk to confirm your slot.
      </p>

      <div className="zpots-card p-8 mt-6 inline-block">
        <QRCodeSVG value={`zpots:${booking.txn_id}`} size={220} />
      </div>

      <div className="zpots-card-surface p-5 mt-6 text-left">
        <Eyebrow>BOOKING DETAILS</Eyebrow>
        <div className="font-display text-lg font-bold mt-2">{booking.court_name}</div>
        <div className="text-sm text-zpots-muted">{formatDateFull(booking.date)}</div>
        <div className="text-sm text-zpots-muted">{formatTimeRange(booking.time_start, booking.time_end)}</div>
        {court && (
          <>
            <div className="border-t border-zpots-mint mt-3 pt-3">
              <Eyebrow>VENUE</Eyebrow>
              <div className="text-sm">{court.address}</div>
              <div className="text-xs text-zpots-muted">{court.district}</div>
            </div>
          </>
        )}
        <div className="border-t border-zpots-mint mt-3 pt-3">
          <Eyebrow>TRANSACTION</Eyebrow>
          <div className="text-sm font-mono">{booking.txn_id}</div>
        </div>
      </div>

      <Link href={`/player/bookings/${booking.txn_id}/feedback`} className="inline-block mt-6">
        <span className="text-sm text-zpots-moss">Leave feedback after your session →</span>
      </Link>
    </div>
  );
}
