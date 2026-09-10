from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''    const end=path[path.length-1],prev=path[path.length-2],dx=end[0]-prev[0],dy=end[1]-prev[1],len=Math.hypot(dx,dy)||1;
    const bx=end[0]-dx/len*18,by=end[1]-dy/len*18;
    ctx.save();
    ctx.translate(bx,by);'''
new='''    const end=path[path.length-1],prev=path[path.length-2],dx=end[0]-prev[0],dy=end[1]-prev[1],len=Math.hypot(dx,dy)||1;
    const ux=dx/len,uy=dy/len;
    // Pull the visual base well inside the canvas so the whole building is visible.
    // The road visually finishes at its front door rather than disappearing off-screen.
    const margin=72;
    let bx=end[0]-ux*72,by=end[1]-uy*72;
    bx=Math.max(margin,Math.min(W-margin,bx));
    by=Math.max(margin,Math.min(H-margin,by));
    ctx.save();
    // Finish the road cleanly underneath the base entrance.
    ctx.strokeStyle=currentSeries===1?"#d8b35b":"#f0d18a";
    ctx.lineWidth=72;ctx.lineCap="round";
    ctx.beginPath();ctx.moveTo(prev[0],prev[1]);ctx.lineTo(bx,by);ctx.stroke();
    ctx.translate(bx,by);'''
if old not in s: raise SystemExit('base position marker not found')
s=s.replace(old,new,1)
p.write_text(s)
