'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { SplitHero } from '@/components/primitives/SplitHero';

export default function PlayerLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('player@zpots.ai');
  const [password, setPassword] = useState('demo123');

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email.trim() && password.trim()) router.push('/player');
  }

  return (
    <SplitHero
      eyebrow="ATHLETE LOGIN"
      headline={<>Welcome back,<br />Athlete.</>}
      sub="Your next session is one click away."
    >
      <form onSubmit={onSubmit} className="flex flex-col gap-4">
        <div>
          <label className="text-label-sm text-ink-700/60 block mb-2">EMAIL</label>
          <input type="email" className="field-input" value={email}
            onChange={(e) => setEmail(e.target.value)} placeholder="athlete@zpots.ai" />
        </div>
        <div>
          <label className="text-label-sm text-ink-700/60 block mb-2">PASSWORD</label>
          <input type="password" className="field-input" value={password}
            onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
        </div>
        <button
          type="submit"
          className="w-full px-5 py-3 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill hover:scale-[1.02] active:bg-lime-press transition-transform duration-quick ease-precision focus-ring mt-2"
        >
          LOG IN
        </button>
        <p className="text-body-sm text-ink-700/60 text-center mt-2">
          Demo: <code className="font-geist-mono text-ink-900">player@zpots.ai</code> / <code className="font-geist-mono text-ink-900">demo123</code>
        </p>
      </form>
    </SplitHero>
  );
}
