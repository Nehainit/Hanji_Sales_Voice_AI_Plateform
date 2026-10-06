"use client";

import { useEffect, useSyncExternalStore } from "react";
import en, { type TextKey } from "./en";
import hi from "./hi";

export type Lang = "en" | "hi";

const STORAGE_KEY = "haanji-lang";
const TEXTS: Record<Lang, Record<TextKey, string>> = { en, hi };
const listeners = new Set<() => void>();
let memory: Lang = "en"; // used when the browser blocks storage

function read(): Lang {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "en" || saved === "hi") return saved;
  } catch {}
  return memory;
}

function subscribe(onChange: () => void) {
  listeners.add(onChange);
  window.addEventListener("storage", onChange);
  return () => {
    listeners.delete(onChange);
    window.removeEventListener("storage", onChange);
  };
}

export function setLang(lang: Lang) {
  memory = lang;
  try {
    localStorage.setItem(STORAGE_KEY, lang);
  } catch {}
  listeners.forEach((notify) => notify());
}

/** The current app language (remembered on this device) and its labels. */
export function useLanguage() {
  const lang = useSyncExternalStore(subscribe, read, () => "en" as Lang);

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  return { lang, setLang, t: (key: TextKey) => TEXTS[lang][key] };
}
