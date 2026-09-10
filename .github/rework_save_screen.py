from pathlib import Path
p=Path('index.html');s=p.read_text()
old='''      <button class="primary" id="playBtn">▶ New Game</button>
      <button class="secondary" id="continueBtn" style="display:none;margin-left:8px">↩ Continue Battle</button>
    </div>

    <div class="section-title">Save slots & backup</div>
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
'''
new='''      <button class="primary" id="chooseSaveBtn" style="width:100%;font-size:18px">▶ Play Now</button>
      <button class="secondary" id="continueBtn" style="display:none;margin-top:9px;width:100%">↩ Continue Battle</button>
      <button class="primary" id="playBtn" style="display:none">▶ New Game</button>
    </div>
'''
assert old in s;s=s.replace(old,new,1)
anchor='''  <section id="battleScreen" class="screen">'''
save_screen='''  <section id="saveScreen" class="screen">
    <div class="hero center">
      <div style="font-size:48px">💾</div><h1>Choose your save</h1>
      <p>Select a save slot to continue. Your normal autosave is kept separately.</p>
    </div>
    <div style="display:grid;gap:10px;margin-top:14px">
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
    </div>
    <button class="secondary" id="backFromSaves" style="width:100%;margin-top:12px">← Back</button>
  </section>

'''
assert anchor in s;s=s.replace(anchor,save_screen+anchor,1)
needle='''setTimeout(()=>{
  document.querySelectorAll(".saveSlotBtn")'''
rep='''setTimeout(()=>{
  document.getElementById("chooseSaveBtn")?.addEventListener("click",()=>showScreen("saveScreen"));
  document.getElementById("backFromSaves")?.addEventListener("click",()=>showScreen("homeScreen"));
  document.querySelectorAll(".saveSlotBtn")'''
assert needle in s;s=s.replace(needle,rep,1)
p.write_text(s)
