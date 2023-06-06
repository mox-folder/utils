# wsl-setup.ps1

function IsAdmin {
    $admin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    if ($admin -eq $false) {
        Write-Host "Script must be run as admin. Please re-run as administrator."
        exit
    }
}

function CheckAndEnableFeature {
    param([string]$featureName)
    $feature = Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -eq $featureName}
    if ($feature.State -eq 'Disabled') {
        Write-Host "Enabling $featureName..."
        Enable-WindowsOptionalFeature -Online -FeatureName $featureName -NoRestart
        Write-Host "$featureName feature has been enabled. Host will restart. Enter anything to continue."
        Read-Host
        Restart-Computer
        exit
    } else {
        Write-Host "$featureName is already enabled."
    }
}

function DownloadAndRunWSL2Update {
    Write-Host "Downloading WSL2 Linux Kernel update..."
    $url = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
    $output = "C:\temp\wsl_update_x64.msi"
    if(!(Test-Path -Path "C:\temp\" )){
        New-Item -ItemType directory -Path "C:\temp\"
    }
    Invoke-WebRequest -Uri $url -OutFile $output
    Start-Process -FilePath $output -Wait
    Write-Host "Please confirm succesful installation of WSL2 Linux Kernel update. Enter anything to continue."
    Read-Host
}

# Check if script is run as admin
IsAdmin

# Check required features are enabled
CheckAndEnableFeature -featureName "Microsoft-Windows-Subsystem-Linux"
CheckAndEnableFeature -featureName "VirtualMachinePlatform"
CheckAndEnableFeature -featureName "Hyper-V"

# Download and run WSL2 Linux Kernel update
DownloadAndRunWSL2Update

# Set WSL 2 as default version
wsl --set-default-version 2

Write-Host "WSL is ready. You can now download your preferred Linux distro from the Windows Store. We also recommend downloading the Windows Terminal from the Windows Store."
Write-Host "Host will restart. Enter anything to continue."
Read-Host
Restart-Computer
