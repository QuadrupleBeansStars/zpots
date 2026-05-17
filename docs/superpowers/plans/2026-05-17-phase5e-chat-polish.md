# Phase 5e — Chat Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Autonomous per [[feedback-design-revamp-autonomy]].

**Goal:** Apply KP+Motion to the floating chat (launcher + panel + bubbles + confirm draft). No backend or API changes.

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase5e-chat-polish-design.md`
**Branch:** `feat/nextjs-phase5e` off main

---

## Task 0: Branch + baseline

- [ ] `git checkout main && git pull && git checkout -b feat/nextjs-phase5e`
- [ ] `cd apps/web && pnpm test:unit` → **47 passed**

---

## Task 1: ChatBubble

**File:** `apps/web/components/chat/ChatBubble.tsx`

- [ ] Replace with:

```tsx
import Markdown from 'react-markdown';

type Props = {
  role: 'user' | 'assistant';
  children: React.ReactNode;
};

export function ChatBubble({ role, children }: Props) {
  const isUser = role === 'user';
  return (
    <>
      <style>{`
        @keyframes chat-bubble-in {
          from { opacity: 0; transform: translateY(4px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .chat-bubble-in { animation: chat-bubble-in var(--dur-quick, 220ms) var(--ease-precision, cubic-bezier(0.16,1,0.3,1)); }
        @media (prefers-reduced-motion: reduce) { .chat-bubble-in { animation: none; } }
      `}</style>
      <div className={`flex chat-bubble-in ${isUser ? 'justify-end' : 'justify-start'}`}>
        <div
          className={[
            'max-w-[85%] rounded-kp-card px-3 py-2 text-body-sm',
            isUser
              ? 'bg-lime text-ink-900 font-geist'
              : 'bg-white shadow-float text-ink-900 font-geist',
          ].join(' ')}
        >
          {typeof children === 'string' ? (
            <div className="prose prose-sm max-w-none whitespace-pre-wrap">
              <Markdown>{children}</Markdown>
            </div>
          ) : (
            children
          )}
        </div>
      </div>
    </>
  );
}
```

- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): ChatBubble → KP+Motion (lime user, glass assistant, fade-up)`

---

## Task 2: ConfirmDraft

**File:** `apps/web/components/chat/ConfirmDraft.tsx`

- [ ] Replace with:

```tsx
'use client';
import { formatPrice } from '@/lib/format';
import { PulseAccent } from '@/components/primitives/PulseAccent';
import type { ChatDraft } from '@/lib/chat-types';

type Props = {
  draft: ChatDraft;
  onConfirm: () => void;
  onCancel: () => void;
  disabled?: boolean;
};

export function ConfirmDraft({ draft, onConfirm, onCancel, disabled }: Props) {
  return (
    <div className="bg-surface-low rounded-kp-card p-4 text-body-sm mt-1">
      {draft.kind === 'booking_draft' ? (
        <div className="text-ink-900 font-geist">
          📌 Confirm booking:{' '}
          <strong>{draft.court_name}</strong> on {draft.date} {draft.time_start}–{draft.time_end} for{' '}
          <strong className="font-geist-mono">{formatPrice(draft.total_price)}</strong>?
        </div>
      ) : (
        <div className="text-ink-900 font-geist">
          ⚠️ Cancel booking{' '}
          <strong className="font-geist-mono">{draft.txn_id}</strong> at {draft.court_name} on {draft.date} {draft.time_start}?
        </div>
      )}
      <div className="flex gap-2 mt-3">
        <PulseAccent className="!rounded-kp-pill">
          <button
            type="button"
            onClick={onConfirm}
            disabled={disabled}
            className="px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring disabled:opacity-60"
          >
            Confirm
          </button>
        </PulseAccent>
        <button
          type="button"
          onClick={onCancel}
          disabled={disabled}
          className="px-4 py-2 bg-white text-ink-700 font-geist font-semibold text-body-sm rounded-kp-pill hover:bg-surface-med transition-colors duration-quick focus-ring disabled:opacity-60"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
```

- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): ConfirmDraft → KP+Motion (PulseAccent confirm)`

---

## Task 3: ChatWidget — launcher, panel, header, input

**File:** `apps/web/components/chat/ChatWidget.tsx`

Major visual update with no logic changes. Replace the file with:

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';

import { Icon } from '@/components/Icon';
import { ChatBubble } from './ChatBubble';
import { ConfirmDraft } from './ConfirmDraft';
import { currentUser, currentOwner } from '@/lib/auth-stub';
import { useBookingStore } from '@/lib/booking-store';
import { chatOwner, chatPlayer } from '@/lib/chat-client';
import type { ChatDraft, ChatMessage } from '@/lib/chat-types';
import { PulseAccent } from '@/components/primitives/PulseAccent';

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
      <style>{`
        @keyframes chat-panel-in {
          from { opacity: 0; transform: scale(0.94); }
          to   { opacity: 1; transform: scale(1); }
        }
        .chat-panel-in { animation: chat-panel-in var(--dur-smooth, 360ms) var(--ease-precision, cubic-bezier(0.16,1,0.3,1)); transform-origin: bottom right; }
        @media (prefers-reduced-motion: reduce) { .chat-panel-in { animation: none; } }

        @keyframes chat-think-bounce {
          0%,80%,100% { transform: scale(0.6); opacity: 0.4; }
          40%         { transform: scale(1);   opacity: 1; }
        }
        .chat-think-dot { display:inline-block; width:6px; height:6px; margin: 0 2px; background:#272e42; border-radius:99px; animation: chat-think-bounce 1.4s var(--ease-precision, cubic-bezier(0.16,1,0.3,1)) infinite; }
        .chat-think-dot:nth-child(2) { animation-delay: 0.16s; }
        .chat-think-dot:nth-child(3) { animation-delay: 0.32s; }
        @media (prefers-reduced-motion: reduce) { .chat-think-dot { animation: none; opacity: 0.6; } }
      `}</style>

      {/* Mobile backdrop — only when panel open and viewport < md */}
      {open && (
        <div
          onClick={() => setOpen(false)}
          className="md:hidden fixed inset-0 z-40 bg-ink-900/30 backdrop-blur-sm"
          aria-hidden
        />
      )}

      {/* Floating launcher */}
      {!open ? (
        <PulseAccent className="fixed bottom-6 right-6 z-50">
          <button
            type="button"
            onClick={() => setOpen(true)}
            aria-label="Open chat"
            className="w-16 h-16 rounded-kp-pill bg-lime text-ink-900 shadow-lift flex items-center justify-center text-2xl hover:scale-105 active:bg-lime-press transition-transform duration-quick ease-precision focus-ring"
          >
            💬
          </button>
        </PulseAccent>
      ) : (
        <button
          type="button"
          onClick={() => setOpen(false)}
          aria-label="Close chat"
          className="fixed bottom-6 right-6 z-50 w-16 h-16 rounded-kp-pill bg-ink-900 text-white shadow-lift flex items-center justify-center text-2xl hover:scale-105 transition-transform duration-quick ease-precision focus-ring"
        >
          ✕
        </button>
      )}

      {/* Panel */}
      {open && (
        <div className="chat-panel-in fixed bottom-24 right-6 z-50 w-[400px] max-w-[calc(100vw-2rem)] h-[600px] max-h-[calc(100vh-8rem)] bg-white/95 backdrop-blur-2xl rounded-kp-card shadow-lift flex flex-col overflow-hidden">
          <header className="px-5 py-3 flex items-center justify-between bg-white/40">
            <div className="flex items-center gap-2">
              <span aria-hidden className="w-2 h-2 rounded-kp-pill bg-lime" style={{ boxShadow: '0 0 8px #cffc00' }} />
              <Icon name="smart_toy" style={{ fontSize: 18, color: '#272e42' }} />
              <span className="font-geist font-semibold text-title-md text-ink-900">
                {role === 'player' ? 'Player Assistant' : 'Owner Assistant'}
              </span>
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              aria-label="Close chat"
              className="p-1 focus-ring rounded-kp-chip"
            >
              <Icon name="close" style={{ fontSize: 18, color: '#272e42' }} />
            </button>
          </header>

          <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 flex flex-col gap-3 bg-surface-low/50">
            {visible.length === 0 && (
              <ChatBubble role="assistant">{welcome}</ChatBubble>
            )}
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
            {busy && (
              <div className="text-label-sm text-ink-700/60 px-2 inline-flex items-center gap-1">
                <span className="chat-think-dot" />
                <span className="chat-think-dot" />
                <span className="chat-think-dot" />
              </div>
            )}
            {error && (
              <div className="text-label-sm text-red-700 px-2">{error}</div>
            )}
          </div>

          <form
            className="p-3 flex gap-2 bg-white/60"
            onSubmit={(e) => {
              e.preventDefault();
              send();
            }}
          >
            <input
              className="field-input flex-1 bg-white"
              placeholder={role === 'player' ? 'Ask about courts or bookings…' : 'Ask about your venue…'}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={busy}
            />
            <button
              type="submit"
              disabled={busy || !input.trim()}
              className="px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring disabled:opacity-60"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
}
```

Key visual changes:
- Launcher gets `<PulseAccent>` halo at idle (turns into ✕ on ink-900 when open)
- Panel uses glassmorphic white/95 with backdrop-blur-2xl and shadow-lift
- Lime status dot in header with subtle glow
- "Thinking…" replaced with 3-dot bouncing animation
- Mobile backdrop for tap-to-close
- All buttons match the standard lime/ink-pill style

- [ ] Replace file
- [ ] `pnpm build` → clean
- [ ] Commit: `feat(web): ChatWidget → KP+Motion (glass panel, PulseAccent launcher, bouncing dots, mobile backdrop)`

---

## Task 4: Final smoke + PR + merge

- [ ] Suites:
```bash
cd /Users/nchawanp/Desktop/ZPOTS && conda run -n MADT pytest tests/ -q
cd apps/api && conda run -n MADT pytest -q && cd ..
cd apps/web && pnpm test:unit && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```
Expected: 29 · 53 · 47 · build clean

- [ ] PR body to `/tmp/pr5e-body.md`:
```markdown
## Summary

Phase 5e — final sub-phase of the design revamp. The floating chat widget now uses KP+Motion. After this PR, every surface in the app shares the new language.

- Spec: `docs/superpowers/specs/2026-05-17-phase5e-chat-polish-design.md`
- Plan: `docs/superpowers/plans/2026-05-17-phase5e-chat-polish.md`

## What ships

- **ChatBubble:** lime user / glass assistant, no borders, fade-up animation on mount
- **ConfirmDraft:** surface-low card, lime/ink button pair, PulseAccent on Confirm
- **ChatWidget:**
  - Glass panel (`bg-white/95 backdrop-blur-2xl shadow-lift`)
  - Launcher with continuous PulseAccent halo (off when open)
  - Lime status dot in header (live AI indicator)
  - 3-dot bouncing "thinking" animation
  - Mobile tap-to-close backdrop
  - Open/close scale + opacity transition

No backend or API changes.

## Tests

| Suite | Result |
|---|---|
| Streamlit | 29 / 29 ✅ |
| FastAPI | 53 / 53 ✅ |
| Vitest | 47 / 47 ✅ |
| Playwright | 2 / 3 ⚠️ (player-flow pre-existing, unrelated) |
| `pnpm build` | clean ✅ |

## Phase 5 — DONE

After this PR:
- ✅ 5a Foundation (tokens, primitives, TopNav, PageShell)
- ✅ 5b Owner anchor (dashboard, insights, bookings)
- ✅ 5c Owner cascade (venues, slots, pricing, optimization)
- ✅ 5d Player revamp (11 pages + mobile menu)
- ✅ 5e Chat polish (this PR)

Whole app uses Kinetic Precision + Motion. Geist + Geist Mono throughout. Glass nav. Dark heroes everywhere. No more Streamlit-shaped layouts.

Next up: Phase 4b (Dockerfiles, parked on `feat/nextjs-phase4b`), then Phase 4c (Cloud Run deploy).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

```bash
git push -u origin feat/nextjs-phase5e
gh pr create --base main --title "Phase 5e: chat polish (Phase 5 complete)" --body-file /tmp/pr5e-body.md
gh pr merge --merge --delete-branch
git checkout main && git pull
```
