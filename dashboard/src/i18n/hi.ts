import type { TextKey } from "./en";

// Every Hindi label in the app. Must have exactly the same keys as en.ts.
const hi: Record<TextKey, string> = {
  nav_main: "मुख्य मेन्यू",
  nav_dash: "डैशबोर्ड",
  nav_calls: "कॉल्स",
  nav_script: "कॉल स्क्रिप्ट",
  nav_settings: "सेटिंग्स",
  lang_label: "ऐप की भाषा",
  building: "ये स्क्रीन अभी बन रही है।",
  dash_h: "नमस्ते",
  dash_p: "आज आपकी कॉल्स ने क्या किया।",
  calls_h: "कॉल्स",
  calls_p: "हर कॉल, रिकॉर्डिंग और ग्राहक ने क्या कहा।",
  script_h: "कॉल स्क्रिप्ट",
  script_p: "एजेंट क्या बोलेगा, अपने शब्दों में लिखें। कोई फ़्लोचार्ट नहीं।",
  settings_h: "सेटिंग्स",
  settings_p: "कॉल कब और कैसे जाएँ।",
};

export default hi;
