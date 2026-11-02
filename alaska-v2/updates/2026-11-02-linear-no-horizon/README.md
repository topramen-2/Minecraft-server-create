# Alaska client update — Linear Bearing and No Horizon

This update adds three mods to the existing **v2.0.2-alaska** client pack:

| Mod | Version |
| --- | --- |
| Linear Bearing | 1.3.5 |
| Linear Bearings Fix | 1.0.3 |
| Aeronautics: No Horizon | 1.0.4 |

## Download and install

1. Close Minecraft and back up your current mods folder.
2. If starting fresh, install the [v2.0.2 client pack](https://github.com/topramen-2/Minecraft-server-create/releases/tag/v2.0.2-alaska) first.
3. Download [the three-mod upgrade ZIP](https://github.com/topramen-2/Minecraft-server-create/raw/refs/heads/main/alaska-v2/updates/2026-11-02-linear-no-horizon/Alaska-v2.0.2-linear-no-horizon-update.zip).
4. Remove any older Linear Bearing, Linear Bearings Fix, or Aeronautics No Horizon JARs from your game's mods folder. In particular, remove linearbearingsfix-1.0.1.jar.
5. Extract the ZIP and copy its three mods/*.jar files into that same mods folder. Keep the other v2.0.2 mods.
6. Launch Minecraft 1.21.1 with NeoForge 21.1.265 and Java 21, then join Alaska.

This is an **add-on update**, not a complete client pack. The v2.0.2 release ZIP does not contain these additions. The individual JARs are also available in [individual-mods](../../individual-mods/).

## Validation and troubleshooting

The server initially failed with Linear Bearing 1.3.5 and Linear Bearings Fix 1.0.1:
```text
Attempted to load class net/minecraft/client/resources/model/BakedModel for invalid dist DEDICATED_SERVER
```

Replacing the fix with **1.0.3** allowed startup to finish. The supplied server log shows:
```text
[20:59:37] [Server thread/INFO] [minecraft/DedicatedServer]: Done (3.223s)!
```

Server startup is confirmed. Joining with this updated client and testing the new blocks are still pending. Earlier v2.0.2 gameplay checks do not certify these additions.

The JAR archives were checked for corruption; the two Modrinth downloads matched their published SHA-1 hashes. SHA-512 hashes for all three files are in SHA512SUMS, and pack-info.json records the expected complete client inventory after this update.

## Next checks

- Join with the updated client.
- Test Linear Bearing motion and No Horizon blocks.
- Check a second player's join and reconnect.

The original v2.0.2 release remains available for reference. Do not rerun the historical migration script to apply this update.
