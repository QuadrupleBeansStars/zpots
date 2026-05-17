import { CourtForm } from '@/components/owner/CourtForm';
import { PageHero } from '@/components/primitives/PageHero';

export default function NewCourtPage() {
  return (
    <div className="flex flex-col gap-6">
      <PageHero
        eyebrow="REGISTER VENUE · ELITE PARTNER"
        headline="Add a new court."
        sub="Fill in the details — the AI will surface pricing recommendations once you publish."
      />
      <CourtForm mode="new" />
    </div>
  );
}
