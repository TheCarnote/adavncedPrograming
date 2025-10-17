import { useState } from 'react';
import GraphViewer3D from './components/GraphViewer3D';
import ControlPanel from './components/ControlPanel';
import LogConsole from './components/LogConsole';
import LoadingOverlay from './components/LoadingOverlay';
import graphAPI from './api/graphAPI';
import './App.css';

function App() {
  const [graphData, setGraphData] = useState(null);
  const [stats, setStats] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);  // CHANGÉ selectedAd -> selectedNode
  const [searchResults, setSearchResults] = useState([]);
  const [highlightedNodes, setHighlightedNodes] = useState([]);
  const [highlightedLinks, setHighlightedLinks] = useState([]);
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [currentFeatures, setCurrentFeatures] = useState([0, 1, 2]);

  // Fonction pour ajouter un log
  const addLog = (message, type = 'info') => {
    const now = new Date();
    const time = now.toLocaleTimeString('fr-FR');
    setLogs(prev => [...prev, { time, message, type }]);
  };

  // Uploader les fichiers CSV (handler passé à ControlPanel)
  const handleUploadFiles = async (nodesFile, adsFile) => {
    setIsLoading(true);
    setLoadingMessage('Upload des fichiers CSV...');
    addLog('📁 Upload des fichiers CSV...', 'step');

    try {
      const response = await graphAPI.uploadFiles(nodesFile, adsFile);
      addLog(response.message, 'success');
    } catch (error) {
      addLog(`❌ Erreur: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  // Construire le graphe (handler passé à ControlPanel)
  const handleBuildGraph = async (k) => {
    setIsLoading(true);
    setLoadingMessage(`Construction du graphe avec K=${k}...`);
    addLog(`🔨 Construction du graphe avec K=${k}...`, 'step');

    try {
      const response = await graphAPI.buildGraph(k);
      addLog(`✅ Graphe construit: ${response.total_nodes} nodes`, 'success');
      setStats(response);
      await loadGraphData(currentFeatures);
    } catch (error) {
      addLog(`❌ Erreur: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  // Charger le graphe (handler passé à ControlPanel)
  const handleLoadGraph = async () => {
    setIsLoading(true);
    setLoadingMessage('Chargement du graphe...');
    addLog('📂 Chargement du graphe...', 'step');

    try {
      const response = await graphAPI.loadGraph();
      addLog(`✅ Graphe chargé: ${response.total_nodes} nodes`, 'success');
      setStats(response);
      await loadGraphData(currentFeatures);
    } catch (error) {
      addLog(`❌ Erreur: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  // Charger les données du graphe pour la visualisation
  const loadGraphData = async (featureIndices) => {
    addLog(`🎨 Chargement de la vue 3D...`, 'info');
    try {
      const data = await graphAPI.fetchGraphData(featureIndices);
      setGraphData(data);
      addLog(`✅ ${data.nodes.length} nœuds chargés`, 'success');
    } catch (error) {
      addLog(`❌ Erreur: ${error.message}`, 'error');
    }
  };

  // Rechercher dans le rayon D (handler passé à ControlPanel)
  const handleSearch = async (nodeId, adId, method) => {
    setIsLoading(true);
    setLoadingMessage(`Recherche depuis ${nodeId} avec ad ${adId}...`);
    addLog(`🎯 Recherche depuis ${nodeId} avec ad ${adId}`, 'step');

    try {
      const response = await graphAPI.searchInRadius(nodeId, adId, method);
      setSelectedNode(nodeId);  // CHANGÉ selectedAd -> selectedNode
      setSearchResults(response.nodes_found);
      addLog(`✅ ${response.total_nodes} nodes trouvés`, 'success');
    } catch (error) {
      addLog(`❌ Erreur: ${error.message}`, 'error');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  // Rafraîchir la visualisation (handler passé à ControlPanel)
  const handleGraphDataChange = async () => {
    await loadGraphData(currentFeatures);
  };

  // Clic sur un nœud
  const handleNodeClick = (node) => {
    addLog(`👆 Nœud cliqué: ${node.id}`, 'info');
    // Pas de recherche auto sur clic, car on choisit manuellement
  };

  const clearSearch = () => {
    setSelectedNode(null);
    setSearchResults([]);
    setHighlightedNodes([]);
    setHighlightedLinks([]);

  }

  return (
    <div className="app">
      {isLoading && <LoadingOverlay message={loadingMessage} />}

      {/* Header */}
      <header className="app-header">
        <h1>🌐 Visualiseur de Graphe Publicitaire 3D</h1>
        <div className="header-info">
          {stats && (
            <span className="badge">
              {stats.total_nodes} nœuds
            </span>
          )}
          {searchResults.length > 0 && (
            <span className="badge badge-success">
              {searchResults.length} nœuds dans le rayon D
            </span>
          )}
        </div>
      </header>

      {/* Main content */}
      <div className="app-content">
        {/* Left panel */}
        <aside className="sidebar">
          <ControlPanel
            stats={stats}
            clearSearch={clearSearch}
            nodesData={graphData ? graphData.nodes : []}
            selectedNode={selectedNode}
            searchResults={searchResults}
            onUploadFiles={handleUploadFiles}
            onBuildGraph={handleBuildGraph}
            onLoadGraph={handleLoadGraph}
            onSearch={handleSearch}
            onGraphDataChange={handleGraphDataChange}
            onLog={addLog}
            isLoading={isLoading}
          />
        </aside>

        {/* Center - 3D viewer */}
        <main className="main-viewer">
          <GraphViewer3D
            graphData={graphData}
            selectedNode={selectedNode}  // CHANGÉ selectedAd -> selectedNode
            searchResults={searchResults}
            highlightedNodes={highlightedNodes}
            highlightedLinks={highlightedLinks}
            onNodeClick={handleNodeClick}
          />
        </main>
      </div>

      {/* Bottom - Console */}
      <footer className="app-footer">
        <LogConsole logs={logs} />
      </footer>
    </div>
  );
}

export default App;