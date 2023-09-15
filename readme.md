# Genshin Voice Mod Manager

**WARNING :** I am not responsible for any problems that arise from using this software.

### future works

[ ] GUI Implementation

## Tested Env

| name    | version     |
| ------- | ----------- |
| windows | 22H2(22621) |
| python  | 3.11.2      |

## Usage

### Installation

```bash
pip3 install -r requirement.txt
```

### configuration

| name             | desc                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------ |
| temp path        | Path for Temprary file save                                                                |
| resource path    | Path for Save Resource files like `Generated Sound File`                                   |
| genshin path     | Genshin GameData Path                                                                      |
| mods source path | Mod Source folders saved path                                                              |
| backup path      | Path for Original Sound File will saved, **Recommand to Set same drive with Genshin Path** |
| voice_lang       | Voice Language for apply mod                                                               |
| locale           | display locale, Currently support code are [`en`, `kr`]                                    |

<details><summary>Json Example</summary>
    
```json
{
    "temp_path": ".\\temp",
    "resource_path": ".\\resources",
    "genshin_path": "C:\\Program Files\\Genshin Impact\\Genshin Impact game",
    "mod_sources_path": ".\\resources\\mods",
    "voice_lang": "Japanese",
    "backup_path": ".\\resources\\backup",
    "locale": "en"
}
```
    
</details>

### Usage Stem

1. Configuration Setting
    - required to update for your computer
2. Backup Original Resource
    - step for isolate original file
    - then link voice file as symblic link
3. Generate Mod file
    1. Select Mod Base
        - default is Backup file, if you cange, you can override mods
    2. Clear Inpt(If Required)
    3. Add Mod Source
    4. Pack Mod
        - Generate Mod
4. Apply Mod
    - Make Symlink from Packed Mods
5. Restore Mod when update
