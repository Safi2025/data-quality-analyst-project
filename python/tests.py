import pandas as pd
from database import execute_quality_check

#Liste des contrôles à exécuter (Nom du test, Requête sql)
Quality_tests = [
    {
        "name" : "1. Complétude - EMails clients ",
        "query" : "SELECT client_id, nom, prenom, email FROM clients WHERE email IS NULL OR email NOT LIKE '%@%.%'; "
    },
    {
        "name": "2. Unicité - Doublons client_id",
        "query": "SELECT client_id, COUNT(*) AS occurences FROM clients GROUP BY client_id HAVING COUNT(*) > 1;"
    },
    {
        "name": "3. Intégrité - Contrats orphelins",
        "query": "SELECT c.contrat_id, c.client_id FROM contrats c LEFT JOIN clients cl ON c.client_id = cl.client_id WHERE cl.client_id IS NULL;"
    },
    {
        "name": "4. Validité - Primes négatives",
        "query": "SELECT contrat_id, prime_annuelle FROM contrats WHERE prime_annuelle <= 0;"
    },
    {
        "name": "5. Cohérence - Dates de contrat invalides",
        "query": "SELECT contrat_id, date_debut, date_fin FROM contrats WHERE date_fin < date_debut;"
    },
    {
        "name": "6. Métier - Paiements supérieurs à la prime",
        "query": "SELECT p.paiement_id, p.contrat_id, p.montant AS paiement, c.prime_annuelle FROM paiements p JOIN contrats c ON p.contrat_id = c.contrat_id WHERE p.montant > c.prime_annuelle;"
    }
]

def run_all_tests():
    summary = []
    print("\n" + "="*60)
    print(" LANCEUR AUTOMATISÉ DE CONTRÔLES DATA QUALITY ")
    print("="*60)

    for test in Quality_tests:
        res = execute_quality_check(test["query"], test["name"])
        summary.append({
            "Test Name": res["check_name"],
            "Status": res["status"],
            "Anomalies Count": res["anomalies_count"]
        })
        
        # Affichage console
        symbol = " " if res["status"] == "FAIL" else " "
        print(f"{symbol} [{res['status']}] {res['check_name']} -> {res['anomalies_count']} anomalie(s)")

    # Sauvegarde du rapport synthétique dans le dossier reports/
    df_report = pd.DataFrame(summary)
    df_report.to_csv("reports/quality_report.csv", index=False)
    print("\n[+] Rapport exporté avec succès dans 'reports/quality_report.csv'")

if __name__ == "__main__":
    run_all_tests()
