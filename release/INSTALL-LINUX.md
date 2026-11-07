# Linux — install Create Kingdoms Alaska v2.1.0

This guide uses the official Minecraft Launcher and Minecraft **Java Edition**. You need an account that owns Java Edition, an internet connection, and preferably **16 GB or more of computer RAM** to allocate 8 GB to Minecraft.

## 1. Download and extract the pack

1. Open [the latest release](https://github.com/topramen-2/Minecraft-server-create/releases/latest).
2. Download **01-Create-Kingdoms-Alaska-v2.1.0-CLIENT.zip**. Expand **Assets** if needed. Ignore the **Source code** downloads. No older pack or patch is needed.
3. Open your file manager. In your Home folder, create a folder named **Games**.
4. Open the downloaded ZIP with your archive manager. Extract its contents into a new folder named **Create-Kingdoms-Alaska-v2.1.0** inside Games.
5. Open the extracted folder. It should directly contain **mods**, **config**, **installer**, and **START-HERE.txt**. This is your **game folder**. Keep the individual mod JARs intact; do not extract them.
6. Press **Ctrl+L** in the file manager to show the full path, then copy it. It will resemble `/home/yourname/Games/Create-Kingdoms-Alaska-v2.1.0`. Use your actual path in the launcher, not the example and not a literal `~`.

## 2. Install Java 21 and prepare Minecraft

1. Install the [official Minecraft Launcher](https://www.minecraft.net/download) using the Linux download/package appropriate to your distribution. Sign in with the Microsoft account that owns Minecraft Java Edition.
2. Install a **64-bit Java 21** runtime or JDK through your distribution's software/package manager. Choose the desktop runtime, not a headless-only package, because the NeoForge installer has a window. Alternatively use [Eclipse Temurin Java 21](https://adoptium.net/temurin/releases/?version=21&os=linux) and follow its Linux installation instructions for your system. Select your computer's architecture; most gaming PCs use x64.
For Ubuntu 24.04 / Linux Mint 22, open **Terminal** from the applications menu and run each line separately:

```sh
sudo apt update
```

```sh
sudo apt install openjdk-21-jre
```

For Arch Linux, use:

```sh
sudo pacman -Syu jre21-openjdk
```

The Arch command also performs the normal system upgrade; finish it before continuing. When `sudo` asks for your password, type your computer login password and press Enter. Nothing appears while you type. If asked to continue, type `y` and press Enter. Other distributions can use the Temurin Java 21 installation instructions linked above.

3. Open a terminal and check:

```sh
java -version
```

The result should say **21**. If it names a different version and you have several Java versions installed, select Java 21 through your distribution's Java settings or use the full path to its `bin/java` executable when running the installer. Do not uninstall Java versions needed by other applications. On Arch, you can use `/usr/lib/jvm/java-21-openjdk/bin/java` in place of `java` in step 3's installer command without changing your system default.

4. Open Minecraft Launcher → **Minecraft: Java Edition** → **Installations** → **New installation**.
5. Name it **Minecraft 1.21.1 Setup**, choose **release 1.21.1** under Version, and save/create it (the button may say Install).
6. Launch it once, wait for Minecraft's main menu, then quit both Minecraft and the launcher.

## 3. Install NeoForge 21.1.265

1. In your file manager, open your extracted game folder, then **installer**.
2. Right-click an empty area and choose **Open in Terminal** (wording varies by desktop).
3. Run:

```sh
java -jar neoforge-21.1.265-installer.jar
```

4. In the window, choose **Install client**. Leave the launcher directory at its normal Minecraft location, usually `/home/yourname/.minecraft`. Click **Proceed** and wait for the success message.
5. Do not select Install server or move the installer into mods. Use this exact NeoForge version, not Forge/Fabric or a newer NeoForge.

If the installer says it cannot find the launcher, verify that you launched vanilla Minecraft 1.21.1 once and closed the launcher. Sandboxed launchers (such as Flatpak builds) can store launcher files in another location; use the launcher's actual Minecraft directory rather than blindly creating `.minecraft`. This guide's default paths assume the official, non-sandboxed launcher.

## 4. Create the Alaska installation

1. Reopen Minecraft Launcher → **Minecraft: Java Edition** → **Installations**.
2. Enable **Modded** if that filter is shown, then click **New installation**.
3. Set Name to **Create Kingdoms Alaska v2.1.0**.
4. Choose the Version entry containing **neoforge-21.1.265**.
5. Set **Game Directory** to the full path you copied in step 1. Use Browse if available. Select the folder directly containing mods and config, not the mods folder.
6. Open **More Options**. Keep the bundled/default **Java Executable** unless you have overridden it; a custom executable must point to Java 21's `bin/java`.

## 5. Set RAM to 8 GB

1. Under **More Options**, find **JVM Arguments**.
2. Replace the existing `-Xmx` argument (often `-Xmx2G`) with **`-Xmx8G`**.
3. Leave the other arguments alone. Keep exactly one `-Xmx` argument.
4. Save/create the installation (some launcher versions label the button Install).

This gives Minecraft a maximum of 8 GB. A machine with only 8 GB total cannot spare all of it for the game. Check your system's About/Memory page; 16 GB or more total is recommended for this setup.

## 6. Launch and connect

1. Return to **Play** and select **Create Kingdoms Alaska v2.1.0** beside the Play button.
2. Click **Play** and accept the modded-installation notice if shown. Allow several minutes for the first launch.
3. At the main menu, choose **Multiplayer** → **Add Server**.
4. Enter **Create Kingdoms Alaska** as the name and the server address Jackson provides, including `:25566` if supplied. Save and join. The website/management address and RCON port are not the Minecraft server address.
5. Keep shaders off for the first connection. The included shader/resource packs are optional; enable them later if desired.

## Troubleshooting

- **No mods:** verify the chosen NeoForge installation and Game Directory. JARs belong directly in `your game folder/mods`, not a second nested mods directory.
- **NeoForge missing:** restart the launcher, enable Modded in Installations, and check that the installer completed successfully.
- **Missing/mismatched mods:** extract the complete pack into a new empty folder; don't merge old packs or add the newest versions of individual mods.
- **Crash or connection failure:** send Jackson the error and `logs/latest.log` from the game folder.
- **Updating an older installation:** keep the old folder as a backup and create this separate installation. Don't overwrite the new mods/config with old copies.

Exact versions: Minecraft **1.21.1** · NeoForge **21.1.265** · Java **21 (64-bit)** · game RAM **8 GB**.

Reference: [NeoForge client installation](https://docs.neoforged.net/user/docs/client/), [Ubuntu Java 21 package](https://packages.ubuntu.com/noble/openjdk-21-jre), [Arch Java 21 package](https://archlinux.org/packages/extra/x86_64/jre21-openjdk/).
