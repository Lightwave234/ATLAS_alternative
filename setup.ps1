$install = $false
$uninstall = $false
foreach ($arg in $args) {
    if($arg -eq "-i"){
        $install = $true
    }elseif ($arg -eq "-u"){
        $uninstall = $true
    }
}
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
#param([switch]$i, [switch]$u)
if($isAdmin){
    if($install){
        Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        choco install python nodejs -y
        pip install pip install requests requests.auth pytz pandas
        npm install -g lora-packet
        cls
    }elseif($uninstall){
        pip uninstall -y requests requests.auth pytz pandas
        npm uninstall -g lora-packet -y
        choco uninstall python nodejs -y
    }else{
        Write-Host "Avalable options: [-i, -u] (-i will install dependancies, -u uninstalls dependancies)"
    }
    Write-Host "Process complete."
}else{
    Write-Host "You do not have administrative permissions to run this setup script."
}