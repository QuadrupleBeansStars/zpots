'use client';
import { useParams } from 'next/navigation';
import { CourtForm } from '@/components/owner/CourtForm';
import { PageHero } from '@/components/primitives/PageHero';

export default function EditCourtPage() {
  const params = useParams<{ id: string }>();
  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow="EDIT VENUE"
        headline="Update court details."
        sub="Changes go live immediately. Past bookings are unaffected."
      />
      <CourtForm mode="edit" courtId={params.id} />
    </div>
  );
}
