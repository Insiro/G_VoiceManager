# Genshin Voice Mod Manager

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

| name          | desc                                                                                   |
| ------------- | -------------------------------------------------------------------------------------- |
| temp path     | Path for Temprary file save                                                            |
| resource path | Path for Save Resource files like `Generated Sound File`                               |
| genshin path  | Genshin GameData Path                                                                  |
| mods path     | Mod Source folders saved path                                                          |
| backup path   | Path for Original Sound File will saved, recommand to Set same drive with Genshin Path |
| language      | Language for apply mod                                                                 |

#### Json Example

```json
{
    "temp_path": "C:\\temp",
    "resource_path": "..\\resources",
    "genshin_path": "C:\\Program Files\\Genshin Impact\\Genshin Impact game",
    "mods_path": "..\\resources\\mods",
    "backup_path": "..\\resources\\backup",
    "language": "Korean"
}
```
