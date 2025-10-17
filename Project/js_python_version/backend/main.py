# -*- coding: utf-8 -*-
"""
API FastAPI pour le système de graphe publicitaire
"""

import os
import time
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # AJOUTÉ
from pydantic import BaseModel
from typing import List, Optional
import time
import shutil
import os
import csv
from graph_manager import graph_manager

app = FastAPI(title="Advertising Graph API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],  # Port par défaut de Vite (frontend)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

script_dir = os.path.dirname(os.path.abspath(__file__))

class SearchRequest(BaseModel):
    node_id: str
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
    Upload des fichiers CSV personnalisés
    """
    try:
        # Sauvegarder nodes
        nodes_path = os.path.join(script_dir, nodes_file.filename)
        with open(nodes_path, "wb") as f:
            f.write(await nodes_file.read())
        
        # Sauvegarder ads
        ads_path = os.path.join(script_dir, ads_file.filename)
        with open(ads_path, "wb") as f:
            f.write(await ads_file.read())
        
        # Mettre à jour les chemins dans graph_manager (priorité aux uploadés)
        graph_manager.nodes_file = nodes_path
        graph_manager.ads_file = ads_path
        
        print(f"✅ Fichiers uploadés : {nodes_file.filename}, {ads_file.filename}")
        
        return {"message": f"Fichiers uploadés : {nodes_file.filename}, {ads_file.filename}."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur upload : {str(e)}")

@app.post("/build-graph")
def build_graph(k: int = 10):
    """
    Construit le graphe depuis les fichiers (uploadés en priorité, sinon défauts).
    """
    try:
        result = graph_manager.build_new_graph(k=k)
        print(f"DEBUG: Après build, ads_data = {len(graph_manager.ads_data) if graph_manager.ads_data else 0} ads")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load-graph")
def load_graph():
    """
    Charge un graphe sauvegardé.
    """
    try:
        result = graph_manager.load_existing_graph()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph-stats")
def get_graph_stats():
    """
    Retourne les statistiques du graphe chargé.
    """
    try:
        return graph_manager._get_graph_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph-data")
def get_graph_data(fx: int = 0, fy: int = 1, fz: int = 2):
    """
    Retourne les données du graphe pour visualisation 3D.
    """
    try:
        return graph_manager.get_graph_data((fx, fy, fz))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Dans main.py, ajoutez après les autres endpoints

@app.get("/ads-data")
def get_ads_data():
    """
    Retourne les données des ads (Y_vector, D).
    """
    try:
        if graph_manager.ads_data is None:
            graph_manager.load_ads_data()
        
        # Si toujours None ou vide, retourner un objet vide au lieu d'erreur
        if graph_manager.ads_data is None or not graph_manager.ads_data:
            print("⚠️ Aucune donnée ads chargée, retour d'objet vide")
            return {}
        
        return graph_manager.ads_data
    except Exception as e:
        print(f"❌ Erreur dans /ads-data: {e}")
        # Retourner un objet vide au lieu de 500
        return {}



@app.post("/search")
def search_in_radius(request: SearchRequest):
    """
    Recherche les nœuds dans le rayon D d'un ad, en partant d'un node régulier.
    """
    try:
        start_time = time.time()
        
        print(f"🔍 RECHERCHE DANS LE RAYON D")
        print(f"Node de départ: {request.node_id}")
        print(f"Ad: {request.ad_id}")
        print(f"Méthode: {request.method}")
        
        if graph_manager.graph is None:
            raise HTTPException(status_code=400, detail="Aucun graphe chargé. Utilisez /build-graph ou /load-graph d'abord.")
        
        if graph_manager.ads_data is None:
            graph_manager.load_ads_data()
        
        if not graph_manager.ads_data:
            raise HTTPException(status_code=400, detail="Aucune ad chargée. Vérifiez le fichier CSV des ads.")
        
        if request.ad_id not in graph_manager.ads_data:
            raise HTTPException(status_code=404, detail=f"Ad {request.ad_id} introuvable.")
        
        radius_D = graph_manager.ads_data[request.ad_id]['D']
        print(f"Rayon D: {radius_D:.6f}")
        
        # Effectuer la recherche avec le rayon D
        nodes_found_with_dist = graph_manager.search_in_radius(
            request.ad_id,
            request.method
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ {len(nodes_found_with_dist)} nœuds trouvés en {elapsed_time:.3f}s")
        print(f"{'='*60}\n")
        
        # Formater les résultats pour l'API
        nodes_found = [{"node_id": node_id, "distance": distance} 
                      for node_id, distance in nodes_found_with_dist]
        
        return {
            "node_id": request.node_id,
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
        print(f"❌ Erreur dans /search: {e}")
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
        print(f"{'='*60}\n")
        
        return {
            "message": "Recherche globale terminée",
            "method_used": method,
            "ads_processed": len(results),
            "total_nodes_found": total_nodes_found,
            "elapsed_time": elapsed_time,
            "average_time_per_ad": elapsed_time / len(ad_nodes) if ad_nodes else 0,
            "csv_file": csv_filename,
            "csv_path": csv_path,
            "results_preview": results[:5]  # Aperçu des 5 premiers résultats
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur dans search_all: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)