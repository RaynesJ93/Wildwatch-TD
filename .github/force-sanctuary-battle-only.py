from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add an ultra-specific visibility guard so Sanctuary can only ever render on the active Battle screen.
css='''\n/* Hard guard: Sanctuary must never appear on Home/Cards/Quests/Packs */\n#mapSanctuary{display:none!important}\n#battleScreen.screen.active.map-select-mode #mapSanctuary{display:block!important}\nbody:not(.battle-map-menu) #mapSanctuary{display:none!important}\nbody.battle-map-menu #battleScreen.screen.active.map-select-mode #mapSanctuary{display:block!important}\n'''
if '/* Hard guard: Sanctuary must never appear on Home/Cards/Quests/Packs */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Replace showScreen with a version that explicitly clears Battle/Sanctuary state before activating another screen.
start=s.find('function showScreen(id){')
if start<0: raise SystemExit('showScreen not found')
# find matching function end by brace counting
brace=0; end=None
for i in range(start,s.find('\n}',start)+2 if s.find('\n}',start)>0 else len(s)):
    if s[i]=='{': brace+=1
    elif s[i]=='}':
        brace-=1
        if brace==0:
            end=i+1; break
if end is None: raise SystemExit('showScreen end not found')
old=s[start:end]
new='''function showScreen(id){
  const battleScreen=document.getElementById("battleScreen");
  const choosingMap=id==="battleScreen" && (!battle?.started || battle.ended);

  // Clear Sanctuary/Battle presentation first so it cannot leak into any other screen.
  document.body.classList.remove("battle-mode","battle-map-menu");
  battleScreen?.classList.remove("map-select-mode");
  const sanctuary=document.getElementById("mapSanctuary");
  if(sanctuary)sanctuary.style.display="none";

  if(id==="questScreen")setTimeout(renderDailyQuests,0);
  document.querySelectorAll(".screen").forEach(el=>el.classList.toggle("active",el.id===id));
  document.querySelectorAll(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.screen===id));

  if(id==="battleScreen" && choosingMap){
    document.body.classList.add("battle-map-menu");
    battleScreen?.classList.add("map-select-mode");
    if(sanctuary)sanctuary.style.display="block";
    mapMenuSeries=(currentSeries&&sanctuaryUnlocked(currentSeries))?currentSeries:1;
    mapMenuDifficulty="normal";
    renderMapSanctuary();
  }else if(id==="battleScreen"){
    document.body.classList.add("battle-mode");
  }
}'''
s=s[:start]+new+s[end:]

for marker in ['body:not(.battle-map-menu) #mapSanctuary','document.body.classList.remove("battle-mode","battle-map-menu")','sanctuary.style.display="none"']:
    if marker not in s: raise SystemExit('missing '+marker)

p.write_text(s,encoding='utf-8')
print('Forced Sanctuary to Battle screen only')
