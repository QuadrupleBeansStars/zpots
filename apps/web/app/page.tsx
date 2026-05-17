import Link from 'next/link';
import { SplitHero } from '@/components/primitives/SplitHero';
import { Ticker } from '@/components/primitives/Ticker';

export default function LandingPage() {
  return (
    <SplitHero
      eyebrow="KINETIC PRECISION ENGINEERED"
      headline={<>ZPOTS. <span className="text-lime">Book your next game.</span></>}
      sub="AI-powered sports court booking for Bangkok athletes. Real-time availability, smart pricing, instant confirmation."
    >
      <div className="flex flex-col gap-4">
        <RoleCard
          icon="🏸"
          title="I'm a Player"
          description="Discover courts, book sessions, and track your games."
          href="/player/login"
          cta="Enter as Player"
        />
        <RoleCard
          icon="🏟"
          title="I'm a Court Owner"
          description="Manage venues, optimize pricing, grow your business."
          href="/owner-login"
          cta="Enter as Owner"
        />
        <div className="mt-3">
          <Ticker speed={50} className="text-label-sm text-ink-700/60">
            BANGKOK · 247 COURTS · 18 DISTRICTS · 6 SPORTS · AI-MATCHED
          </Ticker>
        </div>
      </div>
    </SplitHero>
  );
}

function RoleCard({ icon, title, description, href, cta }: {
  icon: string; title: string; description: string; href: string; cta: string;
}) {
  return (
    <Link
      href={href}
      className="group block bg-white rounded-kp-card shadow-float p-5 hover:shadow-lift transition-shadow duration-quick ease-precision focus-ring"
    >
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-kp-pill bg-surface-low flex items-center justify-center text-2xl flex-shrink-0">
          {icon}
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="font-geist font-bold text-title-md text-ink-900">{title}</h2>
          <p className="mt-1 text-body-sm text-ink-700/60">{description}</p>
          <span className="inline-flex items-center gap-1 mt-3 text-label-sm font-geist font-semibold text-lime-deep group-hover:text-ink-900">
            {cta} →
          </span>
        </div>
      </div>
    </Link>
  );
}
