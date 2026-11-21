from nlp.nlp_service import classify_report_fr

reports = [
    "L'étudiant est arrivé en retard mais a respecté les consignes.",
    "L'étudiant a insulté le professeur et perturbé le cours.",
    "Une agression physique a eu lieu entre deux étudiants."
]

for r in reports:
    print(classify_report_fr(r))
