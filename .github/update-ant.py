from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Update Ant description to explain its special ability.
old='ant:{name:"Ant",emoji:"🐜",rarity:"Common",cost:38,range:105,rate:1/1.60,dmg:5,color:"#633",desc:"Very fast basic attacker."}'
new='ant:{name:"Ant",emoji:"🐜",rarity:"Common",cost:38,range:105,rate:1/1.60,dmg:5,color:"#633",desc:"Fast pincer attacker. Every 3rd attack has a 25% chance to permanently boost this tower’s damage by 5% for the battle."}'
if old in s:
    s=s.replace(old,new,1)

# Add Ant self-buff logic before damage is calculated.
old='  const nearbyLion=battle.towers.some(o=>o.key==="lion"&&o!==t&&Math.hypot(o.x-t.x,o.y-t.y)<145);\n  const dmg=towerDamage(t)*(nearbyLion?1.15:1);'
new='''  const nearbyLion=battle.towers.some(o=>o.key==="lion"&&o!==t&&Math.hypot(o.x-t.x,o.y-t.y)<145);\n  if(t.key==="ant"){\n    t.antAttackCount=(t.antAttackCount||0)+1;\n    if(t.antAttackCount%3===0 && Math.random()<.25){\n      t.antDamageBoost=(t.antDamageBoost||0)+.05;\n      battle.shots.push({x:t.x,y:t.y,tx:t.x,ty:t.y,life:.45,type:"antbuff"});\n    }\n  }\n  const selfDamageBoost=t.key==="ant"?(1+(t.antDamageBoost||0)):1;\n  const dmg=towerDamage(t)*(nearbyLion?1.15:1)*selfDamageBoost;'''
if old in s:
    s=s.replace(old,new,1)
elif 't.antAttackCount' not in s:
    raise SystemExit('Ant buff insertion marker not found')

# Give Ant a dedicated pincer attack animation.
old='t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="butterfly"?.34:.12'
new='t.key==="fox"?.30:t.key==="eagle"?.28:t.key==="ant"?.24:t.key==="butterfly"?.34:.12'
if old in s:
    s=s.replace(old,new,1)

old='t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="butterfly"?"seedpod":"beam"'
new='t.key==="fox"?"tailswipe":t.key==="eagle"?"feather":t.key==="ant"?"pincers":t.key==="butterfly"?"seedpod":"beam"'
if old in s:
    s=s.replace(old,new,1)

marker='    }else if(s.type==="seedpod"){'
pincer_branch='''    }else if(s.type==="pincers"){\n      const p=1-Math.max(0,s.life)/.24;\n      const snap=Math.sin(Math.min(1,p)*Math.PI);\n      const x=s.tx,y=s.ty;\n      ctx.save();ctx.translate(x,y);\n      ctx.strokeStyle="#6f2f24";ctx.lineWidth=5;ctx.lineCap="round";ctx.shadowColor="#d46f4b";ctx.shadowBlur=6;\n      ctx.beginPath();ctx.arc(-8+5*snap,0,10,-1.15,1.15);ctx.stroke();\n      ctx.beginPath();ctx.arc(8-5*snap,0,10,Math.PI-1.15,Math.PI+1.15);ctx.stroke();\n      ctx.restore();\n    }else if(s.type==="antbuff"){\n      const p=1-Math.max(0,s.life)/.45;\n      ctx.save();ctx.globalAlpha=1-p;ctx.strokeStyle="#7cff8f";ctx.lineWidth=3;ctx.beginPath();ctx.arc(s.x,s.y,10+p*18,0,Math.PI*2);ctx.stroke();ctx.restore();\n'''
if 's.type==="pincers"' not in s:
    if marker not in s:
        raise SystemExit('Projectile renderer marker not found')
    s=s.replace(marker,pincer_branch+marker,1)

p.write_text(s,encoding='utf-8')
print('Ant updated: pincer attack + every-third-attack 25% chance for +5% self damage')
