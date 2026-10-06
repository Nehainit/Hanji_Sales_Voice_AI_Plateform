"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { TextKey } from "@/i18n/en";
import { useLanguage } from "@/i18n/useLanguage";
import styles from "./AppShell.module.css";

const NAV: { href: string; label: TextKey; icon: string }[] = [
  { href: "/", label: "nav_dash", icon: "M3 13h8V3H3zM13 21h8V11h-8zM3 21h8v-6H3zM13 3v6h8V3z" },
  { href: "/calls", label: "nav_calls", icon: "M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2" },
  { href: "/script", label: "nav_script", icon: "M4 5h16M4 10h16M4 15h10M4 20h7" },
  { href: "/settings", label: "nav_settings", icon: "M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1" },
];

function Logo() {
  return (
    <span className={styles.logo}>
      <svg width="26" height="26" viewBox="0 0 30 30" aria-hidden="true">
        <rect width="30" height="30" rx="9" fill="var(--brand)" />
        <path d="M9 15.5l4 4 8-9" fill="none" stroke="var(--brand-ink)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      HaanJi
    </span>
  );
}

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { lang, setLang, t } = useLanguage();

  return (
    <div className={styles.shell}>
      <aside className={styles.side}>
        <Logo />
        <nav className={styles.nav} aria-label={t("nav_main")}>
          {NAV.map((item) => (
            <Link key={item.href} href={item.href} aria-current={pathname === item.href ? "page" : undefined}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d={item.icon} />
              </svg>
              <span>{t(item.label)}</span>
            </Link>
          ))}
        </nav>
      </aside>
      <div className={styles.main}>
        <header className={styles.top}>
          <div className={styles.langToggle} role="group" aria-label={t("lang_label")}>
            <button type="button" aria-pressed={lang === "en"} onClick={() => setLang("en")}>EN</button>
            <button type="button" aria-pressed={lang === "hi"} onClick={() => setLang("hi")}>हिंदी</button>
          </div>
        </header>
        <main className={styles.content}>{children}</main>
      </div>
    </div>
  );
}
