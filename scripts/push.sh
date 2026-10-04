#!/bin/bash

echo -n "Enter commit message: "
read message

# Fallback, falls keine Nachricht eingegeben wurde
if [ -z "$message" ]; then
  message="Automated update"
fi

echo "📦 Füge Änderungen hinzu..."
git add . || { echo "❌ Fehler bei git add"; exit 1; }

echo "📝 Erstelle Commit mit Nachricht: '$message'..."
git commit -m "$message" || { echo "❌ Fehler bei git commit (Keine Änderungen?)"; exit 1; }

echo "🚀 Lade zu GitHub hoch..."
git push || { echo "❌ Fehler bei git push"; exit 1; }

echo "✅ Fertig! Alles ist auf GitHub."
