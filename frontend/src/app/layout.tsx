import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Todo App with Chatbot',
  description: 'A modern Todo application with AI chatbot assistance',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
