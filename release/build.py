"""Build the complete, pinned client release. No server access or credentials needed."""
import hashlib,json,os,pathlib,shutil,urllib.request,zipfile
ROOT=pathlib.Path(__file__).resolve().parent.parent
WORK=pathlib.Path(os.environ.get('RELEASE_WORK',str(ROOT/'.release-work')))
OUT=ROOT/'release-assets'; PACK=WORK/'pack'; CACHE=WORK/'cache'
VERSION='v2.1.0'; TAG='v2.1.0-alaska'
BASE_URL='https://github.com/topramen-2/Minecraft-server-create/releases/download/v2.0.2-alaska/Create-Kingdoms-Alaska-v2.0.2-client.zip'
BASE_SHA='ab6c24819dc37d17bcf6a6319bc74ab346f845a050f66f6578c3467d50fd079d'
def sha(p): return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
def get(url,dest,expected):
 dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists() or sha(dest)!=expected:
  print('Downloading',dest.name,flush=True)
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Create-Kingdoms-Alaska-release/2.1.0'}),timeout=120) as r,open(dest,'wb') as f: shutil.copyfileobj(r,f)
 if sha(dest)!=expected: raise ValueError('Checksum mismatch: '+str(dest))
 return dest
CACHE.mkdir(parents=True,exist_ok=True)
base=get(BASE_URL,CACHE/'base.zip',BASE_SHA)
if PACK.exists(): shutil.rmtree(PACK)
PACK.mkdir(parents=True)
with zipfile.ZipFile(base) as z:
 for n in z.namelist():
  p=pathlib.PurePosixPath(n)
  if p.is_absolute() or '..' in p.parts: raise ValueError('Unsafe ZIP path')
  if p.parts[0] in {'mods','config','shaderpacks','resourcepacks'}: z.extract(n,PACK)
# The three additions already published in the November 2 patch.
extras=json.loads((ROOT/'release/existing-extras.json').read_text())
for e in extras:
 p=ROOT/'alaska-v2/individual-mods'/e['filename']
 if sha(p)!=e['sha256']: raise ValueError('Changed existing extra: '+p.name)
 shutil.copy2(p,PACK/'mods'/p.name)
(PACK/'mods/moonlight-1.21-2.29.33-neoforge.jar').unlink()
for e in json.loads((ROOT/'release/additions.json').read_text()):
 p=get(e['url'],CACHE/e['filename'],e['sha256']);shutil.copy2(p,PACK/'mods'/p.name)
installer=json.loads((ROOT/'release/installer.json').read_text())
p=get(installer['url'],CACHE/installer['filename'],installer['sha256'])
(PACK/'installer').mkdir();shutil.copy2(p,PACK/'installer'/p.name)
for name in ['INSTALL-WINDOWS.md','INSTALL-LINUX.md','START-HERE.txt','KNOWN-ISSUES.md']:
 shutil.copy2(ROOT/'release'/name,PACK/name)
mods=sorted((PACK/'mods').glob('*.jar'))
assert len(mods)==120, f'Expected 120 mods, got {len(mods)}'
assert not (PACK/'mods/linearbearingsfix-1.0.1.jar').exists()
for p in mods:
 with zipfile.ZipFile(p) as z:
  if z.testzip(): raise ValueError('Corrupt JAR: '+p.name)
manifest={'pack':'Create Kingdoms Alaska','version':VERSION,'minecraft':'1.21.1','neoforge':'21.1.265','java':21,'memory':'8G','mod_count':len(mods),'validation':'Archive and JAR integrity checked; server startup and RCON confirmed by operator. Updated client launch and join not yet tested.','mods':[{'filename':p.name,'sha256':sha(p),'size':p.stat().st_size} for p in mods]}
(PACK/'pack-info.json').write_text(json.dumps(manifest,indent=2)+'\n')
(PACK/'MOD-LIST.txt').write_text('\n'.join(p.name for p in mods)+'\n')
# Keep the browsable folder exactly synchronized with the pack.
individual=ROOT/'alaska-v2/individual-mods'
for old in individual.glob('*.jar'): old.unlink()
for p in mods: shutil.copy2(p,individual/p.name)
(individual/'README.md').write_text('# Individual client mods — v2.1.0\n\nThese 120 JARs exactly match the full v2.1.0 client ZIP. For a fresh install, use the [complete release](https://github.com/topramen-2/Minecraft-server-create/releases/latest), which also supplies configs, the NeoForge installer, and instructions.\n\nTo download one JAR, open it and click **Download raw file**. Do not extract the JAR or add a second version of the same mod.\n')
(ROOT/'release/client-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
zip_path=OUT/f'01-Create-Kingdoms-Alaska-{VERSION}-CLIENT.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(PACK.rglob('*')):
  if p.is_file():
   info=zipfile.ZipInfo(p.relative_to(PACK).as_posix(),(2026,11,7,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   z.writestr(info,p.read_bytes())
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.startswith('mods/')])==120
shutil.copy2(PACK/'installer'/installer['filename'],OUT/('02-'+installer['filename']))
for name,target in [('INSTALL-WINDOWS.md','03-INSTALL-WINDOWS.txt'),('INSTALL-LINUX.md','04-INSTALL-LINUX.txt'),('MOD-LIST.txt','05-MOD-LIST.txt'),('pack-info.json','client-manifest.json')]:
 shutil.copy2(PACK/name,OUT/target)
(OUT/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(OUT.iterdir()) if p.is_file()))
print(f'Validated {len(mods)} mod JARs; full pack {zip_path.stat().st_size/1024**2:.1f} MiB',flush=True)
