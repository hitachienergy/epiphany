#Given binaries and scripts package path and config file path (certificate info for Kubernetes conenction) 
#configures Windows node. 

Param(
    [parameter(Mandatory = $true)] [string] $packagePath,
    [parameter(Mandatory = $true)] [string] $configFilePath
)
$nodeInstallLocation = "C:/k/"
$dockerFileLocation = "$PSScriptRoot/Dockerfile"

If((test-path $nodeInstallLocation))
{
    Remove-Item -Recurse -Force $nodeInstallLocation
}

mkdir $nodeInstallLocation

cp "$packagePath/*" $nodeInstallLocation -r
cp $configFilePath "$nodeInstallLocation/config"
cp $dockerFileLocation "$nodeInstallLocation"

[Environment]::SetEnvironmentVariable("KUBECONFIG", "$nodeInstallLocation/config", [System.EnvironmentVariableTarget]::Machine )

$env:Path += ";$nodeInstallLocation"
[Environment]::SetEnvironmentVariable("Path", "$env:Path", [System.EnvironmentVariableTarget]::Machine )

docker pull microsoft/windowsservercore:1709
docker tag microsoft/windowsservercore:1709 microsoft/windowsservercore:latest
cd C:/k/
docker build -t kubeletwin/pause .
Restart-Computer -Force
