const C='snb-v15';
const CORE=['./','manifest.webmanifest','icons/icon-192.png','icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))));self.clients.claim()});
self.addEventListener('fetch',e=>{const r=e.request,u=new URL(r.url);
 if(r.method!=='GET')return;
 // Fonts: cache-first (never change)
 if(/fonts\.(googleapis|gstatic)\.com$/.test(u.hostname)){e.respondWith(caches.match(r).then(m=>m||fetch(r).then(x=>{const cp=x.clone();caches.open(C).then(c=>c.put(r,cp));return x})));return}
 if(u.origin!==location.origin)return;
 // Live data: network-first
 if(u.pathname.startsWith('/api/')||u.pathname.endsWith('top4.json')){e.respondWith(fetch(r).catch(()=>caches.match(r)));return}
 // App files: instant from cache, refreshed in background (stale-while-revalidate)
 const key=r.mode==='navigate'?'./':r;
 e.respondWith(caches.open(C).then(c=>c.match(key).then(m=>{const net=fetch(r).then(x=>{if(x.ok)c.put(key,x.clone());return x}).catch(()=>m);return m||net})))});
