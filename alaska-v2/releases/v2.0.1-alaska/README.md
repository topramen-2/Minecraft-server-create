# Create Kingdoms Alaska v2.0.1

Minecraft Java 1.21.1 | NeoForge 21.1.265 | Java 21

## New installation

Download Create-Kingdoms-Alaska-v2.0.1-client.zip from the release assets.
Install NeoForge 21.1.265 using the official installer:
https://neoforged.net/

Extract the client ZIP into a new game directory. Select that directory
and NeoForge version in the Minecraft launcher. Allow 8 GB of RAM where
your computer has sufficient memory. Start with shaders disabled.

Use the server address supplied by the host. No address or credentials
are bundled here.

## Upgrading from v2.0.0-alaska

Close Minecraft and back up your existing game directory.

Move your existing mods folder outside the active game directory, then
copy the complete mods folder from this release into its place.
Do not merge old and new mods: replacing the folder removes outdated
or duplicate JARs, including kotlinforforge-5.11.0-all.jar.

Keep your existing personal settings, saves, maps, and waypoints.
The release retains the previous packaged configs and resource/shader packs.
The new mods create their default configuration files on first launch.

Do not use this procedure to connect an old TerraForged installation
directly to Alaska. Use a separate Alaska installation.

## Changes

- Added Xaero Minimap for waypoint markers.
- Added Unified Xaero Worldmap 2.0.4 for shared exploration.
- Retained Xaero World Map 1.47.0 and existing Waystones.
- Added Towns and Towers, Better Archeology, and YUNG Nether Fortresses.
- Added Cristel Lib, Cloth Config, Resourceful Config, and YUNG API.
- Client retains Kotlin for Forge 5.12.0 without the duplicate 5.11.0.

Server startup and one updated client join passed.
Two-player exploration syncing and new-structure gameplay remain to be tested.
This release is a prerelease.

## Individual mods

The repository folder alaska-v2/individual-mods contains the exact client
JARs used for this release. Open a file and use its raw/download button.

This is a CLIENT inventory. Do not copy the entire folder to a dedicated
server because it contains client rendering, audio, and interface mods.

The root mods folder belongs to the legacy pack and is not the Alaska list.
The original alaska-v2 migration tools and lockfile describe the earlier
migration baseline. This release inventory is in
alaska-v2/releases/v2.0.1-alaska/pack-info.json.

## Credits

Mods remain the work of their respective authors.
Xaero Minimap: https://modrinth.com/mod/xaeros-minimap
Xaero World Map: https://modrinth.com/mod/xaeros-world-map
Unified Xaero Worldmap:
https://www.curseforge.com/minecraft/mc-mods/unified-xaero-worldmap
Towns and Towers: https://modrinth.com/datapack/towns-and-towers
Better Archeology: https://modrinth.com/mod/better-archeology
YUNG Nether Fortresses:
https://modrinth.com/mod/yungs-better-nether-fortresses
