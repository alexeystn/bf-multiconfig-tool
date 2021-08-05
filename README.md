## BF Multiconfig Tool
Load identical configs to multiple Betaflight drones.<br>
Set different OSD craft names (or other settings) automatically, depending on `mcu_id`

## How to setup:

1) Download and run `multiconfig.exe` from [releases](https://github.com/alexeystn/bf-multiconfig-tool/releases) page. <br>
File `parameters.json` will be automatically created on the first run.
2) Edit `parameters.json` according to `mcu_id` and desired commands for every drone. 
3) Specify path to text file with `diff all` configuration. File must have `save` line in the end.
<details>
<summary>Example</summary>
  
```
{
  "path": "C:/Users/Pilot/diff.txt",
  "setups": {
    "003b001b3538510e34393631": [
      "set name = Drone One"
    ],
    "002c00303538510e34393631": [
      "set name = Drone Two"
    ],
    "0023002f3438510831353632": [
      "set name = Drone Three",
      "resource motor 1 A08",
      "set ibata_scale = 120"
    ]
  }
}
```

</details>

## How to use:

1) Run `multiconfig.exe`.
2) Connect FC to your computer.
3) Press Enter when FC is recognized. If detected `mcu_id` is found in the `parameters.json`, additional lines will be inserted to config for this drone.
4) Press Enter to confirm. Configuration is uploaded to FC, saved and rebooted.
5) Connect next FC and go step 2.

## For developers:

Executable is assembled with PyInstaller. You may run Python script `multiconfig.py` directly.
`pyinstaller multiconfig.py --onefile`
