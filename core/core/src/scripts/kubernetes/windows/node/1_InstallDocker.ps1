# This script installs docker module for Windows 

Install-Module -Name DockerMsftProvider -Repository PSGallery -Force
Install-Package -Name Docker -ProviderName DockerMsftProvider

Restart-Computer -Force
