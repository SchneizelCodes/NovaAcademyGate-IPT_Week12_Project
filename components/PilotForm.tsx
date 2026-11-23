"use client";
import { useRef, useState } from "react";
import { EMPTY_PILOT, manilaToday, validatePilot, type Field, type FieldErrors, type PilotInput } from "@/lib/pilot";
const fields: { key: Field; label: string; placeholder: string; hint: string; type: string; autoComplete: string; inputMode?: "numeric" | "tel" | "email" }[] = [
  { key: "pilotName", label: "Pilot callsign", placeholder: "What should we call you?", hint: "3–20 characters. Make it yours.", type: "text", autoComplete: "nickname" },
  { key: "age", label: "Age", placeholder: "e.g. 25", hint: "Explorers aged 18–60 are welcome.", type: "text", autoComplete: "off", inputMode: "numeric" },
  { key: "email", label: "Email address", placeholder: "you@youruniverse.com", hint: "A valid email to reach your orbit.", type: "email", autoComplete: "email", inputMode: "email" },
  { key: "mobile", label: "Mobile number", placeholder: "09171234567", hint: "A valid phone number, up to 11 characters.", type: "tel", autoComplete: "tel", inputMode: "tel" },
];
export default function PilotForm() {
  const [values, setValues] = useState<PilotInput>({ ...EMPTY_PILOT });
  const [errors, setErrors] = useState<FieldErrors>({});
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState("");
  const [networkError, setNetworkError] = useState("");
  const [challenge, setChallenge] = useState(false);
  const form = useRef<HTMLFormElement>(null);
  const success = useRef<HTMLDivElement>(null);
  function showErrors(next: FieldErrors) {
    setErrors(next);
    const key = Object.keys(next)[0];
    if (key) requestAnimationFrame(() => form.current?.querySelector<HTMLInputElement>(`[name="${key}"]`)?.focus());
  }
  function update(key: Field, value: string) {
    setValues(prev => ({ ...prev, [key]: value }));
    setMessage(""); setNetworkError("");
    if (errors[key]) setErrors(prev => ({ ...prev, [key]: undefined }));
  }
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(""); setNetworkError("");
    const payload = { ...values, launchDate: challenge ? values.launchDate : "" };
    const checked = validatePilot(payload);
    if (!checked.ok) { showErrors(checked.errors); return; }
    setErrors({}); setPending(true);
    try {
      const response = await fetch("/api/pilots", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      const result = await response.json();
      if (!response.ok || !result.ok) {
        if (result.errors) showErrors(result.errors);
        else setNetworkError(result.message || "The gate is temporarily unavailable. Please try again.");
        return;
      }
      setMessage(result.message); setValues({ ...EMPTY_PILOT });
      requestAnimationFrame(() => success.current?.focus());
    } catch { setNetworkError("We could not reach the gate. Your details are still here. Please try again."); }
    finally { setPending(false); }
  }
  return <form ref={form} onSubmit={submit} noValidate aria-label="Pilot registration" aria-busy={pending}>
    {message && <div ref={success} className="success" role="status" tabIndex={-1}><span className="success-symbol" aria-hidden="true">✓</span><div><strong>{message}</strong><p>Flight check complete. You’re ready for your next chapter.</p></div></div>}
    {!!Object.values(errors).filter(Boolean).length && <div className="error-summary" role="alert"><strong>A quick flight check.</strong><p>Please fix the highlighted fields. Your other details are saved in the form.</p><ul>{Object.entries(errors).filter(([, value]) => value).map(([key, value]) => <li key={key}><a href={`#${key}`}>{value}</a></li>)}</ul></div>}
    {networkError && <p className="error-summary" role="alert">{networkError}</p>}
    <div className="fields">{fields.map((field, index) => <div className={`field field-${field.key}`} key={field.key}><div className="label-row"><label htmlFor={field.key}>{field.label} <span className="required" aria-label="required">*</span></label><span className="field-index">0{index + 1}</span></div><input id={field.key} name={field.key} type={field.type} inputMode={field.inputMode} autoComplete={field.autoComplete} placeholder={field.placeholder} value={values[field.key]} onChange={event => update(field.key, event.target.value)} aria-invalid={!!errors[field.key]} aria-describedby={`${field.key}-hint${errors[field.key] ? ` ${field.key}-error` : ""}`} required disabled={pending}/><p className="hint" id={`${field.key}-hint`}>{field.hint}</p>{errors[field.key] && <p className="field-error" id={`${field.key}-error`}>{errors[field.key]}</p>}</div>)}</div>
    <div className="challenge"><button type="button" aria-expanded={challenge} aria-controls={challenge ? "launch-fields" : undefined} onClick={() => { setChallenge(!challenge); setErrors(prev => ({ ...prev, launchDate: undefined })); }}><span><span className="plus" aria-hidden="true">{challenge ? "−" : "+"}</span> Plan your launch</span><span className="optional">OPTIONAL QUEST</span></button>{challenge && <div id="launch-fields" className="launch-field"><label htmlFor="launchDate">Launch date <span className="optional">OPTIONAL</span></label><input type="date" id="launchDate" name="launchDate" min={manilaToday()} value={values.launchDate} onChange={event => update("launchDate", event.target.value)} aria-invalid={!!errors.launchDate} aria-describedby={`launchDate-hint${errors.launchDate ? " launchDate-error" : ""}`} disabled={pending}/><p className="hint" id="launchDate-hint">Today or a future date, based on Philippine time.</p>{errors.launchDate && <p className="field-error" id="launchDate-error">{errors.launchDate}</p>}</div>}</div>
    <button className="submit" type="submit" disabled={pending}><span>{pending ? "Checking your flight details…" : "Request boarding clearance"}</span><span aria-hidden="true">↗</span></button><p className="required-note">* All flight-check fields are required.</p>
  </form>;
}
