# ADMWS12 - Profil matériel
# Ce script collecte les informations principales du PC.

Write-Host "=== CPU ==="
Get-CimInstance Win32_Processor |
    Select-Object Name, NumberOfCores, NumberOfLogicalProcessors

Write-Host "`n=== RAM ==="
Get-CimInstance Win32_PhysicalMemory |
    Measure-Object -Property Capacity -Sum |
    Select-Object @{Name="RAM_Go";Expression={[math]::Round($_.Sum / 1GB, 2)}}

Write-Host "`n=== GPU ==="
Get-CimInstance Win32_VideoController |
    Select-Object Name, AdapterRAM, DriverVersion

Write-Host "`n=== NVIDIA ==="
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    nvidia-smi
}
else {
    Write-Host "nvidia-smi non disponible."
}
