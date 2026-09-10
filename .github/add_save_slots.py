from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''    <div class="section-title">Current deck</div>'''
new='''    <div class="section-title">Save slots & backup</div>
    <div class="info-box" style="display:grid;gap:9px">
      <div class="small">Keep extra copies of your progress on this device, and export a backup for safekeeping.</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px">
        <button class="secondary saveSlotBtn" data-slot="1">💾 Save 1</button>
        <button class="secondary saveSlotBtn" data-slot="2">💾 Save 2</button>
        <button class="secondary saveSlotBtn" data-slot="3">💾 Save 3</button>
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px">
        <button class="secondary loadSlotBtn" data-slot="1">↩ Load 1</button>
        <button class="secondary loadSlotBtn" data-slot="2">↩ Load 2</button>
        <button class="secondary loadSlotBtn" data-slot="3">↩ Load 3</button>
      </div>
      <div style="display:flex;gap:7px;flex-wrap:wrap">
        <button class="secondary" id="exportSaveBtn">📤 Export Backup</button>
        <button class="secondary" id="importSaveBtn">📥 Import Backup</button>
      </div>
      <div class="small" id="saveStatus">Autosave is on.</div>
    </div>

    <div class="section-title">Current deck</div>'''
assert old in s
s=s.replace(old,new,1)
old2='''function persist(){localStorage.setItem("wildwatchSave",JSON.stringify(save)); renderMeta();}'''
new2='''function persist(){localStorage.setItem("wildwatchSave",JSON.stringify(save)); renderMeta();}
const SAVE_SLOT_PREFIX="wildwatchSaveSlot";
function setSaveStatus(msg){const el=document.getElementById("saveStatus");if(el)el.textContent=msg;}
function saveToSlot(slot){
  localStorage.setItem(SAVE_SLOT_PREFIX+slot,JSON.stringify({version:1,savedAt:new Date().toISOString(),save}));
  setSaveStatus(`Slot ${slot} saved • ${new Date().toLocaleString()}`);
}
function loadFromSlot(slot){
  const raw=localStorage.getItem(SAVE_SLOT_PREFIX+slot);if(!raw){alert(`Save slot ${slot} is empty.`);return;}
  try{const data=JSON.parse(raw);const restored=data&&data.save?data.save:data;if(!restored||typeof restored!=="object")throw 0;
    if(!confirm(`Load save slot ${slot}? Your current autosave will be replaced.`))return;
    localStorage.setItem("wildwatchSave",JSON.stringify(restored));location.reload();
  }catch(e){alert(`Save slot ${slot} could not be read.`);}
}
function exportSaveBackup(){
  const payload=JSON.stringify({game:"Critter Clan Tower Defence",version:1,exportedAt:new Date().toISOString(),save},null,2);
  const blob=new Blob([payload],{type:"application/json"});const url=URL.createObjectURL(blob);const a=document.createElement("a");
  a.href=url;a.download=`critter-clan-backup-${new Date().toISOString().slice(0,10)}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  setSaveStatus("Backup exported. Keep the JSON file somewhere safe.");
}
function importSaveBackup(){
  const input=document.createElement("input");input.type="file";input.accept="application/json,.json";input.onchange=()=>{const file=input.files&&input.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{try{const data=JSON.parse(reader.result);const restored=data&&data.save?data.save:data;if(!restored||typeof restored!=="object"||!Array.isArray(restored.deck))throw 0;if(!confirm("Import this backup? Your current autosave will be replaced."))return;localStorage.setItem("wildwatchSave",JSON.stringify(restored));location.reload();}catch(e){alert("That is not a valid Critter Clan save backup.");}};reader.readAsText(file);};input.click();
}
setTimeout(()=>{
  document.querySelectorAll(".saveSlotBtn").forEach(b=>b.addEventListener("click",()=>saveToSlot(b.dataset.slot)));
  document.querySelectorAll(".loadSlotBtn").forEach(b=>b.addEventListener("click",()=>loadFromSlot(b.dataset.slot)));
  document.getElementById("exportSaveBtn")?.addEventListener("click",exportSaveBackup);
  document.getElementById("importSaveBtn")?.addEventListener("click",importSaveBackup);
},0);'''
assert old2 in s
s=s.replace(old2,new2,1)
p.write_text(s)
