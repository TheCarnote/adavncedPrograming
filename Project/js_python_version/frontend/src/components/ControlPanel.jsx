import { useState, useEffect, useRef } from 'react';
import './ControlPanel.css';

const ControlPanel = ({
    stats,
    graphData,
    selectedAd,
    searchResults,
    onUploadFiles,
    onBuildGraph,
    onRegenerateView,
    onSearch,
    onClearSelection,
    isLoading
}) => {
    const [kValue, setKValue] = useState(10);
    const [featureX, setFeatureX] = useState(0);
    const [featureY, setFeatureY] = useState(1);
    const [featureZ, setFeatureZ] = useState(2);
    const [localSelectedAd, setLocalSelectedAd] = useState('');
    const [defaultD, setDefaultD] = useState(null);
    const [nodesFile, setNodesFile] = useState(null);
    const [adsFile, setAdsFile] = useState(null);

    const nodesFileInputRef = useRef(null);
    const adsFileInputRef = useRef(null);

    const numFeatures = stats?.num_features || 50;
    const ads = stats?.ads || [];

    // Synchroniser la sélection externe avec la sélection locale
    useEffect(() => {
        if (selectedAd) {
            setLocalSelectedAd(selectedAd);
        } else {
            setLocalSelectedAd('');
        }
    }, [selectedAd]);

    // Mettre à jour le D par défaut quand un ad est sélectionné
    useEffect(() => {
        if (localSelectedAd && graphData && graphData.nodes) {
            const adNode = graphData.nodes.find(n => n.id === localSelectedAd);
            if (adNode && adNode.radius_D !== undefined) {
                setDefaultD(adNode.radius_D);
            } else {
                setDefaultD(null);
            }
        } else {
            setDefaultD(null);
        }
    }, [localSelectedAd, graphData]);

    // Lancer la recherche automatiquement quand un ad est sélectionné
    const handleAdSelection = (adId) => {
        setLocalSelectedAd(adId);
        if (adId && graphData) {
            onSearch(adId, 'hybrid');
        }
    };

    const handleClearSelection = () => {
        setLocalSelectedAd('');
        setDefaultD(null);
        if (onClearSelection) {
            onClearSelection();
        }
    };

    // Gestion des fichiers
    const handleNodesFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setNodesFile(file);
        }
    };

    const handleAdsFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setAdsFile(file);
        }
    };

    const handleUploadFiles = () => {
        if (!nodesFile || !adsFile) {
            alert('⚠️ Veuillez sélectionner les deux fichiers CSV (Nodes et Ads)');
            return;
        }

        onUploadFiles(nodesFile, adsFile);
    };

    return (
        <div className="control-panel">
            <div className="control-header">
                <h2>Panneau de Contrôle</h2>
                {selectedAd && (
                    <button
                        onClick={handleClearSelection}
                        className="btn btn-warning btn-clear-global"
                        disabled={isLoading}
                        title="Désélectionner l'ad actuel"
                    >
                        ❌ Désélectionner
                    </button>
                )}
            </div>

            {/* Bannière de l'ad sélectionné */}
            {selectedAd && (
                <div className="selected-ad-banner">
                    <span className="selected-label">Ad sélectionné:</span>
                    <strong className="selected-id">{selectedAd}</strong>
                    {defaultD !== null && (
                        <span className="selected-info">D = {defaultD.toFixed(4)}</span>
                    )}
                </div>
            )}

            {/* Section Upload des fichiers CSV */}
            <div className="section section-upload">
                <h3>📁 Charger les fichiers CSV</h3>

                <p className="section-description">
                    Uploadez vos fichiers CSV pour construire un nouveau graphe personnalisé.
                </p>

                <div className="input-group">
                    <label>Fichier Nodes (nœuds réguliers):</label>
                    <input
                        ref={nodesFileInputRef}
                        type="file"
                        accept=".csv"
                        onChange={handleNodesFileChange}
                        disabled={isLoading}
                        style={{ display: 'none' }}
                    />
                    <button
                        onClick={() => nodesFileInputRef.current?.click()}
                        className="btn btn-file"
                        disabled={isLoading}
                    >
                        {nodesFile ? `✅ ${nodesFile.name}` : '📄 Choisir fichier Nodes'}
                    </button>
                </div>

                <div className="input-group">
                    <label>Fichier Ads (annonces):</label>
                    <input
                        ref={adsFileInputRef}
                        type="file"
                        accept=".csv"
                        onChange={handleAdsFileChange}
                        disabled={isLoading}
                        style={{ display: 'none' }}
                    />
                    <button
                        onClick={() => adsFileInputRef.current?.click()}
                        className="btn btn-file"
                        disabled={isLoading}
                    >
                        {adsFile ? `✅ ${adsFile.name}` : '📄 Choisir fichier Ads'}
                    </button>
                </div>

                <button
                    onClick={handleUploadFiles}
                    className="btn btn-success"
                    disabled={isLoading || !nodesFile || !adsFile}
                >
                    {isLoading ? '⏳ Upload...' : '📤 Uploader les fichiers'}
                </button>
            </div>

            {/* Section Construction */}
            <div className="section">
                <h3>📊 Construction du Graphe</h3>

                <div className="input-group">
                    <label>Nombre de voisins K-NN:</label>
                    <input
                        type="number"
                        value={kValue}
                        onChange={(e) => setKValue(parseInt(e.target.value) || 10)}
                        min="1"
                        max="50"
                        disabled={isLoading}
                    />
                </div>

                <button
                    onClick={() => onBuildGraph(kValue)}
                    disabled={isLoading}
                    className="btn btn-primary"
                >
                    {isLoading ? '⏳ Construction...' : '🔨 Construire le graphe'}
                </button>
            </div>

            {/* Section Statistiques */}
            {stats && (
                <div className="section stats">
                    <h3>📈 Statistiques</h3>
                    <div className="stat-item">
                        <span>Nœuds totaux:</span>
                        <strong>{stats.total_nodes}</strong>
                    </div>
                    <div className="stat-item">
                        <span>Arêtes:</span>
                        <strong>{stats.total_edges}</strong>
                    </div>
                    <div className="stat-item">
                        <span>Ads:</span>
                        <strong>{stats.ad_nodes}</strong>
                    </div>
                    <div className="stat-item">
                        <span>Features:</span>
                        <strong>{stats.num_features}</strong>
                    </div>
                    {stats.build_time && (
                        <div className="stat-item highlight">
                            <span>⏱️ Temps construction:</span>
                            <strong>{stats.build_time.toFixed(2)}s</strong>
                        </div>
                    )}
                </div>
            )}

            {/* Section Visualisation */}
            {stats && (
                <div className="section">
                    <h3>🎨 Visualisation 3D</h3>

                    <div className="input-group">
                        <label>Feature X (axe horizontal):</label>
                        <select
                            value={featureX}
                            onChange={(e) => setFeatureX(parseInt(e.target.value))}
                        >
                            {[...Array(numFeatures)].map((_, i) => (
                                <option key={i} value={i}>Feature {i + 1}</option>
                            ))}
                        </select>
                    </div>

                    <div className="input-group">
                        <label>Feature Y (axe vertical):</label>
                        <select
                            value={featureY}
                            onChange={(e) => setFeatureY(parseInt(e.target.value))}
                        >
                            {[...Array(numFeatures)].map((_, i) => (
                                <option key={i} value={i}>Feature {i + 1}</option>
                            ))}
                        </select>
                    </div>

                    <div className="input-group">
                        <label>Feature Z (profondeur):</label>
                        <select
                            value={featureZ}
                            onChange={(e) => setFeatureZ(parseInt(e.target.value))}
                        >
                            {[...Array(numFeatures)].map((_, i) => (
                                <option key={i} value={i}>Feature {i + 1}</option>
                            ))}
                        </select>
                    </div>

                    <button
                        onClick={() => onRegenerateView([featureX, featureY, featureZ])}
                        className="btn btn-primary"
                        disabled={isLoading}
                    >
                        🔄 Régénérer la vue 3D
                    </button>
                </div>
            )}

            {/* Section Analyse du Rayon D */}
            {stats && ads.length > 0 && (
                <div className="section section-search">
                    <h3>🎯 Analyse du Rayon D</h3>

                    <p className="section-description">
                        Sélectionnez un ad pour afficher automatiquement tous les nœuds dans son rayon D.
                    </p>

                    <div className="input-group">
                        <label>Sélectionner un Ad:</label>
                        <select
                            value={localSelectedAd}
                            onChange={(e) => handleAdSelection(e.target.value)}
                            disabled={isLoading}
                        >
                            <option value="">-- Choisir un ad --</option>
                            {ads.map(ad => (
                                <option key={ad} value={ad}>{ad}</option>
                            ))}
                        </select>
                    </div>

                    {defaultD !== null && (
                        <div className="info-box-large">
                            <div className="info-row">
                                <span className="info-label">📏 Rayon D:</span>
                                <strong className="info-value">{defaultD.toFixed(4)}</strong>
                            </div>
                            <div className="info-description">
                                Ce rayon D est utilisé automatiquement pour la recherche.
                            </div>
                        </div>
                    )}

                    {/* Liste des nœuds trouvés */}
                    {searchResults && searchResults.length > 0 && (
                        <div className="results-container">
                            <div className="results-header">
                                <h4>📋 Nœuds dans le rayon D</h4>
                                <span className="results-count">{searchResults.length} nœuds</span>
                            </div>
                            <div className="results-list">
                                {searchResults.slice(0, 20).map((nodeId, index) => (
                                    <div key={nodeId} className="result-item">
                                        <span className="result-number">{index + 1}</span>
                                        <span className="result-id">{nodeId}</span>
                                    </div>
                                ))}
                                {searchResults.length > 20 && (
                                    <div className="result-item result-more">
                                        <span>... et {searchResults.length - 20} autres nœuds</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ControlPanel;