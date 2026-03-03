# URL de ton API locale
$uri = "http://localhost:5000/api/generate"

# Corps de la requête
$body = @{
    prompt = "Propose une description premium pour une Toyota Corolla en location"
    temperature = 0.4
} | ConvertTo-Json -Depth 5

# Appel POST
$response = Invoke-RestMethod `
    -Uri $uri `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Affichage de la réponse
$response.response | Out-File -FilePath ".\gemini-output.txt" -Encoding utf8
Write-Host "✅ Réponse écrite dans gemini-output.txt"