'use client';

const TAGS = ['Clean Courts', 'Good Lighting', 'Great Staff', 'Easy Access', 'Pro Grade Gear'];

type Props = { selected: string[]; onToggle: (tag: string) => void };

export function FeedbackTagPicker({ selected, onToggle }: Props) {
  return (
    <div className="flex flex-wrap gap-2">
      {TAGS.map((t) => {
        const isOn = selected.includes(t);
        return (
          <button
            key={t}
            type="button"
            onClick={() => onToggle(t)}
            className={`chip ${isOn ? 'chip-selected' : 'chip-default'}`}
          >
            {t}
          </button>
        );
      })}
    </div>
  );
}
