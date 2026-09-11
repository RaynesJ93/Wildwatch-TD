from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''    const es=currentSeries===2?null:(enemyType&&spriteSrc[enemyType]);'''
new='''    // IOS_WAVE_STABILITY_FIX: avoid clipped sprite-sheet rendering for moving enemies.
    // Safari/iOS can terminate the renderer without throwing a JavaScript error, so
    // enemies use the lightweight emoji path while towers/cards keep their artwork.
    const es=null;'''

if old not in s:
    if 'IOS_WAVE_STABILITY_FIX' in s:
        print('iPhone enemy-render stability fix already installed')
    else:
        raise SystemExit('enemy sprite render marker not found')
else:
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Switched moving enemies to lightweight rendering for iPhone stability')
