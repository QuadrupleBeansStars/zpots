'use client';
import { useParams } from 'next/navigation';
import { CourtForm } from '@/components/owner/CourtForm';

export default function EditCourtPage() {
  const params = useParams<{ id: string }>();
  return <CourtForm mode="edit" courtId={params.id} />;
}
