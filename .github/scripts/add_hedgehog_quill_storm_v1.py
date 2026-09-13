from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='HEDGEHOG_QUILL_STORM_V1'
if marker in s:
    print('Already applied')
    raise SystemExit(0)
old='hedgehog:{name:"Hedgehog",emoji:"🦔",rarity:"Common",cost:60,range:135,rate:3,dmg:12,color:"#76543b",desc:"Solid basic attacker."},'
new='hedgehog:{name:"Hedgehog",emoji:"🦔",rarity:"Common",cost:60,range:135,rate:3,dmg:12,color:"#76543b",desc:"Fires spinning Quill Shots. At Level 10, every 6th attack triggers Quill Storm: 8 quills burst outward, each dealing 75% current tower damage and retargeting enemies in range."},'
if old not in s:
    raise RuntimeError('Hedgehog card definition anchor not found')
s=s.replace(old,new,1)
attack_anchor='''  // CAT_NINE_LIVES_V2\n  if(t.key===\"cat\"){'''
attack='''  // HEDGEHOG_QUILL_STORM_V1: Quill Shot + Level 10 Quill Storm.\n  if(t.key===\"hedgehog\"){\n    let quillStorm=false;\n    if(t.level>=10){t.hedgehogAttackCount=(t.hedgehogAttackCount||0)+1;quillStorm=t.hedgehogAttackCount%6===0;}\n    if(quillStorm){\n      battle.shots.push({x:t.x,y:t.y-8,tx:t.x,ty:t.y-8,life:.55,maxLife:.55,type:\"hedgehogStormBurst\"});\n      for(let i=0;i<8;i++){\n        const pool=battle.enemies.filter(e=>!e.dead&&e.hp>0&&Math.hypot(e.x-t.x,e.y-t.y)<=range);\n        if(!pool.length)break;\n        const e=pool[i%pool.length];\n        e.hp-=dmg*.75;\n        battle.shots.push({x:t.x,y:t.y,tx:e.x,ty:e.y,life:.28,maxLife:.28,type:\"hedgehogQuill\",special:true,spin:i*.8});\n        if(e.hp<=0)killEnemy(e);\n      }\n    }else{\n      target.hp-=dmg;\n      battle.shots.push({x:t.x,y:t.y,tx:target.x,ty:target.y,life:.24,maxLife:.24,type:\"hedgehogQuill\",special:false,spin:0});\n      if(target.hp<=0)killEnemy(target);\n    }\n    t.cd=cardRate(t.key);\n    return;\n  }\n\n  // CAT_NINE_LIVES_V2\n  if(t.key===\"cat\"){'''
if attack_anchor not in s:
    raise RuntimeError('Cat attack anchor not found')
s=s.replace(attack_anchor,attack,1)
draw_anchor='''    }else if(s.type===\"catClaw\"){'''
draw='''    }else if(s.type===\"hedgehogQuill\"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.24),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q,ang=Math.atan2(s.ty-s.y,s.tx-s.x)+q*10+(s.spin||0);\n      ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.strokeStyle=s.special?\"#ffe08a\":\"#ead6b8\";ctx.shadowColor=s.special?\"#ffca45\":\"#fff0d0\";ctx.shadowBlur=s.special?10:4;ctx.lineWidth=s.special?3:2.2;ctx.lineCap=\"round\";ctx.beginPath();ctx.moveTo(-10,0);ctx.lineTo(10,0);ctx.stroke();ctx.beginPath();ctx.moveTo(5,-3);ctx.lineTo(10,0);ctx.lineTo(5,3);ctx.stroke();ctx.restore();\n    }else if(s.type===\"hedgehogStormBurst\"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.55);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);ctx.strokeStyle=\"#ffe08a\";ctx.shadowColor=\"#ffca45\";ctx.shadowBlur=14;ctx.lineWidth=3;for(let i=0;i<8;i++){const a=i*Math.PI/4+q*.7,r1=12+q*8,r2=28+q*22;ctx.beginPath();ctx.moveTo(Math.cos(a)*r1,Math.sin(a)*r1);ctx.lineTo(Math.cos(a)*r2,Math.sin(a)*r2);ctx.stroke();}ctx.fillStyle=\"#fff1ad\";ctx.font=\"bold 14px system-ui\";ctx.textAlign=\"center\";ctx.fillText(\"QUILL STORM!\",0,-32-q*10);ctx.restore();\n    }else if(s.type===\"catClaw\"){'''
if draw_anchor not in s:
    raise RuntimeError('Cat projectile draw anchor not found')
s=s.replace(draw_anchor,draw,1)
p.write_text(s,encoding='utf-8')
print('Added Hedgehog Quill Shot and Quill Storm')
