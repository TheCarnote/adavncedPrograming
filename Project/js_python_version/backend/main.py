# -*- coding: utf-8 -*-
"""
API FastAPI pour le graphe publicitaire
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import shutil
import os
import csv
from graph_manager import graph_manager

# Initialiser FastAPI
app = FastAPI(
    title="API Graphe Publicitaire",
    description="API pour construire, charger et analyser un graphe publicitaire avec K-NN",
    version="1.0.0",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== MODÈLES PYDANTIC ====================

class BuildGraphRequest(BaseModel):
    k: int = 10

class SearchRequest(BaseModel):
    ad_id: str
    method: str = 'hybrid'


# ==================== ENDPOINTS ====================

@app.get("/")
def read_root():
    return {
        "message": "API Graphe Publicitaire - Bienvenue !",
        "endpoints": {
            "POST /upload-files": "Uploader les fichiers CSV",
            "POST /build-graph": "Construire un nouveau graphe",
            "GET /graph-data": "Obtenir les données du graphe",
            "POST /search": "Rechercher dans le rayon D d'un ad",
            "POST /search-all": "Rechercher pour toutes les ads et générer un CSV"  # AJOUTÉ
        }
    }


@app.post("/upload-files")
async def upload_files(
    nodes_file: UploadFile = File(...),
    ads_file: UploadFile = File(...)
):
    """
    Upload les fichiers CSV (nodes et ads)
    """
    try:
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Vérifier les extensions
        if not nodes_file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Le fichier nodes doit être un CSV")
        if not ads_file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Le fichier ads doit être un CSV")
        
        # Sauvegarder le fichier nodes
        nodes_path = os.path.join(backend_dir, "adsSim_data_nodes.csv")
        with open(nodes_path, "wb") as buffer:
            shutil.copyfileobj(nodes_file.file, buffer)
        
        # Sauvegarder le fichier ads
        ads_path = os.path.join(backend_dir, "queries_structured.csv")
        with open(ads_path, "wb") as buffer:
            shutil.copyfileobj(ads_file.file, buffer)
        
        print(f"\n{'='*60}")
        print(f"📁 FICHIERS UPLOADÉS")
        print(f"{'='*60}")
        print(f"✅ Nodes: {nodes_file.filename} → adsSim_data_nodes.csv")
        print(f"✅ Ads: {ads_file.filename} → queries_structured.csv")
        print(f"{'='*60}\n")
        
        return {
            "message": "Fichiers uploadés avec succès",
            "nodes_file": nodes_file.filename,
            "ads_file": ads_file.filename,
            "nodes_path": "adsSim_data_nodes.csv",
            "ads_path": "queries_structured.csv"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/build-graph")
def build_graph(request: BuildGraphRequest):
    """
    Construit un nouveau graphe avec K-NN
    """
    try:
        stats = graph_manager.build_new_graph(k=request.k)
        return {
            "message": f"Graphe construit avec succès (K={request.k})",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/graph-data")
def get_graph_data(
    feature_x: int = 0,
    feature_y: int = 1,
    feature_z: int = 2
):
    """
    Retourne les données du graphe pour la visualisation 3D
    """
    try:
        data = graph_manager.get_graph_data((feature_x, feature_y, feature_z))
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
def search_in_radius(request: SearchRequest):
    """
    Recherche les nœuds dans le rayon D d'un ad.
    Le rayon D est automatiquement récupéré depuis les propriétés de l'ad.
    """
    try:
        start_time = time.time()
        
        # Récupérer le rayon D depuis le graphe
        if graph_manager.graph is None:
            raise HTTPException(status_code=400, detail="Aucun graphe chargé")
        
        if request.ad_id not in graph_manager.graph:
            raise HTTPException(status_code=404, detail=f"Ad {request.ad_id} introuvable")
        
        ad_data = graph_manager.graph.nodes[request.ad_id]
        radius_D = ad_data.get('radius_D')
        
        if radius_D is None:
            raise HTTPException(status_code=400, detail=f"Rayon D non défini pour {request.ad_id}")
        
        print(f"🔍 RECHERCHE DANS LE RAYON D")
        print(f"Ad: {request.ad_id}")
        print(f"Rayon D: {radius_D:.6f}")
        print(f"Méthode: {request.method}")
        
        # Effectuer la recherche avec le rayon D
        nodes_found_with_dist = graph_manager.search_in_radius(
            request.ad_id,
            radius_D,
            request.method
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ {len(nodes_found_with_dist)} nœuds trouvés en {elapsed_time:.3f}s")
        print(f"{'='*60}\n")
        
        # Formater les résultats pour l'API
        nodes_found = [{"node_id": node_id, "distance": distance} 
                      for node_id, distance in nodes_found_with_dist]
        
        return {
            "ad_id": request.ad_id,
            "radius_D": radius_D,
            "method_used": request.method,
            "nodes_found": nodes_found,  # CHANGÉ : Format avec distance
            "total_nodes": len(nodes_found_with_dist),
            "elapsed_time": elapsed_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search-all")
def search_all(method: str = 'hybrid'):
    """
    Effectue une recherche dans le rayon D pour TOUTES les ads
    et génère un fichier CSV avec les résultats.
    """
    try:
        start_time = time.time()
        
        if graph_manager.graph is None:
            raise HTTPException(status_code=400, detail="Aucun graphe chargé")
        
        print(f"🔍 RECHERCHE GLOBALE POUR TOUTES LES ADS")
        print(f"Méthode: {method}")
        
        # Récupérer toutes les ads
        ad_nodes = [node_id for node_id, node_data in graph_manager.graph.nodes(data=True) 
                   if node_data.get('node_type') == 'ad']
        
        print(f"📊 {len(ad_nodes)} ads à traiter...")
        
        # Préparer les résultats
        results = []
        total_nodes_found = 0
        
        for i, ad_id in enumerate(ad_nodes, 1):
            print(f"  [{i}/{len(ad_nodes)}] Processing {ad_id}...", end=' ')
            
            ad_data = graph_manager.graph.nodes[ad_id]
            radius_D = ad_data.get('radius_D')
            
            if radius_D is None:
                print("❌ Rayon D manquant")
                continue
            
            # Effectuer la recherche
            nodes_found = graph_manager.search_in_radius(ad_id, radius_D, method)
            
            # MODIFIÉ : Gestion flexible du format de retour
            nodes_list = []
            for node_result in nodes_found:
                if isinstance(node_result, tuple):
                    # Si c'est un tuple (node_id, distance) ou (node_id, distance, autre...)
                    node_id = node_result[0]
                    distance = node_result[1]
                    nodes_list.append(f"{node_id}:{distance:.6f}")
                elif isinstance(node_result, str):
                    # Si c'est juste l'ID du node (pas de distance)
                    nodes_list.append(f"{node_result}:0.000000")
                else:
                    # Format inconnu, convertir en string
                    nodes_list.append(f"{str(node_result)}:0.000000")
            
            nodes_list_str = ";".join(nodes_list)
            
            results.append({
                'ad_id': ad_id,
                'distance_D': radius_D,
                'nombre_nodes': len(nodes_found),
                'liste_nodes': nodes_list_str
            })
            
            total_nodes_found += len(nodes_found)
            print(f"✅ {len(nodes_found)} nodes")
        
        # Générer le fichier CSV
        csv_filename = f"search_all_results_{method}.csv"
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_filename)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ad_id', 'distance_D', 'nombre_nodes', 'liste_nodes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ Recherche terminée !")
        print(f"📊 Statistiques globales :")
        print(f"   - Ads traitées: {len(results)}")
        print(f"   - Nodes trouvés (total): {total_nodes_found}")
        print(f"   - Temps total: {elapsed_time:.3f}s")
        print(f"   - Temps moyen par ad: {elapsed_time/len(ad_nodes):.3f}s")
        print(f"📁 Fichier généré: {csv_filename}")
        # print(f"{'='*60}\n")
        
        return {
            "message": "Recherche globale terminée",
            "method_used": method,
            "ads_processed": len(results),
            "total_nodes_found": total_nodes_found,
            "elapsed_time": elapsed_time,
            "average_time_per_ad": elapsed_time / len(ad_nodes) if ad_nodes else 0,
            "csv_file": csv_filename,
            "csv_path": csv_path,
            "results_preview": results  # Aperçu des 5 premiers résultats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur dans search_all: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DE L'API GRAPHE PUBLICITAIRE")
    print("="*60)
    print("📍 URL: http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    print("📘 ReDoc: http://localhost:8000/redoc")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)