# conseil-disciplinaire-ml
AI-powered school disciplinary decision support system using Machine Learning, NLP, BERT and Flask.

## Comparaison de la gravité

La version de référence vient de l’autre groupe. Elle utilise le modèle de sentiment `nlptown/bert-base-multilingual-uncased-sentiment` et des listes de mots-clés pour proposer un niveau. La page Flask compare cette méthode à un pipeline TF-IDF sur les mots et les groupes de deux mots, suivi d’une régression logistique.

### Démarrer sous Windows

Depuis le dossier contenant `app.py`, avec Python 3.13 et l’environnement `.venv` du projet, exécuter dans PowerShell :

```powershell
if (-not (Test-Path .\.venv\Scripts\python.exe)) { python -m venv .venv }
$python = '.\.venv\Scripts\python.exe'
& $python -m pip install -r requirements.txt
$env:HF_HOME = Join-Path (Get-Location) '.cache\huggingface'
& $python -m ml.train
& $python -m flask --app app run --host 127.0.0.1 --port 5001
```

Ouvrir [la page de comparaison](http://127.0.0.1:5001/). Le premier appel BERT peut télécharger les poids depuis Hugging Face. L’entraînement enregistre le pipeline dans `artifacts/gravite.joblib`.

Pour recalculer les mesures sur les mêmes rapports de test après entraînement, exécuter `& $python -m ml.evaluate` dans la même session PowerShell. La [grille d’annotation et les résultats](docs/comparaison.md) décrivent le corpus, les mesures et des erreurs observées.

### API

Les deux routes reçoivent un objet JSON avec le champ `report_text`. Les niveaux `1`, `2` et `3` correspondent respectivement à **mineur**, **modéré** et **grave**.

| Méthode | Route | Réponse réussie |
| --- | --- | --- |
| BERT + mots-clés | `POST /api/analyze-report` | `report_text`, `disciplinary_level`, `details` (`stars`, `confidence`, `reason`) |
| TF-IDF + régression logistique | `POST /api/analyze-report-ml` | `report_text`, `disciplinary_level`, `level_label`, `probabilities` (`mineur`, `modéré`, `grave`, sur une échelle de 0 à 1) |

La route ML renvoie une erreur JSON avec le statut `400` pour une saisie vide ou invalide et `503` si le modèle entraîné est absent.
