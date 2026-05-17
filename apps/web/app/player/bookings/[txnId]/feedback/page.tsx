'use client';
import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useBookingStore } from '@/lib/booking-store';
import { StarRating } from '@/components/player/StarRating';
import { FeedbackTagPicker } from '@/components/player/FeedbackTagPicker';
import { Button } from '@/components/Button';
import { Eyebrow } from '@/components/Tags';

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
        <h1 className="font-display text-xl">Booking not found</h1>
        <Link href="/player/bookings" className="text-zpots-moss text-sm mt-2 inline-block">← My bookings</Link>
      </div>
    );
  }

  function submit(e: React.FormEvent) {
    e.preventDefault();
    console.info('[feedback]', { txn_id: booking!.txn_id, rating, tags, text });
    setSubmitted(true);
  }

  return (
    <div className="max-w-xl mx-auto">
      <Link href="/player/bookings" className="text-sm text-zpots-moss">← My bookings</Link>
      <h1 className="font-display text-3xl font-bold mt-3">Rate your session</h1>
      <p className="text-sm text-zpots-muted">{booking.court_name} • {booking.date} {booking.time_start}</p>

      {submitted ? (
        <div className="zpots-card-lime p-6 mt-6 text-center">
          <div className="text-3xl">🙌</div>
          <h2 className="font-display font-bold text-lg mt-2">Thanks for your feedback!</h2>
          <Link href="/player/bookings" className="text-sm text-zpots-forest font-semibold mt-3 inline-block">Back to bookings</Link>
        </div>
      ) : (
        <form onSubmit={submit} className="space-y-5 mt-5">
          <div>
            <Eyebrow>OVERALL RATING</Eyebrow>
            <div className="mt-2"><StarRating value={rating} onChange={setRating} /></div>
          </div>
          <div>
            <Eyebrow>WHAT WORKED</Eyebrow>
            <div className="mt-2"><FeedbackTagPicker selected={tags} onToggle={(t) => setTags((s) => s.includes(t) ? s.filter((x) => x !== t) : [...s, t])} /></div>
          </div>
          <div>
            <label className="field-label">YOUR THOUGHTS</label>
            <textarea
              className="field-input"
              rows={4}
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Tell us more about your experience…"
            />
          </div>
          <Button variant="primary" type="submit" className="w-full justify-center" disabled={rating === 0}>
            Submit feedback
          </Button>
        </form>
      )}
    </div>
  );
}
