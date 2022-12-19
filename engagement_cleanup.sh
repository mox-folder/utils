#!/bin/bash
mkdir ~/project_archive
cd project_archive
zip -r responder-logs.zip /usr/share/resonder/logs
zip -r responder-db.zip /usr/share/responder/Responder.db
zip -r tmp-files.zip /tmp
zip -r cme.zip ~/.cme/
mkdir msf4-files
cd msf4-files
cp ~/.msf4/history .
zip -4 msf4-loot ~/.msf4/loot
zip -r msf4-logs ~/.msf4/logs
cd ..
cp ~/.zsh_history .zsh_history
cd ~
zip -r project_archive.zip ~/project_archive
rm -rf ~/project_archive
echo ''
echo "***** Don't forget to export msfconsole WORKSPACES and DUMPS -- if desired! *****"
