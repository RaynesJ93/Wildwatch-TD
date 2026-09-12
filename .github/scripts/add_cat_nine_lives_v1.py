from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
if 'CAT_NINE_LIVES_V1' in s:
    print('Cat Nine Lives already installed'); raise SystemExit(0)
old='cat:{name:"Cat",emoji:"🐱",rarity:"Uncommon",cost:75,range:170,rate:1/1.30,dmg:17,color:"#d99",desc:"Fast balanced attacker."}'
new='cat:{name:"Cat",emoji:"🐱",rarity:"Uncommon",cost:75,range:170,rate:1/1.30,dmg:17,color:"#d99",desc:"Fast Paw Slash attacker. At tower level 10, every 9th attack triggers Nine Lives: 9 rapid claw strikes dealing 50% current tower damage each across enemies in range."}'
if old not in s: raise SystemExit('Cat definition anchor not found')
s=s.replace(old,new,1)
anchor='  if(t.key==="raccoon"){'
block='''  // CAT_NINE_LIVES_V1\n  if(t.key==="cat"){\n    t.catAttackCount=(t.catAttackCount||0)+1;\n    const nineLives=t.level>=10 && t.catAttackCount%9===0;\n    if(nineLives){\n      const targets=battle.enemies.filter(e=>!e.dead&&Math.hypot(e.x-t.x,e.y-t.y)<=range).sort((a,b)=>(b.seg||0)-(a.seg||0));\n      for(let i=0;i<9;i++){\n        const e=targets[i%Math.max(1,targets.length)]||target;\n        battle.shots.push({x:t.x,y:t.y-6,tx:e.x,ty:e.y,life:.18+i*.025,maxLife:.18+i*.025,type:"catClaw",special:true,clawIndex:i});\n        e.hp-=dmg*.5;if(e.hp<=0)killEnemy(e);\n      }\n      battle.shots.push({x:t.x,y:t.y-16,tx:t.x,ty:t.y-16,life:.55,maxLife:.55,type:"catNineLives"});\n    }else{\n      battle.shots.push({x:t.x,y:t.y-6,tx:target.x,ty:target.y,life:.22,maxLife:.22,type:"catClaw",special:false});\n      target.hp-=dmg;if(target.hp<=0)killEnemy(target);\n    }\n    t.cd=cardRate(t.key);return;\n  }\n\n'''
if anchor not in s: raise SystemExit('towerTick anchor not found')
s=s.replace(anchor,block+anchor,1)
# Add renderer before existing raccoonBin renderer.
render_anchor='    }else if(s.type==="raccoonBin"){' 
render='''    }else if(s.type==="catClaw"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.22),x=s.x+(s.tx-s.x)*q,y=s.y+(s.ty-s.y)*q;\n      const ang=Math.atan2(s.ty-s.y,s.tx-s.x);ctx.save();ctx.translate(x,y);ctx.rotate(ang);ctx.globalAlpha=.95;\n      ctx.strokeStyle=s.special?"#fff4a8":"#fff";ctx.shadowColor=s.special?"#ffd95c":"#ffffff";ctx.shadowBlur=s.special?10:5;ctx.lineWidth=s.special?3.2:2.4;ctx.lineCap="round";\n      for(let i=-1;i<=1;i++){ctx.beginPath();ctx.moveTo(-13,i*5-4);ctx.quadraticCurveTo(0,i*5+5,13,i*5-2);ctx.stroke();}\n      ctx.restore();\n    }else if(s.type==="catNineLives"){\n      const q=1-Math.max(0,s.life)/(s.maxLife||.55);ctx.save();ctx.translate(s.x,s.y);ctx.globalAlpha=Math.max(0,1-q);\n      ctx.shadowColor="#ffd95c";ctx.shadowBlur=14;ctx.fillStyle="#ffe98a";ctx.font="bold 16px system-ui";ctx.textAlign="center";ctx.fillText("9 LIVES!",0,-25-q*14);\n      ctx.font="18px 'Apple Color Emoji','Segoe UI Emoji'";for(let i=0;i<5;i++){const a=i*Math.PI*2/5+q;ctx.fillText("🐾",Math.cos(a)*(22+q*12),Math.sin(a)*(15+q*8));}ctx.restore();\n'''
if render_anchor not in s: raise SystemExit('shot renderer anchor not found')
s=s.replace(render_anchor,render+render_anchor,1)
p.write_text(s,encoding='utf-8')
print('Installed Cat Paw Slash + Level 10 Nine Lives')
