from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

MARK='CHICKEN_EXPLOSIVE_EGG_V2'
if MARK in s:
    print('Chicken Explosive Egg V2 already installed')
    raise SystemExit(0)

# Update the card description without depending on the exact old wording.
pat=r'chicken:\{name:"Chicken",emoji:"🐔",rarity:"Common",cost:55,range:145,rate:1/1\.25,dmg:10,color:"#fff",desc:"[^"]*"\}'
new='chicken:{name:"Chicken",emoji:"🐔",rarity:"Common",cost:55,range:145,rate:1/1.25,dmg:10,color:"#fff",desc:"Launches cracking egg bombs. At Level 10, every 5th attack fires an Explosive Egg: 2x damage to the target, 100% splash damage within 75 range and a 20% slow for 2s."}'
s,n=re.subn(pat,new,s,count=1)
if n!=1:
    raise SystemExit('Chicken card definition not found')

# Add the combat branch if it is not already present.
if 'chickenAttackCount' not in s or 'type:"chickenEgg"' not in s:
    anchors=['  }else if(t.key==="rabbit"):', '  }else if(t.key==="hamster"):', '  }else if(t.key==="zebra"):', '  }else if(t.key==="raccoon"):']
    anchor=next((a for a in anchors if a in s),None)
    if not anchor:
        raise SystemExit('No safe tower branch anchor found')
    branch='''  // CHICKEN_EXPLOSIVE_EGG_V2\n  }else if(t.key==="chicken"){\n    let explosive=false;\n    if(t.level>=10){t.chickenAttackCount=(t.chickenAttackCount||0)+1;explosive=t.chickenAttackCount%5===0;}\n    if(explosive){\n      target.hp-=dmg*2;\n      const splash=battle.enemies.filter(e=>e!==target&&!e.dead&&e.hp>0&&Math.hypot(e.x-target.x,e.y-target.y)<=75);\n      [target,...splash].forEach(e=>{if(e!==target)e.hp-=dmg;e.chickenSlowTimer=Math.max(e.chickenSlowTimer||0,2);if(e.hp<=0)killEnemy(e);});\n      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.34,maxLife:.34,type:"chickenEgg",special:true});\n    }else{\n      target.hp-=dmg;\n      battle.shots.push({x:t.x,y:t.y-5,tx:target.x,ty:target.y,life:.30,maxLife:.30,type:"chickenEgg",special:false});\n      if(target.hp<=0)killEnemy(target);\n    }\n'''
    s=s.replace(anchor,branch+anchor,1)
else:
    # Existing implementation: still add marker so future runs are idempotent.
    s=s.replace(new,new+'/* CHICKEN_EXPLOSIVE_EGG_V2 */',1)

# Hook Chicken's 20% slow into enemy movement if missing.
if 'if(e.chickenSlowTimer>0)e.chickenSlowTimer=Math.max(0,e.chickenSlowTimer-dt);' not in s:
    oldslow='if(e.zebraSlowTimer>0)e.zebraSlowTimer=Math.max(0,e.zebraSlowTimer-dt);'
    if oldslow in s:
        s=s.replace(oldslow,oldslow+'if(e.chickenSlowTimer>0)e.chickenSlowTimer=Math.max(0,e.chickenSlowTimer-dt);',1)
    else:
        raise SystemExit('Enemy slow timer anchor not found')
if '*(e.chickenSlowTimer>0?.80:1)' not in s:
    oldmult='*(e.zebraSlowTimer>0?.75:1)'
    if oldmult in s:
        s=s.replace(oldmult,oldmult+'*(e.chickenSlowTimer>0?.80:1)',1)
    else:
        raise SystemExit('Enemy movement multiplier anchor not found')

# Add projectile visuals if missing.
if 's.type==="chickenEgg"' not in s:
    render_anchors=['    }else if(s.type==="rabbitCarrot"):', '    }else if(s.type==="hamsterSeed"):', '    }else if(s.type==="zebraStripeKick"):', '    }else if(s.type==="raccoonBin"):']
    rmark=next((a for a in render_anchors if a in s),None)
    if not rmark:
        raise SystemExit('No safe projectile renderer anchor found')
    render='''    }else if(s.type==="chickenEgg"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.30),arc=Math.sin(q*Math.PI)*(s.special?28:20),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q-arc;\n      ctx.save();ctx.translate(x,y);ctx.rotate(q*Math.PI*5);ctx.fillStyle=s.special?"#ffd84d":"#fff8df";ctx.strokeStyle=s.special?"#e0a800":"#cfc8b5";ctx.lineWidth=s.special?2:1.2;ctx.beginPath();ctx.ellipse(0,0,s.special?8:6,s.special?10:8,0,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();\n      if(q>.82){const a=(q-.82)/.18;ctx.save();ctx.globalAlpha=Math.max(0,1-a);ctx.translate(s.tx,s.ty);ctx.fillStyle=s.special?"#ffd21f":"#ffd84d";ctx.beginPath();ctx.arc(0,0,s.special?30:13,0,Math.PI*2);ctx.fill();ctx.fillStyle="#fff7dd";for(let i=0;i<(s.special?9:5);i++){const ang=i*Math.PI*2/(s.special?9:5);ctx.save();ctx.rotate(ang);ctx.fillRect(s.special?18:8,-2,s.special?13:7,4);ctx.restore();}ctx.fillStyle="#fff";for(let i=0;i<6;i++){const ang=i*Math.PI/3+.3;ctx.fillRect(Math.cos(ang)*(s.special?24:11)-2,Math.sin(ang)*(s.special?24:11)-2,5,3);}ctx.restore();}\n'''
    s=s.replace(rmark,render+rmark,1)

# Ensure marker exists even if an older partial implementation was detected.
if MARK not in s:
    s=s.replace(new,new+'/* CHICKEN_EXPLOSIVE_EGG_V2 */',1)

p.write_text(s,encoding='utf-8')
print('Chicken Egg Bomb + Level 10 Explosive Egg V2 installed')
