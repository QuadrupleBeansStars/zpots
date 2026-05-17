'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { SplitHero } from '@/components/primitives/SplitHero';

export default function OwnerLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('owner@zpots.ai');
  const [password, setPassword] = useState('owner123');

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email.trim() && password.trim()) router.push('/owner');
  }

  return (
    <SplitHero
      eyebrow="BUSINESS LOGIN"
      headline={<>Manage<br />your courts.</>}
      sub="Welcome back to the dashboard."
    >
      <form onSubmit={onSubmit} className="flex flex-col gap-4">
        <div>
          <label className="text-label-sm text-ink-700/60 block mb-2">EMAIL</label>
          <input type="email" className="field-input" value={email}
            onChange={(e) => setEmail(e.target.value)} placeholder="owner@zpots.ai" />
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
          ENTER CONSOLE →
        </button>
        <p className="text-body-sm text-ink-700/60 text-center mt-2">
          Demo: <code className="font-geist-mono text-ink-900">owner@zpots.ai</code> / <code className="font-geist-mono text-ink-900">owner123</code>
        </p>
      </form>
    </SplitHero>
  );
}
