'use client';
import { useRouter, useSearchParams, useParams } from 'next/navigation';
import { useState, useEffect, Suspense } from 'react';
import { getCourt } from '@/lib/data-client';
import { fallbackCourt } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { useBookingStore, generateTxnId } from '@/lib/booking-store';
import { Button } from '@/components/Button';
import { AITag, Eyebrow } from '@/components/Tags';
import { formatPrice, formatDateShort } from '@/lib/format';

function BookingPageInner() {
  const router = useRouter();
  const params = useParams<{ id: string }>();
  const search = useSearchParams();

  const [court, setCourt] = useState<Court | undefined>(undefined);
  const [courtLoading, setCourtLoading] = useState(true);

  useEffect(() => {
    getCourt(params.id)
      .then(setCourt)
      .catch(() => setCourt(fallbackCourt(params.id)))
      .finally(() => setCourtLoading(false));
  }, [params.id]);

  const date = search.get('date');
  const timeStart = search.get('time_start');
  const duration = parseInt(search.get('duration') ?? '1', 10);

  const [payMethod, setPayMethod] = useState<'card' | 'promptpay' | 'apple'>('card');

  if (courtLoading) {
    return <div className="text-zpots-muted text-sm py-10 text-center">Loading…</div>;
  }

  if (!court || !date || !timeStart) {
    return (
      <div className="text-zpots-muted">
        Missing booking details. <a href="/player/search" className="text-zpots-moss">Back to search.</a>
      </div>
    );
  }

  const startH = parseInt(timeStart.slice(0, 2), 10);
  const timeEnd = `${String(startH + duration).padStart(2, '0')}:00`;
  const basePrice = court.price_per_hour * duration;
  const discount = Math.round(basePrice * 0.07);
  const serviceFee = 25;
  const total = basePrice - discount + serviceFee;

  function confirm() {
    const txnId = generateTxnId();
    useBookingStore.getState().addBookingWithTxn(txnId, {
      court_id: court!.id,
      court_name: court!.name,
      date: date!,
      time_start: timeStart!,
      time_end: timeEnd,
      duration,
      total_price: total,
    });
    router.push(`/player/bookings/${txnId}/confirmation`);
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr] gap-6 max-w-4xl mx-auto">
      {/* Left: session details + payment */}
      <div className="space-y-4">
        <a href={`/player/courts/${court.id}`} className="text-sm text-zpots-moss">← Back</a>
        <Eyebrow>SECURE CHECKOUT</Eyebrow>

        <div
          className="rounded-card p-5 text-white"
          style={{ background: `linear-gradient(135deg, ${court.color}, ${court.color}cc)` }}
        >
          <h2 className="font-display text-2xl font-bold">{court.name}</h2>
          <p className="text-sm opacity-90">📍 {court.district}</p>
        </div>

        <div className="zpots-card-surface p-4">
          <Eyebrow>SELECTED SESSION</Eyebrow>
          <div className="font-semibold mt-1">{court.name} | {formatDateShort(date)}</div>
          <div className="text-sm text-zpots-muted">🕐 {timeStart} – {timeEnd} • {duration * 60} Minutes ({duration} hr{duration > 1 ? 's' : ''})</div>
        </div>

        <div>
          <div className="font-semibold mb-2">Payment Method</div>
          <label className="flex items-center gap-2 mb-1">
            <input type="radio" checked={payMethod === 'card'} onChange={() => setPayMethod('card')} />
            💳 Credit/Debit — Visa, Mastercard, JCB
          </label>
          <label className="flex items-center gap-2 mb-1">
            <input type="radio" checked={payMethod === 'promptpay'} onChange={() => setPayMethod('promptpay')} />
            🏧 PromptPay — Local Thai Transfer
          </label>
          <label className="flex items-center gap-2">
            <input type="radio" checked={payMethod === 'apple'} onChange={() => setPayMethod('apple')} />
            🍎 Apple Pay — Express Checkout
          </label>
        </div>
      </div>

      {/* Right: summary + confirm */}
      <aside className="zpots-card p-5 h-fit">
        <h3 className="font-display font-bold mb-3">Summary</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between"><span>Base price ({duration} hr{duration > 1 ? 's' : ''})</span><span>{formatPrice(basePrice)}</span></div>
          <div className="flex justify-between text-zpots-moss">
            <span className="flex items-center gap-1"><AITag>AI APPLIED</AITag> Dynamic Discount</span>
            <span>-{formatPrice(discount)}</span>
          </div>
          <div className="flex justify-between"><span>Service Fee</span><span>{formatPrice(serviceFee)}</span></div>
        </div>

        <div className="border-t border-zpots-mint mt-4 pt-3">
          <Eyebrow>TOTAL AMOUNT</Eyebrow>
          <div className="font-display text-3xl font-bold mt-1">{formatPrice(total)}</div>
          <div className="text-[11px] text-zpots-muted">includes taxes &amp; fees</div>
        </div>

        <Button variant="primary" onClick={confirm} className="w-full justify-center mt-4">
          Confirm &amp; Pay →
        </Button>
        <div className="text-[11px] text-zpots-muted text-center mt-2">🔒 BANK-GRADE ENCRYPTED</div>

        <div className="zpots-card-surface mt-4 p-3">
          <AITag>ZPOTS AI SUGGESTION</AITag>
          <p className="text-xs mt-2 italic text-zpots-muted">"This time slot is typically quieter. You'll likely have more space for warm-ups on Court 01."</p>
        </div>
      </aside>
    </div>
  );
}

export default function BookingPage() {
  return (
    <Suspense fallback={null}>
      <BookingPageInner />
    </Suspense>
  );
}
