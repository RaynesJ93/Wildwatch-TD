from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
css=r'''
    /* Polished game-menu theme */
    body{background:
      radial-gradient(circle at 20% 0%,#35643b55 0 16%,transparent 17%),
      radial-gradient(circle at 85% 8%,#4f7b4050 0 15%,transparent 16%),
      linear-gradient(180deg,#173e2c 0%,#0b2118 44%,#07150f 100%)}
    #app{max-width:820px}
    .topbar{margin:4px 0 12px;padding:8px 8px;border-radius:18px;background:linear-gradient(180deg,#183f2d,#0c241a);border:2px solid #476d52;box-shadow:0 8px 20px #0006,inset 0 1px #ffffff18}
    .brand{font-family:Impact,Haettenschweiler,'Arial Black',sans-serif;letter-spacing:.7px;color:#ffe08a;text-shadow:0 2px 0 #583a16,0 4px 7px #0009}
    .pill{background:linear-gradient(180deg,#193b2b,#0b2118);border:2px solid #56785c;box-shadow:inset 0 1px #ffffff1a,0 4px 10px #0005}
    .hero{border:2px solid #55735d;background:linear-gradient(145deg,#1f4933,#0c2118 68%);box-shadow:0 14px 30px #0008,inset 0 1px #ffffff1f}
    .primary{background:linear-gradient(180deg,#ffd965,#e2a82d);border:2px solid #fff09a;color:#3d2a08;box-shadow:0 5px 0 #8f651c,0 9px 16px #0005;text-shadow:0 1px #fff3b5}
    .primary:active{transform:translateY(3px);box-shadow:0 2px 0 #8f651c,0 5px 10px #0005}
    .secondary{background:linear-gradient(180deg,#39734f,#21503a);border:2px solid #639b74;box-shadow:0 4px 0 #143524,0 7px 12px #0004}
    .section-title{color:#ffe08a;text-shadow:0 2px #3e2b14}
    .menu-shell{position:relative;overflow:hidden;min-height:62vh;padding:24px 18px;border-radius:26px;border:2px solid #62816a;background:
      radial-gradient(circle at 8% 12%,#76a35a30 0 8%,transparent 9%),
      radial-gradient(circle at 92% 20%,#6b9c5030 0 10%,transparent 11%),
      linear-gradient(155deg,#244f35 0%,#10291d 58%,#091a13 100%);box-shadow:0 20px 45px #0009,inset 0 0 60px #99d36f10}
    .menu-logo{max-width:560px;margin:14px auto 22px;text-align:center}
    .menu-logo .critters{font-size:54px;letter-spacing:4px;filter:drop-shadow(0 5px 4px #0006)}
    .menu-logo h1{margin:4px 0 0;font-family:Impact,Haettenschweiler,'Arial Black',sans-serif;font-size:42px;line-height:.9;letter-spacing:1px;color:#ffc85a;text-transform:uppercase;-webkit-text-stroke:1px #583619;text-shadow:0 4px 0 #6e431b,0 8px 12px #0009}
    .menu-logo h1 span{display:block;color:#f1eee3;font-size:30px;margin-top:8px}
    .menu-tag{color:#c7dccb;text-align:center;margin:14px auto 26px;max-width:520px}
    .play-now{display:block;width:min(520px,92%);margin:0 auto;padding:18px 20px;font-size:24px;border-radius:18px;text-transform:uppercase}
    .save-grid{display:grid;gap:12px;margin-top:15px}
    .save-card{background:linear-gradient(155deg,#214b35,#0f281c);border:2px solid #5d8067;border-radius:20px;padding:14px;box-shadow:0 9px 20px #0005,inset 0 1px #ffffff14}
    .save-card-top{display:flex;align-items:center;justify-content:space-between;gap:10px}.save-card h3{margin:0;color:#ffe08a;font-size:20px}.slot-meta{margin:8px 0 12px;color:#c5d9ca;font-size:13px;line-height:1.45}.slot-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px}.backup-row{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:14px}
    @media(max-width:520px){.menu-logo h1{font-size:36px}.menu-logo h1 span{font-size:25px}.menu-logo .critters{font-size:44px}.backup-row{grid-template-columns:1fr}.slot-actions{grid-template-columns:1fr 1fr}}
'''
s=s.replace('</style>',css+'\n  </style>',1)
start=s.index('  <section id="homeScreen" class="screen active">')
end=s.index('  <section id="battleScreen" class="screen">',start)
new=r'''  <section id="homeScreen" class="screen active">
    <div class="menu-shell">
      <div class="menu-logo">
        <div class="critters">🦊 🦉 🐻 🐇</div>
        <h1>Critter Clan<span>Tower Defence</span></h1>
      </div>
      <p class="menu-tag">Build your animal squad, collect cards and defend the Wildwood.</p>
      <button class="primary play-now" id="chooseSaveBtn">▶ Play Now</button>
      <div style="height:14px"></div>
      <button class="secondary" id="continueBtn" style="display:none;width:min(520px,92%);margin:0 auto">↩ Continue Battle</button>
      <button class="primary" id="playBtn" style="display:none">▶ New Game</button>
    </div>
  </section>

  <section id="saveScreen" class="screen">
    <div class="menu-shell">
      <div class="hero center" style="padding:14px">
        <div style="font-size:40px">💾</div>
        <h1 style="margin:2px 0 4px">Select a Save</h1>
        <p>Choose a slot to continue, or store your current autosave in a slot.</p>
      </div>
      <div class="save-grid">
        <div class="save-card"><div class="save-card-top"><h3>🌲 Slot 1</h3><span class="small" id="slotDate1">Empty</span></div><div class="slot-meta" id="slotMeta1">No saved game yet.</div><div class="slot-actions"><button class="primary loadSlotBtn" data-slot="1">▶ Continue</button><button class="secondary saveSlotBtn" data-slot="1">💾 Save Here</button></div></div>
        <div class="save-card"><div class="save-card-top"><h3>🏜️ Slot 2</h3><span class="small" id="slotDate2">Empty</span></div><div class="slot-meta" id="slotMeta2">No saved game yet.</div><div class="slot-actions"><button class="primary loadSlotBtn" data-slot="2">▶ Continue</button><button class="secondary saveSlotBtn" data-slot="2">💾 Save Here</button></div></div>
        <div class="save-card"><div class="save-card-top"><h3>🌿 Slot 3</h3><span class="small" id="slotDate3">Empty</span></div><div class="slot-meta" id="slotMeta3">No saved game yet.</div><div class="slot-actions"><button class="primary loadSlotBtn" data-slot="3">▶ Continue</button><button class="secondary saveSlotBtn" data-slot="3">💾 Save Here</button></div></div>
      </div>
      <div class="backup-row"><button class="secondary" id="exportSaveBtn">📤 Export Backup</button><button class="secondary" id="importSaveBtn">📥 Import Backup</button></div>
      <div class="small center" id="saveStatus" style="margin-top:10px">Autosave is on.</div>
      <button class="secondary" id="backFromSaves" style="width:100%;margin-top:14px">← Back</button>
    </div>
  </section>

'''
s=s[:start]+new+s[end:]
# enhance save functions and route to battle after loading
s=s.replace('localStorage.setItem("wildwatchSave",JSON.stringify(restored));location.reload();','sessionStorage.setItem("critterOpenBattle","1");localStorage.setItem("wildwatchSave",JSON.stringify(restored));location.reload();',1)
# add renderSaveSlots and navigation after save functions block listener marker
needle='''setTimeout(()=>{\n  document.querySelectorAll(".saveSlotBtn")'''
if needle in s:
    rep='''function renderSaveSlots(){
  for(let i=1;i<=3;i++){
    const raw=localStorage.getItem(SAVE_SLOT_PREFIX+i),meta=document.getElementById("slotMeta"+i),date=document.getElementById("slotDate"+i);
    if(!raw){if(meta)meta.textContent="No saved game yet.";if(date)date.textContent="Empty";continue;}
    try{const d=JSON.parse(raw),x=d.save||d;if(meta)meta.textContent=`Level ${x.level||1} • ${x.metaCoins||0} coins • Best wave ${x.bestWave||0}`;if(date)date.textContent=d.savedAt?new Date(d.savedAt).toLocaleDateString():"Saved";}catch(e){if(meta)meta.textContent="Save data unreadable.";}
  }
}
setTimeout(()=>{
  document.getElementById("chooseSaveBtn")?.addEventListener("click",()=>{showScreen("saveScreen");renderSaveSlots();});
  document.getElementById("backFromSaves")?.addEventListener("click",()=>showScreen("homeScreen"));
  document.querySelectorAll(".saveSlotBtn")'''
    s=s.replace(needle,rep,1)
else:
    raise SystemExit('listener marker missing')
# refresh slot labels after save
s=s.replace('setSaveStatus(`Slot ${slot} saved • ${new Date().toLocaleString()}`);','setSaveStatus(`Slot ${slot} saved • ${new Date().toLocaleString()}`);renderSaveSlots();',1)
# after app JS initialization, route loaded slot to battle once
s=s.replace('</script>','''setTimeout(()=>{if(sessionStorage.getItem("critterOpenBattle")==="1"){sessionStorage.removeItem("critterOpenBattle");showScreen("battleScreen");}},80);
</script>''',1)
p.write_text(s)
