from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = """function battleCoinReward(kind){
  const base=kind==='wave'?12:kind==='elite'?20:kind==='boss'?45:0;
  return Math.round(base*regionCoinMultiplier());
}"""
new = """function battleCoinReward(kind){
  const base=kind==='wave'?12:kind==='elite'?20:kind==='boss'?45:0;
  const hardModeMultiplier=hardMode?1.30:1;
  return Math.round(base*regionCoinMultiplier()*hardModeMultiplier);
}"""

if old not in s:
    raise SystemExit('battleCoinReward anchor not found')

s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Added 30% Hard Mode battle coin bonus')
