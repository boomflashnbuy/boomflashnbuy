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
 setTimeout(()=>{const i=$('#nfq'),m=$('#nfmic');if(!i)return;i.oninput=()=>onQ(enrichQ(i.value));if(i.value.trim())onQ(enrichQ(i.value));m&&(m.onclick=()=>dictate(i,m));try{i.focus();i.setSelectionRange(i.value.length,i.value.length)}catch(e){}},30);
 return h}
window.lookupWikidata=async function(code){const alt=code.length===12?'0'+code:code;const q=`SELECT ?l ?b WHERE {VALUES ?g {"${code}" "${alt}"} ?i wdt:P3962 ?g. ?i rdfs:label ?l. FILTER(LANG(?l) IN ("${lang}","en")) OPTIONAL{?i wdt:P1716 ?x. ?x rdfs:label ?b. FILTER(LANG(?b)="en")}} LIMIT 1`;
 const r=await fetch('https://query.wikidata.org/sparql?format=json&query='+encodeURIComponent(q));if(!r.ok)throw r.status;const j=await r.json();const x=j.results.bindings[0];if(!x)return null;
 const nm=x.l.value,b=x.b?x.b.value:'';return {name:nm,brand:b,q:(b&&!nm.toLowerCase().includes(b.toLowerCase())?b+' ':'')+nm}}


window.boomOpen=function(){boomClose(true);if(scanStop){scanStop();scanStop=null}const K=BM[lang]||BM.en;
 const o=document.createElement('div');o.id='boomv';o.className='boomv';
 o.innerHTML=`<div class="bm-top"><img src="${LOGO}" alt=""><b class="q" id="bmw0">BOOM?</b><span>FlashnBuy</span><button class="snd" type="button"></button></div>
  <div class="bm-cam"><video playsinline muted></video><i class="bm-frame"></i><i class="bm-laser"></i>
   <div class="vtools"><button type="button" id="bt-t" hidden>🔦</button><button type="button" id="bt-z" hidden>🔍 2×</button></div></div>
  <p class="bm-msg" id="bmmsg">${K.t}</p>
  <div class="bm-card" id="bmcard" hidden></div>
  <button class="bm-ocr" type="button" id="bmocr">🔤 ${K.label}</button>
  <p class="bm-go" id="bmgo" hidden><span>${K.go}</span><i>⬇</i></p>
  <button class="bm-btn" type="button" id="bmbtn"><span class="bm-ic">✕</span><span class="bm-tx">${K.close}</span></button>
  <button type="button" class="bm-app" id="bmapp"><img class="bm-ai" src="${LOGO}" alt="">${K.app} <i>→</i></button>`;
 document.body.appendChild(o);sndPaint();requestAnimationFrame(()=>o.classList.add('on'));
 let st='scan',q='',dep='',name='',ean='',nf=false;
 const btn=$('#bmbtn'),card=$('#bmcard'),msg=$('#bmmsg'),v=o.querySelector('video');
 const toFound=()=>{st='found';o.classList.add('hit');const w0=$('#bmw0');if(w0){w0.textContent='BOOM!';w0.classList.remove('q');w0.classList.add('lit')}$('#bmgo').hidden=false;btn.classList.add('found');btn.querySelector('.bm-ic').textContent='✓';btn.querySelector('.bm-tx').textContent=K.found+' →';$('#bmocr').hidden=true};
 const showCard=(title,sub,extra)=>{card.hidden=false;card.innerHTML=`<small>${sub}</small><b>${esc(title)}</b>${extra||''}
   <label class="bm-pq"><span class="bm-pl">${K.store}<em>${K.opt}</em></span><span><input id="bmsp" inputmode="decimal" placeholder="0"><b>${cur()}</b></span></label><p class="bm-anon">${PRN[lang]||PRN.en}</p>
   <button type="button" class="bm-again" id="bmag">📷 ${K.again}</button>`;$('#bmag').onclick=boomOpen};
 const onCode=code=>{beep();try{navigator.vibrate&&navigator.vibrate(60)}catch(e){}toFound();msg.textContent='';
  const isNum=/^\d{6,14}$/.test(code);q=isNum?code:enrichQ(code.slice(0,80));name=q;ean=isNum?code:'';addRecent(q);
  showCard(isNum?code:q,K.read,`<p class="bm-wait" id="bmw">⏳ ${K.look}</p>`);
  if(!isNum){dep=guessDep(q);return}
  lookupCode(code).then(info=>{const w=$('#bmw');if(!$('#boomv'))return;
   if(info){q=info.q;name=info.name;dep=info.dep||guessDep(info.q+' '+(info.brand||''));const sp=$('#bmsp')&&$('#bmsp').value;showCard(info.name,(info.brand?info.brand+' · ':'')+code);if(sp)$('#bmsp').value=sp}
   else{nf=true;q='';if(w)w.outerHTML=askBox(code,v=>{q=v;name=v;dep=guessDep(v)});const bt=btn.querySelector('.bm-tx');if(bt)bt.textContent=PLK[lang][3]+' →'}})};
 const onFail=()=>{msg.textContent=K.camNo;o.querySelector('.bm-cam').classList.add('off');$('#bmocr').hidden=true};
 boomCam=camStart(v,onCode,onFail,{onReady:api=>{const cp=api.caps();
   if(cp.torch){const t=$('#bt-t');t.hidden=false;let on=false;t.onclick=async()=>{on=!on;await api.torch(on);t.classList.toggle('on',on)}}
   if(cp.zoom&&cp.zoom.max>=1.5){const z=$('#bt-z');z.hidden=false;let on=false;z.onclick=async()=>{on=!on;await api.zoom(on?Math.min(2.5,cp.zoom.max):cp.zoom.min||1);z.classList.toggle('on',on)}}},
  onSlow:()=>{if(st==='scan'){msg.textContent='💡 '+K.nc;$('#bmocr').classList.add('pulse')}}});
 $('#bmapp').onclick=()=>boomClose(false,true);
 $('#bmocr').onclick=async()=>{const c=boomCam&&boomCam.grab();if(!c)return;const b=$('#bmocr');b.disabled=true;b.textContent='⏳ '+K.reading;
  try{const r=await withTimeout(readLabel(c),25000);if(r&&r.q&&r.q.length>2){boomCam.stop();beep();toFound();q=enrichQ(r.q);name=r.q;dep=guessDep(r.q);addRecent(q);showCard(r.q,'🔤 '+K.label)}else{b.disabled=false;b.textContent='🔤 '+K.label;msg.textContent=K.ocrNo}}
  catch(e){b.disabled=false;b.textContent='🔤 '+K.label;msg.textContent=K.ocrNo}};
 btn.onclick=()=>{if(st==='scan'){boomClose();return}
  if(!q||q===ean){const i=$('#nfq');if(i){i.focus();i.classList.remove('shake');void i.offsetWidth;i.classList.add('shake')}return}if(nf&&ean)teachCode(ean,q);
  const sp=parseFloat((($('#bmsp')||{}).value||'').replace(',','.'));const url=amazonUrl({what:q},{dep:dep});
  if(sp>0){try{localStorage.setItem('snb-pend',JSON.stringify({t:Date.now(),n:name||q,store:sp,e:ean}))}catch(e){}reportPrice({e:ean,n:name||q,p:sp})}
  kaching();if(isPhone()&&!installed()){goAmazon(url);return}const a=document.createElement('a');a.href=url;a.target='_blank';a.rel='noopener sponsored';document.body.appendChild(a);a.click();a.remove()}}
