from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='TOWER_TARGETING_DROPDOWN_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)

# Add targeting dropdown to tower modal.
old='''<div class="modal" id="towerModal">\n  <div class="sheet">\n    <h2 id="towerName">Animal</h2>\n    <p id="towerInfo" class="small"></p>\n    <div style="display:flex;gap:8px">'''
new='''<div class="modal" id="towerModal">\n  <div class="sheet">\n    <h2 id="towerName">Animal</h2>\n    <p id="towerInfo" class="small"></p>\n    <div style="margin:10px 0 12px">\n      <label for="towerTargetMode" style="display:block;font-weight:900;margin-bottom:6px">Targeting</label>\n      <select id="towerTargetMode" style="width:100%;padding:11px 12px;border-radius:12px;border:1px solid #4b8469;background:#0f211a;color:#f4fff8;font:inherit;font-weight:800">\n        <option value="closest">Closest</option>\n        <option value="strongest">Strongest</option>\n        <option value="last">Last</option>\n      </select>\n      <div class="small" style="margin-top:5px">Closest = nearest enemy • Strongest = highest HP • Last = furthest back on the path</div>\n    </div>\n    <div style="display:flex;gap:8px">'''
if old not in s: raise RuntimeError('tower modal anchor missing')
s=s.replace(old,new,1)

# New towers default to closest targeting.
old='battle.towers.push({key:selectedCard,x,y,pad:null,cd:0,level:1,spent:a.cost});'
new='battle.towers.push({key:selectedCard,x,y,pad:null,cd:0,level:1,spent:a.cost,targetMode:"closest"});'
if old not in s: raise RuntimeError('tower placement anchor missing')
s=s.replace(old,new,1)

# Replace existing automatic target selection.
old='''  let target=null,best=-1;\n  battle.enemies.forEach(e=>{if(e.dead)return;const d=Math.hypot(e.x-t.x,e.y-t.y);if(d<=range){const prog=e.seg+(1-d/1000);if(prog>best){best=prog;target=e}}});'''
new='''  // TOWER_TARGETING_DROPDOWN_V1: per-tower target priority.\n  const inRange=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);\n  let target=null;\n  const mode=t.targetMode||"closest";\n  if(inRange.length){\n    if(mode==="strongest"){\n      target=inRange.reduce((best,e)=>!best||e.hp>best.hp?e:best,null);\n    }else if(mode==="last"){\n      target=inRange.reduce((best,e)=>{\n        const ep=Number(e.seg||0),bp=best?Number(best.seg||0):Infinity;\n        return !best||ep<bp?e:best;\n      },null);\n    }else{\n      target=inRange.reduce((best,e)=>!best||Math.hypot(e.x-t.x,e.y-t.y)<Math.hypot(best.x-t.x,best.y-t.y)?e:best,null);\n    }\n  }'''
if old not in s: raise RuntimeError('target selection anchor missing')
s=s.replace(old,new,1)

# Sync dropdown when popup opens and when HUD refreshes it.
open_anchor='''  upgradeTower.textContent=`Upgrade • 🥩 ${up}`;\n  upgradeTower.disabled=cash<up;\n  upgradeTower.style.opacity=cash<up?".55":"1";\n  towerModal.classList.add("show");'''
open_repl='''  upgradeTower.textContent=`Upgrade • 🥩 ${up}`;\n  upgradeTower.disabled=cash<up;\n  upgradeTower.style.opacity=cash<up?".55":"1";\n  if(typeof towerTargetMode!=="undefined"&&towerTargetMode)towerTargetMode.value=t.targetMode||"closest";\n  towerModal.classList.add("show");'''
if open_anchor not in s: raise RuntimeError('openTowerModal anchor missing')
s=s.replace(open_anchor,open_repl,1)

hud_anchor='''    upgradeTower.disabled=cash<up;\n    upgradeTower.style.opacity=cash<up?".55":"1";\n  }\n}'''
hud_repl='''    upgradeTower.disabled=cash<up;\n    upgradeTower.style.opacity=cash<up?".55":"1";\n    if(typeof towerTargetMode!=="undefined"&&towerTargetMode)towerTargetMode.value=selectedTower.targetMode||"closest";\n  }\n}'''
if hud_anchor not in s: raise RuntimeError('HUD tower modal anchor missing')
s=s.replace(hud_anchor,hud_repl,1)

# Apply target choice immediately.
anchor='closeTower.onclick=()=>{towerModal.classList.remove("show");selectedTower=null;};'
insert='''towerTargetMode.onchange=()=>{\n  if(!selectedTower)return;\n  selectedTower.targetMode=towerTargetMode.value||"closest";\n};\n'''
if anchor not in s: raise RuntimeError('closeTower anchor missing')
s=s.replace(anchor,insert+anchor,1)

p.write_text(s,encoding='utf-8')
print('Added tower targeting dropdown: Closest / Strongest / Last')
