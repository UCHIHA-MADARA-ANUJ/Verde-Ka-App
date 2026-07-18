import "./globals.css";

export const metadata = {
  title: "Verde Tech V3.0 — Autonomous Plant OS",
  description:
    "Industrial-grade smart garden monitoring, AI plant diagnostics and remote irrigation control. Project Verde V3.0 for DAV ACON 5.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-verde-bg font-mono antialiased">
        {children}
      </body>
    </html>
  );
}
