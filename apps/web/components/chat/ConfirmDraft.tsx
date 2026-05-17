'use client';
import { Button } from '@/components/Button';
import { formatPrice } from '@/lib/format';
import type { ChatDraft } from '@/lib/chat-types';

type Props = {
  draft: ChatDraft;
  onConfirm: () => void;
  onCancel: () => void;
  disabled?: boolean;
};

export function ConfirmDraft({ draft, onConfirm, onCancel, disabled }: Props) {
  return (
    <div className="zpots-card-surface p-3 mt-1 text-sm">
      {draft.kind === 'booking_draft' ? (
        <div className="text-zpots-ink">
          📌 Confirm booking:{' '}
          <strong>{draft.court_name}</strong> on {draft.date} {draft.time_start}–{draft.time_end} for{' '}
          <strong>{formatPrice(draft.total_price)}</strong>?
        </div>
      ) : (
        <div className="text-zpots-ink">
          ⚠️ Cancel booking{' '}
          <strong>{draft.txn_id}</strong> at {draft.court_name} on {draft.date} {draft.time_start}?
        </div>
      )}
      <div className="flex gap-2 mt-2">
        <Button variant="primary" onClick={onConfirm} disabled={disabled}>
          Confirm
        </Button>
        <Button variant="secondary" onClick={onCancel} disabled={disabled}>
          Cancel
        </Button>
      </div>
    </div>
  );
}
