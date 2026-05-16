'use client';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Button } from '@/components/Button';

export default function PlayerLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('player@zpots.ai');
  const [password, setPassword] = useState('demo123');

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (email.trim() && password.trim()) {
      router.push('/player');
    }
  }

  return (
    <div className="max-w-md mx-auto mt-12">
      <div className="zpots-card p-10">
        <h1 className="font-display text-3xl font-bold text-zpots-ink">
          Welcome Back,<br />Athlete
        </h1>
        <p className="text-sm text-zpots-muted mt-2">
          Log in or create an account to book your next game.
        </p>

        <form onSubmit={onSubmit} className="mt-6 flex flex-col gap-4">
          <div>
            <label className="field-label">EMAIL</label>
            <input
              type="email"
              className="field-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="athlete@zpots.ai"
            />
          </div>
          <div>
            <label className="field-label">PASSWORD</label>
            <input
              type="password"
              className="field-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          <Button variant="primary" type="submit" className="w-full justify-center mt-2">
            LOG IN
          </Button>
        </form>

        <p className="text-xs text-zpots-muted text-center mt-4">
          Demo: <code>player@zpots.ai</code> / <code>demo123</code>
        </p>
      </div>
    </div>
  );
}
