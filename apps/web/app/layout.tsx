import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ZPOTS — AI-Powered Sports Court Booking',
  description: 'Discover, book, and manage sports courts in Bangkok.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans bg-white text-zpots-ink antialiased">
        {children}
      </body>
    </html>
  );
}
