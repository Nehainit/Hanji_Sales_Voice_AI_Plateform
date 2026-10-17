// Sample numbers from the prototype, shown until the backend sends real ones.

export type Outcome = "confirmed" | "cancelled" | "callback" | "noanswer";

export const RTO_COST = 160;

export const today = { calls: 128, vsYesterday: 9, confirmed: 97, cancelled: 14, pending: 17 };
export const cancelledThisMonth = 293;
export const balance = 1840;

export const week = [
  { d: "Tue", c: 88, x: 12, p: 18 },
  { d: "Wed", c: 95, x: 15, p: 14 },
  { d: "Thu", c: 79, x: 9, p: 16 },
  { d: "Fri", c: 102, x: 14, p: 13 },
  { d: "Sat", c: 110, x: 18, p: 21 },
  { d: "Sun", c: 84, x: 16, p: 15 },
  { d: "Today", c: 97, x: 14, p: 17 },
];

export const latestCalls: { time: string; id: string; name: string; city: string; amount: number; outcome: Outcome; tries: number }[] = [
  { time: "6:42 PM", id: "KK2148", name: "Priya Sharma", city: "Jaipur", amount: 649, outcome: "confirmed", tries: 1 },
  { time: "6:31 PM", id: "KK2147", name: "Rahul Verma", city: "Lucknow", amount: 3499, outcome: "confirmed", tries: 2 },
  { time: "6:20 PM", id: "KK2146", name: "Sneha Patil", city: "Pune", amount: 1299, outcome: "confirmed", tries: 1 },
  { time: "6:09 PM", id: "KK2145", name: "Aman Gupta", city: "Indore", amount: 749, outcome: "noanswer", tries: 3 },
  { time: "5:58 PM", id: "KK2144", name: "Fatima Khan", city: "Bhopal", amount: 899, outcome: "confirmed", tries: 1 },
];

export const rupee = (n: number) => "₹" + n.toLocaleString("en-IN");
