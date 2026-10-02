#!/bin/bash

# Prüfen, ob eine Nachricht übergeben wurde, sonst Standard-Nachricht nutzen
if [ -z "$1" ]; then
    MSG="Auto-Update: Noten aktualisiert"
else
    MSG="$1"
fi

echo "📦 Füge Änderungen hinzu..."
git add .

echo "📝 Erstelle Commit mit Nachricht: '$MSG'..."
git commit -m "$MSG"

echo "🚀 Lade zu GitHub hoch..."
git push

echo "✅ Fertig! Alles ist auf GitHub."
