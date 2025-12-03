# Setup script for Google OAuth in the Injury Prediction Model
# Run this script after you have your Google OAuth credentials

$ErrorActionPreference = "Stop"

Write-Host "Google OAuth Setup for Injury Prediction Model" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend")) {
    Write-Host "ERROR: This script must be run from the project root directory" -ForegroundColor Red
    exit 1
}

# Check if backend/.env exists
$envFile = "backend\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "Creating backend/.env file..." -ForegroundColor Yellow
    "" | Out-File -Encoding UTF8 $envFile
}

# Read existing .env file
$envContent = Get-Content $envFile -Raw

# Prompt for credentials
Write-Host "Please enter your Google OAuth credentials from Google Cloud Console:" -ForegroundColor Yellow
Write-Host ""

$clientId = Read-Host "Google Client ID"
$clientSecret = Read-Host "Google Client Secret (press Tab for password input)" -AsSecureString
$clientSecretPlain = [System.Net.NetworkCredential]::new("", $clientSecret).Password

# Update or add environment variables in .env
$lines = $envContent -split "`n" | Where-Object { $_ -notmatch "^GOOGLE_CLIENT_ID=" -and $_ -notmatch "^GOOGLE_SECRET=" }
$updatedContent = ($lines -join "`n").TrimEnd() + "`nGOOGLE_CLIENT_ID=$clientId`nGOOGLE_SECRET=$clientSecretPlain`n"

# Write back to .env
$updatedContent | Out-File -Encoding UTF8 $envFile

Write-Host ""
Write-Host "✓ Updated backend/.env with Google OAuth credentials" -ForegroundColor Green

# Run the Django setup script
Write-Host ""
Write-Host "Setting up Django SocialApp..." -ForegroundColor Yellow

Push-Location backend
$env:GOOGLE_CLIENT_ID = $clientId
$env:GOOGLE_SECRET = $clientSecretPlain

try {
    $venvScript = "env\Scripts\activate.ps1"
    if (Test-Path $venvScript) {
        & $venvScript
    } else {
        Write-Host "Virtual environment not found at env/Scripts/activate.ps1" -ForegroundColor Yellow
        Write-Host "Make sure to activate your virtual environment before running this script" -ForegroundColor Yellow
    }
    
    python scripts/create_socialapp.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Google OAuth SocialApp created successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Start your backend server: python manage.py runserver" -ForegroundColor White
        Write-Host "2. Start your frontend server: cd ../frontend && npm run dev" -ForegroundColor White
        Write-Host "3. Go to http://localhost:5173/register and test 'Sign up with Google'" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "ERROR: Failed to create SocialApp" -ForegroundColor Red
        Write-Host "Make sure your virtual environment is activated and Django is set up correctly" -ForegroundColor Yellow
    }
} finally {
    Pop-Location
}
