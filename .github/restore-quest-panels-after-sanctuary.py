from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='/* Quest panel visibility repair */'
if marker in s:
    raise SystemExit('repair already present')
# The Sanctuary visibility patch may hide descendants globally. Reassert quest panels/tools only while questScreen is active.
css='''\n/* Quest panel visibility repair */\n#questScreen.active .questPanel{visibility:visible!important;opacity:1!important}\n#questScreen.active #dailyQuestList{display:grid}\n#questScreen.active #weeklyQuestList,#questScreen.active #milestoneQuestList,#questScreen.active #challengeQuestList{visibility:visible!important;opacity:1!important}\n'''
if '</style>' not in s: raise SystemExit('style marker missing')
s=s.replace('</style>',css+'\n</style>',1)
# Make opening Quests always select/render a valid tab, so stale inline display state cannot leave every list hidden.
old='if(id==="questScreen")setTimeout(renderDailyQuests,0);'
new='''if(id==="questScreen")setTimeout(()=>{\n    renderDailyQuests();\n    if(typeof renderExtraQuestBoards==="function")renderExtraQuestBoards();\n    if(typeof setQuestTab==="function")setQuestTab("daily");\n  },0);'''
if old not in s: raise SystemExit('showScreen quest hook missing')
s=s.replace(old,new,1)
p.write_text(s)
print('Quest panels repaired')
