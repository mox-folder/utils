# utils
General utility scripts

## engagement_cleanup.sh
Zip and move a bunch of CYA files and logs into a project_archive folder and then zip it for extraction over scp. CAUTION: by default this includes files that may contain sensitive information gathered during an engagement, use your best judgement here. Useful when you're doing an engagement on a temporal host that's going to be wiped or removed after work completes.

## wsl-setup.ps1
Enables all requirements and downloads WSL2 updates to get WSL running on Win10
