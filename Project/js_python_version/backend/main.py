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
import uvicorn

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
        
        nodes_found = graph_manager.search_in_radius(
            request.node_id,
            request.ad_id,
            request.method
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ {len(nodes_found)} nœuds trouvés en {elapsed_time:.3f}s")
        
        return {
            "node_id": request.node_id,
            "ad_id": request.ad_id,
            "radius_D": radius_D,
            "method_used": request.method,
            "nodes_found": nodes_found,
            "total_nodes": len(nodes_found),
            "elapsed_time": elapsed_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur dans /search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)