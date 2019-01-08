#This script downloads prerequisites required to run Windows Kubernetes Node
#Binaries and scripts will be downloaded to "package" folder in script directory

$downloadLocation = "$PSScriptRoot/package/"
$logFile = "$downloadLocation/package-info.md"
$tempLocation = "$downloadLocation/temp/"

function Create-FolderIfNotExist($location)
{
    If(!(test-path $location))
    {
          New-Item -ItemType Directory -Force -Path $location
    }
}
function Expand-Archive($file, $dest) {
    
        if (-not (Get-Command Expand-7Zip -ErrorAction Ignore)) {
            Install-Package -Scope CurrentUser -Force 7Zip4PowerShell > $null
        }
    
        Expand-7Zip $file $dest
}

function Write-Log($logstring) {
    Add-content $logFile -value $logstring   
}

Create-FolderIfNotExist $downloadLocation
Create-FolderIfNotExist $tempLocation

Write-Log "#Creation time: $((Get-Date).ToString())"
Write-Log "#This package contains all scripts and binaries required to run Windows Kubernetes Node "

Import-Module BitsTransfer
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$scriptsZipUrl = "https://github.com/Microsoft/SDN/archive/master.zip"
Write-Log "* Scripts used to run cluster were downloaded from $scriptsZipUrl "
Invoke-WebRequest -Uri $scriptsZipUrl -OutFile "$tempLocation/master.zip"
#wget $scriptsZipUrl -o "$tempLocation/master.zip"
Expand-Archive -file "$tempLocation/master.zip" -dest $tempLocation
cp "$tempLocation/SDN-master/Kubernetes/windows/*" $downloadLocation -r

$binariesTarUrl = "https://storage.googleapis.com/kubernetes-release/release/v1.10.1/kubernetes-node-windows-amd64.tar.gz"
Write-Log "* Binaries (kubectl, kubeadm, kubelet, kube-proxy) were downloaded from $binariesTarUrl"
Start-BitsTransfer -Source $binariesTarUrl -Destination $tempLocation
Expand-Archive -file "$tempLocation/kubernetes-node-windows-amd64.tar.gz" -dest $tempLocation
Expand-Archive -file "$tempLocation/kubernetes-node-windows-amd64.tar" -dest $tempLocation
cp "$tempLocation/kubernetes/node/bin/*" $downloadLocation -r

Remove-Item -Recurse -Force $tempLocation