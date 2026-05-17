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
