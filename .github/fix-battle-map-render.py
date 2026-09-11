from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'const spriteArt=new Image();' in s and 'const spriteSrc={' in s:
    raise SystemExit('sprite runtime globals already restored')

marker='const W=canvas.width,H=canvas.height;'
if marker not in s:
    raise SystemExit('canvas size marker not found')

sprite_block=r'''
// ENEMY_SPRITE_RUNTIME_FIX: these globals are required as soon as the first
// woodland enemy is drawn. They were removed during a later map-series patch,
// which left the map visible but crashed the animation loop when a wave spawned.
const spriteArt=new Image();
spriteArt.src="assets/wildwatch-realistic-sprites.jpg";
const spriteSrc={
  monkey:[0,0,128,128], frog:[128,0,128,128], owl:[256,0,128,128], snake:[384,0,128,128],
  rhino:[0,128,128,128], eagle:[128,128,128,128], panda:[256,128,128,128], lion:[384,128,128,128],
  rat:[0,256,128,128], raccoon:[128,256,128,128], boar:[256,256,128,128], boss:[384,256,128,128]
};
'''

s=s.replace(marker,marker+'\n'+sprite_block,1)

for required in ['const spriteArt=new Image();','const spriteSrc={','rat:[0,256,128,128]','raccoon:[128,256,128,128]','boar:[256,256,128,128]']:
    if required not in s:
        raise SystemExit('missing after sprite repair: '+required)

p.write_text(s,encoding='utf-8')
print('Restored enemy sprite globals so waves can render without crashing')
