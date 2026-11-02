// Contatore anonimo dell'app: nessun dato personale, solo totali giornalieri per tipo di evento.
import { getStore } from "@netlify/blobs";

const EV = ["new", "dau", "dau_app", "install", "scan", "found", "nf", "ocr", "voice", "amz", "teach"];
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export default async (req) => {
  const store = getStore("stats");
  if (req.method === "POST") {
    let b = {};
    try { b = JSON.parse(await req.text()); } catch (e) {}
    const e = String(b.e || "");
    if (!EV.includes(e)) return J({ error: "e" }, 400);
    const lg = /^[a-z]{2}$/.test(b.l || "") ? b.l : "xx";
    const day = new Date().toISOString().slice(0, 10);
    const d = (await store.get(day, { type: "json" })) || {};
    d[e] = (d[e] || 0) + 1;
    d["lang_" + lg] = e === "dau" ? (d["lang_" + lg] || 0) + 1 : (d["lang_" + lg] || 0);
    await store.setJSON(day, d);
    return J({ ok: true });
  }
  if (req.method === "GET") {
    // solo totali anonimi, nessun dato personale
    const { blobs } = await store.list();
    const days = blobs.map((x) => x.key).sort().slice(-60);
    const out = {};
    for (const k of days) out[k] = await store.get(k, { type: "json" });
    const tot = {};
    for (const v of Object.values(out)) for (const [k, n] of Object.entries(v || {})) tot[k] = (tot[k] || 0) + n;
    return J({ totals: tot, days: out });
  }
  return J({ error: "method" }, 405);
};

export const config = { path: "/api/stats" };
