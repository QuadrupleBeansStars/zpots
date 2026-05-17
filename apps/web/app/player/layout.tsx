import { PlayerTopBar } from '@/components/PlayerTopBar';
import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { currentUser } from '@/lib/auth-stub';

export default function PlayerLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <BookingsHydrator userId={currentUser.id} />
      <PlayerTopBar />
      <main className="max-w-[1200px] mx-auto px-8 py-6">{children}</main>
      <ChatWidget role="player" />
    </>
  );
}
