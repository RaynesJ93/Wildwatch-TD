/* Region atlas: deterministic, resolution-independent scenery, cached once per map.
   Purely visual: path, placement, saves, combat and progression are never mutated. */
window.CritterAtlas=(()=>{
'use strict';
const themes=[null,
 ['#163e37','#59855a','#96b86e','#294b36','#af956a','#decba0','#63cdb0','Timber lodge'],
 ['#a96838','#edca85','#ffdfa1','#8f613b','#c59d61','#f7dda0','#4bb9a3','Sandstone keep'],
 ['#19172d','#49405e','#716278','#171729','#62586f','#a797ac','#9df3c9','Haunted chapel'],
 ['#588aa2','#d4edf0','#f8ffff','#618ba1','#9ecedc','#e9ffff','#80d7ee','Ice fortress'],
 ['#211f2c','#54403e','#875442','#211d29','#66525b','#ab8d7d','#ff9447','Basalt forge'],
 ['#172b44','#3d5274','#666d96','#1b293f','#627eaa','#b9d4e7','#8beeea','Crystal citadel'],
 ['#126b86','#48b6bd','#a0e2d0','#877555','#dcc591','#fff0c1','#ef9f9d','Coral lighthouse'],
 ['#102f33','#3d7758','#80ad66','#334b34','#8c9c70','#c4c998','#e6bf66','Jungle temple'],
 ['#292647','#65517c','#9981a4','#3d355b','#9a87ac','#e5bddd','#9ff0d6','Mushroom sanctuary'],
 ['#597caa','#bbd9e4','#f3f9ff','#647891','#a6baca','#ebf7ff','#efd799','Sky citadel']];
let cache=null,key='',builds=0;
function rng(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let n=Math.imul(seed^seed>>>15,1|seed);n^=n+Math.imul(n^n>>>7,61|n);return((n^n>>>14)>>>0)/4294967296;};}
function ellipse(c,x,y,rx,ry,color){c.fillStyle=color;c.beginPath();c.ellipse(x,y,rx,ry,0,0,Math.PI*2);c.fill();}
function poly(c,pts,color){c.fillStyle=color;c.beginPath();pts.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.closePath();c.fill();}
function line(c,pts,color,width){c.strokeStyle=color;c.lineWidth=width;c.lineCap='round';c.lineJoin='round';c.beginPath();pts.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.stroke();}
function distance(x,y,path){let best=Infinity;for(let i=1;i<path.length;i++){const a=path[i-1],b=path[i],dx=b[0]-a[0],dy=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy||1)));best=Math.min(best,Math.hypot(x-a[0]-t*dx,y-a[1]-t*dy));}return best;}
function exit(path,w,h){ // Intersect the final route with an inset rectangle, never independently clamp x/y.
 for(let i=path.length-1;i>0;i--){const a=path[i-1],b=path[i],dx=b[0]-a[0],dy=b[1]-a[1],angle=Math.atan2(dy,dx)+Math.PI/2;for(const scale of [1,.8,.6,.4]){const mx=scale*(60*Math.abs(Math.cos(angle))+102*Math.abs(Math.sin(angle))),my=scale*(60*Math.abs(Math.sin(angle))+102*Math.abs(Math.cos(angle)));let lo=0,hi=1;for(const [p,q] of [[-dx,a[0]-mx],[dx,w-mx-a[0]],[-dy,a[1]-my],[dy,h-my-a[1]]]){if(p===0){if(q<0)hi=-1;}else if(p<0)lo=Math.max(lo,q/p);else hi=Math.min(hi,q/p);}if(lo<=hi){return{x:a[0]+hi*dx,y:a[1]+hi*dy,angle,scale};}}}
 return{x:path.at(-1)[0],y:path.at(-1)[1],angle:0};
}
function tree(c,x,y,s,t,kind){c.save();c.translate(x,y);c.scale(s,s);ellipse(c,6,14,23,9,'#10232d45');line(c,[[0,14],[0,-27]],'#665344',8);
 if(kind===3){for(let j=-1;j<=1;j+=2){line(c,[[0,-4],[j*14,-18],[j*22,-39]],t[3],5);line(c,[[j*12,-17],[j*30,-20]],t[3],3);}line(c,[[0,-20],[7,-48]],t[3],5);}
 else if(kind===7||kind===8){for(let j=0;j<5;j++){let a=j*1.25;poly(c,[[0,-25],[Math.cos(a)*38,-25+Math.sin(a)*20],[Math.cos(a+.4)*26,-19+Math.sin(a+.4)*15]],j%2?t[2]:t[1]);}}
 else {for(let j=0;j<3;j++)poly(c,[[0,-56+j*16],[-25-j*3,-13+j*16],[26+j*3,-13+j*16]],j%2?t[1]:t[3]);line(c,[[0,-51],[-17,-18]],t[2],2);if(kind===4)poly(c,[[0,-56],[-14,-31],[0,-37],[12,-31]],'#effbff');}c.restore();}
function prop(c,x,y,s,t,r,k){c.save();c.translate(x,y);c.scale(s,s);ellipse(c,4,8,19,7,'#081b2938');
 if((r===6)||(r===4&&k%3===0)){for(let i=-1;i<=1;i++){poly(c,[[i*13,-9],[i*13+3,-40+(i===0?-15:0)],[i*13+14,-14],[i*13+8,9]],i%2?t[6]:t[2]);line(c,[[i*13+3,-38],[i*13+8,5]],'#ffffff85',2);}}
 else if(r===9||k===3){c.fillStyle=r===9?'#e3d7bd':t[4];c.fillRect(-4,-12,8,22);ellipse(c,0,-14,22,12,r===9?'#c782af':t[6]);ellipse(c,-7,-18,4,2,'#fff4d4');ellipse(c,8,-12,3,2,'#fff4d4');}
 else if(r===2&&k%2===0){line(c,[[0,8],[0,-36]],'#528267',9);line(c,[[0,-10],[-15,-10],[-15,-23]],'#528267',7);line(c,[[0,-20],[14,-20],[14,-31]],'#528267',7);line(c,[[-2,-29],[-2,2]],'#92b084',2);}
 else if(r===7){for(let j=-1;j<=1;j++)line(c,[[0,8],[j*10,-8],[j*17,-24]],k%2?'#eeae9c':'#b5c8e4',5);ellipse(c,0,-15,4,4,'#fff0d1');}
 else if(r===3&&k%2===0){c.fillStyle='#898395';c.beginPath();c.roundRect(-13,-25,26,33,[12,12,2,2]);c.fill();line(c,[[-5,-15],[5,-15]],'#4b465e',2);line(c,[[0,-20],[0,-6]],'#4b465e',2);}
 else if(r===5){poly(c,[[-23,4],[-16,-18],[4,-28],[22,-6],[15,10]],t[3]);line(c,[[-10,-16],[0,-5],[-4,5]],t[6],3);}
 else{poly(c,[[-20,4],[-14,-13],[1,-22],[19,-6],[13,11]],t[3]);poly(c,[[-14,-13],[1,-22],[19,-6],[0,-4]],t[2]);}c.restore();}
function landmark(c,x,y,t,r,variant){c.save();c.translate(x,y);ellipse(c,6,18,62,29,'#071a2835');
 if([1,2,4,6,7,9].includes(r)&&variant%3!==2){ellipse(c,0,0,65,43,t[2]);ellipse(c,0,0,57,35,r===4?'#74b5cc':r===9?'#69bdb4':'#278a9e');ellipse(c,-6,-5,45,24,r===4?'#b2ebf5':'#4fb8bd');line(c,[[-30,-5],[-10,-10],[20,-8]],'#d7fff3a0',3);if(r===2||r===7)tree(c,43,13,.75,t,7);if(r===4){ellipse(c,8,11,14,8,'#1b526c');line(c,[[2,-15],[20,0],[11,10]],'#f3ffff',2);}}
 else if(r===5){ellipse(c,0,0,65,40,'#241c2c');ellipse(c,0,0,48,27,'#e76238');ellipse(c,-6,-3,30,15,'#ffb757');poly(c,[[-30,20],[-12,-9],[7,22]],'#403141');}
 else if(r===10){ellipse(c,0,16,74,29,'#f3fbff');poly(c,[[-51,0],[0,90],[52,0]],'#5c728d');poly(c,[[-55,0],[-28,-23],[38,-20],[56,0],[4,19]],'#a8c0b3');for(let j=-1;j<=1;j++)prop(c,j*24,-9,.7,t,6,j+1);}
 else{for(let j=-1;j<=1;j++){c.fillStyle=t[3];c.fillRect(j*37-11,-35,22,65);c.fillStyle=t[2];c.fillRect(j*37-15,-39,30,10);line(c,[[j*37-4,-24],[j*37-4,20]],t[4],3);}poly(c,[[-59,-42],[0,-77],[59,-42]],t[4]);if(r===8){line(c,[[-35,-35],[-25,-4],[-35,20]],'#89b976',5);}if(r===3)line(c,[[0,-76],[0,-98],[-10,-88],[10,-88]],t[2],5);}
 c.restore();}
function base(c,b,t,r,m){c.save();c.translate(b.x,b.y);c.rotate(b.angle);c.scale(b.scale||1,b.scale||1);ellipse(c,4,7,61,46,'#0b172955');ellipse(c,0,0,57,42,t[3]);
 c.fillStyle=t[4];c.beginPath();c.roundRect(-44,-30,88,63,9);c.fill();c.fillStyle=t[2];c.fillRect(-44,-30,88,7);
 // Region-specific silhouette, built behind the doorway aligned to the final road segment.
 if(r===1){poly(c,[[-56,-23],[0,-64],[56,-23]],'#534233');poly(c,[[-49,-25],[0,-57],[49,-25]],'#7b935b');for(let j=0;j<4;j++)line(c,[[-39,-13+j*11],[39,-13+j*11]],'#685740',2);}
 else if(r===2||r===8){for(let j=0;j<3;j++){c.fillStyle=j%2?t[2]:t[4];c.fillRect(-42+j*10,-34-j*13,84-j*20,14);}if(r===8){line(c,[[-38,-30],[-28,-11],[-35,7]],'#3e7250',6);}}
 else if(r===3){poly(c,[[-54,-24],[0,-80],[54,-24]],'#29253e');line(c,[[0,-77],[0,-98],[-10,-88],[10,-88]],'#bbadc3',4);ellipse(c,0,-42,9,12,t[6]);}
 else if(r===4||r===6){for(let j=-1;j<=1;j++){poly(c,[[j*30-14,-20],[j*30,-64-(j===0?15:0)],[j*30+14,-20]],j===0?t[6]:t[2]);}line(c,[[-38,-24],[38,-24]],'#eeffff',3);}
 else if(r===5){c.fillStyle='#2b2634';c.fillRect(-37,-59,20,38);c.fillRect(18,-52,18,30);poly(c,[[-53,-21],[0,-50],[53,-21]],'#372e3d');line(c,[[-33,-14],[33,-14]],t[6],4);}
 else if(r===7){c.fillStyle='#faf1d4';c.fillRect(-22,-69,44,51);c.fillStyle='#d38470';c.fillRect(-22,-48,44,12);c.fillStyle='#ffe1a0';c.fillRect(-17,-80,34,15);poly(c,[[-28,-80],[0,-96],[28,-80]],'#4c8796');}
 else if(r===9){ellipse(c,0,-32,58,29,'#ad609f');ellipse(c,-9,-42,40,14,'#d994bd');for(const [x,y] of [[-31,-33],[8,-46],[31,-27]])ellipse(c,x,y,6,4,'#ffe4d5');}
 else{for(let j=-1;j<=1;j++){c.fillStyle='#dce8ee';c.fillRect(j*32-10,-47,20,26);poly(c,[[j*32-16,-47],[j*32,-71],[j*32+16,-47]],'#637f9f');}line(c,[[0,-70],[0,-92]],t[6],3);poly(c,[[0,-91],[22,-85],[0,-79]],t[6]);}
 // A dark arch faces incoming enemies; road reaches the threshold without a sideways spur.
 c.fillStyle='#192835';c.beginPath();c.roundRect(-17,-8,34,39,[17,17,0,0]);c.fill();line(c,[[-15,30],[15,30]],t[5],5);for(const x of [-31,31]){ellipse(c,x,7,5,7,t[6]);}
 c.restore();}
function build(w,h,r,m,path){const c=document.createElement('canvas');c.width=w;c.height=h;const g=c.getContext('2d'),t=themes[r]||themes[1],random=rng(r*7919+m*104729),mode=(m-1)%5;
 const ground=g.createLinearGradient(0,0,w,h);ground.addColorStop(0,t[0]);ground.addColorStop(.53,t[1]);ground.addColorStop(1,t[0]);g.fillStyle=ground;g.fillRect(0,0,w,h);
 // Broad contour bands and ground islands give every map its own composition.
 for(let i=0;i<22;i++){const x=random()*w,y=random()*h;g.globalAlpha=.12+random()*.12;ellipse(g,x,y,70+random()*150,30+random()*70,i%2?t[2]:t[0]);}g.globalAlpha=1;
 for(let i=0;i<900;i++){const x=random()*w,y=random()*h;g.globalAlpha=.07+random()*.08;line(g,[[x,y],[x+3+random()*9,y-2]],i%2?t[2]:t[0],1);}g.globalAlpha=1;
 // Choose open clearings, rejecting the entire landmark footprint near roads and the base.
 const b=exit(path,w,h),used=[];for(let i=0;i<180&&used.length<3+(m%3);i++){const x=80+random()*(w-160),y=100+random()*(h-200);if(distance(x,y,path)<135||Math.hypot(x-b.x,y-b.y)<150||used.some(p=>Math.hypot(x-p[0],y-p[1])<155))continue;used.push([x,y]);landmark(g,x,y,t,r,m+used.length);}
 const objects=[];for(let i=0;i<240;i++){const x=20+random()*(w-40),y=40+random()*(h-80),s=.55+random()*.65;if(distance(x,y,path)<70+s*25||Math.hypot(x-b.x,y-b.y)<100)continue;objects.push({x,y,s,k:Math.floor(random()*5)});}objects.sort((a,b)=>a.y-b.y);
 objects.forEach((o,i)=>{const wooded=[1,3,4,8].includes(r);if((wooded&&o.k<2)||(r===7&&o.k===0))tree(g,o.x,o.y,o.s,t,r);else prop(g,o.x,o.y,o.s,t,r,(o.k+mode)%5);});
 // Continuous outlined road uses the actual gameplay polyline, including all bends.
 line(g,path,'#081b294a',98);line(g,path,t[3],90);line(g,path,t[5],77);line(g,path,t[4],67);
 g.save();g.globalAlpha=.35;g.setLineDash([2,18]);line(g,path,t[5],52);g.restore();line(g,path,t[4],43);
 // Inlaid stones, ice seams or wooden sleepers vary with the region and stage.
 for(let i=1;i<path.length;i++){const a=path[i-1],z=path[i],dx=z[0]-a[0],dy=z[1]-a[1],len=Math.hypot(dx,dy);for(let d=22;d<len-16;d+=r===10?25:43+(m%3)*6){const x=a[0]+dx*d/len,y=a[1]+dy*d/len;g.save();g.translate(x,y);g.rotate(Math.atan2(dy,dx));g.globalAlpha=.32;line(g,[[0,-25],[r===4?9:0,25]],t[3],r===10?4:2);g.restore();}}
 base(g,b,t,r,m);
 const a=path[0],z=path[1],len=Math.hypot(z[0]-a[0],z[1]-a[1])||1;g.save();g.translate(a[0]+(z[0]-a[0])*75/len,a[1]+(z[1]-a[1])*75/len);g.rotate(Math.atan2(z[1]-a[1],z[0]-a[0]));poly(g,[[-10,-12],[8,0],[-10,12],[-4,0]],'#f8f0bf');g.restore();
 const shade=g.createRadialGradient(w/2,h/2,w*.3,w/2,h/2,h*.7);shade.addColorStop(0,'#00132200');shade.addColorStop(1,'#07182966');g.fillStyle=shade;g.fillRect(0,0,w,h);builds++;return c;}
return {draw(ctx,w,h,r,m,path){const next=[w,h,r,m,JSON.stringify(path)].join(':');if(next!==key){cache=build(w,h,r,m,path);key=next;}ctx.drawImage(cache,0,0);},exit,stats:()=>({builds,key}),themes};
})();
