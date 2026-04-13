import './styles.css';
import { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="container">
          <h1>Arbitrage Scanner Dashboard</h1>
          {children}
        </main>
      </body>
    </html>
  );
}
