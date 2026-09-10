from pathlib import Path
p=Path('index.html');s=p.read_text()
old='''    <div style="display:grid;gap:10px;margin-top:14px">
      <button class="primary loadSlotBtn" data-slot="1">Save Slot 1</button>
      <button class="primary loadSlotBtn" data-slot="2">Save Slot 2</button>
      <button class="primary loadSlotBtn" data-slot="3">Save Slot 3</button>
    </div>
    <div class="section-title">Save management</div>
    <div class="info-box" style="display:grid;gap:9px">
      <div class="small">Save your current progress into a slot, or keep a backup file outside the browser.</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px">
        <button class="secondary saveSlotBtn" data-slot="1">💾 Save 1</button><button class="secondary saveSlotBtn" data-slot="2">💾 Save 2</button><button class="secondary saveSlotBtn" data-slot="3">💾 Save 3</button>
      </div>
      <div style="display:flex;gap:7px;flex-wrap:wrap"><button class="secondary" id="exportSaveBtn">📤 Export Backup</button><button class="secondary" id="importSaveBtn">📥 Import Backup</button></div>
      <div class="small" id="saveStatus">Autosave is on.</div>
    </div>'''
new='''    <div id="saveSlotList" style="display:grid;gap:10px;margin-top:14px">
      <button class="primary loadSlotBtn" data-slot="1">Loading Slot 1…</button>
      <button class="primary loadSlotBtn" data-slot="2">Loading Slot 2…</button>
      <button class="primary loadSlotBtn" data-slot="3">Loading Slot 3…</button>
    </div>
    <div class="section-title">Backups</div>
    <div class="info-box" style="display:grid;gap:9px">
      <div class="small">Your selected slot autosaves while you play. You can also export a backup file outside the browser.</div>
      <div style="display:flex;gap:7px;flex-wrap:wrap"><button class="secondary" id="exportSaveBtn">📤 Export Backup</button><button class="secondary" id="importSaveBtn">📥 Import Backup</button></div>
      <div class="small" id="saveStatus">Autosave is on.</div>
    </div>'''
assert old in s;s=s.replace(old,new,1)
start=s.index('function persist(){localStorage.setItem("wildwatchSave",JSON.stringify(save)); renderMeta();}')
end=s.index('function saveBattleState(){',start)
newjs='''function getSlotRecord(slot){
  try{const raw=localStorage.getItem(SAVE_SLOT_PREFIX+slot);if(!raw)return null;const d=JSON.parse(raw);if(d&&d.save&&typeof d.save==="object")return d;if(d&&typeof d==="object")return {version:1,name:`Save ${slot}`,savedAt:null,save:d};}catch(e){}return null;
}
const SAVE_SLOT_PREFIX="wildwatchSaveSlot";
const ACTIVE_SLOT_KEY="wildwatchActiveSlot";
function persist(){
  localStorage.setItem("wildwatchSave",JSON.stringify(save));
  const active=localStorage.getItem(ACTIVE_SLOT_KEY);
  if(active){const old=getSlotRecord(active);const name=old?.name||`Save ${active}`;localStorage.setItem(SAVE_SLOT_PREFIX+active,JSON.stringify({version:2,name,savedAt:new Date().toISOString(),save}));}
  renderMeta();renderSaveSlots();
}
function setSaveStatus(msg){const el=document.getElementById("saveStatus");if(el)el.textContent=msg;}
function slotSummary(rec,slot){
  if(!rec)return `<b>＋ Create Save ${slot}</b><span>Tap to name this save and keep your current progress.</span>`;
  const sv=rec.save||{};const forest=sv.forestPinesUnlocked||1;const desert=sv.desertDunesUnlocked||0;const where=desert>0?`Desert ${desert}`:`Forest ${forest}`;
  const when=rec.savedAt?new Date(rec.savedAt).toLocaleString():"Saved";
  return `<b>💾 ${rec.name||`Save ${slot}`}</b><span>⭐ Level ${sv.level||1} • 🟡 ${sv.metaCoins||0} • ${where}</span><small>${when}</small>`;
}
function renderSaveSlots(){
  document.querySelectorAll(".loadSlotBtn").forEach(b=>{const slot=b.dataset.slot,rec=getSlotRecord(slot);b.innerHTML=slotSummary(rec,slot);b.style.display="grid";b.style.gap="4px";b.style.textAlign="left";b.querySelectorAll("span,small").forEach(x=>{x.style.fontSize="12px";x.style.opacity=".82"});});
  const active=localStorage.getItem(ACTIVE_SLOT_KEY);if(active)setSaveStatus(`Autosaving to ${getSlotRecord(active)?.name||`Save ${active}`}.`);
}
function createSlot(slot){
  const raw=prompt(`Name Save ${slot}:`,`Adventure ${slot}`);if(raw===null)return;const name=(raw.trim()||`Save ${slot}`).slice(0,24);
  localStorage.setItem(SAVE_SLOT_PREFIX+slot,JSON.stringify({version:2,name,savedAt:new Date().toISOString(),save}));
  localStorage.setItem(ACTIVE_SLOT_KEY,String(slot));renderSaveSlots();setSaveStatus(`${name} created from your current progress. Autosave is on.`);
}
function loadFromSlot(slot){
  const rec=getSlotRecord(slot);if(!rec){createSlot(slot);return;}
  const name=rec.name||`Save ${slot}`;
  if(!confirm(`Continue ${name}?\n\nLevel ${rec.save?.level||1} • ${rec.save?.metaCoins||0} Coins\n\nYour current autosave will be protected before switching.`))return;
  localStorage.setItem("wildwatchSafetyBackup",JSON.stringify({savedAt:new Date().toISOString(),save}));
  localStorage.setItem(ACTIVE_SLOT_KEY,String(slot));
  localStorage.setItem("wildwatchSave",JSON.stringify(rec.save));
  location.reload();
}
function renameActiveSlot(){const active=localStorage.getItem(ACTIVE_SLOT_KEY);if(!active)return;const rec=getSlotRecord(active);if(!rec)return;const raw=prompt("Rename this save:",rec.name||`Save ${active}`);if(raw===null)return;rec.name=(raw.trim()||`Save ${active}`).slice(0,24);localStorage.setItem(SAVE_SLOT_PREFIX+active,JSON.stringify(rec));renderSaveSlots();}
function exportSaveBackup(){
  const active=localStorage.getItem(ACTIVE_SLOT_KEY);const rec=active?getSlotRecord(active):null;
  const payload=JSON.stringify({game:"Critter Clan Tower Defence",version:2,name:rec?.name||"Autosave",exportedAt:new Date().toISOString(),save},null,2);
  const blob=new Blob([payload],{type:"application/json"});const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download=`critter-clan-backup-${new Date().toISOString().slice(0,10)}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);setSaveStatus("Backup exported. Keep the JSON file somewhere safe.");
}
function importSaveBackup(){
  const input=document.createElement("input");input.type="file";input.accept="application/json,.json";input.onchange=()=>{const file=input.files&&input.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{try{const data=JSON.parse(reader.result);const restored=data&&data.save?data.save:data;if(!restored||typeof restored!=="object"||!Array.isArray(restored.deck))throw 0;if(!confirm("Import this backup? Your current autosave will be protected first."))return;localStorage.setItem("wildwatchSafetyBackup",JSON.stringify({savedAt:new Date().toISOString(),save}));localStorage.setItem("wildwatchSave",JSON.stringify(restored));const active=localStorage.getItem(ACTIVE_SLOT_KEY);if(active){const old=getSlotRecord(active);localStorage.setItem(SAVE_SLOT_PREFIX+active,JSON.stringify({version:2,name:data.name||old?.name||`Save ${active}`,savedAt:new Date().toISOString(),save:restored}));}location.reload();}catch(e){alert("That is not a valid Critter Clan save backup.");}};reader.readAsText(file);};input.click();
}
setTimeout(()=>{
  document.getElementById("chooseSaveBtn")?.addEventListener("click",()=>{renderSaveSlots();showScreen("saveScreen")});
  document.getElementById("backFromSaves")?.addEventListener("click",()=>showScreen("homeScreen"));
  document.querySelectorAll(".loadSlotBtn").forEach(b=>b.addEventListener("click",()=>loadFromSlot(b.dataset.slot)));
  document.getElementById("exportSaveBtn")?.addEventListener("click",exportSaveBackup);
  document.getElementById("importSaveBtn")?.addEventListener("click",importSaveBackup);
  renderSaveSlots();
},0);
'''
s=s[:start]+newjs+s[end:]
p.write_text(s)
