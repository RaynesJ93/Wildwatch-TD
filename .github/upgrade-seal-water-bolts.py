from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Update Seal description to reflect its custom attack.
old_desc='seal:{name:"Seal",emoji:"🦭",rarity:"Rare",cost:120,range:205,rate:1,dmg:35,color:"#999",desc:"Strong ranged attacker."}'
new_desc='seal:{name:"Seal",emoji:"🦭",rarity:"Rare",cost:120,range:205,rate:1,dmg:35,color:"#999",desc:"Fires water bolts; at tower level 10 fires 3 bolts, with bolts 2 and 3 dealing half damage."}'
if old_desc in s:
    s=s.replace(old_desc,new_desc,1)
elif 'seal:{name:"Seal"' not in s:
    raise SystemExit('Seal card data not found')

# Add custom Seal attack before Goose attack logic.
anchor='''  if(t.key==="goose"){'''
if anchor not in s:
    raise SystemExit('Goose attack anchor not found')
if 'if(t.key==="seal")' not in s:
    block='''  if(t.key==="seal"){
    const boltCount=t.level>=10?3:1;
    for(let i=0;i<boltCount;i++){
      battle.shots.push({
        x:t.x+(i-1)*4,
        y:t.y-8-(i%2)*3,
        tx:target.x+(i-1)*5,
        ty:target.y+(i%2?3:-2),
        life:.40+i*.06,
        maxLife:.40+i*.06,
        type:"sealWaterBolt",
        boltIndex:i
      });
    }
    const sealDamage=t.level>=10?dmg*2:dmg;
    target.hp-=sealDamage;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }

'''
    s=s.replace(anchor,block+anchor,1)

# Draw Seal projectiles as bright blue water bolts.
draw_anchor='''    if(s.type==="gooseEgg"){'''
if draw_anchor not in s:
    raise SystemExit('Projectile draw anchor not found')
if 's.type==="sealWaterBolt"' not in s:
    draw='''    if(s.type==="sealWaterBolt"){
      const q=1-Math.max(0,s.life)/Math.max(.001,s.maxLife||.4);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;
      const ang=Math.atan2(s.ty-s.y,s.tx-s.x);
      ctx.save();ctx.translate(x,y);ctx.rotate(ang);
      const grad=ctx.createLinearGradient(-15,0,15,0);
      grad.addColorStop(0,"rgba(84,190,255,.20)");
      grad.addColorStop(.45,"#72d8ff");
      grad.addColorStop(1,"#d9f7ff");
      ctx.fillStyle=grad;ctx.strokeStyle="#2f9fe8";ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(-16,0);ctx.quadraticCurveTo(-4,-8,13,0);ctx.quadraticCurveTo(-4,8,-16,0);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.fillStyle="rgba(255,255,255,.85)";ctx.beginPath();ctx.ellipse(4,-2,5,2.5,0,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }else if(s.type==="gooseEgg"){'''
    s=s.replace(draw_anchor,draw,1)

# Safety checks.
for marker in ['if(t.key==="seal")','type:"sealWaterBolt"','s.type==="sealWaterBolt"','const boltCount=t.level>=10?3:1','const sealDamage=t.level>=10?dmg*2:dmg']:
    if marker not in s:
        raise SystemExit(f'Missing expected Seal marker: {marker}')

p.write_text(s,encoding='utf-8')
print('Seal now fires water bolts; tower level 10 fires 3 bolts with 50% damage on bolts 2 and 3')
