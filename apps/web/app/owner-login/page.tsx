'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Button } from '@/components/Button';
import { AITag } from '@/components/Tags';

export default function OwnerLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('owner@zpots.ai');
  const [password, setPassword] = useState('owner123');

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email.trim() && password.trim()) {
      router.push('/owner');
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6"
         style={{ background: 'linear-gradient(160deg,#060e20 0%,#0d1b2e 40%,#162d3e 70%,#1a3040 100%)' }}>
      <div className="w-full max-w-md">
        <div className="bg-white rounded-card p-10 shadow-2xl">
          <div className="flex items-center gap-2 mb-4">
            <span className="font-display text-lg font-bold text-zpots-ink">⚡ ZPOTS Admin</span>
          </div>
          <AITag>ELITE VENUE PARTNER</AITag>
          <h1 className="font-display text-3xl font-bold mt-3 text-zpots-ink">
            Venue Control,<br />Supercharged.
          </h1>
          <p className="text-sm text-zpots-ink mt-2 opacity-75">
            Sign in to manage your Bangkok sports facilities.
          </p>

          <form onSubmit={onSubmit} className="mt-6 flex flex-col gap-4">
            <div>
              <label className="field-label">EMAIL</label>
              <input
                type="email" className="field-input" value={email}
                onChange={(e) => setEmail(e.target.value)} placeholder="owner@zpots.ai"
              />
            </div>
            <div>
              <label className="field-label">PASSWORD</label>
              <input
                type="password" className="field-input" value={password}
                onChange={(e) => setPassword(e.target.value)} placeholder="••••••••"
              />
            </div>
            <Button variant="primary" type="submit" className="w-full justify-center mt-2">
              ENTER CONSOLE →
            </Button>
          </form>
        </div>

        <p className="text-center text-xs text-white/75 mt-4">
          New operator?{' '}
          <strong className="text-zpots-lime cursor-pointer">Contact us to register your venue.</strong>
          <br />
          <small className="text-white/60">Demo: owner@zpots.ai / owner123</small>
        </p>
      </div>
    </div>
  );
}
