// Memoria condivisa dei prodotti: quando un utente insegna il nome di un codice a barre sconosciuto,
// il nome viene salvato in forma anonima e la volta dopo lo riconoscono tutti.
import { getStore } from "@netlify/blobs";

const J = (o, s = 200, h = {}) => new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json", ...h } });

export default async (req) => {
  const url = new URL(req.url);
  const code = (url.searchParams.get("code") || "").replace(/\D/g, "");
  if (!/^\d{8,14}$/.test(code)) return J({ error: "code" }, 400);
  const store = getStore("names");
  if (req.method === "GET") {
    const d = await store.get(code, { type: "json" });
    const best = d && Object.values(d.n || {}).sort((a, b) => b.c - a.c)[0];
    return J(best ? { name: best.t, votes: best.c } : {}, 200, { "cache-control": "public, max-age=300" });
  }
  if (req.method === "POST") {
    let b; try { b = await req.json(); } catch (e) { return J({ error: "body" }, 400); }
    const name = String(b.name || "").replace(/[<>{}\\"`]/g, "").replace(/\s+/g, " ").trim().slice(0, 80);
    if (name.length < 3 || /https?:|www\.|\.com\b|@/i.test(name) || !/\p{L}{2,}/u.test(name)) return J({ error: "name" }, 400);
    const d = (await store.get(code, { type: "json" })) || { n: {} };
    const k = name.toLowerCase();
    if (!d.n[k] && Object.keys(d.n).length >= 20) return J({ ok: true });
    d.n[k] = { t: (d.n[k] && d.n[k].t) || name, c: ((d.n[k] && d.n[k].c) || 0) + 1 };
    d.u = new Date().toISOString().slice(0, 10);
    await store.setJSON(code, d);
    return J({ ok: true });
  }
  return J({ error: "method" }, 405);
};

export const config = { path: "/api/names" };
