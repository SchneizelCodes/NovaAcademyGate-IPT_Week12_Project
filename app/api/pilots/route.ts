import { validatePilot } from "@/lib/pilot";
export const runtime = "nodejs";
export async function POST(request: Request) {
  // Same-origin JSON; no sessions, registration storage or logged personal details.
  if (request.headers.get("origin") !== new URL(request.url).origin) {
    return Response.json({ ok: false, message: "Please submit from the Academy form." }, { status: 403 });
  }
  if (!request.headers.get("content-type")?.startsWith("application/json")) {
    return Response.json({ ok: false, message: "Please send JSON." }, { status: 415 });
  }
  if (Number(request.headers.get("content-length")) > 8192) return Response.json({ ok: false, message: "Request too large." }, { status: 413 });
  let raw: unknown;
  try {
    const body = await request.text();
    if (new TextEncoder().encode(body).byteLength > 8192) return Response.json({ ok: false, message: "Request too large." }, { status: 413 });
    raw = JSON.parse(body);
  } catch { return Response.json({ ok: false, message: "Please send a valid form." }, { status: 400 }); }
  const result = validatePilot(raw);
  if (!result.ok) return Response.json(result, { status: 422, headers: { "Cache-Control": "no-store" } });
  // Like ModelState.IsValid: success is unreachable until server validation passes.
  return Response.json({ ok: true, message: `Welcome aboard, ${result.pilot.pilotName}!` }, { headers: { "Cache-Control": "no-store" } });
}
