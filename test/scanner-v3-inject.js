/* ===== Scanner v3: mai pagine vuote, marca dal prefisso GS1, codici modello, memoria dei nomi ===== */
window.NF={it:{ask:'Non lo conosco ancora: cos’è?',ph:'Es. Nivea crema 150 ml',mic:'Detta',hint:'Marca probabile',teach:'Lo ricordo per la prossima volta',codeS:'Cerca solo con il codice'},
en:{ask:'I don’t know this one yet: what is it?',ph:'E.g. Nivea creme 150 ml',mic:'Speak',hint:'Likely brand',teach:'I’ll remember it next time',codeS:'Search by barcode only'},
es:{ask:'Aún no lo conozco: ¿qué es?',ph:'Ej. Nivea crema 150 ml',mic:'Dictar',hint:'Marca probable',teach:'Lo recordaré la próxima vez',codeS:'Buscar solo con el código'},
fr:{ask:'Je ne le connais pas encore : c’est quoi ?',ph:'Ex. Nivea crème 150 ml',mic:'Dicter',hint:'Marque probable',teach:'Je m’en souviendrai',codeS:'Chercher avec le code seul'},
de:{ask:'Kenne ich noch nicht: was ist es?',ph:'Z. B. Nivea Creme 150 ml',mic:'Sprechen',hint:'Wahrscheinliche Marke',teach:'Merke ich mir fürs nächste Mal',codeS:'Nur mit dem Code suchen'},
pt:{ask:'Ainda não conheço: o que é?',ph:'Ex. Nivea creme 150 ml',mic:'Ditar',hint:'Marca provável',teach:'Lembro-me para a próxima',codeS:'Procurar só com o código'}};
/* prefissi aziendali GS1 noti (EAN-13, 7 cifre) -> marca */
window.GS1={'5449000':'Coca-Cola','8000500':'Ferrero','3017620':'Ferrero','8076800':'Barilla','8076802':'Barilla','8076808':'Barilla','8076809':'Barilla','4005900':'Nivea','4005808':'Nivea','3600523':'L’Oréal','3600531':'L’Oréal','3600541':'L’Oréal','3600542':'Garnier','7622210':'Mondelez','7622300':'Mondelez','8710103':'Philips','8806085':'Samsung','8806086':'Samsung','8806088':'Samsung','8806090':'Samsung','8806092':'Samsung','8806094':'Samsung','8806095':'Samsung','0190198':'Apple','0190199':'Apple','0194252':'Apple','0194253':'Apple','0195949':'Apple','0885909':'Apple','0888462':'Apple','5702015':'LEGO','5702016':'LEGO','5702017':'LEGO','5025155':'Dyson','4548736':'Sony','4905524':'Sony','4242002':'Bosch','4242005':'Bosch','8004399':'De’Longhi','8000070':'Lavazza','7702018':'Gillette','4210201':'Braun','3121040':'Tefal','4006508':'Tchibo'};
window.gs1Brand=function(code){if(!/^\d{12,13}$/.test(code))return '';const e=code.length===12?'0'+code:code;return GS1[e.slice(0,7)]||''}
/* codici modello (scatole/linguette/etichette) -> marca davanti, così Amazon trova il modello giusto */
window.styleBrand=function(s){const t=(s||'').toUpperCase().trim();
 if(/\b[A-Z]{2}\d{4}-\d{3}\b/.test(t))return 'Nike';            // Nike / Jordan: CW2288-111
 if(/\bM[A-Z0-9]{3,4}\d?[A-Z]{1,2}\/A\b/.test(t))return 'Apple';  // Apple: MTJV3ZM/A
 if(/\b(?:[MWU]|ML|WL|MR|WR|GC|PC)\d{3,4}[A-Z]{2,4}\d?\b/.test(t))return 'New Balance'; // M990GL6, ML574EVG
 if(/\b[A-Z]{2}\d{4}\b/.test(t)&&/ADIDAS/.test(t))return 'adidas';
 return ''}
window.enrichQ=function(q){q=(q||'').trim();const b=styleBrand(q);if(b&&!q.toLowerCase().includes(b.toLowerCase()))q=b+' '+q;return q}
window.cleanBrand=function(b){return (b||'').replace(/\b(services?|s\.?\s?a\.?(\/n\.?v\.?)?|n\.?v\.?|s\.?p\.?a\.?|s\.?r\.?l\.?|gmbh|ltd|inc\.?|co\.?|company|group|italia|europe|international)\b/gi,'').replace(/\s{2,}/g,' ').replace(/[\s,\/.-]+$/,'').trim()}
/* nomi insegnati dall'utente: restano sul telefono, così il codice la volta dopo è riconosciuto */
window.teachCode=function(code,q){if(!code||!q||q===code)return;try{const c=JSON.parse(localStorage.getItem('snb-lk')||'{}');c[code]={t:Date.now(),r:{name:q,brand:'',q:q,taught:1}};localStorage.setItem('snb-lk',JSON.stringify(c))}catch(e){}}
/* dettatura con il microfono del telefono */
window.dictate=function(input,btn){const R=window.SpeechRecognition||window.webkitSpeechRecognition;if(!R){input.focus();return}
 try{const r=new R();r.lang={it:'it-IT',en:'en-GB',es:'es-ES',fr:'fr-FR',de:'de-DE',pt:'pt-PT'}[lang]||'it-IT';r.interimResults=false;r.maxAlternatives=1;btn&&btn.classList.add('on');
  r.onresult=e=>{const t=e.results[0][0].transcript;input.value=(input.value&&!/\s$/.test(input.value)?input.value+' ':input.value)+t;input.dispatchEvent(new Event('input'))};
  r.onend=()=>{btn&&btn.classList.remove('on')};r.onerror=()=>{btn&&btn.classList.remove('on');input.focus()};r.start()}catch(e){input.focus()}}
/* box "cos'è?" quando le banche dati non conoscono il codice */
window.askBox=function(code,onQ){const N=NF[lang]||NF.en;const br=gs1Brand(code);
 const h=`<p class="nfask">🤔 ${N.ask}</p>${br?`<small class="nfhint">${N.hint}: <b>${esc(br)}</b></small>`:''}
  <div class="nfrow"><input class="lqi" id="nfq" value="${br?esc(br)+' ':''}" placeholder="${N.ph}" autocomplete="off" enterkeyhint="search"><button type="button" class="nfmic" id="nfmic" aria-label="${N.mic}">🎙️</button></div>`;
 setTimeout(()=>{const i=$('#nfq'),m=$('#nfmic');if(!i)return;i.oninput=()=>onQ(enrichQ(i.value));m&&(m.onclick=()=>dictate(i,m));try{i.focus();i.setSelectionRange(i.value.length,i.value.length)}catch(e){}},30);
 return h}
window.lookupWikidata=async function(code){const alt=code.length===12?'0'+code:code;const q=`SELECT ?l ?b WHERE {VALUES ?g {"${code}" "${alt}"} ?i wdt:P3962 ?g. ?i rdfs:label ?l. FILTER(LANG(?l) IN ("${lang}","en")) OPTIONAL{?i wdt:P1716 ?x. ?x rdfs:label ?b. FILTER(LANG(?b)="en")}} LIMIT 1`;
 const r=await fetch('https://query.wikidata.org/sparql?format=json&query='+encodeURIComponent(q));if(!r.ok)throw r.status;const j=await r.json();const x=j.results.bindings[0];if(!x)return null;
 const nm=x.l.value,b=x.b?x.b.value:'';return {name:nm,brand:b,q:(b&&!nm.toLowerCase().includes(b.toLowerCase())?b+' ':'')+nm}}

window.lookupCode0=async function(code){const J=async u=>{const r=await fetch(u);if(!r.ok)throw r.status;return r.json()};const tries=[];
 /* varianti dello stesso codice: UPC-A (12 cifre) e EAN-13 con lo 0 davanti sono lo stesso prodotto */
 const alt=code.length===12?'0'+code:(code.length===13&&code[0]==='0'?code.slice(1):'');
 if(/^97[89]/.test(code)){
  tries.push(async()=>{const j=await J('https://openlibrary.org/api/books?bibkeys=ISBN:'+code+'&format=json&jscmd=data');const v=j['ISBN:'+code];if(!v||!v.title)return null;const au=(v.authors||[]).map(x=>x.name);return {dep:'stripbooks',name:v.title,brand:au.join(', '),img:v.cover&&(v.cover.medium||v.cover.small),q:v.title+' '+(au[0]||'')}});
  tries.push(async()=>{const j=await J('https://www.googleapis.com/books/v1/volumes?q=isbn:'+code);const v=j.items&&j.items[0]&&j.items[0].volumeInfo;if(!v)return null;return {name:v.title,brand:(v.authors||[]).join(', '),img:v.imageLinks&&(v.imageLinks.thumbnail||v.imageLinks.smallThumbnail),q:v.title+' '+((v.authors||[])[0]||'')}})}
 const HDEP={'world.openfoodfacts.org':'grocery','world.openbeautyfacts.org':'beauty','world.openpetfoodfacts.org':'pets','world.openproductsfacts.org':''};
 for(const cc of [code,alt].filter(Boolean))for(const host of ['world.openfoodfacts.org','world.openbeautyfacts.org','world.openpetfoodfacts.org','world.openproductsfacts.org'])tries.push(async()=>{const j=await J('https://'+host+'/api/v2/product/'+cc+'.json?fields=product_name,product_name_'+lang+',generic_name,brands,quantity,image_front_small_url');const p=j&&j.status===1&&j.product;const nm=p&&(p['product_name_'+lang]||p.product_name||p.generic_name);if(!nm)return null;const bl=(p.brands||'').split(',').map(x=>x.trim()).filter(Boolean);const br=cleanBrand(bl.find(x=>!/\b(srl|s\.?p\.?a|spa|services|gmbh|ltd|inc|sa)\b/i.test(x))||bl[0]||'');return {dep:HDEP[host],name:nm+(p.quantity?' · '+p.quantity:''),brand:br,img:p.image_front_small_url,q:(br&&!nm.toLowerCase().includes(br.toLowerCase())?br+' ':'')+nm+(p.quantity?' '+p.quantity:'')}});
 const upcUrl=(/^https?:/.test(location.protocol)&&!/claude|claudeusercontent|localhost|127\.0\.0\.1/.test(location.hostname))?'/api/upc?upc=':'https://api.upcitemdb.com/prod/trial/lookup?upc=';
 tries.push(async()=>{const q=code.length===13&&code[0]==='0'?code.slice(1):code;let j;try{j=await J(upcUrl+q)}catch(e){if(e===429){await new Promise(r=>setTimeout(r,1600));j=await J(upcUrl+q)}else{if(upcUrl[0]!=='/')throw e;j=await J('https://api.upcitemdb.com/prod/trial/lookup?upc='+q)}}const it=j&&j.items&&j.items[0];if(!it||!it.title)return null;return {name:it.title,brand:cleanBrand(it.brand||''),img:(it.images||[]).find(x=>/^https/.test(x))||(it.images||[])[0],q:it.title}});
 tries.push(()=>lookupWikidata(code));
 // tutte le banche dati in parallelo: vince la prima che risponde con un nome
 const wrap=t=>withTimeout(t(),8000).then(r=>{if(r&&r.name)return r;throw 0});
 try{const r=await Promise.any(tries.map(wrap));r.q=r.q.split(/\s+/).slice(0,9).join(' ');if(r.img)r.img=r.img.replace(/^http:/,'https:');return r}catch(e){return null}}

