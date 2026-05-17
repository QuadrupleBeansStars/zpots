'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useBookingStore } from '@/lib/booking-store';
import { StarRating } from '@/components/player/StarRating';
import { FeedbackTagPicker } from '@/components/player/FeedbackTagPicker';
import { PageHero } from '@/components/primitives/PageHero';
import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

export default function FeedbackPage() {
  const params = useParams<{ txnId: string }>();
  const storeBookings = useBookingStore((s) => s.bookings);
  const booking = storeBookings.find((b) => b.txn_id === params.txnId);

  const [rating, setRating] = useState(0);
  const [tags, setTags] = useState<string[]>([]);
  const [text, setText] = useState('');
  const [submitted, setSubmitted] = useState(false);

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

  function submit(e: React.FormEvent) {
    e.preventDefault();
    console.info('[feedback]', { txn_id: booking!.txn_id, rating, tags, text });
    setSubmitted(true);
  }

  return (
    <div className="flex flex-col gap-6 max-w-xl mx-auto">
      <PageHero
        eyebrow={`LEAVE FEEDBACK · ${booking.court_name}`}
        headline="How was your game?"
        sub={`${booking.court_name} · ${booking.date} ${booking.time_start}`}
      />

      {submitted ? (
        <RevealOnScroll>
          <div className="bg-lime rounded-kp-card p-8 text-center">
            <div className="text-4xl">🙌</div>
            <h2 className="font-geist font-bold text-title-md text-ink-900 mt-3">Thanks for your feedback!</h2>
            <Link href="/player/bookings" className="text-body-sm text-ink-900 font-geist font-semibold mt-4 inline-block underline-offset-4 hover:underline">
              Back to bookings
            </Link>
          </div>
        </RevealOnScroll>
      ) : (
        <RevealOnScroll>
          <form onSubmit={submit} className="bg-white rounded-kp-card shadow-float p-6 space-y-5">
            <div>
              <div className="text-label-sm text-ink-700/60 mb-2">OVERALL RATING</div>
              <StarRating value={rating} onChange={setRating} />
            </div>
            <div>
              <div className="text-label-sm text-ink-700/60 mb-2">WHAT WORKED</div>
              <FeedbackTagPicker
                selected={tags}
                onToggle={(t) => setTags((s) => s.includes(t) ? s.filter((x) => x !== t) : [...s, t])}
              />
            </div>
            <div>
              <label className="text-label-sm text-ink-700/60 block mb-2">YOUR THOUGHTS</label>
              <textarea
                className="field-input"
                rows={4}
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Tell us more about your experience…"
              />
            </div>
            <button
              type="submit"
              disabled={rating === 0}
              className="w-full px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring disabled:opacity-50 disabled:scale-100"
            >
              Submit feedback
            </button>
          </form>
        </RevealOnScroll>
      )}
    </div>
  );
}
