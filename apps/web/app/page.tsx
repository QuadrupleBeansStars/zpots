import Link from 'next/link';
import { Button } from '@/components/Button';

export default function LandingPage() {
  return (
    <main className="min-h-screen flex flex-col items-center px-6 py-16">
      <div className="w-full max-w-3xl">
        <header className="text-center">
          <h1 className="font-display text-5xl font-bold text-zpots-ink">
            <span aria-hidden>⚡</span> ZPOTS
          </h1>
          <p className="mt-2 text-zpots-muted">
            AI-Powered Sports Court Booking Platform
          </p>
        </header>

        <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 gap-6">
          <RoleCard
            icon="🏸"
            title="I'm a Player"
            description="Discover courts, book sessions, and track your games in Bangkok."
            href="/player/login"
            cta="Enter as Player"
          />
          <RoleCard
            icon="🏟"
            title="I'm a Court Owner"
            description="Manage venues, optimize pricing, and grow your sports business."
            href="/owner/login"
            cta="Enter as Owner"
          />
        </div>

        <div className="mt-10 flex justify-center">
          <span className="ai-tag">KINETIC PRECISION ENGINEERED</span>
        </div>
      </div>
    </main>
  );
}

function RoleCard({
  icon,
  title,
  description,
  href,
  cta,
}: {
  icon: string;
  title: string;
  description: string;
  href: string;
  cta: string;
}) {
  return (
    <div className="zpots-card p-6 flex flex-col items-center text-center">
      <div className="text-4xl mb-3" aria-hidden>{icon}</div>
      <h2 className="font-display text-xl font-bold text-zpots-ink">{title}</h2>
      <p className="mt-2 text-sm text-zpots-muted">{description}</p>
      <Link href={href} className="mt-6 w-full">
        <Button variant="primary" icon="arrow_forward" className="w-full justify-center">
          {cta}
        </Button>
      </Link>
    </div>
  );
}
