# Windows 10 / 11 — install Create Kingdoms Alaska v2.1.0

This guide uses the official Minecraft Launcher and Minecraft **Java Edition**. Bedrock Edition cannot load this pack. You need an account that owns Java Edition, an internet connection, and preferably **16 GB or more of computer RAM** to give the game 8 GB.

## 1. Download the complete pack

1. Open [the latest release](https://github.com/topramen-2/Minecraft-server-create/releases/latest).
2. Click **01-Create-Kingdoms-Alaska-v2.1.0-CLIENT.zip**. If needed, expand **Assets** near the bottom of the release.
3. Wait for the download to finish. You do not need any older release, patch ZIP, or individual mod download. Ignore GitHub's **Source code** downloads.
4. In File Explorer, make a folder named **Minecraft Packs** inside your Documents folder.
5. Right-click the downloaded ZIP and choose **Extract All**. Choose a new folder named **Create-Kingdoms-Alaska-v2.1.0** inside Minecraft Packs, then click **Extract**.
6. Open that extracted folder. You should see **mods**, **config**, **installer**, and **START-HERE.txt** directly inside it. This is your **game folder**. Do not move the mods into another mods folder or open the individual JAR files.
7. Click File Explorer's address bar and copy the full folder path. Keep it for step 4 below.

## 2. Install Java 21 and prepare Minecraft

1. Install the [official Minecraft Launcher](https://www.minecraft.net/download) if you do not have it. Sign in with the Microsoft account that owns Minecraft Java Edition.
2. Install **Eclipse Temurin Java 21**, Windows **x64**, **JDK**, **MSI**, from [Adoptium](https://adoptium.net/temurin/releases/?version=21&os=windows&arch=x64). This is free. Use Java 21, not the newest numbered Java release. In the installer, enable the `.jar` file association and PATH options if offered.
3. Open Minecraft Launcher → **Minecraft: Java Edition** → **Installations** → **New installation**.
4. Name this temporary installation **Minecraft 1.21.1 Setup**. For **Version**, choose **release 1.21.1**. Save/Create it (some launcher versions label this button **Install**).
5. Launch that installation once. When Minecraft reaches its main menu, quit the game, then close the launcher completely.

## 3. Install the exact NeoForge version

1. In your extracted game folder, open **installer**.
2. Double-click **neoforge-21.1.265-installer.jar**.
3. Select **Install client**, leave the Minecraft launcher directory at its default, and click **Proceed**. Wait for the success message. This installs NeoForge into the launcher; you choose your separate game folder in the next step.
4. Do not put this installer JAR in the mods folder. Do not select **Install server**. Do not substitute Forge, Fabric, or a different NeoForge version.

**If double-clicking the JAR does nothing or opens an archive:** open the installer folder, click the File Explorer address bar, type `cmd`, and press Enter. In the window that opens, run these commands separately:

```bat
java -version
```

The result should say version **21**. If Java is not found, finish installing Java 21 and open a new command window. Then run:

```bat
java -jar neoforge-21.1.265-installer.jar
```

## 4. Make the Alaska launcher installation

1. Reopen Minecraft Launcher → **Minecraft: Java Edition** → **Installations**.
2. Enable the **Modded** checkbox/filter if it is shown.
3. Click **New installation**.
4. Set **Name** to **Create Kingdoms Alaska v2.1.0**.
5. Under **Version**, choose the entry containing **neoforge-21.1.265**. Do not choose Latest release or Latest snapshot.
6. Under **Game Directory**, click **Browse** and select the extracted game folder from step 1. Alternatively paste its full path. Select the folder that directly contains **mods** and **config**, not the mods folder itself.
7. Open **More Options**. Leave **Java Executable** on the launcher's bundled/default Java unless you have deliberately overridden it. Any custom Java executable must be 64-bit Java 21.

## 5. Give Minecraft 8 GB of RAM

1. In the same **More Options** section, find **JVM Arguments**.
2. Find the part beginning with `-Xmx`, normally `-Xmx2G`.
3. Replace only that part with **`-Xmx8G`**. Keep all the other arguments unchanged. There must be only one `-Xmx` argument.
4. Click **Save/Create** (or **Install**, depending on launcher version).

`-Xmx8G` sets the maximum game memory to 8 GB. It does not give your computer more RAM. If your entire computer has only 8 GB, do not allocate all of it to Minecraft; this pack's 8 GB setup needs more system memory. See Settings → System → About → Installed RAM to check.

## 6. Play

1. Return to the launcher's **Play** tab.
2. Use the installation selector beside the Play button to choose **Create Kingdoms Alaska v2.1.0**, then click **Play**. Accept the launcher's modded-installation notice if shown.
3. The first launch can take several minutes. Wait for Minecraft's main menu.
4. Click **Multiplayer** → **Add Server**. Name it **Create Kingdoms Alaska**. Enter the server address provided by Jackson, including `:25566` if that is part of the address. Do not use a website address or the server's RCON port.
5. Save, select the server, and click **Join Server**.

Shaders and resource packs are included as optional visuals/audio. Leave shaders off for the first connection. Enable them later through Options → Video Settings → Shader Packs if desired.

## If something goes wrong

- **NeoForge missing from the launcher:** close and reopen the launcher, enable Modded in Installations, and confirm the installer reported success.
- **Minecraft opens without mods:** check the selected installation, NeoForge version, and Game Directory. The actual files should be directly inside `your game folder\mods`, not `mods\mods`.
- **Missing or mismatched mods:** use this complete ZIP in a new empty game folder. Do not mix it with old releases or update individual mods to newer versions.
- **Crashes or refuses to join:** send Jackson the error screen and `logs\latest.log` from your game folder. The server can be running even when a client has a separate issue.
- **Already have an old pack?** Keep it as a backup and make this new installation beside it. Copy personal screenshots/maps later if desired; don't overwrite the new mods/config with old folders.

Exact versions: Minecraft **1.21.1** · NeoForge **21.1.265** · Java **21 (64-bit)** · game RAM **8 GB**.

Reference: [NeoForge client installation](https://docs.neoforged.net/user/docs/client/) and [Minecraft Launcher memory settings](https://help.minecraft.net/hc/en-us/articles/39083573916941).
