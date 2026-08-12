import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Structured Data Copilot",
  description: "Generate and validate JSON-LD structured data for any URL",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
