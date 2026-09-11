from pathlib import Path
p=Path('index.html')
s=p.read_text()
needle='function weightedAnimal(pool,weights){'
if 'ENDGAME_MASTERY_V1' in s:
    print('Endgame mastery already installed')
    raise SystemExit(0)
insert=r'''// ENDGAME_MASTERY_V1: post-collection pack progression.
const MASTERY_MAX=10;
function fullCollectionOwned(){return Object.keys(animals).every(k=>save.unlocked.includes(k));}
function ensureMastery(){
  save.masteryShards=save.masteryShards||{};
  save.masteryLevels=save.masteryLevels||{};
  save.mythicShards=Math.max(0,Number(save.mythicShards||0));
  save.mythicAnimals=save.mythicAnimals||{};
}
function masteryLevel(k){ensureMastery();return Math.max(0,Math.min(MASTERY_MAX,Number(save.masteryLevels[k]||0)));}
function masteryNeed(k){return 20+masteryLevel(k)*15;}
function addMasteryShards(k,n){
  ensureMastery();
  save.masteryShards[k]=(save.masteryShards[k]||0)+Math.max(1,Math.floor(n));
  while(masteryLevel(k)<MASTERY_MAX && save.masteryShards[k]>=masteryNeed(k)){
    const need=masteryNeed(k);save.masteryShards[k]-=need;save.masteryLevels[k]=masteryLevel(k)+1;
  }
  if(masteryLevel(k)>=MASTERY_MAX)save.masteryShards[k]=Math.max(0,save.masteryShards[k]||0);
}
function masteryRewardText(k){
  const lv=masteryLevel(k),skin=lv>=10?' • 🥇 Golden skin':lv>=5?' • 🥉 Bronze skin':'';
  return `⭐ Mastery ${lv}/${MASTERY_MAX}${skin}`;
}
function masteryDamageMult(k){const lv=masteryLevel(k);return 1+(lv>=3?.02:0)+(lv>=9?.03:0);}
function masteryRangeMult(k){return masteryLevel(k)>=7?1.02:1;}
function mythicChanceForChest(tier){return tier==='Legendary'?.03:tier==='Rare'?.02:.01;}
function postCollectionPackReward(key,chestTier){
  ensureMastery();
  const shardGain={Common:5,Uncommon:6,Rare:8,Legendary:10}[chestTier]||5;
  addMasteryShards(key,shardGain);
  let mythic=false;
  if(Math.random()<mythicChanceForChest(chestTier)){save.mythicShards++;mythic=true;}
  return {shardGain,mythic};
}
'''
s=s.replace(needle,insert+'\n'+needle,1)
# Apply the small mastery combat bonuses.
s=s.replace('function cardBaseDamage(k){const a=animals[k];return a.dmg*(1+(cardLevel(k)-1)*.06);}', 'function cardBaseDamage(k){const a=animals[k];return a.dmg*(1+(cardLevel(k)-1)*.06)*masteryDamageMult(k);}',1)
s=s.replace('function cardBaseRange(k){const a=animals[k];return a.range*(1+(cardLevel(k)-1)*.035);}', 'function cardBaseRange(k){const a=animals[k];return a.range*(1+(cardLevel(k)-1)*.035)*masteryRangeMult(k);}',1)
# Replace duplicate pack reward with mastery when the entire collection is complete.
old='''  }else{\n    // Once every card in the tier is owned, duplicate pulls still count as a card and add one shard.\n    save.shards[key]=(save.shards[key]||0)+1;\n  }'''
new='''  }else{\n    if(fullCollectionOwned()){\n      const endgame=postCollectionPackReward(key,chestTier);\n      a._lastEndgameReward=endgame;\n    }else{\n      save.shards[key]=(save.shards[key]||0)+1;\n    }\n  }'''
if old not in s: raise SystemExit('duplicate reward block not found')
s=s.replace(old,new,1)
old2='''  packDesc.textContent=fresh?`Guaranteed ${a.rarity} card from your ${cfg.name}!`:`Guaranteed ${a.rarity} card from your ${cfg.name}! Duplicate converted to 1 ${a.name} shard.`;'''
new2='''  if(fresh)packDesc.textContent=`Guaranteed ${a.rarity} card from your ${cfg.name}!`;\n  else if(fullCollectionOwned()){\n    const r=a._lastEndgameReward||{shardGain:0,mythic:false};\n    packTitle.textContent=`⭐ ${a.name} Mastery!`;\n    packDesc.textContent=`+${r.shardGain} ${a.name} Mastery Shards • ${masteryRewardText(key)}${r.mythic?` • ✨ MYTHIC SHARD! (${save.mythicShards}/50)`: ` • ✨ Mythic Shards ${save.mythicShards}/50`}`;\n    delete a._lastEndgameReward;\n  }else packDesc.textContent=`Guaranteed ${a.rarity} card from your ${cfg.name}! Duplicate converted to 1 ${a.name} shard.`;'''
if old2 not in s: raise SystemExit('pack description block not found')
s=s.replace(old2,new2,1)
# Show mastery on owned collection cards.
marker='''<span>✨ XP ${(save.cardXP[k]||0)}/${cardLevel(k)>=MAX_CARD_LEVEL?"MAX":cardXpNeeded(k)}</span>'''
s=s.replace(marker, marker+'''<span>⭐ M ${masteryLevel(k)}/${MASTERY_MAX}</span>''',1)
p.write_text(s)
print('Installed endgame Animal Mastery, Mythic Shards and combat bonuses')
