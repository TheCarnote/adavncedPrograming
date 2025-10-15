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
            "POST /search": "Rechercher dans le rayon D d'un ad"
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
        
        
        print(f"📁 FICHIERS UPLOADÉS")
        
        print(f"✅ Nodes: {nodes_file.filename} → adsSim_data_nodes.csv")
        print(f"✅ Ads: {ads_file.filename} → queries_structured.csv")
      
        
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
        nodes_found = graph_manager.search_in_radius(
            request.ad_id,
            radius_D,
            request.method
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ {len(nodes_found)} nœuds trouvés en {elapsed_time:.3f}s")
      
        
        return {
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