# Mod decisions

Target: Minecraft 1.21.1 / NeoForge, preserving the current Create Kingdoms server mods as the baseline.

## Terrain and Alaska focus

Tectonic provides large landforms. Regions Unexplored provides northern forests and biome variety. Project: Vibrant Journeys adds fallen logs, rocks and vegetation. Snow Under Trees supplies snow beneath forest canopies. Biome Replacer and custom Regions Unexplored region tables bias the Overworld toward cold forests, tundra, wetlands and mountains; Biome Spawn Point targets northern forests. This is Alaska-inspired, not an Alaska-only biome guarantee. The Nether and End remain available.

The selected Regions Unexplored 0.5.6.1 uses TerraBlender and its configurable region tables. TerraBlender is a required dependency, not TerraForged; retain it. TerraForged's JAR and old world datapack do not enter the new installation. The old world and its original files remain intact for rollback.

## Substitutions and omissions

| Requested | Selected / decision |
|---|---|
| Alex's Mobs | Alex's Mobs Unofficial Port, with its matching Citadel port |
| Spartan Weaponry | Spartan Weaponry Unofficial |
| Immersive Weathering | Immersive Weathering Renewed; beta port, not all upstream mechanics implemented |
| Embeddium / Oculus | Sodium 0.6.13 / Iris 1.8.12 |
| Inventory Sorter | Inventory Profiles Next and libIPN |
| Held-torch light | LambDynamicLights, client-side; visual lighting does not change server light levels or prevent mob spawns |
| North American Fishes | Omitted: no verified matching build; other selected fishing/wildlife mods provide some fish variety |
| Simple Farming | Omitted: no verified matching build; Farmer's Delight and Farm & Charm cover farming/cooking |
| Salt | Omitted: no verified matching build; no exact replacement claimed |
| Hearth & Home | Omitted: no verified matching build; existing building mods and Refurbished Furniture cover decoration |
| Audio resource packs | Enhanced Audio and Alternative Rain Sounds |
| Complementary | Both Reimagined and Unbound supplied as alternatives |

All other requested selections are represented below. Dependencies are included. Client effects and shaders stay off the dedicated server. The client also receives the biome controls so new single-player worlds can use them. Distant Horizons is client-only in this kit. Shaders start disabled; select one after the basic client works.

## Pinned files

The lockfile is authoritative for exact URLs, filenames and SHA-512 checksums. Some projects publish only beta builds for this Minecraft version. Version availability and dependency metadata are not proof of whole-pack runtime compatibility.

| Project | Version | Install side | Release type |
|---|---|---|---|
| [Moonlight Lib](https://modrinth.com/mod/moonlight) | 1.21-2.29.33-neoforge | both | release |
| [Panda's Falling Trees](https://modrinth.com/mod/pandas-falling-trees) | 0.14.0 | both | beta |
| [Serene Seasons](https://modrinth.com/mod/serene-seasons) | 10.1.0.9 | both | beta |
| [Alex's Mobs (Unofficial Port)](https://modrinth.com/mod/alexs-mobs-1.21.1) | 1.22.17 | both | release |
| [Naturalist](https://modrinth.com/mod/naturalist) | 2.0.7+1.21.1-neoforge | both | release |
| [[Let's Do] WilderNature](https://modrinth.com/mod/lets-do-wildernature) | 1.1.4 | both | release |
| [Farmer's Delight](https://modrinth.com/mod/farmers-delight) | 1.21.1-1.2.11a | both | release |
| [Variants&Ventures](https://modrinth.com/mod/variants-and-ventures) | neoforge-1.0.29+mc1.21.1 | both | release |
| [Farsighted Mobs](https://modrinth.com/mod/farsighted-mobs) | 3.0.2 | server | beta |
| [Villainous Fish AI](https://modrinth.com/mod/villainous-fish-ai) | 1.2 | server | release |
| [[Let's Do] Farm & Charm](https://modrinth.com/mod/lets-do-farm-charm) | 1.1.29 | both | release |
| [[HUGE UPDATE] Fisherman's Haven](https://modrinth.com/mod/fishermans-haven) | 3.0507 | both | release |
| [Swashbucklers](https://modrinth.com/mod/swashbucklers) | 2.6.6 | both | release |
| [Spartan Weaponry Unofficial](https://modrinth.com/mod/spartan-weaponry-unofficial) | 1.21.1-1.2.3 | both | release |
| [[Let's Do] Camping](https://modrinth.com/mod/lets-do-camping) | 2.1.6 | both | release |
| [Advanced Chimneys](https://modrinth.com/mod/advanced-chimneys) | 11.1.14.0 | both | release |
| [Immersive Weathering: Renewed](https://modrinth.com/mod/immersive-weather-renewed) | V1.0.4-NeoForge | both | beta |
| [Snow! Real Magic! ⛄](https://modrinth.com/mod/snow-real-magic) | 12.2.3+neoforge | both | release |
| [Distant Horizons](https://modrinth.com/mod/distanthorizons) | 2.4.5-b-1.21.1 | client | beta |
| [Better Foliage Renewed](https://modrinth.com/mod/better-foliage-renewed) | 6.0 | client | release |
| [Sound Physics Remastered](https://modrinth.com/mod/sound-physics-remastered) | neoforge-1.21.1-1.5.2 | client | beta |
| [AmbientSounds](https://modrinth.com/mod/ambientsounds) | 6.3.11 | client | release |
| [Sodium](https://modrinth.com/mod/sodium) | mc1.21.1-0.6.13-neoforge | client | release |
| [Iris Shaders](https://modrinth.com/mod/iris) | 1.8.12+1.21.1-neoforge | client | release |
| [Mouse Tweaks](https://modrinth.com/mod/mouse-tweaks) | 1.21-2.26.1-neoforge | client | release |
| [Inventory Profiles Next](https://modrinth.com/mod/inventory-profiles-next) | neoforge-1.21.1-2.2.5 | client | release |
| [(Bee's) Fancy Crops](https://modrinth.com/resourcepack/fancy-crops) | 1.3 | client | release |
| [Just Fancy Torches](https://modrinth.com/resourcepack/just-fancy-torches) | v3.0 | client | release |
| [Enhanced Audio (Sound Pack)](https://modrinth.com/resourcepack/enhanced-audio) | r7 | client | release |
| [Alternative Rain Sounds](https://modrinth.com/resourcepack/alternative-rain-sounds) | 1.21-1.21.1 | client | release |
| [Bliss Shaders](https://modrinth.com/shader/bliss-shader) | 2.1.2 | client | release |
| [BSL Shaders](https://modrinth.com/shader/bsl-shaders) | 10.1.8 | client | release |
| [Complementary Shaders - Reimagined](https://modrinth.com/shader/complementary-reimagined) | r5.9.3 | client | release |
| [Complementary Shaders - Unbound](https://modrinth.com/shader/complementary-unbound) | r5.9.3 | client | release |
| [Solas Shader](https://modrinth.com/shader/solas-shader) | 3.8 | client | release |
| [LambDynamicLights - Dynamic Lights](https://modrinth.com/mod/lambdynamiclights) | 4.8.11+1.21.1 | client | release |
| [Tectonic](https://modrinth.com/mod/tectonic) | 3.0.28-neoforge-21.1 | both | release |
| [Regions Unexplored](https://modrinth.com/mod/regions-unexplored) | N-0.5.6.1+1.21.1 | both | release |
| [Project: Vibrant Journeys](https://modrinth.com/mod/project-vibrant-journeys) | 1.21.1-7.0.9 | both | release |
| [Snow Under Trees](https://modrinth.com/mod/snow-under-trees) | v1.5.1 | server | release |
| [Biome Replacer](https://modrinth.com/mod/biome-replacer) | 2.1-hippo-neo | server | release |
| [Biome Spawn Point](https://modrinth.com/mod/biome-spawn-point) | 1.21.1-2.4-fabric+forge+neo | server | release |
| [PandaLib](https://modrinth.com/mod/pandalib) | 0.6.2 | both | beta |
| [GlitchCore](https://modrinth.com/mod/glitchcore) | 2.1.0.2 | both | beta |
| [Citadel (Unofficial Port)](https://modrinth.com/mod/citadel-1.21.1-port) | 2.7.6 | both | release |
| [Curios API](https://modrinth.com/mod/curios) | 9.5.1+1.21.1 | both | release |
| [Architectury API](https://modrinth.com/mod/architectury-api) | 13.0.11+neoforge | both | release |
| [Resourceful Lib](https://modrinth.com/mod/resourceful-lib) | 3.0.12 | both | release |
| [ForgeEndertech](https://modrinth.com/mod/forgeendertech) | 12.1.4.0 | both | release |
| [Kiwi 🥝](https://modrinth.com/mod/kiwi) | 15.8.7+neoforge | both | release |
| [CreativeCore](https://modrinth.com/mod/creativecore) | 2.13.52 | client | release |
| [Kotlin for Forge](https://modrinth.com/mod/kotlin-for-forge) | 5.12.0 | client | release |
| [libIPN](https://modrinth.com/mod/libipn) | neoforge-1.21.1-6.6.3 | client | release |
| [Lithostitched](https://modrinth.com/mod/lithostitched) | 1.8.1-neoforge-21.1 | server | release |
| [TerraBlender](https://modrinth.com/mod/terrablender) | 4.1.0.8 | both | beta |
| [Collective](https://modrinth.com/mod/collective) | 1.21.1-8.73-fabric+forge+neo | both | release |
| [MrCrayfish Furniture Refurbished](https://github.com/MrCrayfish/MrCrayfishFurnitureMod-Refurbished/releases/tag/v1.21.1-1.0.22) | v1.21.1-1.0.22 | both | release |
| [Framework](https://github.com/MrCrayfish/Framework/releases/tag/v1.21.1-0.13.19) | v1.21.1-0.13.19 | both | release |
| [Alex's Delight](https://www.curseforge.com/minecraft/mc-mods/alexs-delight/files/7612806) | 1.6 | both | release |

## Gameplay checks before inviting players

- Test Create saw farms and MineColonies foresters with Panda's Falling Trees.
- Check seasonal crop behavior and Immersive Weathering's block changes before building production farms.
- Check new-chunk generation and modded ore/resource availability for Create, Applied Energistics 2 and TFMG.
- Start with shaders disabled and modest Distant Horizons settings, then test shader choices individually.
- Wildlife content is varied; the biome configuration does not make every creature geographically accurate to Alaska.

Metadata and staged-install tests passed. Full server startup, client rendering and gameplay integration remain untested until deployment.
