from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="""document.querySelectorAll('.questTab').forEach(b=>b.onclick=()=>setQuestTab(b.dataset.qtab));
renderExtraQuestBoards();
setQuestTab('daily');"""
new="""document.querySelectorAll('.questTab').forEach(b=>b.onclick=()=>{renderExtraQuestBoards();setQuestTab(b.dataset.qtab)});
renderExtraQuestBoards();
setQuestTab('daily');
// Refresh quest contents every time the Quests screen becomes active, so Weekly/Milestones/Challenges never open blank.
const _questObserver=new MutationObserver(()=>{const qs=document.getElementById('questScreen');if(qs?.classList.contains('active'))renderExtraQuestBoards();});
const _questScreen=document.getElementById('questScreen');if(_questScreen)_questObserver.observe(_questScreen,{attributes:true,attributeFilter:['class']});"""
if old not in s:
    raise SystemExit('quest tab block not found')
s=s.replace(old,new)
css_old="#questScreen.active #weeklyQuestList,#questScreen.active #milestoneQuestList,#questScreen.active #challengeQuestList{visibility:visible!important;opacity:1!important}"
css_new="#questScreen.active #weeklyQuestList,#questScreen.active #milestoneQuestList,#questScreen.active #challengeQuestList{visibility:visible!important;opacity:1!important}\n#questScreen.active .questPanel[style*='display: grid']{display:grid!important}"
s=s.replace(css_old,css_new)
p.write_text(s)
print('patched quest visibility refresh')
