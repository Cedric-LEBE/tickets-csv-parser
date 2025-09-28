import csv
import json
import os
from datetime import datetime

# Configuration
INPUT_FOLDER = "/Users/chiefpriest/Documents/UTT_Courses/TP_PYTHON_UTT_2025/Data"
OUTPUT_FOLDER = "/Users/chiefpriest/Documents/UTT_Courses/TP_PYTHON_UTT_2025/Data/json_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_csv_files():
    """Version simplifiée pour un seul fichier JSON"""
    all_tickets = []
    
    # Vérifier que le dossier d'entrée existe
    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ Erreur: Le dossier {INPUT_FOLDER} n'existe pas")
        return
    
    # Parcourir tous les fichiers CSV
    for filename in os.listdir(INPUT_FOLDER):
        if not filename.lower().endswith('.csv'):
            continue
            
        csv_path = os.path.join(INPUT_FOLDER, filename)
        print(f"📖 Traitement du fichier: {filename}")
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                
                for row_num, row in enumerate(reader, 1):
                    if len(row) < 5:
                        continue
                    
                    # Vérifier que les colonnes obligatoires ne sont pas vides
                    if not row[0].strip() or not row[1].strip() or not row[2].strip() or not row[3].strip():
                        continue
                    
                    try:
                        # Créer le ticket
                        ticket = {
                            "magasin": row[1].strip(),
                            "timestamp": f"{row[0].strip()} {row[3].strip()}",
                            "client": int(row[4].strip()) if row[4].strip() and row[4].strip().isdigit() else None,
                            "id ticket": int(row[2].strip()),
                            "articles": []
                        }
                        
                        # Ajouter les articles (groupes de 4 colonnes)
                        for i in range(5, len(row), 4):
                            if i + 3 < len(row) and row[i].strip():
                                try:
                                    # Nettoyer et convertir les valeurs
                                    produit = row[i].strip()
                                    categorie = row[i+1].strip() if i+1 < len(row) else ""
                                    prix_str = row[i+2].replace(',', '.') if i+2 < len(row) else "0"
                                    qte_str = row[i+3] if i+3 < len(row) else "0"
                                    
                                    article = {
                                        "produit": produit,
                                        "categorie": categorie,
                                        "prix_u": float(prix_str),
                                        "qte": int(float(qte_str))
                                    }
                                    ticket["articles"].append(article)
                                except (ValueError, IndexError) as e:
                                    # Continuer avec l'article suivant en cas d'erreur
                                    continue
                        
                        # Uniquement si au moins un article valide
                        if ticket["articles"]:
                            all_tickets.append(ticket)
                            
                    except (ValueError, IndexError) as e:
                        # Passer à la ligne suivante en cas d'erreur sur un ticket
                        continue
                        
        except Exception as e:
            print(f"❌ Erreur avec le fichier {filename}: {e}")
            continue
    
    if not all_tickets:
        print("❌ Aucun ticket valide trouvé dans les fichiers CSV")
        return
    
    # Écrire le fichier JSON unique
    output_path = os.path.join(OUTPUT_FOLDER, "tickets_consolidated.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_tickets, json_file, ensure_ascii=False, indent=2)
        
        # Statistiques
        total_articles = sum(len(ticket["articles"]) for ticket in all_tickets)
        magasins = set(ticket["magasin"] for ticket in all_tickets)
        
        print(f"✅ Fichier unique généré: {output_path}")
        print(f"📊 Statistiques:")
        print(f"   • Tickets traités: {len(all_tickets)}")
        print(f"   • Magasins distincts: {len(magasins)}")
        print(f"   • Total articles: {total_articles}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier JSON: {e}")

if __name__ == "__main__":
    process_csv_files()