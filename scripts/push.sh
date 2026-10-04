#!/bin/bash

# Prüfen, ob eine Nachricht übergeben wurde, sonst Standard-Nachricht nutzen
echo "Enter commit message: "
read message

MSG="$message"

echo "📦 Füge Änderungen hinzu..."
git add .

echo "📝 Erstelle Commit mit Nachricht: '$MSG'..."
git commit -m "$MSG"

echo "🚀 Lade zu GitHub hoch..."
git push

echo "✅ Fertig! Alles ist auf GitHub."
