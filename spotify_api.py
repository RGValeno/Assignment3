import curl

curl -X POST "https://accounts.spotify.com/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=6bdf722070284ef6b55cda124b59f887&client_secret=67d4caea543742d38f9b065922eff576"
