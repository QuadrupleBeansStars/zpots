'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/Button';
import { Eyebrow, AITag } from '@/components/Tags';
import { aiCourtDescription } from '@/lib/api-client';
import { FALLBACK_COURTS } from '@/lib/mock-data';
import type { Court } from '@/lib/types';

const SPORTS = ['Badminton', 'Football', 'Basketball', 'Padel', 'Tennis', 'Volleyball'];
const SURFACES = ['Professional Mat', 'Premium Synthetic', 'Hardwood', 'Artificial Turf', 'Glass Panels', 'Clay', 'Sprung Floor'];
const AMENITY_OPTIONS = ['AC Units', 'Pro Lighting', 'Locker Rooms', 'Water Station', 'AV Video', 'Showers', 'Cafe', 'Parking'];

export function CourtForm({ mode, courtId }: { mode: 'new' | 'edit'; courtId?: string }) {
  const existing: Court | undefined = courtId ? FALLBACK_COURTS.find((c) => c.id === courtId) : undefined;
  const [name, setName] = useState(existing?.name ?? '');
  const [sport, setSport] = useState(existing?.sport ?? 'Badminton');
  const [surface, setSurface] = useState(existing?.surface ?? 'Premium Synthetic');
  const [location, setLocation] = useState(existing?.location ?? '');
  const [description, setDescription] = useState('');
  const [amenities, setAmenities] = useState<string[]>(
    existing ? existing.amenities.map((a) => a.label) : [],
  );
  const [descLoading, setDescLoading] = useState(false);

  function toggleAmenity(a: string) {
    setAmenities((s) => (s.includes(a) ? s.filter((x) => x !== a) : [...s, a]));
  }

  return (
    <div>
      <Link href="/owner/venues" className="text-label-sm text-lime-deep hover:underline">← Back to courts</Link>

      <div className="bg-white rounded-kp-card shadow-float p-6 mt-5 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <Eyebrow>COURT FUNDAMENTALS</Eyebrow>

          <div className="mt-3">
            <label className="field-label">COURT NAME</label>
            <input className="field-input" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Center Court" />
          </div>

          <div className="grid grid-cols-2 gap-3 mt-3">
            <div>
              <label className="field-label">SPORT CATEGORY</label>
              <select className="field-input" value={sport} onChange={(e) => setSport(e.target.value)}>
                {SPORTS.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="field-label">SURFACE TYPE</label>
              <select className="field-input" value={surface} onChange={(e) => setSurface(e.target.value)}>
                {SURFACES.map((s) => <option key={s}>{s}</option>)}
              </select>
            </div>
          </div>

          <div className="mt-3">
            <label className="field-label">LOCATION / FULL ADDRESS</label>
            <input className="field-input" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Sukhumvit Soi 39, Bangkok 10110" />
          </div>

          <div className="mt-3">
            <label className="field-label">COURT DESCRIPTION</label>
            <textarea className="field-input" rows={4} value={description} onChange={(e) => setDescription(e.target.value)}
                      placeholder="Write a description so users discover & connect with your court..." />
            <Button variant="primary" className="mt-2" type="button"
                    disabled={descLoading}
                    onClick={async () => {
                      setDescLoading(true);
                      try {
                        const res = await aiCourtDescription({ name, sport, surface, location, amenities });
                        setDescription(res.description);
                      } catch {
                        setDescription('Unable to generate description. Is the API running?');
                      } finally {
                        setDescLoading(false);
                      }
                    }}>
              <AITag>AI</AITag> {descLoading ? 'Generating…' : 'Generate Description'}
            </Button>
          </div>

          <div className="mt-4">
            <Eyebrow>KINETIC AMENITIES</Eyebrow>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2">
              {AMENITY_OPTIONS.map((a) => (
                <label key={a} className="flex items-center gap-2 text-body-sm text-ink-900 font-geist">
                  <input type="checkbox" checked={amenities.includes(a)} onChange={() => toggleAmenity(a)} />
                  {a}
                </label>
              ))}
            </div>
          </div>
        </div>

        <div>
          <Eyebrow>VISUAL & BRANDING</Eyebrow>
          <div className="bg-surface-low rounded-kp-card mt-3 h-48 flex items-center justify-center text-ink-700/60 text-body-sm font-geist">
            Drag and drop file here<br />Limit 200MB · JPG, PNG, MP4
          </div>
          <Button variant="secondary" className="mt-3 w-full justify-center" type="button">Browse files</Button>

          <div className="mt-6">
            <Eyebrow>MICROLOCATION</Eyebrow>
            <div className="bg-surface-low rounded-kp-card h-40 mt-2 flex items-center justify-center text-ink-700/60 text-body-sm font-geist">
              (Map placeholder — real map lands in Phase 4)
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-2 mt-5">
        <Link href="/owner/venues"><Button variant="secondary">Discard Changes</Button></Link>
        <Button variant="primary" type="button" onClick={() => alert('Saved (demo). Real backend lands in Phase 4.')}>
          Save & Continue →
        </Button>
      </div>
    </div>
  );
}
