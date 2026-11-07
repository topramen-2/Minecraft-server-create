"""Verify required client dependency IDs, following NeoForge's jar-in-jar metadata."""
import io,json,pathlib,tomllib,zipfile
ROOT=pathlib.Path(__file__).resolve().parent.parent
found={};required=[];top={}
def scan(data,label,nested=False):
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  for n in ('META-INF/neoforge.mods.toml','META-INF/mods.toml'):
   if n in z.namelist():
    t=tomllib.loads(z.read(n).decode())
    for m in t.get('mods',[]):
     found.setdefault(m['modId'],[]).append(label)
     if not nested:top.setdefault(m['modId'],[]).append(label)
    for owner,ds in t.get('dependencies',{}).items():
     for d in ds:
      if (d.get('type')=='required' or d.get('mandatory') is True) and d.get('side','BOTH')!='SERVER':required.append((owner,d['modId']))
    break
  metadata='META-INF/jarjar/metadata.json'
  if metadata in z.namelist():
   for j in json.loads(z.read(metadata)).get('jars',[]):scan(z.read(j['path']),label+'!'+j['path'],True)
for p in sorted((ROOT/'alaska-v2/individual-mods').glob('*.jar')):scan(p.read_bytes(),p.name)
missing=sorted(set((a,b) for a,b in required if b not in found and b not in ('minecraft','neoforge')))
duplicates={k:v for k,v in top.items() if len(v)>1}
assert not missing,missing
assert not duplicates,duplicates
print('Required client dependency IDs present; no duplicate top-level mod IDs.')
print('Nested libraries are resolved by NeoForge; this check does not replace a game-launch test.')
