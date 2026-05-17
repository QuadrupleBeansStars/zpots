import Markdown from 'react-markdown';

type Props = {
  role: 'user' | 'assistant';
  children: React.ReactNode;
};

export function ChatBubble({ role, children }: Props) {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={[
          'max-w-[85%] rounded-card px-3 py-2 text-sm',
          isUser
            ? 'bg-zpots-lime text-zpots-forest'
            : 'bg-white border border-zpots-mint text-zpots-ink',
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
  );
}
