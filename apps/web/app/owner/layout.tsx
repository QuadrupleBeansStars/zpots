import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { PageShell } from '@/components/PageShell';
import { currentOwner } from '@/lib/auth-stub';

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-surface">
      <BookingsHydrator userId={currentOwner.id} />
      <PageShell role="owner">{children}</PageShell>
      <ChatWidget role="owner" />
    </div>
  );
}
