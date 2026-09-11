from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='caterpillar:{name:"Caterpillar",emoji:"🐛",rarity:"Common",cost:40,range:120,rate:1/1.20,dmg:6,color:"#7c5",desc:"Cheap basic attacker."}'
new='caterpillar:{name:"Caterpillar",emoji:"🐛",rarity:"Common",cost:40,range:120,rate:1/1.20,dmg:12,color:"#7c5",desc:"Leaf-firing attacker."}'
if old not in s: raise SystemExit('caterpillar stats marker not found')
s=s.replace(old,new,1)

old='''  if(t.key==="goose"){
    let gooseSpecial=false;'''
new='''  if(t.key==="caterpillar"){
    let caterpillarSpecial=false;
    if(t.level>=10){
      t.caterpillarAttackCount=(t.caterpillarAttackCount||0)+1;
      caterpillarSpecial=t.caterpillarAttackCount%4===0;
    }
    battle.shots.push({x:t.x,y:t.y-7,tx:target.x,ty:target.y,life:.36,maxLife:.36,type:caterpillarSpecial?"bigLeaf":"leaf"});
    const hitDamage=caterpillarSpecial?animals.caterpillar.dmg*5:dmg;
    target.hp-=hitDamage;
    if(target.hp<=0)killEnemy(target);
    t.cd=cardRate(t.key);
    return;
  }

  if(t.key==="goose"){
    let gooseSpecial=false;'''
if old not in s: raise SystemExit('caterpillar attack insertion marker not found')
s=s.replace(old,new,1)

old='''  battle.shots?.forEach(s=>{
    if(s.type==="gooseEgg"){'''
new='''  battle.shots?.forEach(s=>{
    if(s.type==="leaf"||s.type==="bigLeaf"){
      const q=1-Math.max(0,s.life)/(s.maxLife||.36);
      const x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-Math.sin(Math.PI*q)*18;
      const big=s.type==="bigLeaf";
      ctx.save();ctx.translate(x,y);ctx.rotate(-.7+q*3.8);ctx.scale(big?1.9:1,big?1.9:1);
      ctx.fillStyle=big?"#7ed957":"#68b948";ctx.strokeStyle="#2f6b2d";ctx.lineWidth=2;
      ctx.beginPath();ctx.ellipse(0,0,12,7,-.35,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.strokeStyle="#d7ef9b";ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(-9,3);ctx.lineTo(9,-3);ctx.stroke();
      ctx.restore();
    }else if(s.type==="gooseEgg"){'''
if old not in s: raise SystemExit('caterpillar leaf draw marker not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('Caterpillar damage 12 + leaf projectile + level 10 every-fourth 5x special added')
