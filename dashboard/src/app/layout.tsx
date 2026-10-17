import type { Metadata } from "next";
import { IBM_Plex_Mono, Noto_Sans_Devanagari, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

// Same fonts as the marketing site (website/index.html).
const body = Plus_Jakarta_Sans({
  variable: "--font-body",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

// Plus Jakarta Sans has no Devanagari, so Hindi text uses Noto Sans Devanagari.
const hindi = Noto_Sans_Devanagari({
  variable: "--font-hindi",
  subsets: ["devanagari"],
  weight: ["400", "500", "600", "700"],
});

const mono = IBM_Plex_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["500"],
});

export const metadata: Metadata = {
  title: "HaanJi",
  description: "Confirm every COD order with a phone call, automatically.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${body.variable} ${hindi.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
