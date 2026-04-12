# Handoff — B1-K21

**Von Phase:** ausarbeitung → **Zu Phase:** lektorat-fix  
**Erstellt:** 2026-04-12  
**Status beim Handoff:** lektorat

## Modell-Empfehlung
```
claude --model sonnet
```
(oder `claude --model haiku` für Mikro-Fixes)

## Aufruf für nächste Session
```
/lektorat-fix B1-K21
```

## Kontext
- **Datei:** buch/kapitel/B1-K21-alphina.md (3827 W)
- **POV:** Alphina, 23. Blütenmond 551
- **Phase:** Lektorat-Fixes (Autor-getrieben, kleine Edits)
- **Umfang:** Kein neuer Stil-Check, kein Council. Nur was der Autor anfasst.

## Council + Autorin-Durchgang abgeschlossen
- Stil-Check: Findings eingearbeitet (Wut-Streichung, Hypothetische -5, Aphorismen -9)
- Stilkritiker: ✓ bestanden
- Dark-Romance-Leserin: ✓ bestanden
- Romantasy-Leserin: ✓ bestanden
- Autorin-Durchgang (Opus): 9 Streichungen + 11 Umformulierungen eingearbeitet

## Anweisungen
- Edit-Tool bevorzugt vor Write-Tool
- Kein ungefragtes Umformulieren
- Bei größeren Wünschen: Hinweis auf Rückstufung zu `/ausarbeitung`
- Status `final` nur auf explizite Autor-Freigabe hin

---

**Nach Fertigstellung:** `git add buch/kapitel/B1-K21-alphina.md` → `commit` → `push` → `ssh-deploy`
