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
