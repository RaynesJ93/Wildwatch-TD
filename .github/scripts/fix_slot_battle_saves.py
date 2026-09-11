from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = 'const ACTIVE_SLOT_KEY="wildwatchActiveSlot";'
helper = '''const ACTIVE_SLOT_KEY="wildwatchActiveSlot";\nconst BATTLE_SAVE_PREFIX="wildwatchBattleSave";\nfunction battleSaveKey(){\n  const active=localStorage.getItem(ACTIVE_SLOT_KEY);\n  return active?`${BATTLE_SAVE_PREFIX}${active}`:BATTLE_SAVE_PREFIX;\n}\n'''
if marker not in s:
    raise SystemExit('ACTIVE_SLOT_KEY marker not found')
s = s.replace(marker, helper, 1)

old = '''function saveBattleState(){\n  if(!battle?.started || battle.ended)return;\n  localStorage.setItem("wildwatchBattleSave",JSON.stringify({...battle,mapNumber:currentMap,mapSeries:currentSeries,shots:[]}));\n  continueBtn.style.display="inline-block";\n}\nfunction clearBattleState(){localStorage.removeItem("wildwatchBattleSave");continueBtn.style.display="none"}\nfunction loadBattleState(){\n  try{\n    const raw=localStorage.getItem("wildwatchBattleSave"); if(!raw)return false;'''
new = '''function saveBattleState(){\n  if(!battle?.started || battle.ended)return;\n  localStorage.setItem(battleSaveKey(),JSON.stringify({...battle,mapNumber:currentMap,mapSeries:currentSeries,shots:[]}));\n  continueBtn.style.display="inline-block";\n}\nfunction clearBattleState(){localStorage.removeItem(battleSaveKey());continueBtn.style.display="none"}\nfunction loadBattleState(){\n  try{\n    const key=battleSaveKey();\n    let raw=localStorage.getItem(key);\n    if(!raw){\n      const active=localStorage.getItem(ACTIVE_SLOT_KEY);\n      const legacy=localStorage.getItem(BATTLE_SAVE_PREFIX);\n      if(active&&legacy){raw=legacy;localStorage.setItem(key,legacy);localStorage.removeItem(BATTLE_SAVE_PREFIX);}\n    }\n    if(!raw)return false;'''
if old not in s:
    raise SystemExit('battle save block not found')
s = s.replace(old, new, 1)

old2 = 'continueBtn.style.display=localStorage.getItem("wildwatchBattleSave")?"inline-block":"none";'
new2 = 'continueBtn.style.display=localStorage.getItem(battleSaveKey())?"inline-block":"none";'
if old2 not in s:
    raise SystemExit('continue button battle key line not found')
s = s.replace(old2, new2, 1)

old3 = '''  localStorage.setItem("wildwatchSafetyBackup",JSON.stringify({savedAt:new Date().toISOString(),save}));\n  localStorage.setItem(ACTIVE_SLOT_KEY,String(slot));'''
new3 = '''  localStorage.setItem("wildwatchSafetyBackup",JSON.stringify({savedAt:new Date().toISOString(),save}));\n  saveBattleState();\n  localStorage.setItem(ACTIVE_SLOT_KEY,String(slot));'''
if old3 not in s:
    raise SystemExit('slot switch block not found')
s = s.replace(old3, new3, 1)

p.write_text(s, encoding='utf-8')
print('Patched per-slot battle saves')
