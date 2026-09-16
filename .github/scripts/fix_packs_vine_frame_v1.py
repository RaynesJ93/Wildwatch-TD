from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '/* PACKS_VINE_FRAME_FIT_V1 */'
if marker in s:
    raise SystemExit('PACKS_VINE_FRAME_FIT_V1 already applied')

css = r'''

/* PACKS_VINE_FRAME_FIT_V1
   Packs screen: let the vine artwork be the frame, remove the extra gold/olive outline,
   and fit the vine border more naturally around the panel on phones. */
#packsScreen .hero{
  border:0!important;
  box-shadow:0 3px 8px #0004!important;
  background-size:112% 104%!important;
  background-position:center top!important;
  background-repeat:no-repeat!important;
  border-radius:20px!important;
  overflow:hidden;
}
@media(max-width:520px){
  #packsScreen .hero{
    background-size:118% 103%!important;
    padding:24px 20px!important;
  }
}
'''

needle = '</style>\n<style id="coral-coast-v2-style">'
if needle not in s:
    raise SystemExit('Could not find jungle menu style insertion point')
s = s.replace(needle, css + '\n</style>\n<style id="coral-coast-v2-style">', 1)
p.write_text(s, encoding='utf-8')
print('Applied Packs vine-frame fit update')
