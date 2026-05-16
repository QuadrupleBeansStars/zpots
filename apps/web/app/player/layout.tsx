import { PlayerTopBar } from '@/components/PlayerTopBar';

export default function PlayerLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <PlayerTopBar />
      <main className="max-w-[1200px] mx-auto px-8 py-6">{children}</main>
    </>
  );
}
