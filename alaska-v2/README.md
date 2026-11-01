# Create Kingdoms Alaska — fresh-world migration

Minecraft Java 1.21.1 / NeoForge. Prepared November 1, 2026.

This builds an Alaska-inspired successor to Create Kingdoms using the existing server's mods as the baseline. Tectonic shapes the terrain; Regions Unexplored supplies northern forests; Project: Vibrant Journeys adds forest detail; Snow Under Trees adds canopy snow. Custom Regions Unexplored tables and Biome Replacer favor taiga, tundra, mountains and wetlands. Biome Spawn Point favors northern forests. This is not an exact reproduction of the 1.20.1 Alaskan Wilderness pack.

## What changes

- Original container: `create-kingdoms-test`, preserved and stopped only at cutover.
- New container: `create-kingdoms-alaska`, using the original image ID, NeoForge version and published ports.
- New server data: `/DATA/AppData/create-kingdoms-alaska`.
- New world: `world-alaska`, random seed, Survival, no old inventories, advancements, stats, colonies, map or dimension saves.
- New Arch game directory: `~/.minecraft-create-kingdoms-alaska`.
- Existing operator, whitelist and ban settings are retained. Operator permissions are not game progression.
- TerraForged is absent from both new installations. The original installations retain it so the old world can still be used.
- Server view/simulation distances start at 12/8 to limit generation load while testing. Original memory settings are retained.
- Visual mods, resource packs and shaders go to the client. Distant Horizons is client-only here; distant terrain on multiplayer fills as you explore.
- All shader choices are installed, with shaders disabled initially. Select one after the initial join succeeds.
- Four requested mods are omitted; substitutions and exact versions are in `MOD-DECISIONS.md` and `mods.lock.json`.

## Requirements

Run the Arch commands with Minecraft and the launcher closed. The Arch-to-Zima commands assume your existing SSH account `topramen@192.168.0.5`; connect to your home network/VPN first.

On Arch, install missing command tools:

```bash
sudo pacman -S --needed python unzip openssh git github-cli
```

ZimaOS uses its installed Python if it supports `tomllib` (Python 3.11+). Otherwise the wrapper runs a disposable `python:3.12-slim` helper with the required `/DATA` and Docker socket access. It does not install Python into ZimaOS.

Preflight expects the server to have one bind mount at `/data` and standard Docker bridge networking. It refuses unfamiliar automatic mod/world-download settings rather than guessing. If preflight stops, share the error before changing Docker settings.

## 1. Download and copy the setup kit — Arch

Save `Create-Kingdoms-Alaska-Setup.zip` from the chat into `~/Downloads`. The ZIP contains the `alaska-kit` folder.

```bash
unzip -n "$HOME/Downloads/Create-Kingdoms-Alaska-Setup.zip" -d "$HOME"
scp -r "$HOME/alaska-kit" topramen@192.168.0.5:~/
```

## 2. Prepare the Zima server and matching client export — Arch terminal

This downloads checksum-pinned additions and dependencies, clones the current server's mods/configuration into the new folder, removes TerraForged there, writes the Alaska configuration, audits dependencies and builds the client ZIP. It does not stop the original server.

```bash
ssh -t topramen@192.168.0.5 'cd ~/alaska-kit && sudo bash run-server.sh prepare'
```

The existing server may remain running while preparation downloads files. Do not change its mods/configuration concurrently. Preparation takes time and uses several GiB of free disk for downloaded files, staging, client packaging and eventual world growth.

If you are already in ZimaOS's terminal, the equivalent command is:

```bash
cd ~/alaska-kit
sudo bash run-server.sh prepare
```

A failed preparation never modifies the original server. It may leave a partial staging folder for diagnosis; it intentionally refuses to overwrite that folder on a second run. Do not remove the old server folder to resolve a staging error.

## 3. Install the new Arch client — Arch

```bash
scp topramen@192.168.0.5:~/alaska-kit/build/Create-Kingdoms-Alaska-client.zip "$HOME/Downloads/"
python3 "$HOME/alaska-kit/manage.py" client "$HOME/Downloads/Create-Kingdoms-Alaska-client.zip"
```

The installer prints the server's exact NeoForge version and new game directory. In the official launcher, create a separate installation named **Create Kingdoms Alaska**, select **Minecraft 1.21.1 with that NeoForge version**, and set **Game Directory** to:

```text
/home/jackson/.minecraft-create-kingdoms-alaska
```

Use the version printed by the script, not a guessed newer release. If it is not installed, use the matching installer from https://neoforged.net/ and install its client profile. Minecraft 1.21.1 requires Java 21. Start with 8 GiB of client RAM. Keep your old launcher installation for rollback.

The new directory intentionally starts with fresh options except the resource-pack selection and, if available, your old `servers.dat`. Your old worlds, options and mods remain in the old game directory. Before the server cutover, you may launch the new profile to the main menu to catch client loader/rendering errors. Do not try joining the old server with the new pack.

## 4. Start the new world — Arch terminal

Tell your friends the server will briefly be unavailable. Then run:

```bash
ssh -t topramen@192.168.0.5 'cd ~/alaska-kit && sudo bash run-server.sh start'
```

This creates the new container, disables automatic restart of the old container, stops the old server cleanly, and starts the new server on the original ports. A Docker-level start failure restores the old server. A Minecraft/mod crash after the container starts requires the rollback command below.

Check progress:

```bash
ssh -t topramen@192.168.0.5 'cd ~/alaska-kit && sudo bash run-server.sh status'
```

Repeat the status command until the log shows the server's `Done (...)!` message. First generation may take several minutes. The new server initially has restart disabled so a crash does not become a restart loop.

Equivalent direct Zima commands:

```bash
cd ~/alaska-kit
sudo bash run-server.sh start
sudo bash run-server.sh status
```

Join with the new launcher installation at your existing server address/port. Confirm:

- You spawn in Survival with no old inventory or experience.
- The spawn biome is a northern forest; explore nearby terrain and check for a cold-biome mix.
- JEI loads, a basic Create contraption renders, and a held torch lights your surroundings.
- Trees, snow, food crafting and a basic MineColonies setup behave normally.
- New chunks generate without repeated errors; verify Create/AE2/TFMG resources in the new world.
- Try shaders one at a time after the shader-free client works. Large Distant Horizons settings, dense foliage and shaders can be expensive.

Serene Seasons can change farm growth. Immersive Weathering can change blocks over time and its port does not reproduce every upstream feature. Panda's Falling Trees needs gameplay testing with Create saw farms and MineColonies foresters. Required-dependency checks do not prove these gameplay integrations.

After a successful join, enable the new container's normal restart policy:

```bash
ssh -t topramen@192.168.0.5 'cd ~/alaska-kit && sudo bash run-server.sh accept'
```

The ZimaOS application tile for the original server may still point at the old container. Use the new container name for logs/start/stop and do not manually start the old container while the new one uses its ports. This script creates a Docker container; it does not edit CasaOS/ZimaOS application definitions.

## 5. Publish the GitHub update — Arch

After the new server and client work, authenticate GitHub CLI if necessary:

```bash
gh auth status
```

If it reports that you are not logged in, run `gh auth login` and sign in as the account with write access to `topramen-2/Minecraft-server-create`. Git also needs your normal commit author name/email configured.

Publish:

```bash
python3 "$HOME/alaska-kit/manage.py" publish "$HOME/Downloads/Create-Kingdoms-Alaska-client.zip"
```

This clones the repository to `~/Minecraft-server-create-alaska-release`, commits only the setup scripts, pinned download list, worldgen overrides and documentation under `alaska-v2/`, pushes the commit and creates **v2.0.0-alaska as a prerelease**. The release contains the full client ZIP and its SHA-512 checksum. It never commits local server state, passwords, world saves or downloaded server configuration. Existing v1.0.0 assets remain available.

The command performs an actual push and release publication when you run it. It will stop on authentication failures, an existing local release checkout, or conflicting remote changes rather than force-push. If a push/release step fails, inspect the existing checkout/release before retrying; do not delete remote history.

Friends can download:

https://github.com/topramen-2/Minecraft-server-create/releases/tag/v2.0.0-alaska

That URL will exist only after the publish command succeeds. They should extract the client ZIP into an empty game directory and select the matching NeoForge version printed in `INSTALL.txt`. They should not merge it into their previous mods folder. The ZIP works for the official launcher on Windows as well as Linux; its instructions specify the exact required loader.

Once friends have validated the pack, promote the prerelease:

```bash
gh release edit v2.0.0-alaska --repo topramen-2/Minecraft-server-create --prerelease=false
```

## Rollback

On Arch:

```bash
ssh -t topramen@192.168.0.5 'cd ~/alaska-kit && sudo bash run-server.sh rollback'
```

Or directly on ZimaOS:

```bash
cd ~/alaska-kit
sudo bash run-server.sh rollback
```

This stops the new server, disables its restart policy, restores the original container's restart policy and starts the original server. Select your old client profile to join it. Both worlds remain on disk. Progress made in Alaska is not transferred back into the original world.

## Validation performed

- Queried matching Minecraft 1.21.1 / NeoForge project versions and recursively resolved required downloads.
- Downloaded and checked every pinned file's SHA-512.
- Inspected actual JAR metadata, including nested libraries, to catch dependencies missing from project metadata.
- Verified TOML syntax and referenced Regions Unexplored biome names against the selected release.
- Tested the staged migration and client installation against the existing GitHub v1.0.0 pack with a simulated Docker API.
- Checked original-world preservation, reset-world paths, client/server separation, shared file hashes, duplicate-run refusal, port retention and exclusion of private server data from the release package.

Not performed: a real Minecraft server boot, real client render test, or gameplay test of the complete combination. These require the first-start and first-join checks above. This is a prepared migration kit, not a claim that changes were already applied to your machines or repository.
