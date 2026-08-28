import os
import subprocess
import sys

def run_pipeline():
    print("=== 1. Exécution des tests de Qualité de Données ===")
    res_tests = subprocess.run([sys.executable, "python/tests.py"])
    if res_tests.returncode != 0:
        print("Échec lors des tests de qualité.")
        sys.exit(1)

    print("\n=== 2. Calcul et Génération des Business Analytics ===")
    res_analytics = subprocess.run([sys.executable, "python/business_analytics.py"])
    if res_analytics.returncode != 0:
        print(" Échec lors du calcul des KPIs business.")
        sys.exit(1)

    print("\n Pipeline exécuté avec succès. Tous les rapports sont générés dans /reports.")

if __name__ == "__main__":
    run_pipeline()