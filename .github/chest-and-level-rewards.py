from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Level completion rewards: Normal 100, Hard 175.
s,n=re.subn(r'save\.metaCoins\+=hardMode\?300:200;', 'save.metaCoins+=hardMode?175:100;', s)
if n!=1: raise SystemExit(f'level reward replacement count={n}')
# Replace chest opening handler so every chest guarantees a card from its own tier.
start=s.find('document.querySelectorAll(".chestBtn").forEach(btn=>btn.onclick=()=>{')
if start<0: raise SystemExit('chest handler start not found')
end_marker='  packModal.classList.add("show");persist();renderCards();renderHome();\n});'
end=s.find(end_marker,start)
if end<0: raise SystemExit('chest handler end not found')
end+=len(end_marker)
new='''document.querySelectorAll(".chestBtn").forEach(btn=>btn.onclick=()=>{
  const cfg=chestConfig[btn.dataset.chest];
  if(save.metaCoins<cfg.cost){alert(`You need ${cfg.cost} Coins for this chest. Earn more by completing levels.`);return}
  save.metaCoins-=cfg.cost;
  const chestTier={common:"Common",uncommon:"Uncommon",epic:"Rare",legendary:"Legendary"}[btn.dataset.chest];
  const allowedPool=Object.keys(animals).filter(k=>animals[k].rarity===chestTier);
  const locked=allowedPool.filter(k=>!save.unlocked.includes(k));
  if(!allowedPool.length){save.metaCoins+=cfg.cost;alert(`No ${chestTier} cards are available in this chest yet.`);return}
  // Every chest guarantees a complete card. Prefer a card the player has not unlocked yet.
  const pool=locked.length?locked:allowedPool;
  const key=pool[Math.floor(Math.random()*pool.length)];
  const a=animals[key];
  const fresh=!save.unlocked.includes(key);
  if(fresh){
    save.unlocked.push(key);
    save.levels[key]=save.levels[key]||1;
    save.cardXP[key]=save.cardXP[key]||0;
  }else{
    // Once every card in the tier is owned, duplicate pulls still count as a card and add one shard.
    save.shards[key]=(save.shards[key]||0)+1;
  }
  packEmoji.className="reward";
  packEmoji.style.backgroundImage="none";
  packEmoji.style.backgroundPosition="";
  packEmoji.textContent=a.emoji;
  const rarityLabel=a.rarity==="Legendary"?"🌟 LEGENDARY • ":a.rarity==="Rare"?"💎 RARE • ":a.rarity==="Uncommon"?"🟩 UNCOMMON • ":"⚪ COMMON • ";
  packTitle.textContent=`${rarityLabel}${fresh?"New ":""}${a.name}!`;
  packDesc.textContent=fresh?`Guaranteed ${a.rarity} card from your ${cfg.name}!`:`Guaranteed ${a.rarity} card from your ${cfg.name}! Duplicate converted to 1 ${a.name} shard.`;
  packModal.classList.add("show");persist();renderCards();renderHome();
});'''
s=s[:start]+new+s[end:]
p.write_text(s)
