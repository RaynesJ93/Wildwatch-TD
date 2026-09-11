from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='// MAP_VISUAL_FIX_V2: force canvas render on every battle entry path'
if marker in s:
    raise SystemExit('battle map render v2 already present')

# 1) Continue Playing previously bypassed showScreen(), so force the canvas to draw
# immediately and restart the animation loop even when a saved battle loads successfully.
old='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));if(!loadBattleState())resetBattle();};'''
new='''continueBtn.onclick=()=>{document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="battleScreen"));document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen==="battleScreen"));document.body.classList.add("battle-mode");if(!loadBattleState())resetBattle();/* MAP_VISUAL_FIX_V2: force canvas render on every battle entry path */draw();if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}};'''
if old not in s:
    raise SystemExit('continue button marker not found')
s=s.replace(old,new,1)

# 2) Opening an already-active battle via the Battle tab must also repaint immediately.
old2='''  }else if(id==="battleScreen"){
    document.body.classList.add("battle-mode");
  }
}'''
new2='''  }else if(id==="battleScreen"){
    document.body.classList.add("battle-mode");
    draw();
    if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}
  }
}'''
if old2 not in s:
    raise SystemExit('battle-screen entry marker not found')
s=s.replace(old2,new2,1)

# 3) Restarting after a difficulty change should repaint without waiting for Start wave.
old3='''  clearBattleState();
  resetBattle();
  updateDifficultyUI();'''
new3='''  clearBattleState();
  resetBattle();
  draw();
  if(!raf){last=performance.now();raf=requestAnimationFrame(loop);}
  updateDifficultyUI();'''
if old3 in s:
    s=s.replace(old3,new3,1)

p.write_text(s,encoding='utf-8')
print('Applied battle-map render repair to Continue, Battle tab, and difficulty reset paths')
