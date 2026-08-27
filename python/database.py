import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Récupération des variables d'environnement (avec valeurs par défaut pour votre Mac local)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "data_quality_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgrespassword")

# Construction dynamique de l'URL (compatible Mac local ET Docker Compose)
DATABASE_URL = os.getenv(
    "Base_URL", 
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)
Session_local = sessionmaker(bind=engine)

def execute_quality_check(query_str: str, check_name: str):
    """Exécute une requête SQL de contrôle et renvoie le bilan des anomalies"""
    with engine.connect() as connection:
        result = connection.execute(text(query_str))
        anomalies = [dict(row) for row in result.mappings()]
        status = "FAIL" if len(anomalies) > 0 else "PASS"

        return {
            "check_name": check_name,
            "status": status,
            "anomalies_count": len(anomalies),
            "details": anomalies
        }

if __name__ == "__main__":
    test_sql = """
        SELECT client_id, nom, prenom, email
        FROM clients
        WHERE email IS NULL OR email NOT LIKE '%@%.%';
    """
    
    res = execute_quality_check(test_sql, "Emails manquants ou invalides")
    print(f"[*] Contrôle : {res['check_name']}")
    print(f"[*] Statut : {res['status']}")
    print(f"[*] Anomalies trouvées : {res['anomalies_count']}")
    print(f"[*] Détails : {res['details']}")