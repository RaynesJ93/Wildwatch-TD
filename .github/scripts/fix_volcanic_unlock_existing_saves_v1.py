from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='VOLCANIC_EXISTING_SAVE_UNLOCK_V1'
if marker in s:
    print('already installed')
    raise SystemExit(0)
anchor='''save.normalCompleted={...defaults.normalCompleted,...(save.normalCompleted||{})};\nsave.hardCompleted={...defaults.hardCompleted,...(save.hardCompleted||{})};'''
replacement='''save.normalCompleted={...defaults.normalCompleted,...(save.normalCompleted||{})};\nsave.hardCompleted={...defaults.hardCompleted,...(save.hardCompleted||{})};\n// VOLCANIC_EXISTING_SAVE_UNLOCK_V1: players who cleared Tundra 4-10 before Region 5 existed should unlock it automatically.\nif(save.normalCompleted["4-10"]||save.hardCompleted["4-10"])save.volcanicWastelandUnlocked=Math.max(save.volcanicWastelandUnlocked||0,1);'''
if anchor not in s:
    raise SystemExit('save completion anchor missing')
s=s.replace(anchor,replacement,1)
p.write_text(s,encoding='utf-8')
print('Volcanic Wasteland now auto-unlocks for existing saves with Tundra 4-10 completed.')
