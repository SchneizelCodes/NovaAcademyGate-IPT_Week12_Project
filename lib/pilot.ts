// Shared model and validation: used by the React form AND the server route.
export type PilotInput = { pilotName: string; age: string; email: string; mobile: string; launchDate: string };
export type Field = keyof PilotInput;
export type FieldErrors = Partial<Record<Field, string>>;
export type Pilot = { pilotName: string; age: number; email: string; mobile: string; launchDate?: string };
export const EMPTY_PILOT: PilotInput = { pilotName: "", age: "", email: "", mobile: "", launchDate: "" };
export const MESSAGES = {
  pilotName: "Every pilot needs a callsign (3 to 20 characters)!",
  age: "Pilots must be 18 to 60 years old.",
  ageRequired: "Please enter your age.",
  email: "That email is lost in space.",
  mobile: "Please enter a valid mobile number.",
  launchDate: "You cannot launch yesterday!",
} as const;
export function manilaToday(now = new Date()): string {
  const parts = new Intl.DateTimeFormat("en-US", { timeZone: "Asia/Manila", year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(now);
  return ["year", "month", "day"].map(part => parts.find(p => p.type === part)!.value).join("-");
}
function text(value: unknown): string { return typeof value === "string" ? value.trim() : ""; }
export function validatePilot(raw: unknown, today = manilaToday()): { ok: false; errors: FieldErrors } | { ok: true; pilot: Pilot } {
  const obj = raw && typeof raw === "object" && !Array.isArray(raw) ? raw as Record<string, unknown> : {};
  const pilotName = text(obj.pilotName);
  const ageText = typeof obj.age === "number" ? String(obj.age) : text(obj.age);
  const email = text(obj.email);
  const mobile = text(obj.mobile);
  const launchDate = text(obj.launchDate);
  const errors: FieldErrors = {};
  if (pilotName.length < 3 || pilotName.length > 20) errors.pilotName = MESSAGES.pilotName;
  if (!ageText) errors.age = MESSAGES.ageRequired;
  else if (!/^\d+$/.test(ageText) || !Number.isInteger(Number(ageText)) || Number(ageText) < 18 || Number(ageText) > 60) errors.age = MESSAGES.age;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.email = MESSAGES.email;
  // Lab Phone + StringLength intent; not a Philippine-carrier-specific rule.
  const digits = mobile.replace(/\D/g, "");
  if (!mobile || mobile.length > 11 || !/^\+?[0-9() .-]+$/.test(mobile) || digits.length < 7 || digits.length > 11 || (mobile.match(/\(/g)?.length ?? 0) !== (mobile.match(/\)/g)?.length ?? 0)) errors.mobile = MESSAGES.mobile;
  if (launchDate) {
    const date = new Date(launchDate + "T00:00:00Z");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(launchDate) || Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== launchDate) errors.launchDate = "Please enter a valid launch date.";
    else if (launchDate < today) errors.launchDate = MESSAGES.launchDate;
  }
  if (Object.keys(errors).length) return { ok: false, errors };
  return { ok: true, pilot: { pilotName, age: Number(ageText), email, mobile, ...(launchDate ? { launchDate } : {}) } };
}
