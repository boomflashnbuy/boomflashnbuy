// Contatore anonimo dell'app: nessun dato personale, solo totali giornalieri per tipo di evento.
import { getStore } from "@netlify/blobs";

const EV = ["new", "dau", "dau_app", "install", "scan", "found", "nf", "ocr", "voice", "amz", "teach"];
const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export default async (req, context) => {
  const store = getStore("stats");
  if (req.method === "POST") {
    let b = {};
    try { b = JSON.parse(await req.text()); } catch (e) {}
    const e = String(b.e || "");
    if (!EV.includes(e)) return J({ error: "e" }, 400);
    const lg = /^[a-z]{2}$/.test(b.l || "") ? b.l : "xx";
    const day = new Date().toISOString().slice(0, 10);
    // un blob per ogni evento (niente lettura-modifica-scrittura): due eventi simultanei non si sovrascrivono più
    const cc = (context && context.geo && context.geo.country && context.geo.country.code) || "XX";
    const keys = [e];
    if (e === "dau") keys.push("lang_" + lg);
    if (["new", "dau", "install", "scan", "amz"].includes(e)) keys.push(e + "_" + cc);
    const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    await store.set(`h/${day}/${id}`, keys.join(","));
    return J({ ok: true });
  }
  if (req.method === "GET") {
    // solo totali anonimi, nessun dato personale
    const { blobs } = await store.list();
    const out = {};
    // vecchi totali giornalieri (fino al 3/11)
    for (const k of blobs.map((x) => x.key).filter((k) => /^\d{4}-\d{2}-\d{2}$/.test(k))) out[k] = (await store.get(k, { type: "json" })) || {};
    // nuovi eventi singoli
    const hits = blobs.map((x) => x.key).filter((k) => k.startsWith("h/"));
    await Promise.all(hits.map(async (k) => {
      const day = k.split("/")[1];
      const v = (await store.get(k)) || "";
      const d = (out[day] = out[day] || {});
      for (const f of v.split(",").filter(Boolean)) d[f] = (d[f] || 0) + 1;
    }));
    const days = Object.keys(out).sort().slice(-60);
    const sel = {};
    for (const k of days) sel[k] = out[k];
    const tot = {};
    for (const v of Object.values(sel)) for (const [k, n] of Object.entries(v || {})) tot[k] = (tot[k] || 0) + n;
    return J({ totals: tot, days: sel });
  }
  return J({ error: "method" }, 405);
};

export const config = { path: "/api/stats" };
