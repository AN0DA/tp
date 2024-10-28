$pythonCheck = & python --version 2>&1
if ($pythonCheck -notmatch "Python 3\.12") {
    Write-Host "Python 3.12 is not installed."
    Write-Host "Please download and install Python 3.12 from: https://www.python.org/downloads/"
    Write-Host "Make sure to check the 'Add Python to PATH' option during installation."
    exit
}

$gitCheck = & git --version 2>&1
if ($gitCheck -notmatch "git version") {
    Write-Host "Git is not installed."
    Write-Host "Please download and install Git from: https://git-scm.com/download/win"
    exit
}

Write-Host "Installing tp from GitHub repository..."
pip install git+https://github.com/AN0DA/tp.git@latest

# Add Python Scripts to PATH if it's not already there
$pythonScriptsPath = [System.IO.Path]::Combine($env:LOCALAPPDATA, "Programs\Python\Python312\Scripts")
if (-not $env:Path.Contains($pythonScriptsPath)) {
    Write-Host "Adding Python Scripts folder to PATH..."
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";" + $pythonScriptsPath, [System.EnvironmentVariableTarget]::User)
    Write-Host "PATH updated. You may need to restart your terminal for changes to take effect."
} else {
    Write-Host "Python Scripts folder is already in PATH."
}

$createGuiShortcut = Read-Host "Do you want to create a desktop shortcut for 'tp gui' (GUI version)? [y/n]"
$createWebShortcut = Read-Host "Do you want to create a desktop shortcut for 'tp web' (web version)? [y/n]"

$desktopPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"))

function Create-Shortcut {
    param (
        [string]$shortcutPath,
        [string]$targetPath,
        [string]$arguments,
        [string]$description
    )
    $wshShell = New-Object -ComObject WScript.Shell
    $shortcut = $wshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $targetPath
    $shortcut.Arguments = $arguments
    $shortcut.Description = $description
    $shortcut.Save()
}

if ($createGuiShortcut -eq "y") {
    Write-Host "Creating desktop shortcut for 'tp gui'..."
    Create-Shortcut -shortcutPath "$desktopPath\tp GUI.lnk" -targetPath "python" -arguments "-m tp gui" -description "Launch tp GUI version"
}

if ($createWebShortcut -eq "y") {
    Write-Host "Creating desktop shortcut for 'tp web'..."
    Create-Shortcut -shortcutPath "$desktopPath\tp Web.lnk" -targetPath "python" -arguments "-m tp web" -description "Launch tp Web version"
}

Write-Host "Installation complete. You can use 'tp' commands in PowerShell, and shortcuts have been created if selected."
