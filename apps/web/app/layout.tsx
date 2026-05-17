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
      <head>
        {/* Load Google Fonts via <link> rather than @import in globals.css —
            Tailwind/PostCSS sometimes silently fails to fetch remote @imports,
            which leaves Material Symbols spans showing their ligature text
            (arrow_forward, ac_unit, …) instead of icons. */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=Lexend:wght@300;400;500;600;700&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
        />
      </head>
      <body className="font-sans bg-white text-zpots-ink antialiased">
        {children}
      </body>
    </html>
  );
}
