from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add Pig custom projectile attack before Goose attack logic.
attack_anchor='''  if(t.key==="goose"){'''
if attack_anchor not in s:
    raise SystemExit('goose attack anchor not found')
attack_block='''  if(t.key==="pig"){
    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:.44,maxLife:.44,type:"pigHam"});
    target.hp-=dmg;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }\n\n'''
if 'type:"pigHam"' not in s:
    s=s.replace(attack_anchor,attack_block+attack_anchor,1)

# Draw the Pig projectile as a visible ham/bacon-style meat projectile.
draw_anchor='''    if(s.type==="gooseEgg"){'''
if draw_anchor not in s:
    raise SystemExit('goose projectile draw anchor not found')
draw_block='''    if(s.type==="pigHam"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.44);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*14;
      ctx.save();ctx.translate(x,y);ctx.rotate(q*5.2);
      ctx.font="30px sans-serif";ctx.textAlign="center";ctx.textBaseline="middle";
      ctx.fillText("🥓",0,0);
      ctx.restore();
    }else if(s.type==="gooseEgg"){'''
if 's.type==="pigHam"' not in s:
    s=s.replace(draw_anchor,draw_block,1)

p.write_text(s,encoding='utf-8')
print('Pig now fires a bacon/ham projectile')
