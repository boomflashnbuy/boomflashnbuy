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
   else{nf=true;q='';if(w)w.outerHTML=askBox(code,v=>{q=v;name=v;dep=guessDep(v)})}})};
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
;
window.scanResult=function(code){const b=$('#sbx'),S=SCN[lang],P=PLK[lang];if(!b)return;b.className='sbx done';addRecent(code);
 b.innerHTML=`<div class="sres"><span class="ok2">✓</span><div><small>${S[2]}</small><b>${esc(code)}</b></div></div><p class="sdesc" id="plk">⏳ ${P[0]}</p>`;
 lookupCode(code).then(info=>{if(!$('#sbx')||$('#sbx').className!=='sbx done')return;
  const o={what:info?info.q:(gs1Brand(code)||code)},oc={what:code};let price=0;
  const mk=mkList().map(m=>`<a href="${amazonUrl(o,{dom:MK[m][1]})}" target="_blank" rel="noopener sponsored" class="${MK[m][1]===STORE?'cur':''}">${MK[m][0]} ${m.toUpperCase()}</a>`).join('');
  b.innerHTML=(info?`<div class="pcard">${info.img?`<img src="${esc(info.img)}" alt="" loading="lazy" onerror="this.remove()">`:''}<div><small>${S[2]} · ${esc(code)}</small><b>${esc(info.name)}</b>${info.brand?`<span>${esc(info.brand)}</span>`:''}</div></div>`
   :`<div class="sres"><span class="ok2">✓</span><div><small>${S[2]}</small><b>${esc(code)}</b></div></div>`+askBox(code,v=>{o.what=v||code;upd()})+`<a class="again" href="${amazonUrl(oc)}" target="_blank" rel="noopener sponsored">${(NF[lang]||NF.en).codeS}</a>`)+
  `<label class="pq">${P[1]}<span><input id="sp" inputmode="decimal" placeholder="0"><b>${cur()}</b></span></label>
  <a class="cta" id="scta" href="${amazonUrl(o)}" target="_blank" rel="noopener sponsored"><span id="sctat">${P[3]}</span> <span>→</span></a>
  <div class="mk">${mk}</div>
  <div class="row"><button class="opt" type="button" id="sag">📷 ${S[4]}</button><button class="opt" type="button" id="ssv">${X[lang].save}</button></div>
  ${info?`<a class="again" href="${amazonUrl(oc)}" target="_blank" rel="noopener sponsored">${P[5]}</a>`:''}`;
  const upd=()=>{const v=parseFloat(($('#sp').value||'').replace(',','.'));price=v>0?v:0;const oo=Object.assign({},o,price?{budget:Math.max(1,Math.ceil(price)-1)}:{});$('#scta').href=amazonUrl(oo,price?{sort:'price-asc-rank'}:{});$('#sctat').textContent=price?`${P[2]} ${money(price)}`:P[3]};
  $('#sp').oninput=upd;if(!info)$('#scta').addEventListener('click',()=>{if(o.what&&o.what!==code)teachCode(code,o.what)});
  $('#sag').onclick=scanOpen;$('#ssv').onclick=e=>{const q=info?info.q:code;const a2=getSaved().filter(x=>x!==q);a2.unshift(q);setSaved(a2);e.currentTarget.textContent=X[lang].saved;myTop()}})}
;
(()=>{const st=document.createElement('style');st.textContent='.nfask{font-weight:800;font-size:17px;margin:10px 0 6px}.nfhint{display:block;color:#b9c2b2;margin:-2px 0 6px}.nfrow{display:flex;gap:8px;align-items:center}.nfrow .lqi{flex:1;margin:0}.nfmic{flex:0 0 48px;height:48px;border-radius:14px;border:1.5px solid #D4FF4A;background:#171914;font-size:22px;cursor:pointer}.nfmic.on{background:#D4FF4A;animation:pulse 1s infinite}@keyframes shk{0%,100%{transform:none}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}.shake{animation:shk .35s;border-color:#ff5a5a!important}';document.head.appendChild(st)})();