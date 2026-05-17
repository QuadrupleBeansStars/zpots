'use client';
import { useRouter, useSearchParams, useParams } from 'next/navigation';
import { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { getCourt } from '@/lib/data-client';
import { fallbackCourt } from '@/lib/mock-data';
import type { Court } from '@/lib/types';
import { useBookingStore, generateTxnId } from '@/lib/booking-store';
import { DarkHero } from '@/components/primitives/DarkHero';
import { PulseAccent } from '@/components/primitives/PulseAccent';
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
    return <div className="text-ink-700/60 text-body-sm py-10 text-center">Loading…</div>;
  }

  if (!court || !date || !timeStart) {
    return (
      <div className="text-ink-700/60 text-body-sm">
        Missing booking details. <Link href="/player/search" className="text-ink-900 underline">Back to search.</Link>
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
    <div className="flex flex-col gap-6 max-w-4xl mx-auto">
      <Link href={`/player/courts/${court.id}`} className="text-body-sm text-ink-700 hover:text-ink-900 underline-offset-4 hover:underline">
        ← Back
      </Link>

      <DarkHero glow="lime" className="p-8">
        <div className="text-label-sm text-lime/70 mb-2">SECURE CHECKOUT</div>
        <h1 className="font-geist font-bold text-display-md text-white leading-none tracking-tight">
          {court.name}
        </h1>
        <p className="mt-2 text-body-md text-white/60">📍 {court.district}</p>
        <div className="mt-3 flex gap-3 flex-wrap text-body-sm text-white/70">
          <span>🕐 {timeStart} – {timeEnd}</span>
          <span>·</span>
          <span>{formatDateShort(date)}</span>
          <span>·</span>
          <span>{duration} hr{duration > 1 ? 's' : ''}</span>
        </div>
      </DarkHero>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr] gap-6">
        <div className="space-y-4">
          <div className="bg-white rounded-kp-card shadow-float p-5">
            <div className="text-label-sm text-ink-700/60 mb-3">PAYMENT METHOD</div>
            <div className="space-y-3">
              {[
                { id: 'card' as const, label: '💳 Credit/Debit — Visa, Mastercard, JCB' },
                { id: 'promptpay' as const, label: '🏧 PromptPay — Local Thai Transfer' },
                { id: 'apple' as const, label: '🍎 Apple Pay — Express Checkout' },
              ].map((m) => (
                <label key={m.id} className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="radio"
                    name="payMethod"
                    checked={payMethod === m.id}
                    onChange={() => setPayMethod(m.id)}
                    className="accent-lime"
                  />
                  <span className="text-body-sm text-ink-900">{m.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        <aside className="bg-white rounded-kp-card shadow-float p-5 h-fit">
          <h3 className="font-geist font-bold text-title-md text-ink-900 mb-4">Summary</h3>
          <div className="space-y-2 text-body-sm">
            <div className="flex justify-between text-ink-700">
              <span>Base price ({duration} hr{duration > 1 ? 's' : ''})</span>
              <span className="font-geist font-semibold text-ink-900">{formatPrice(basePrice)}</span>
            </div>
            <div className="flex justify-between text-ink-700">
              <span className="flex items-center gap-1">
                <span className="px-2 py-0.5 bg-lime text-ink-900 text-label-sm font-geist font-semibold rounded-kp-pill">AI</span>
                Dynamic Discount
              </span>
              <span className="font-geist font-semibold text-lime-deep">-{formatPrice(discount)}</span>
            </div>
            <div className="flex justify-between text-ink-700">
              <span>Service Fee</span>
              <span className="font-geist font-semibold text-ink-900">{formatPrice(serviceFee)}</span>
            </div>
          </div>

          <div className="border-t border-surface-med mt-4 pt-4">
            <div className="text-label-sm text-ink-700/60">TOTAL AMOUNT</div>
            <div className="font-geist font-bold text-display-md text-ink-900 mt-1">{formatPrice(total)}</div>
            <div className="text-body-sm text-ink-700/60 mt-0.5">includes taxes & fees</div>
          </div>

          <PulseAccent>
            <button
              onClick={confirm}
              className="w-full px-5 py-3.5 bg-lime text-ink-900 font-geist font-bold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring mt-4"
            >
              Confirm & Pay →
            </button>
          </PulseAccent>
          <div className="text-body-sm text-ink-700/60 text-center mt-2">🔒 BANK-GRADE ENCRYPTED</div>

          <div className="bg-surface-low rounded-kp-card p-3 mt-4">
            <span className="px-2 py-0.5 bg-lime text-ink-900 text-label-sm font-geist font-semibold rounded-kp-pill">AI TIP</span>
            <p className="text-body-sm text-ink-700/70 mt-2 italic">"This time slot is typically quieter. You'll likely have more space for warm-ups on Court 01."</p>
          </div>
        </aside>
      </div>
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
