# AI-Q Docker Runner Script
# Provides easy access to Docker commands from the project root

param(
    [Parameter(Mandatory=$true)]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$ComposeFile = "unified",
    
    [Parameter(Mandatory=$false)]
    [string]$Service = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$Build,
    
    [Parameter(Mandatory=$false)]
    [switch]$Down,
    
    [Parameter(Mandatory=$false)]
    [switch]$Logs,
    
    [Parameter(Mandatory=$false)]
    [switch]$Follow
)

# Define compose file paths
$composeFiles = @{
    "unified" = "docker/compose/docker-compose.unified.yml"
    "development" = "docker/compose/docker-compose.yml"
    "infrastructure" = "docker/compose/docker-compose.infrastructure.yml"
    "feature-flags" = "docker/compose/docker-compose.feature-flags.yml"
}

# Validate compose file selection
if (-not $composeFiles.ContainsKey($ComposeFile)) {
    Write-Host "Error: Invalid compose file '$ComposeFile'" -ForegroundColor Red
    Write-Host "Available options: $($composeFiles.Keys -join ', ')" -ForegroundColor Yellow
    exit 1
}

$composePath = $composeFiles[$ComposeFile]

# Check if compose file exists
if (-not (Test-Path $composePath)) {
    Write-Host "Error: Compose file not found: $composePath" -ForegroundColor Red
    exit 1
}

function Show-Help {
    Write-Host "AI-Q Docker Runner" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\scripts\docker-run.ps1 up [compose-file] [options]" -ForegroundColor Gray
    Write-Host "  .\scripts\docker-run.ps1 down [compose-file]" -ForegroundColor Gray
    Write-Host "  .\scripts\docker-run.ps1 logs [compose-file] [service] [-Follow]" -ForegroundColor Gray
    Write-Host "  .\scripts\docker-run.ps1 build [compose-file]" -ForegroundColor Gray
    Write-Host "  .\scripts\docker-run.ps1 status [compose-file]" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Compose Files:" -ForegroundColor Yellow
    Write-Host "  unified        - Unified container setup (default)" -ForegroundColor Gray
    Write-Host "  development    - Development setup with all services" -ForegroundColor Gray
    Write-Host "  infrastructure - Infrastructure services only" -ForegroundColor Gray
    Write-Host "  feature-flags  - Generated based on feature flags" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\scripts\docker-run.ps1 up unified" -ForegroundColor Gray
    Write-Host "  .\scripts\docker-run.ps1 logs unified ai-q-app -Follow" -ForegroundColor Gray
    Write-Host "  .\scripts\docker-run.ps1 build feature-flags" -ForegroundColor Gray
}

function Invoke-DockerCompose {
    param(
        [string]$Action,
        [string]$Service = ""
    )
    
    $dockerCmd = "docker-compose -f $composePath $Action"
    
    if ($Service) {
        $dockerCmd += " $Service"
    }
    
    Write-Host "Running: $dockerCmd" -ForegroundColor Yellow
    Invoke-Expression $dockerCmd
}

# Main command logic
switch ($Command.ToLower()) {
    "up" {
        if ($Build) {
            Invoke-DockerCompose "up --build -d" $Service
        } else {
            Invoke-DockerCompose "up -d" $Service
        }
    }
    "down" {
        Invoke-DockerCompose "down"
    }
    "logs" {
        $logCmd = "logs"
        if ($Follow) {
            $logCmd += " -f"
        }
        Invoke-DockerCompose $logCmd $Service
    }
    "build" {
        Invoke-DockerCompose "build" $Service
    }
    "status" {
        Invoke-DockerCompose "ps"
    }
    "restart" {
        Invoke-DockerCompose "restart" $Service
    }
    "stop" {
        Invoke-DockerCompose "stop" $Service
    }
    "start" {
        Invoke-DockerCompose "start" $Service
    }
    "help" {
        Show-Help
    }
    default {
        Write-Host "Error: Unknown command '$Command'" -ForegroundColor Red
        Show-Help
        exit 1
    }
} 