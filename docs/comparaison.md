# Évaluation de la gravité sur des rapports fictifs

Les 96 rapports du [dataset](../data/rapports_fictifs.csv) ont été rédigés en français pour cette comparaison. Chaque ligne décrit un scénario et contient deux formulations du même incident. Le champ `ensemble` affecte la ligne entière à l’entraînement ou au test. Le pipeline est ajusté sur 72 rapports de 36 scénarios. Les deux méthodes sont évaluées sur les mêmes 24 rapports de 12 autres scénarios, avec 8 rapports par classe.

## Grille d’annotation

| Niveau | Critères | Exemple |
| --- | --- | --- |
| 1 · Mineur | Écart isolé, effet bref, sans mise en danger ni atteinte à une personne. Le cours reprend après un rappel ou une correction immédiate. | Entrer dans la mauvaise salle et rejoindre son groupe sur indication. |
| 2 · Modéré | Écart répété malgré les rappels ou atteinte caractérisée au déroulement du cours, à l’intégrité d’une épreuve, à la dignité d’un camarade ou à ses biens. Les faits décrits sont sans danger physique sérieux. | Échanger des réponses pendant une épreuve ou endommager volontairement un cartable. |
| 3 · Grave | Violence physique avec blessure ou risque sérieux, menace crédible de violence ou mise en danger immédiate. | Une poussée volontaire provoque une chute dans un escalier et nécessite l’intervention des secours. |

L’annotation retient le niveau le plus élevé justifié par les faits décrits. Une mention niée, comme « aucun coup », ne compte pas comme un fait survenu. La répétition malgré les rappels ou les conséquences observées distinguent des situations proches, par exemple un retard isolé et des retards qui perturbent régulièrement le cours.

## Résultats obtenus

| Méthode | F1-macro | Rapports correctement classés |
| --- | ---: | ---: |
| BERT + mots-clés | 0,284 | 9/24 |
| TF-IDF + régression logistique | 0,874 | 21/24 |

Le F1-macro est la moyenne non pondérée des F1 des trois classes. Dans les matrices, les lignes correspondent à la gravité annotée et les colonnes à la gravité proposée.

### BERT + mots-clés

| Annotation \ prédiction | Mineur | Modéré | Grave |
| --- | ---: | ---: | ---: |
| Mineur | 2 | 1 | 5 |
| Modéré | 1 | 0 | 7 |
| Grave | 1 | 0 | 7 |

### TF-IDF + régression logistique

| Annotation \ prédiction | Mineur | Modéré | Grave |
| --- | ---: | ---: | ---: |
| Mineur | 6 | 1 | 1 |
| Modéré | 0 | 7 | 1 |
| Grave | 0 | 0 | 8 |

### Exemples d’erreurs

| Extrait du rapport | Annotation | BERT + mots-clés | TF-IDF + régression logistique |
| --- | --- | --- | --- |
| « Il n’a porté aucun coup et a repris le cours au rappel. » | Mineur | Grave | Mineur |
| « La victime, qui manquait d’air, a été prise en charge par les secours. » | Grave | Mineur | Grave |
| « Un élève a entrouvert la fenêtre sans demander et l’a refermée dès la première remarque. » | Mineur | Grave | Grave |
| « Le sac d’un camarade a été volontairement rendu inutilisable pendant la pause. Personne n’a été blessé. » | Modéré | Grave | Grave |

Le mot « coup » entraîne la classe grave pour BERT + mots-clés même quand le rapport nie le geste. Les deux formulations du scénario de la fenêtre ouverte sont mal classées par le modèle TF-IDF. Ces mesures décrivent un corpus fictif équilibré de petite taille. La performance sur des rapports réels et la calibration des probabilités restent à évaluer.

L’évaluation a utilisé les versions de `requirements.txt` et la révision BERT `8f6f4e3a8f70be4b65d3a4a8762b6d781cda240d`. La commande `python -m ml.evaluate` fournit le détail des erreurs pour les deux méthodes après l’entraînement.
