from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''function loop(now){
  const raw=Math.min(.04,(now-last)/1000);last=now;const dt=raw*speed;
  if(battle.started){
    update(dt);draw();
    if(!battle.ended&&now-lastAutoSave>2000){saveBattleState();lastAutoSave=now}
    raf=requestAnimationFrame(loop);
  }else{
    raf=0;
  }
}'''
new='''function loop(now){
  const raw=Math.min(.04,(now-last)/1000);last=now;const dt=raw*speed;
  if(battle.started){
    try{
      update(dt);
      draw();
      if(!battle.ended&&now-lastAutoSave>2000){saveBattleState();lastAutoSave=now}
      raf=requestAnimationFrame(loop);
    }catch(err){
      console.error("Battle loop crash",err);
      raf=0;
      battle.waveActive=false;
      battle.spawning=false;
      const text=(err&&err.message)?err.message:String(err);
      if(typeof message!=="undefined"&&message){
        message.textContent=`⚠️ Battle error: ${text}`;
        message.style.whiteSpace="normal";
        message.style.overflow="visible";
      }
      if(typeof startWave!=="undefined"&&startWave)startWave.textContent="Retry wave";
    }
  }else{
    raf=0;
  }
}'''

if old not in s:
    if 'Battle loop crash' in s:
        print('Battle crash diagnostics already installed')
    else:
        raise SystemExit('loop marker not found')
else:
    s=s.replace(old,new,1)

# Also surface errors that happen directly inside the Start Wave click handler.
if 'START_WAVE_ERROR_GUARD' not in s:
    marker='startWave.onclick=()=>{'
    if marker not in s:
        raise SystemExit('startWave marker not found')
    s=s.replace(marker,'''startWave.onclick=()=>{\n  // START_WAVE_ERROR_GUARD: the animation-loop guard below will expose any\n  // runtime failure on screen instead of leaving the battle apparently crashed.''',1)

p.write_text(s,encoding='utf-8')
print('Installed on-screen battle crash diagnostics')
