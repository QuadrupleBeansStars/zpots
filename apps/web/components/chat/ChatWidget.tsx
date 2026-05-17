'use client';
import { useEffect, useRef, useState } from 'react';

import { Button } from '@/components/Button';
import { Icon } from '@/components/Icon';
import { ChatBubble } from './ChatBubble';
import { ConfirmDraft } from './ConfirmDraft';
import { currentUser, currentOwner } from '@/lib/auth-stub';
import { useBookingStore } from '@/lib/booking-store';
import { chatOwner, chatPlayer } from '@/lib/chat-client';
import type { ChatDraft, ChatMessage } from '@/lib/chat-types';

type Props = { role: 'player' | 'owner' };

const PLAYER_WELCOME =
  "Hi! I can find courts, check availability, or book you a slot. " +
  "Try **find badminton near Sukhumvit Friday under 400 baht** or **book bbc-01 tomorrow 6pm**.";

const OWNER_WELCOME =
  "Hi! Ask me about revenue, no-show risk, or busiest hours. " +
  "Try **what's my revenue this week?** or **which upcoming bookings are highest risk?**";

export function ChatWidget({ role }: Props) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [pendingDraft, setPendingDraft] = useState<ChatDraft | null>(null);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const user = role === 'player' ? currentUser : currentOwner;
  const addBookingAsync = useBookingStore((s) => s.addBooking);
  const cancelBookingAsync = useBookingStore((s) => s.cancelBooking);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, busy]);

  const visible = messages.filter(
    (m) => m.role === 'user' || (m.role === 'assistant' && m.content),
  );

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    setInput('');
    setError(null);
    setPendingDraft(null);

    const userMsg: ChatMessage = { role: 'user', content: text };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setBusy(true);

    try {
      if (role === 'player') {
        const res = await chatPlayer({ messages: nextMessages, user });
        setMessages(res.history);
        setPendingDraft(res.draft);
      } else {
        const res = await chatOwner({ messages: nextMessages, user });
        setMessages(res.history);
      }
    } catch (e) {
      setError("Couldn't reach the assistant. Try again?");
    } finally {
      setBusy(false);
    }
  }

  async function handleConfirm() {
    if (!pendingDraft) return;
    try {
      if (pendingDraft.kind === 'booking_draft') {
        const txn = await addBookingAsync(user.id, {
          court_id: pendingDraft.court_id,
          court_name: pendingDraft.court_name,
          date: pendingDraft.date,
          time_start: pendingDraft.time_start,
          time_end: pendingDraft.time_end,
          duration: pendingDraft.duration,
          total_price: pendingDraft.total_price,
        });
        setMessages((m) => [
          ...m,
          { role: 'assistant', content: `✅ Booked! Transaction id **${txn}**.` },
        ]);
      } else {
        await cancelBookingAsync(pendingDraft.txn_id);
        setMessages((m) => [...m, { role: 'assistant', content: '✅ Cancelled.' }]);
      }
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: 'assistant', content: "Sorry — that didn't go through. Try again?" },
      ]);
    } finally {
      setPendingDraft(null);
    }
  }

  function handleDecline() {
    setMessages((m) => [...m, { role: 'assistant', content: 'Okay, no changes made.' }]);
    setPendingDraft(null);
  }

  const welcome = role === 'player' ? PLAYER_WELCOME : OWNER_WELCOME;

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-label={open ? 'Close chat' : 'Open chat'}
        className="fixed bottom-6 right-6 z-50 w-16 h-16 rounded-full bg-zpots-lime text-zpots-forest shadow-card-lift flex items-center justify-center text-2xl hover:scale-105 transition-transform"
      >
        {open ? '✕' : '💬'}
      </button>

      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-[400px] h-[600px] bg-white rounded-card shadow-card-lift flex flex-col overflow-hidden border border-zpots-mint">
          <header className="px-4 py-3 border-b border-zpots-mint flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="smart_toy" style={{ fontSize: 18, color: '#2E6B00' }} />
              <span className="font-display font-bold text-sm">
                {role === 'player' ? 'ZPOTS Player Assistant' : 'ZPOTS Owner Assistant'}
              </span>
            </div>
            <button type="button" onClick={() => setOpen(false)} aria-label="Close chat">
              <Icon name="close" style={{ fontSize: 18, color: '#3d4455' }} />
            </button>
          </header>

          <div ref={scrollRef} className="flex-1 overflow-y-auto p-3 flex flex-col gap-3 bg-zpots-surface">
            {visible.length === 0 && <ChatBubble role="assistant">{welcome}</ChatBubble>}
            {visible.map((m, i) => (
              <ChatBubble key={i} role={m.role as 'user' | 'assistant'}>
                {m.content ?? ''}
              </ChatBubble>
            ))}
            {pendingDraft && (
              <ConfirmDraft
                draft={pendingDraft}
                onConfirm={handleConfirm}
                onCancel={handleDecline}
                disabled={busy}
              />
            )}
            {busy && <div className="text-xs text-zpots-muted italic px-2">Thinking…</div>}
            {error && <div className="text-xs text-red-700 px-2">{error}</div>}
          </div>

          <form
            className="border-t border-zpots-mint p-2 flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              send();
            }}
          >
            <input
              className="field-input flex-1"
              placeholder={role === 'player' ? 'Ask about courts or bookings…' : 'Ask about your venue…'}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={busy}
            />
            <Button variant="primary" type="submit" disabled={busy || !input.trim()}>
              Send
            </Button>
          </form>
        </div>
      )}
    </>
  );
}
