# Automated Git Push Script
param (
    [string]$message = "Update project files and models"
)

Write-Host ">>> Staging files..." -ForegroundColor Cyan
git add .

Write-Host ">>> Committing with message: '$message'..." -ForegroundColor Cyan
git commit -m "$message"

Write-Host ">>> Pushing to GitHub..." -ForegroundColor Cyan
git push

Write-Host ">>> Successfully pushed to GitHub!" -ForegroundColor Green
