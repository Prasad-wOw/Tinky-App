# build_installer.ps1
# Downloads VC++ 2022 runtime, then compiles the Inno Setup installer.
# Run AFTER build_nuitka.ps1 has produced dist_release\Tinky.exe
# Usage: .\build_installer.ps1

$ErrorActionPreference = "Stop"
$ROOT = $PSScriptRoot

Write-Host "=== Tinky Installer Build ===" -ForegroundColor Cyan

# 1. Ensure dist_release\Tinky.exe exists
$exe = Join-Path $ROOT "dist_release\Tinky.exe"
if (-not (Test-Path $exe)) {
    Write-Host "ERROR: dist_release\Tinky.exe not found. Run build_nuitka.ps1 first." -ForegroundColor Red
    exit 1
}
Write-Host "  Tinky.exe : $([math]::Round((Get-Item $exe).Length/1MB,1)) MB" -ForegroundColor Green

# 2. Create deps folder and download VC++ 2022 x64 Redistributable
$depsDir = Join-Path $ROOT "installer_deps"
New-Item -ItemType Directory -Force -Path $depsDir | Out-Null

$vcRedist = Join-Path $depsDir "vc_redist.x64.exe"
if (-not (Test-Path $vcRedist)) {
    Write-Host "  Downloading VC++ 2022 x64 Redistributable..." -ForegroundColor Cyan
    Invoke-WebRequest `
        -Uri "https://aka.ms/vs/17/release/vc_redist.x64.exe" `
        -OutFile $vcRedist `
        -UseBasicParsing
    Write-Host "  Downloaded: $([math]::Round((Get-Item $vcRedist).Length/1MB,1)) MB" -ForegroundColor Green
} else {
    Write-Host "  VC++ runtime already cached." -ForegroundColor Green
}

# 3. Create output folder
$outDir = Join-Path $ROOT "installer_output"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# 4. Find ISCC (Inno Setup Compiler)
$iscc = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Antigravity IDE\resources\app\node_modules\innosetup\bin\ISCC.exe",
    $(if (Get-Command "iscc" -ErrorAction SilentlyContinue) { (Get-Command "iscc" -ErrorAction SilentlyContinue).Source } else { $null })
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1

if (-not $iscc) {
    Write-Host "ERROR: Inno Setup 6 not found. Install from https://jrsoftware.org/isdl.php" -ForegroundColor Red
    exit 1
}
Write-Host "  ISCC : $iscc" -ForegroundColor Green

# 5. Compile installer
Write-Host "`nCompiling installer..." -ForegroundColor Cyan
& $iscc "$ROOT\setup.iss"

if ($LASTEXITCODE -eq 0) {
    $installer = Get-ChildItem $outDir -Filter "*.exe" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $sizeMB = [math]::Round($installer.Length / 1MB, 1)
    Write-Host ""
    Write-Host "=== INSTALLER BUILD SUCCESSFUL ===" -ForegroundColor Green
    Write-Host "Installer : $($installer.FullName) ($sizeMB MB)" -ForegroundColor Green
    Write-Host ""
    Write-Host "DISTRIBUTION CHECKLIST:" -ForegroundColor Yellow
    Write-Host "  [x] VC++ 2022 Runtime bundled" -ForegroundColor Green
    Write-Host "  [x] Per-user install (no admin required)" -ForegroundColor Green
    Write-Host "  [x] Desktop + Start Menu shortcuts" -ForegroundColor Green
    Write-Host "  [x] Uninstaller registered in Apps & Features" -ForegroundColor Green
    Write-Host "  [ ] Code signing (get cert from Certum/DigiCert for store distribution)" -ForegroundColor Yellow
} else {
    Write-Host "=== INSTALLER BUILD FAILED (exit $LASTEXITCODE) ===" -ForegroundColor Red
    exit 1
}
