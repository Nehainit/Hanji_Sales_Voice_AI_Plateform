"use client";

import type { TextKey } from "@/i18n/en";
import { useLanguage } from "@/i18n/useLanguage";

/** Title and one-line description at the top of a screen, in the app language. */
export default function ScreenHeading({ title, subtitle, building = false }: { title: TextKey; subtitle: TextKey; building?: boolean }) {
  const { t } = useLanguage();
  return (
    <div>
      <h2>{t(title)}</h2>
      <p style={{ color: "var(--ink-2)", marginTop: 4 }}>{t(subtitle)}</p>
      {building && <p style={{ color: "var(--muted)", marginTop: 16 }}>{t("building")}</p>}
    </div>
  );
}
