from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='BOSS_WAVE_ESCORTS_V1'
if marker in s:
    print('already installed')
    raise SystemExit(0)
old='''  battle.spawnLeft=isBossWave?1:Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));'''
new='''  // BOSS_WAVE_ESCORTS_V1: Wave 15 spawns the boss plus a reduced escort group.\n  // Escort size is about 55% of Wave 14, so the boss wave stays busy without being as crowded as the previous round.\n  const normalWaveCount=Math.ceil((6+battle.wave*2)*(hardMode?1.25:1));\n  const previousWaveCount=Math.ceil((6+(battle.wave-1)*2)*(hardMode?1.25:1));\n  const bossEscortCount=Math.max(8,Math.ceil(previousWaveCount*.55));\n  battle.spawnLeft=isBossWave?1+bossEscortCount:normalWaveCount;'''
if old not in s:
    raise SystemExit('boss wave spawn anchor missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Wave 15 now spawns the boss plus reduced escort enemies.')
