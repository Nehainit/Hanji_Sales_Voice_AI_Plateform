// Every English label in the app. hi.ts must have the same keys.
const en = {
  nav_main: "Main menu",
  nav_dash: "Dashboard",
  nav_calls: "Calls",
  nav_script: "Call script",
  nav_settings: "Settings",
  lang_label: "App language",
  building: "This screen is being built.",
  dash_h: "Good evening",
  dash_p: "Here's what your calls did today.",
  calls_h: "Calls",
  calls_p: "Every call, with recording and what the customer said.",
  script_h: "Call script",
  script_p: "Write what the agent says, in your own words. No flowcharts.",
  settings_h: "Settings",
  settings_p: "When and how the calls go out.",
};

export type TextKey = keyof typeof en;
export default en;
