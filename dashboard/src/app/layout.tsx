import type { Metadata } from "next";
import { Baloo_2, Hind, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const display = Baloo_2({
  variable: "--font-display",
  subsets: ["latin", "devanagari"],
  weight: ["600", "700", "800"],
});

const body = Hind({
  variable: "--font-body",
  subsets: ["latin", "devanagari"],
  weight: ["400", "500", "600"],
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
    <html lang="en" className={`${display.variable} ${body.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
