# Nächster Milestone nach Phase 2 (konservative Empfehlung)

## Kurze Zusammenfassung

Phase 2 ist laut Abschlussanalyse erreicht und sollte nicht durch große Umbauten wieder geöffnet werden. Der nächste sinnvolle Milestone ist daher **"Phase 3: Stabilisierung & Reifung des bestehenden Vertical Slice"**: Fokus auf **geringes Risiko, hohe Produktwirkung** durch moderate Matching-Verbesserung, punktuelle Explainability-Schärfung und kleine Knowledge-Base-Reifung – ohne API-Neudesign und ohne Architektur-Großumbau.

---

## Priorisierte Empfehlung

## 1) Höchster Nutzen bei geringem Risiko: Demo-/Produktreife + Explainability schärfen

**Empfehlung:** Als erstes den bestehenden `POST /qualify`-Flow robuster und klarer für reale Demo-/Nutzerfälle machen.

Warum priorisiert:
- Compass fordert Explainability und inkrementelle Weiterentwicklung, nicht Richtungswechsel.
- Die Abschlussanalyse bestätigt: Kernarchitektur ist da; offene Punkte sind eher Reifegrad/Kommunikation.
- Diese Richtung verändert weder Datenmodell noch Pipeline-Grundstruktur und hat damit geringes Regressionsrisiko.

Konkreter Fokus:
- Erklärtexte konsistenter machen (knapp, verständlich, stabil).
- Response-Klarheit verbessern (z. B. wann Ergebnis vorläufig ist, wie Confidence zu lesen ist).
- Kuratierte Demo-/Contract-Fälle weiter als Guardrail nutzen.

## 2) Zweite Priorität: kleines bis mittleres KB-Tuning (zielgerichtet)

**Empfehlung:** Kuratierte Ergänzung häufiger Aktivitäten/Aliasse dort, wo aktuelle False-Negatives sichtbar sind.

Warum:
- Compass ist KB-first.
- KB-Reifung ist additive Verbesserung im bestehenden Modell, ohne große Architekturfolgen.
- Direkter Qualitätsgewinn für Matching/Qualification bei sehr kontrolliertem Risiko.

Grenzen:
- Keine breite Schemaänderung.
- Keine große Re-Migration der Datenhaltung.

## 3) Dritte Priorität: Fuzzy Matching nur als eng begrenztes Sicherheitsnetz

**Empfehlung:** Falls nötig, sehr konservatives Fuzzy-Matching als nachgelagerter Fallback hinter Exact/Alias einführen (mit hohen Schwellwerten und klarer Kennzeichnung).

Warum nur Platz 3:
- Höheres Risiko für Fehlmatches als reine Explainability-/KB-Arbeit.
- Noch nicht nötig als großer Umbau, solange viele Lücken über Aliasse/KB geschlossen werden können.

Leitplanken:
- Kein ML/AI-Modell.
- Keine aggressive Heuristik.
- Immer explizit im Response markieren, wenn Fuzzy-Fallback gegriffen hat.

## 4) Lokale Architekturverbesserungen nur dort, wo der Slice es braucht

**Empfehlung:** Nur kleine, lokale Refactorings für Wartbarkeit/Lesbarkeit (z. B. Hilfsfunktionen, klarere Adapter-Grenzen), keine Reorganisation der Gesamtstruktur.

Warum:
- Abschlussanalyse bewertet die aktuelle Architektur bereits als zielkonform für Phase 2.
- Zusätzliche große Strukturarbeit würde aktuell eher Risiko als Nutzen erzeugen.

---

## Was jetzt noch nicht dran ist

- Keine große Reorganisation der Modulstruktur.
- Keine umfangreiche API-Neugestaltung oder Contract-Brüche.
- Keine Vorziehung von ML/AI-Ansätzen.
- Keine breit angelegte Datenmodell-/Schemaumbauten.
- Kein "Phase 2 nochmal von vorne" durch neue Großinitiativen.

Diese Themen bleiben bewusst nachgelagert, bis belastbare Produktsignale zeigen, dass der bestehende konservative Pfad nicht mehr ausreicht.

---

## Vorschlag für die nächsten 1–3 realistischen Slices

## Slice A (kurzfristig, niedriges Risiko): Response-Klarheit & Demo-Härtung

Ziel:
- Explainability und Ergebnislesbarkeit spürbar verbessern, ohne Logikbruch.

Beispiele:
- Einheitliche, kurze Erklärbausteine je Hauptfall (`match`, `qualification`, `personal_status`).
- Präzisere Hinweise bei grenzwertigen Fällen (z. B. warum nicht "active").
- Ergänzende Contract-Tests auf Textkonsistenz/Schlüsselfelder.

Erfolgskriterium:
- Keine Regression in bestehender kuratierter Suite; nachvollziehbarere Antworten in denselben Fällen.

## Slice B (kurzfristig bis mittelfristig, niedrig-mittel): KB-Mikro-Reifung

Ziel:
- Trefferquote mit kuratierten, häufigen Ergänzungen verbessern.

Beispiele:
- Kleine Alias-/Synonym-Erweiterung für häufige Eingaben.
- Ergänzung fehlender Attribute bei bereits bekannten Aktivitäten.
- Testfälle für neue Aliaspfade und bekannte False-Negatives.

Erfolgskriterium:
- Messbar weniger `unknown_activity` bei bekannten Demo-Begriffen, ohne Contract-Änderung.

## Slice C (optional, erst nach A+B): konservativer Fuzzy-Fallback

Ziel:
- Robustheit gegen Tippfehler/nahe Schreibweisen erhöhen.

Beispiele:
- Fuzzy nur als letzter Schritt nach Exact/Alias.
- Hoher Confidence-Threshold + klares `match_type` für Fuzzy.
- Negativtests gegen offensichtliche Fehlmatches.

Erfolgskriterium:
- Mehr sinnvolle Treffer bei Tippfehlern, ohne Anstieg klarer Fehlzuordnungen.

---

## Milestone-Formulierung (empfohlen)

**Phase 3: "Stabilisierung & Reifung des produktiven Slice"**

- Schwerpunkt: Produktklarheit, kontrollierte Trefferverbesserung, konservative Robustheit.
- Vorgehen: strikt inkrementell, testgetrieben, ohne strukturellen Großumbau.
- Abgrenzung: Architektur bleibt im Phase-2-Rahmen; nur lokal dort schärfen, wo direkter Nutzwert entsteht.
