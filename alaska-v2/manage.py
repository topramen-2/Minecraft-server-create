#!/usr/bin/env python3
"""Create Kingdoms Alaska migration. No third-party Python packages required."""
import argparse, hashlib, http.client, io, json, os, pathlib, re, shutil, socket, subprocess, sys, time, urllib.request, urllib.parse, zipfile, tomllib
from concurrent.futures import ThreadPoolExecutor
ROOT = pathlib.Path(__file__).resolve().parent
STATE = ROOT / 'server-state.json'
OLD = 'create-kingdoms-test'
NEW = 'create-kingdoms-alaska'
DEST = pathlib.Path('/DATA/AppData/create-kingdoms-alaska')
CLIENT = pathlib.Path.home()/'.minecraft-create-kingdoms-alaska'
REPO = 'topramen-2/Minecraft-server-create'
TAG = 'v2.0.0-alaska'

def fail(msg): raise RuntimeError(msg)
def digest(p):
    h=hashlib.sha512()
    with open(p,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def records():return json.loads((ROOT/'mods.lock.json').read_text())
def save(p,obj,private=False):
    p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    if private:
        fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
        with os.fdopen(fd,'w') as f:json.dump(obj,f,indent=2)
        os.chmod(p,0o600)
    else:p.write_text(json.dumps(obj,indent=2)+'\n')
class UnixHTTP(http.client.HTTPConnection):
    def connect(self):
        self.sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);self.sock.settimeout(self.timeout);self.sock.connect('/var/run/docker.sock')
def docker(method,path,body=None):
    c=UnixHTTP('localhost',timeout=180)
    c.request(method,path,body=json.dumps(body) if body is not None else None,headers={'Content-Type':'application/json'})
    r=c.getresponse();b=r.read();c.close()
    if r.status>=300:fail(f'Docker {method} {path}: HTTP {r.status}: {b.decode(errors="replace")[:500]}')
    if not b:return None
    try:return json.loads(b)
    except (json.JSONDecodeError, UnicodeDecodeError):return b

def inspect(name):return docker('GET','/containers/'+name+'/json')
def exists_container(name):
    return any('/'+name in c.get('Names',[]) for c in docker('GET','/containers/json?all=1'))
def download(r):
    p=ROOT/'.cache'/r['sha512']/r['filename'];p.parent.mkdir(parents=True,exist_ok=True)
    if p.is_file() and digest(p)==r['sha512']:return p
    print('Downloading:',r['name'],r['version'],flush=True)
    for attempt in range(3):
        try:
            req=urllib.request.Request(r['url'],headers={'User-Agent':'CreateKingdoms-Alaska/2.0'})
            part=p.with_name(p.name+'.part')
            with urllib.request.urlopen(req,timeout=90) as src,part.open('wb') as dst:shutil.copyfileobj(src,dst)
            if digest(part)!=r['sha512']:fail('Checksum mismatch: '+r['filename'])
            part.replace(p);return p
        except Exception:
            if attempt==2:raise
    fail('Download failed')
def fetch_all():
    with ThreadPoolExecutor(6) as pool:return dict(zip((r['filename'] for r in records()),pool.map(download,records())))

def metadata(blob):
    z=zipfile.ZipFile(io.BytesIO(blob))
    t={}
    for n in ('META-INF/neoforge.mods.toml','META-INF/mods.toml'):
        if n in z.namelist():t=tomllib.loads(z.read(n).decode());break
    return z,t

def topids(p):
    try:return {m['modId'] for m in metadata(p.read_bytes())[1].get('mods',[])}
    except (KeyError,zipfile.BadZipFile,tomllib.TOMLDecodeError):return set()

def allmods(blob,label):
    z,t=metadata(blob);result=[]
    for m in t.get('mods',[]):result.append((m['modId'],m.get('version',''),t.get('dependencies',{}).get(m['modId'],[]),label))
    if 'META-INF/jarjar/metadata.json' in z.namelist():
        for j in json.loads(z.read('META-INF/jarjar/metadata.json')).get('jars',[]):
            result.extend(allmods(z.read(j['path']),label+'!'+j['path']))
    return result

def audit(moddir,side):
    found={}; roots={}; deps=[]
    for p in sorted(moddir.glob('*.jar')):
        for mid in topids(p):
            if mid in roots:fail(f'Duplicate mod {mid}: {roots[mid]} and {p.name}')
            roots[mid]=p.name
        for mid,v,ds,label in allmods(p.read_bytes(),p.name):
            found[mid]=v;deps.extend((mid,d) for d in ds)
    missing=[]
    for mid,d in deps:
        if d.get('side','BOTH') not in ('BOTH',side.upper()):continue
        if d.get('type')=='required' or d.get('mandatory'):
            if d['modId'] not in found and d['modId'] not in ('minecraft','neoforge','forge','java'):missing.append(f"{mid} needs {d['modId']} {d.get('versionRange','')}")
        if d.get('type')=='incompatible' and d['modId'] in found:
            # These renderer conflicts are unconditional in the selected builds.
            if d['modId'] in ('embeddium','oculus','optifine'):missing.append(f"{mid} conflicts with {d['modId']}")
    if missing:fail('Dependency check failed:\n'+'\n'.join(sorted(set(missing))))
    if any('terraforged' in x.lower() for x in found):fail('TerraForged remains in staged pack')
    return {'mods':found,'files':{p.name:digest(p) for p in sorted(moddir.glob('*.jar'))}}

def apply_mods(folder,side,cache):
    folder.mkdir(parents=True,exist_ok=True)
    selected=[r for r in records() if r['type']=='mod' and r['side'] in ('both',side)]
    replacing=set().union(*(topids(cache[r['filename']]) for r in selected))
    client_ids=set().union(*(topids(cache[r['filename']]) for r in records() if r['type']=='mod' and r['side']=='client'))
    for p in folder.glob('*.jar'):
        ids=topids(p)
        if ('terraforged' in p.name.lower() or ids & replacing or ids & {'embeddium','oculus','optifine'} or (side=='server' and (ids & client_ids or 'xaeroworldmap' in p.name.lower()))):p.unlink()
    for r in selected:shutil.copy2(cache[r['filename']],folder/r['filename'])
    return audit(folder,side)

def copy_config(target):
    for p in (ROOT/'overrides').rglob('*'):
        if p.is_file():
            q=target/p.relative_to(ROOT/'overrides');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)

def envdict(cfg):return dict(s.split('=',1) for s in cfg.get('Env',[]) if '=' in s)

def plan():
    c=inspect(OLD); mounts=c['Mounts']; dm=[m for m in mounts if m['Destination']=='/data']
    if len(dm)!=1 or dm[0]['Type']!='bind':fail('Expected exactly one bind mount at /data. No changes made.')
    src=pathlib.Path(dm[0]['Source']).resolve()
    if src==DEST or DEST in src.parents or src in DEST.parents:fail('Source and destination overlap')
    if c['HostConfig'].get('NetworkMode') not in ('default','bridge'):fail('This script expects the current server to use Docker bridge networking. No changes made; share docker inspect network mode for adaptation.')
    if len(mounts)!=1:fail('Extra mounts need review before cloning. No changes made.')
    env=envdict(c['Config'])
    if env.get('TYPE','').upper()!='NEOFORGE' or env.get('VERSION')!='1.21.1':fail('Expected TYPE=NEOFORGE and VERSION=1.21.1')
    # Automatic download sources could restore removed mods or overwrite the staged world.
    auto=[k for k,v in env.items() if v and (k in ('MODS','PLUGINS','WORLD','WORLD_URL','MODPACK','GENERIC_PACK','MODS_FILE','CF_SERVER_MOD','FTB_MODPACK_ID','MODRINTH_MODPACK','PACKWIZ_URL','MODS_FILE','MODS_FROM','COPY_MODS_SRC','COPY_CONFIG_SRC','DATAPACKS','DATAPACKS_FILE','REMOVE_OLD_MODS') or k.startswith(('MODRINTH_PROJECT','CURSEFORGE','AUTO_CURSEFORGE')))]
    if auto:fail('Container has automatic content settings requiring review: '+', '.join(auto))
    nv="21.1.265"
    if not re.fullmatch(r'21\.1\.\d+',nv):
        installed=[p.name for p in (src/'libraries/net/neoforged/neoforge').glob('*') if p.is_dir() and re.fullmatch(r'21\.1\.\d+',p.name)]
        if len(installed)==1:nv=installed[0]
    if not re.fullmatch(r'21\.1\.\d+',nv):fail('NEOFORGE_VERSION must be an explicit 21.1.x version, not latest')
    if int(nv.split('.')[-1])<218:fail('Selected mods require NeoForge 21.1.218 or newer')
    if not (src/'mods').is_dir():fail('No source mods directory')
    if exists_container(NEW):fail(NEW+' already exists. Use status/start/rollback; do not prepare again.')
    print('Source:',src,'\nNew data:',DEST,'\nNew container:',NEW,'\nNeoForge:',nv)
    return c,src,nv

def prepare():
    c,src,nv=plan()
    if STATE.exists() or DEST.exists():fail('Staging already exists; preparation will not overwrite it.')
    cache=fetch_all()  # Download and checksum everything before creating any server files.
    if shutil.disk_usage(src.parent).free < 4*1024**3:fail('Need at least 4 GiB free for staging and initial world generation')
    DEST.mkdir(mode=0o755)
    state={'old':OLD,'new':NEW,'source':str(src),'destination':str(DEST),'neoforge':nv,'old_id':c['Id'],'restart':c['HostConfig']['RestartPolicy'],'prepared':False,'started':False}
    save(STATE,state,True)
    try:
        for name in ('mods','config','defaultconfigs'):
            if (src/name).is_dir():shutil.copytree(src/name,DEST/name,dirs_exist_ok=True)
        # Preserve access controls and server settings, never old world/player/colony data.
        for name in ('server.properties','ops.json','whitelist.json','banned-players.json','banned-ips.json'):
            if (src/name).is_file():shutil.copy2(src/name,DEST/name)
        for p in list((DEST/'config').glob('*terraforged*')) if (DEST/'config').exists() else []:
            if p.is_dir():shutil.rmtree(p)
            else:p.unlink()
        properties=DEST/'server.properties'
        lines=properties.read_text().splitlines() if properties.exists() else []
        values={'level-name':'world-alaska','level-type':'minecraft\\:normal','level-seed':'','generator-settings':'{}','initial-enabled-packs':'vanilla','initial-disabled-packs':'','gamemode':'survival','force-gamemode':'true','view-distance':'12','simulation-distance':'8'}
        lines=[s for s in lines if s.split('=',1)[0] not in values]
        properties.write_text('\n'.join(lines+[k+'='+v for k,v in values.items()])+'\n')
        server_audit=apply_mods(DEST/'mods','server',cache);copy_config(DEST)
        # Empty world folder is created by Minecraft on first startup.
        if (DEST/'world-alaska').exists():fail('Fresh world destination unexpectedly exists')
        clientdir=ROOT/'build'/'client';clientdir.mkdir(parents=True,exist_ok=False)
        shutil.copytree(src/'mods',clientdir/'mods')
        # Server-only additions should not be copied into the exported multiplayer client.
        server_ids=set().union(*(topids(cache[r['filename']]) for r in records() if r['type']=='mod' and r['side']=='server'))
        for p in (clientdir/'mods').glob('*.jar'):
            if topids(p)&server_ids:p.unlink()
        client_audit=apply_mods(clientdir/'mods','client',cache)
        # Biome Replacer / Spawn Point are included client-side too for matching solo worlds.
        for r in records():
            if r['type']=='mod' and r['slug'] in ('biome-replacer','biome-spawn-point','snow-under-trees'):
                shutil.copy2(cache[r['filename']],clientdir/'mods'/r['filename'])
        for r in records():
            if r['type'] in ('resourcepack','shader'):
                folder='shaderpacks' if r['type']=='shader' else 'resourcepacks'
                (clientdir/folder).mkdir(exist_ok=True);shutil.copy2(cache[r['filename']],clientdir/folder/r['filename'])
        copy_config(clientdir)
        # Shaders shipped as choices; first launch uses shaders off to establish a baseline.
        (clientdir/'config'/'iris.properties').write_text('enableShaders=false\n')
        res=[r for r in records() if r['type']=='resourcepack']
        (clientdir/'options.txt').write_text('resourcePacks:'+json.dumps(['vanilla']+['file/'+r['filename'] for r in res],separators=(',',':'))+'\n')
        client_audit=audit(clientdir/'mods','client')
        for r in records():
            if r['type']=='mod' and r['side']=='both':
                if digest(DEST/'mods'/r['filename'])!=digest(clientdir/'mods'/r['filename']):fail('Client/server mismatch')
        save(ROOT/'build'/'server-audit.json',server_audit)
        save(clientdir/'pack-info.json',{'name':'Create Kingdoms Alaska','version':TAG,'minecraft':'1.21.1','neoforge':nv,'audit':client_audit})
        (clientdir/'INSTALL.txt').write_text('Minecraft Java 1.21.1 / NeoForge '+nv+'\nExtract into an EMPTY game directory. Select that directory in the official launcher.\nRun the NeoForge installer for '+nv+' if that version is not already installed.\nShader choices: Options > Video Settings > Shader Packs. Start with shaders off.\n')
        outfile=ROOT/'build'/'Create-Kingdoms-Alaska-client.zip'
        with zipfile.ZipFile(outfile,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
            for p in sorted(clientdir.rglob('*')):
                if p.is_file():z.write(p,p.relative_to(clientdir))
        (ROOT/'build'/'SHA512SUMS').write_text(digest(outfile)+'  '+outfile.name+'\n')
        state['prepared']=True;save(STATE,state,True)
        # Make the downloadable client export readable by the SSH user, without exposing server state.
        os.chmod(ROOT/'build',0o755);os.chmod(outfile,0o644)
        print('READY: staged server and matching client export. Old server is still running.\nClient ZIP:',outfile)
    except Exception:
        print('Preparation failed. Original server was not changed. Staging retained for diagnosis.',file=sys.stderr);raise

def loadstate():
    s=json.loads(STATE.read_text())
    if not s.get('prepared'):fail('Preparation did not finish successfully')
    return s

def create_payload(c,s):
    allowed=('Hostname','Domainname','User','AttachStdin','AttachStdout','AttachStderr','ExposedPorts','Tty','OpenStdin','StdinOnce','Env','Cmd','Healthcheck','ArgsEscaped','Image','Volumes','WorkingDir','Entrypoint','NetworkDisabled','MacAddress','OnBuild','Labels','StopSignal','StopTimeout','Shell')
    payload={k:v for k,v in c['Config'].items() if k in allowed};payload['Image']=c['Image'];payload['Hostname']=NEW
    env=envdict(c['Config'])
    env.update(LEVEL='world-alaska',LEVEL_TYPE='minecraft:normal',SEED='',GENERATOR_SETTINGS='{}',MODE='survival',FORCE_GAMEMODE='true',VIEW_DISTANCE='12',SIMULATION_DISTANCE='8',NEOFORGE_VERSION=s['neoforge'])
    # Explicitly empty initial enable lists: vanilla plus loader-provided mods will be discovered.
    env.pop('INITIAL_ENABLED_PACKS',None);env.pop('INITIAL_DISABLED_PACKS',None)
    payload['Env']=[k+'='+v for k,v in env.items()]
    labels=payload.get('Labels') or {}
    payload['Labels']={k:v for k,v in labels.items() if not k.startswith(('com.docker.compose.','com.docker.swarm.','com.centurylinklabs.watchtower.'))}
    payload['Labels']['com.centurylinklabs.watchtower.enable']='false'
    hc=json.loads(json.dumps(c['HostConfig']))
    hc['RestartPolicy']={'Name':'no','MaximumRetryCount':0}
    # Source was verified as one /data bind. Never point the new container at old files.
    hc['Binds']=[s['destination']+':/data:rw'];hc.pop('Mounts',None)
    hc.pop('ContainerIDFile',None);hc.pop('Links',None);hc.pop('VolumesFrom',None)
    payload['HostConfig']=hc
    return payload

def start():
    s=loadstate();c=inspect(OLD)
    if c['Id']!=s['old_id']:fail('Original container identity changed; review before switching')
    if exists_container(NEW):
        n=inspect(NEW)
        if n['State']['Running']:print('New server already running; use status.');return
        fail('New container already exists but is stopped. Inspect logs; do not recreate blindly.')
    if (DEST/'world-alaska').exists():fail('World already exists; refusing an unintended fresh-world operation')
    # Snapshot access controls/config are done in prepare; old data remains entirely intact.
    payload=create_payload(c,s)
    new_id=docker('POST','/containers/create?name='+NEW,payload)['Id']
    try:
        docker('POST','/containers/'+OLD+'/update',{'RestartPolicy':{'Name':'no','MaximumRetryCount':0}})
        if c['State']['Running']:docker('POST','/containers/'+OLD+'/stop?t=120')
        docker('POST','/containers/'+NEW+'/start')
        s['started']=True;s['new_id']=new_id;save(STATE,s,True)
    except Exception:
        # Safe rollback on a Docker startup error; do not delete the new container or world.
        try:
            if inspect(NEW)['State']['Running']:docker('POST','/containers/'+NEW+'/stop?t=120')
            docker('POST','/containers/'+OLD+'/update',{'RestartPolicy':s['restart']})
            if c['State']['Running']:docker('POST','/containers/'+OLD+'/start')
        finally:raise
    print('New server starting on the original published ports.\nRun: sudo bash run-server.sh status\nIf it fails: sudo bash run-server.sh rollback\nAfter a successful join, run: sudo bash run-server.sh accept')

def status():
    s=loadstate()
    if not exists_container(NEW):print('Prepared, not started.');return
    c=inspect(NEW);print('Container:',NEW,'State:',c['State']['Status'])
    raw=docker('GET','/containers/'+NEW+'/logs?stdout=1&stderr=1&tail=100')
    if isinstance(raw,bytes):
        # Docker multiplexed log frames have an eight-byte header.
        chunks=[];i=0
        while i+8<=len(raw) and raw[i] in (0,1,2) and raw[i+1:i+4]==b'\0\0\0':
            size=int.from_bytes(raw[i+4:i+8],'big');chunks.append(raw[i+8:i+8+size]);i+=8+size
        print((b''.join(chunks) if chunks else raw).decode(errors='replace'))

def accept():
    s=loadstate()
    if not inspect(NEW)['State']['Running']:fail('New server is not running')
    docker('POST','/containers/'+NEW+'/update',{'RestartPolicy':s['restart']})
    s['accepted']=True;save(STATE,s,True);print('New server restart policy restored. Old server stays stopped and preserved.')

def rollback():
    s=loadstate()
    if exists_container(NEW):
        docker('POST','/containers/'+NEW+'/update',{'RestartPolicy':{'Name':'no','MaximumRetryCount':0}})
        if inspect(NEW)['State']['Running']:docker('POST','/containers/'+NEW+'/stop?t=120')
    docker('POST','/containers/'+OLD+'/update',{'RestartPolicy':s['restart']})
    if not inspect(OLD)['State']['Running']:docker('POST','/containers/'+OLD+'/start')
    print('Original server restored. Select your original client installation to join it.')

def client(zip_path):
    if CLIENT.exists():fail('New client directory already exists; refusing to overwrite '+str(CLIENT))
    p=pathlib.Path(zip_path).expanduser().resolve()
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        for n in names:
            rel=pathlib.PurePosixPath(n)
            if rel.is_absolute() or '..' in rel.parts:fail('Unsafe ZIP path')
        if 'pack-info.json' not in names:fail('Not an Alaska client export')
        CLIENT.mkdir();z.extractall(CLIENT)
    info=json.loads((CLIENT/'pack-info.json').read_text())
    for filename,h in info['audit']['files'].items():
        if digest(CLIENT/'mods'/filename)!=h:fail('Client checksum mismatch: '+filename)
    audit(CLIENT/'mods','client')
    old=pathlib.Path.home()/'.minecraft-create-kingdoms'
    if (old/'servers.dat').is_file():shutil.copy2(old/'servers.dat',CLIENT/'servers.dat')
    print('Installed:',CLIENT,'\nOfficial launcher: create a new installation using NeoForge '+info['neoforge']+' and this Game Directory.\nUse Java 21; start with 8 GiB allocated. Your old client remains unchanged.')

def publish(zip_path):
    p=pathlib.Path(zip_path).expanduser().resolve()
    with zipfile.ZipFile(p) as z:info=json.loads(z.read('pack-info.json'))
    if info['version']!=TAG:fail('Wrong client pack version')
    for cmd in ('git','gh'):
        if not shutil.which(cmd):fail('Install git and github-cli first')
    subprocess.run(['gh','auth','status'],check=True)
    dest=pathlib.Path.home()/'Minecraft-server-create-alaska-release'
    if dest.exists():fail('Release checkout already exists; inspect it before retrying')
    subprocess.run(['gh','repo','clone',REPO,str(dest)],check=True)
    # Commit only an explicit allowlist. No private state, passwords, or world files.
    pack=dest/'alaska-v2';pack.mkdir(exist_ok=False)
    for name in ('manage.py','run-server.sh','mods.lock.json','README.md','MOD-DECISIONS.md','RELEASE-NOTES.md'):
        shutil.copy2(ROOT/name,pack/name)
    shutil.copytree(ROOT/'overrides',pack/'overrides')
    save(pack/'pack-info.json',info)
    subprocess.run(['git','add','--','alaska-v2'],cwd=dest,check=True)
    subprocess.run(['git','commit','-m','Add Create Kingdoms Alaska v2 pack and migration tools'],cwd=dest,check=True)
    subprocess.run(['git','push','origin','HEAD'],cwd=dest,check=True)
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=dest,text=True).strip()
    sums=p.with_name('SHA512SUMS');sums.write_text(digest(p)+'  '+p.name+'\n')
    subprocess.run(['gh','release','create',TAG,str(p),str(sums),'--repo',REPO,'--target',sha,'--title','Create Kingdoms Alaska v2.0.0','--notes-file',str(ROOT/'RELEASE-NOTES.md'),'--prerelease'],check=True)
    print('Published prerelease: https://github.com/'+REPO+'/releases/tag/'+TAG+'\nAfter friends validate it, promote with: gh release edit '+TAG+' --repo '+REPO+' --prerelease=false')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['plan','prepare','start','status','accept','rollback','client','publish']);p.add_argument('zip',nargs='?');a=p.parse_args()
    if a.action in ('client','publish'):
        if not a.zip:p.error('client/publish requires a ZIP path')
        globals()[a.action](a.zip)
    else:globals()[a.action]()
if __name__=='__main__':
    try:main()
    except Exception as e:print('STOP:',str(e),file=sys.stderr);sys.exit(1)
