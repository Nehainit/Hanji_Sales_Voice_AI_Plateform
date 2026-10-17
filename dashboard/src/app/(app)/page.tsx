"use client";

import Link from "next/link";
import type { TextKey } from "@/i18n/en";
import { useLanguage } from "@/i18n/useLanguage";
import { RTO_COST, balance, cancelledThisMonth, latestCalls, rupee, today, week, type Outcome } from "@/data/sample";
import s from "./Dashboard.module.css";

const DAY_HI: Record<string, string> = { Tue: "मंगल", Wed: "बुध", Thu: "गुरु", Fri: "शुक्र", Sat: "शनि", Sun: "रवि", Today: "आज" };
const GLYPH: Record<Outcome, string> = { confirmed: "✓", cancelled: "✕", callback: "↻", noanswer: "–" };

export default function DashPage() {
  const { lang, t } = useLanguage();
  const day = (d: string) => (lang === "hi" ? DAY_HI[d] : d);
  const pct = Math.round((today.confirmed / today.calls) * 100);

  return (
    <div className={s.page}>
      <div className={s.head}>
        <div>
          <h2>{t("dash_h")}</h2>
          <p>{t("dash_p")}</p>
        </div>
        <span className={s.wallet}>
          {rupee(balance)} <span>≈ {Math.floor(balance / 3)} {t("calls_unit")}</span>
        </span>
      </div>

      <section className={s.hero}>
        <div className={s.saved}>
          <span>{t("saved_month")}</span>
          <span className={`${s.big} ${s.num}`}>{rupee(cancelledThisMonth * RTO_COST)}</span>
          <p>{t("saved_note").replace("{n}", String(cancelledThisMonth)).replace("{rto}", rupee(RTO_COST))}</p>
        </div>
        <div className={s.tiles}>
          <Tile label={t("k_calls")} value={today.calls} note={`+${today.vsYesterday} ${t("vs_yday")}`} />
          <Tile label={t("k_conf")} value={today.confirmed} note={`${pct}% ${t("of_calls")}`} color="var(--s-good)" />
          <Tile label={t("k_canc")} value={today.cancelled} note={`${rupee(today.cancelled * RTO_COST)} ${t("saved_word")}`} color="var(--s-crit)" />
          <Tile label={t("k_pend")} value={today.pending} note={t("retrying")} color="var(--s-none)" />
        </div>
      </section>

      <div className={s.grid2}>
        <section className={s.card}>
          <div className={s.cardHead}>
            <h3>{t("chart_h")}</h3>
            <div className={s.legend}>
              <span><i style={{ background: "var(--s-good)" }} />{t("o_confirmed")}</span>
              <span><i style={{ background: "var(--s-crit)" }} />{t("o_cancelled")}</span>
              <span><i style={{ background: "var(--s-none)" }} />{t("k_pend")}</span>
            </div>
          </div>
          <WeekChart day={day} t={t} />
        </section>

        <section className={s.card}>
          <div className={s.cardHead}><h3>{t("attn_h")}</h3></div>
          <div className={s.attn}>
            <Attn href="/calls" bg="var(--warn-bg)" fg="var(--warn-text)" glyph="3" title={t("a1")} sub={t("a1s")} />
            <Attn href="/calls" bg="var(--brand-soft)" fg="var(--brand-text)" glyph="5" title={t("a2")} sub={t("a2s")} />
            <Attn href="/settings" bg="var(--marigold-soft)" fg="var(--marigold-ink)" glyph="₹" title={t("a3")} sub={t("a3s").replace("{bal}", rupee(balance))} />
          </div>
        </section>
      </div>

      <section style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        <div className={s.cardHead} style={{ margin: 0 }}>
          <h3>{t("latest_h")}</h3>
          <Link href="/calls" className={s.seeAll}>{t("see_all")} →</Link>
        </div>
        <div className={s.tblWrap}>
          <table>
            <thead>
              <tr>
                <th>{t("c_time")}</th><th>{t("c_order")}</th><th>{t("c_cust")}</th>
                <th className={s.r}>{t("c_amount")}</th><th>{t("c_result")}</th><th className={s.r}>{t("c_try")}</th>
              </tr>
            </thead>
            <tbody>
              {latestCalls.map((c) => (
                <tr key={c.id}>
                  <td className={`${s.num} ${s.muted}`}>{c.time}</td>
                  <td className={s.mono}>#{c.id}</td>
                  <td><strong>{c.name}</strong> <span className={s.muted}>{c.city}</span></td>
                  <td className={`${s.r} ${s.num}`}>{rupee(c.amount)}</td>
                  <td><span className={`${s.pill} ${s[c.outcome]}`}><i>{GLYPH[c.outcome]}</i>{t(`o_${c.outcome}` as TextKey)}</span></td>
                  <td className={`${s.r} ${s.num} ${s.muted}`}>{c.tries}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function Tile({ label, value, note, color }: { label: string; value: number; note: string; color?: string }) {
  return (
    <div className={s.tile}>
      <span className={s.k}>{color && <i style={{ background: color }} />}{label}</span>
      <span className={`${s.v} ${s.num}`}>{value}</span>
      <span className={s.d}>{note}</span>
    </div>
  );
}

function Attn({ href, bg, fg, glyph, title, sub }: { href: string; bg: string; fg: string; glyph: string; title: string; sub: string }) {
  return (
    <Link href={href}>
      <span className={s.dot} style={{ background: bg, color: fg }}>{glyph}</span>
      <span><strong>{title}</strong><small>{sub}</small></span>
    </Link>
  );
}

/** Stacked bars: confirmed, cancelled, no answer / later, for the last 7 days. */
function WeekChart({ day, t }: { day: (d: string) => string; t: (k: TextKey) => string }) {
  const W = 560, H = 230, L = 36, R = 8, T = 12, B = 28, max = 150;
  const ph = H - T - B, band = (W - L - R) / week.length, bw = 24;
  const y = (v: number) => T + ph - (v / max) * ph;
  return (
    <div className={s.chart}>
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={t("chart_h")}>
        {[0, 50, 100, 150].map((v) => (
          <g key={v}>
            {v > 0 && <line className={s.gridLine} x1={L} x2={W - R} y1={y(v)} y2={y(v)} />}
            <text x={L - 8} y={y(v) + 4} textAnchor="end">{v}</text>
          </g>
        ))}
        {week.map((w, i) => {
          const cx = L + band * i + band / 2, x = cx - bw / 2;
          const segs: [string, number][] = [["var(--s-good)", w.c], ["var(--s-crit)", w.x], ["var(--s-none)", w.p]];
          let cur = y(0);
          return (
            <g key={w.d} className={s.bar}>
              <title>{`${day(w.d)}: ${w.c} ${t("o_confirmed")}, ${w.x} ${t("o_cancelled")}, ${w.p} ${t("k_pend")}`}</title>
              {segs.map(([fill, v], k) => {
                const h = (v / max) * ph, top = cur - h, gap = k > 0 ? 2 : 0;
                const rect = <rect key={k} x={x} y={top} width={bw} height={h - gap} rx={k === 2 ? 4 : 0} fill={fill} />;
                cur = top;
                return rect;
              })}
              <text x={cx} y={H - 8} textAnchor="middle" className={w.d === "Today" ? s.today : undefined}>{day(w.d)}</text>
            </g>
          );
        })}
        <line className={s.base} x1={L} x2={W - R} y1={y(0)} y2={y(0)} />
      </svg>
    </div>
  );
}
