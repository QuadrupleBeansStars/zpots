import { OwnerSidebar } from '@/components/OwnerSidebar';

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-zpots-surface">
      <OwnerSidebar />
      <main className="flex-1 px-8 py-6 max-w-[1400px]">{children}</main>
    </div>
  );
}
