import { OwnerSidebar } from '@/components/OwnerSidebar';
import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { currentOwner } from '@/lib/auth-stub';

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-zpots-surface">
      <BookingsHydrator userId={currentOwner.id} />
      <OwnerSidebar />
      <main className="flex-1 px-8 py-6 max-w-[1400px]">{children}</main>
      <ChatWidget role="owner" />
    </div>
  );
}
