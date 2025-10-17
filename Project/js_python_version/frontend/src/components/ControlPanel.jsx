import React, { useState, useEffect } from 'react';
import graphAPI from '../api/graphAPI';
import './ControlPanel.css';

const ControlPanel = ({
    stats,
    clearSearch,
    nodesData,
    onUploadFiles,
    onBuildGraph,
    onLoadGraph,
    onSearch,
    onGraphDataChange,
    onLog,
    isLoading
}) => {
    const [k, setK] = useState(10);
    const [searchNodeId, setSearchNodeId] = useState('');
    const [searchAdId, setSearchAdId] = useState('');
    const [searchMethod, setSearchMethod] = useState('hybrid');
    const [adsData, setAdsData] = useState({});
    const [selectedAdYVector, setSelectedAdYVector] = useState(null);

    // États pour l'upload
    const [nodesFile, setNodesFile] = useState(null);
    const [adsFile, setAdsFile] = useState(null);

    const loadAdsData = async () => {
        try {
            const ads = await graphAPI.fetchAdsData();
            setAdsData(ads);
            // onLog('Ads chargées');
        } catch (error) {
            onLog(`Erreur: ${error.message}`);
        }
    };

    // Gestionnaire pour la sélection d'ad : afficher Y_vector
    const handleAdChange = (adId) => {
        setSearchAdId(adId);
        if (adsData[adId]) {
            setSelectedAdYVector(adsData[adId].Y_vector);
        } else {
            setSelectedAdYVector(null);
        }
    };

    // Upload des fichiers (utilise la prop)
    const handleUploadFiles = async () => {
        if (!nodesFile || !adsFile) {
            onLog('Sélectionnez les deux fichiers');
            return;
        }
        try {
            onLog('Upload des fichiers...');
            await onUploadFiles(nodesFile, adsFile);
            await loadAdsData();  // Recharger après upload
            setNodesFile(null);
            setAdsFile(null);
        } catch (error) {
            onLog(`Erreur: ${error.message}`);
        }
    };

    // Construire le graphe (utilise la prop)
    const handleBuildGraph = async () => {
        await onBuildGraph(k);
        await loadAdsData();
        onGraphDataChange();
    };

    // Charger le graphe (utilise la prop)
    const handleLoadGraph = async () => {
        await onLoadGraph();
        await loadAdsData();
        onGraphDataChange();
    };

    // Rechercher (utilise la prop)
    const handleSearch = async () => {
        if (!searchNodeId || !searchAdId) {
            onLog('Sélectionnez un node et un ad');
            return;
        }
        await onSearch(searchNodeId, searchAdId, searchMethod);
    };

    useEffect(() => {
        // Clear search section when nodes data changes
        setSearchNodeId('');
        setSearchAdId('');
        setSelectedAdYVector(null);
    }, [nodesData]);

    useEffect(() => {
        // Clear search section when ads data changes
        setSearchNodeId('');
        setSearchAdId('');
        setSelectedAdYVector(null);
    }, [adsData]);

    return (
        <div className="control-panel">
            <h2>Contrôles</h2>

            {/* Upload de fichiers */}
            <div className="section">
                <h3>Upload Fichiers</h3>
                <label>
                    Fichier Nodes (CSV):
                    <input type="file" accept=".csv" onChange={(e) => setNodesFile(e.target.files[0])} disabled={isLoading} />  {/*AJOUTÉ : disabled={isLoading} */}
                </label>
                <label>
                    Fichier Ads (CSV):
                    <input type="file" accept=".csv" onChange={(e) => setAdsFile(e.target.files[0])} disabled={isLoading} />   {/* AJOUTÉ : disabled={isLoading} */}
                </label>
                <button onClick={handleUploadFiles} disabled={isLoading}>Uploader Fichiers</button>
            </div>

            {/* Build/Load */}
            <div className="section">
                <label>K-NN: <input type="number" value={k} onChange={(e) => setK(e.target.value)} /></label>
                <button onClick={handleBuildGraph} disabled={isLoading}>Construire Graphe</button>
                {/* <button onClick={handleLoadGraph} disabled={isLoading}>Charger Graphe</button> */}
            </div>

            {/* Sélection pour recherche */}
            <div className="section">
                <div style={{ display: 'flex', marginBottom: '10px', }}>
                    <h3 style={{ 'width': 'fit-content', margin: 0 }}>Recherche</h3>
                    <div className='spacer'></div>
                    <button onClick={() => {
                        setSearchNodeId('');
                        setSearchAdId('');
                        setSelectedAdYVector(null);
                        clearSearch();
                    }}>Réinitialiser</button>
                </div>
                <label>
                    Node de départ:
                    <select value={searchNodeId} onChange={(e) => setSearchNodeId(e.target.value)}>
                        <option value="">-- Choisir --</option>
                        {nodesData && nodesData.length > 0 && nodesData.map(node => (
                            <option key={node.id} value={node.id}>{node.id}</option>
                        ))}
                    </select>
                </label>

                <label>
                    Ad:
                    <select value={searchAdId} onChange={(e) => handleAdChange(e.target.value)}>
                        <option value="">-- Choisir --</option>
                        {Object.keys(adsData).map(id => (
                            <option key={id} value={id}>{id}</option>
                        ))}
                    </select>
                </label>

                {/* Affichage du Y_vector de l'ad sélectionné */}
                {selectedAdYVector && (
                    <div className="ad-info">
                        <h4>Y_vector de {searchAdId}:</h4>
                        <p style={{ 'wordBreak': 'break-all' }}>{JSON.stringify(selectedAdYVector)}</p>
                    </div>
                )}

                <label>
                    Méthode:
                    <select value={searchMethod} onChange={(e) => setSearchMethod(e.target.value)}>
                        <option value="naive">Naive</option>
                        <option value="bfs">BFS</option>
                        <option value="dijkstra">Dijkstra</option>
                        <option value="hybrid">Hybrid</option>
                    </select>
                </label>

                <button onClick={handleSearch} disabled={isLoading}>Rechercher</button>
            </div>

            {/* Stats */}
            {stats && (
                <div className="stats">
                    <h3>Stats</h3>
                    <p>Nodes: {stats.total_nodes}</p>
                    <p>Arêtes: {stats.total_edges}</p>
                    <p>Ads: {Object.keys(adsData).length}</p>
                </div>
            )}
        </div>
    );
};

export default ControlPanel;