'use client';
import Link from 'next/link';
import { Button } from '@/components/Button';
import { Eyebrow } from '@/components/Tags';
import { formatPrice } from '@/lib/format';

type Props = {
  courtId: string;
  date: string;
  timeStart: string | null;
  duration: number;
  pricePerHour: number;
};

export function BookingSummaryCard({ courtId, date, timeStart, duration, pricePerHour }: Props) {
  const ready = !!timeStart;
  const total = ready ? pricePerHour * duration : 0;
  const href = ready
    ? `/player/courts/${courtId}/book?date=${date}&time_start=${timeStart}&duration=${duration}`
    : '#';

  return (
    <aside className="zpots-card p-5 sticky top-4">
      <h3 className="font-display font-bold">BOOKING SUMMARY</h3>
      <div className="mt-3 text-sm space-y-1 text-zpots-muted">
        <div>📅 {date}</div>
        <div>🕐 {timeStart ? `${timeStart} (${duration} hr${duration > 1 ? 's' : ''})` : '-- : -- (select a slot)'}</div>
      </div>
      <div className="border-t border-zpots-mint mt-4 pt-3">
        <Eyebrow>TOTAL PRICE</Eyebrow>
        <div className="font-display text-3xl font-bold mt-1">{formatPrice(total)}</div>
        <div className="text-[11px] text-zpots-muted">INCL. TAXES</div>
      </div>
      {ready ? (
        <Link href={href} className="block mt-4">
          <Button variant="primary" className="w-full justify-center">PROCEED TO BOOKING →</Button>
        </Link>
      ) : (
        <Button variant="primary" disabled className="w-full justify-center mt-4 opacity-50">
          PROCEED TO BOOKING →
        </Button>
      )}
      <p className="text-[11px] text-zpots-muted text-center mt-3">Free cancellation up to 1 hr before</p>
    </aside>
  );
}
