from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

marker='// BATTLE_RUNTIME_STATE_FIX'
if marker in s:
    raise SystemExit('battle runtime state fix already present')

# 1) Normalize old/incomplete autosaves when they load so wave updates cannot
# crash on missing runtime arrays added by later tower abilities.
old='''    cancelAnimationFrame(raf);hardMode=!!b.hardMode;save.battleDifficulty=hardMode?"hard":"normal";if(b.mapNumber){currentSeries=b.mapSeries||1;currentMap=b.mapNumber;applyMap(currentSeries,currentMap);}battle=b;battle.shots=[];battle.puddles=battle.puddles||[];selectedCard=null;selectedTower=null;speed=1;'''
new='''    cancelAnimationFrame(raf);hardMode=!!b.hardMode;save.battleDifficulty=hardMode?"hard":"normal";if(b.mapNumber){currentSeries=b.mapSeries||1;currentMap=b.mapNumber;applyMap(currentSeries,currentMap);}battle=b;\n    // BATTLE_RUNTIME_STATE_FIX: normalize every transient battle collection.\n    battle.enemies=Array.isArray(battle.enemies)?battle.enemies:[];\n    battle.towers=Array.isArray(battle.towers)?battle.towers:[];\n    battle.shots=[];\n    battle.puddles=Array.isArray(battle.puddles)?battle.puddles:[];\n    battle.needles=Array.isArray(battle.needles)?battle.needles:[];\n    battle.pendingNeedles=Array.isArray(battle.pendingNeedles)?battle.pendingNeedles:[];\n    battle.pineapples=Array.isArray(battle.pineapples)?battle.pineapples:[];\n    battle.trashZones=Array.isArray(battle.trashZones)?battle.trashZones:[];\n    battle.roars=Array.isArray(battle.roars)?battle.roars:[];\n    battle.pigHamZones=Array.isArray(battle.pigHamZones)?battle.pigHamZones:[];\n    battle.eggSplashes=Array.isArray(battle.eggSplashes)?battle.eggSplashes:[];\n    battle.usedCards=Array.isArray(battle.usedCards)?battle.usedCards:[];\n    battle.spawnLeft=Number.isFinite(battle.spawnLeft)?battle.spawnLeft:0;\n    battle.spawnTimer=Number.isFinite(battle.spawnTimer)?battle.spawnTimer:0;\n    battle.waveActive=!!battle.waveActive;\n    battle.spawning=!!battle.spawning;\n    selectedCard=null;selectedTower=null;speed=1;'''
if old not in s:
    raise SystemExit('loadBattleState marker not found')
s=s.replace(old,new,1)

# 2) Make every fresh battle start with the same complete runtime state.
s=s.replace('''    enemies:[],towers:[],shots:[],puddles:[],needles:[],pineapples:[],\n    trashZones:[],roars:[],pigHamZones:[],eggSplashes:[],usedCards:[],''','''    enemies:[],towers:[],shots:[],puddles:[],needles:[],pendingNeedles:[],pineapples:[],\n    trashZones:[],roars:[],pigHamZones:[],eggSplashes:[],usedCards:[],''',1)

# 3) Before spawning a wave, normalize state again in case an old cached save is
# already in memory. This keeps Start Wave from taking down the animation loop.
wave='''  battle.waveStartLives=battle.lives;\n  battle.waveActive=true;'''
wave_new='''  // Ensure transient collections exist before the first enemy is spawned.\n  battle.enemies=Array.isArray(battle.enemies)?battle.enemies:[];\n  battle.towers=Array.isArray(battle.towers)?battle.towers:[];\n  battle.shots=Array.isArray(battle.shots)?battle.shots:[];\n  battle.puddles=Array.isArray(battle.puddles)?battle.puddles:[];\n  battle.needles=Array.isArray(battle.needles)?battle.needles:[];\n  battle.pendingNeedles=Array.isArray(battle.pendingNeedles)?battle.pendingNeedles:[];\n  battle.pineapples=Array.isArray(battle.pineapples)?battle.pineapples:[];\n  battle.trashZones=Array.isArray(battle.trashZones)?battle.trashZones:[];\n  battle.roars=Array.isArray(battle.roars)?battle.roars:[];\n  battle.pigHamZones=Array.isArray(battle.pigHamZones)?battle.pigHamZones:[];\n  battle.eggSplashes=Array.isArray(battle.eggSplashes)?battle.eggSplashes:[];\n  battle.usedCards=Array.isArray(battle.usedCards)?battle.usedCards:[];\n  battle.waveStartLives=battle.lives;\n  battle.waveActive=true;'''
if wave not in s:
    raise SystemExit('wave start marker not found')
s=s.replace(wave,wave_new,1)

p.write_text(s,encoding='utf-8')
print('Normalized battle runtime state for fresh and loaded battles')
