import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { PageShell } from '@/components/PageShell';
import { currentUser } from '@/lib/auth-stub';

export default function PlayerLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <BookingsHydrator userId={currentUser.id} />
      <PageShell role="player">{children}</PageShell>
      <ChatWidget role="player" />
    </>
  );
}
