from pathlib import Path
p=Path('index.html')
s=p.read_text()

s=s.replace('''    <div style="display:flex;gap:8px;margin-top:8px">\n      <button class="secondary" style="flex:1" id="speedBtn">⏩ Speed: 1×</button>\n      <button class="danger" id="quitBtn">Quit</button>\n    </div>''','''    <div style="display:flex;gap:8px;margin-top:8px">\n      <button class="secondary" style="flex:1" id="speedBtn">⏩ Speed: 1×</button>\n      <button class="secondary" style="flex:1" id="autoWaveBtn">▶️ Auto: OFF</button>\n      <button class="danger" id="quitBtn">Quit</button>\n    </div>''',1)

s=s.replace('let battle={}, selectedCard=null, selectedTower=null, raf=0, last=performance.now(), speed=1;','let battle={}, selectedCard=null, selectedTower=null, raf=0, last=performance.now(), speed=1, autoWave=false, autoWaveTimer=0;',1)

s=s.replace('''  selectedCard=null; selectedTower=null; speed=1; speedBtn.textContent="⏩ Speed: 1×";''','''  selectedCard=null; selectedTower=null; speed=1; speedBtn.textContent="⏩ Speed: 1×";\n  if(typeof autoWaveBtn!=="undefined"&&autoWaveBtn)autoWaveBtn.textContent=`▶️ Auto: ${autoWave?"ON":"OFF"}`;''',1)

needle='speedBtn.onclick=()=>{speed=speed===1?2:speed===2?3:1;speedBtn.textContent=`⏩ Speed: ${speed}×`};'
if needle not in s:
    needle='speedBtn.onclick=()=>{speed=speed===1?2:1;speedBtn.textContent=`⏩ Speed: ${speed}×`};'
s=s.replace(needle,needle+'\nautoWaveBtn.onclick=()=>{autoWave=!autoWave;autoWaveBtn.textContent=`▶️ Auto: ${autoWave?"ON":"OFF"}`;autoWaveBtn.classList.toggle("primary",autoWave);autoWaveBtn.classList.toggle("secondary",!autoWave);message.textContent=autoWave?"Auto waves ON — the next wave will start automatically.":"Auto waves OFF.";};',1)

# Trigger the next wave shortly after a normal wave clear, but never after map completion/defeat.
marker='''  if(clearedWave>=15){'''
insert='''  if(autoWave && clearedWave<15 && !battle.ended){\n    clearTimeout(autoWaveTimer);\n    autoWaveTimer=setTimeout(()=>{if(autoWave && !battle.waveActive && !battle.ended)startWave.click();},900);\n  }\n  if(clearedWave>=15){'''
if marker not in s:
    raise SystemExit('finishWave marker missing')
s=s.replace(marker,insert,1)

p.write_text(s)
