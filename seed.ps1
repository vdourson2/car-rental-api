param(
    [switch]$WithCreate,
    [ValidateSet("auto", "local", "docker")]
    [string]$Mode = "auto"
)

$ErrorActionPreference = "Stop"

function Invoke-LocalSeed {
    if (Test-Path ".\.venv\Scripts\python.exe") {
        $python = ".\.venv\Scripts\python.exe"
    } else {
        $python = "python"
    }

    $args = @("-m", "flask", "--app", "app:create_app", "seed")
    if ($WithCreate) {
        $args += "--with-create"
    }

    Write-Host "Execution du seed en local..."
    & $python @args
    return $LASTEXITCODE
}

function Invoke-DockerSeed {
    $args = @("compose", "-f", "docker-compose.dev.yml", "exec", "backend", "flask", "--app", "app:create_app", "seed")
    if ($WithCreate) {
        $args += "--with-create"
    }

    Write-Host "Execution du seed dans le container backend..."
    & docker @args
    return $LASTEXITCODE
}

if ($Mode -eq "local") {
    $code = Invoke-LocalSeed
    exit $code
}

if ($Mode -eq "docker") {
    $code = Invoke-DockerSeed
    exit $code
}

if ((Invoke-LocalSeed) -ne 0) {
    Write-Host "Seed local indisponible, tentative via Docker..."
    $code = Invoke-DockerSeed
    exit $code
}

exit 0
