# Validation and known issues — v2.1.0

The server reached its Done message, remained running with zero container restarts, and answered an RCON player-list request after the mod update. The complete client archive and all 120 JARs passed archive integrity checks. Downloaded additions are pinned to exact versions and verified by checksums.

**The updated client has not yet been launched and joined to the server as a full pack.** A successful server startup does not prove that every client feature or schematic works.

Existing server logs still report:

- Aeronautics No Horizon: duplicate `track_tool_kit` entry while MineColonies enumerates creative-tab items. The server remained responsive; the underlying issue is unresolved.
- Design n' Decor / Railways: some loot tables refer to unregistered items, including optional mod integrations.
- Create Deco: the placard recipe fails to parse.
- Fisherman's Haven: Aquaculture integration recipes refer to unavailable items.
- Sable: physics-tag entries refer to `copycats:copycat_catwalk`, which is not registered.
- Distant Horizons: a warning involving the AE2 spatial-storage dimension.

This release preserves server-matching versions rather than silently removing gameplay mods to hide these messages. No Horizon and the newer Linear Bearings Fix remain included. The old duplicate Linear Bearings Fix 1.0.1 and old Moonlight 2.29.33 are not in the pack.

If launch or joining fails, send the error screen and `logs/latest.log` from the new game folder to Jackson. Keep the previous installation as a backup.
