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
  const [selectedAd, setSelectedAd] = useState(null);
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

  // Uploader les fichiers CSV
  const handleUploadFiles = async (nodesFile, adsFile) => {
    setIsLoading(true);
    setLoadingMessage('Upload des fichiers CSV...');
    addLog('📁 Upload des fichiers CSV...', 'step');

    try {
      const response = await graphAPI.uploadFiles(nodesFile, adsFile);
      addLog(response.message, 'success');
      addLog(`✅ Nodes: ${response.nodes_file} → ${response.nodes_path}`, 'info');
      addLog(`✅ Ads: ${response.ads_file} → ${response.ads_path}`, 'info');
    } catch (error) {
      console.error('❌ Erreur:', error);
      addLog(`❌ Erreur: ${error.response?.data?.detail || error.message}`, 'error');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  // Construire le graphe
  const handleBuildGraph = async (k) => {
    setIsLoading(true);
    setLoadingMessage(`Construction du graphe avec K=${k}...`);
    addLog(`🔨 Construction du graphe avec K=${k}...`, 'step');

    try {
      const response = await graphAPI.buildGraph(k);
      addLog(response.message, 'success');

      // Afficher les temps
      if (response.stats && response.stats.build_time) {
        addLog(`⏱️  Temps total: ${response.stats.build_time.toFixed(2)}s`, 'success');

        if (response.stats.load_time) {
          addLog(`   📂 Chargement CSV: ${response.stats.load_time.toFixed(2)}s`, 'info');
        }
        if (response.stats.construction_time) {
          addLog(`   🏗️  Construction K-NN: ${response.stats.construction_time.toFixed(2)}s`, 'info');
        }
        if (response.stats.save_time) {
          addLog(`   💾 Sauvegarde: ${response.stats.save_time.toFixed(2)}s`, 'info');
        }
      }

      addLog(`📊 ${response.stats.total_nodes} nœuds, ${response.stats.total_edges} arêtes`, 'info');

      // Afficher les listes de nœuds et arêtes
      if (response.nodes && response.edges) {
        addLog(`\n📋 LISTE DES NŒUDS (${response.nodes.length}):`, 'info');

        // Formatter la liste des nœuds
        const nodesList = response.nodes.map(n => {
          if (n.type === 'ad') {
            return `  • ${n.id} [AD, D=${n.radius_D?.toFixed(4)}]`;
          }
          return `  • ${n.id} [Node]`;
        }).join('\n');

        addLog(nodesList, 'code');

        addLog(`\n🔗 LISTE DES ARÊTES (${response.edges.length}):`, 'info');

        // Afficher un échantillon des arêtes (premières 20)
        const edgesSample = response.edges.slice(0, 20).map(e =>
          `  • ${e.source} → ${e.target} [weight: ${e.weight.toFixed(4)}]`
        ).join('\n');

        addLog(edgesSample, 'code');

        if (response.edges.length > 20) {
          addLog(`  ... et ${response.edges.length - 20} autres arêtes`, 'info');
        }

        // Logger dans la console pour copier facilement
        console.log('📋 NŒUDS COMPLETS:', response.nodes);
        console.log('🔗 ARÊTES COMPLÈTES:', response.edges);
      }

      setStats(response.stats);

      // Charger les données pour la visualisation
      setLoadingMessage('Chargement de la visualisation 3D...');
      await loadGraphData(currentFeatures);

    } catch (error) {
      console.error('❌ Erreur:', error);
      addLog(`❌ Erreur: ${error.response?.data?.detail || error.message}`, 'error');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  // Charger les données du graphe pour la visualisation
  const loadGraphData = async (featureIndices) => {
    addLog(`🎨 Chargement de la vue 3D (features ${featureIndices.map(i => i + 1).join(', ')})...`, 'info');

    try {
      const data = await graphAPI.getGraphData(featureIndices);
      setGraphData(data);
      addLog(`✅ ${data.nodes.length} nœuds et ${data.links.length} arêtes chargés`, 'success');
    } catch (error) {
      addLog(`❌ Erreur de chargement: ${error.message}`, 'error');
    }
  };

  // Régénérer la vue 3D
  const handleRegenerateView = async (featureIndices) => {
    setCurrentFeatures(featureIndices);
    setSearchResults([]);
    setSelectedAd(null);
    setHighlightedNodes([]);
    setHighlightedLinks([]);
    await loadGraphData(featureIndices);
  };

  // Rechercher dans le rayon D
  const handleSearch = async (adId, method = 'hybrid') => {
    setIsLoading(true);
    setLoadingMessage(`Analyse du rayon D pour ${adId}...`);
    addLog(`🎯 Analyse du rayon D pour ${adId}`, 'step');

    try {
      const response = await graphAPI.search(adId, method);

      setSelectedAd(adId);
      setSearchResults(response.nodes_found);
      setHighlightedNodes([]);
      setHighlightedLinks([]);

      addLog(`✅ ${response.nodes_found.length} nœuds trouvés dans le rayon D`, 'success');
      addLog(`📏 Rayon D utilisé: ${response.radius_D.toFixed(6)}`, 'info');
      addLog(`⏱️  Temps d'analyse: ${response.elapsed_time.toFixed(3)}s`, 'info');
      addLog(`📈 Méthode: ${response.method_used}`, 'info');

      // Formater la liste Python
      const formatPythonList = (nodes) => {
        if (nodes.length === 0) return '[]';
        if (nodes.length <= 5) {
          return `['${nodes.join("', '")}']`;
        }
        if (nodes.length <= 50) {
          const formatted = nodes.map(node => `'${node}'`).join(', ');
          return `[${formatted}]`;
        }
        const formatted = nodes.map(node => `    '${node}'`).join(',\n');
        return `[\n${formatted}\n]`;
      };

      const pythonList = formatPythonList(response.nodes_found);
      addLog(`📋 Liste complète des ${response.nodes_found.length} nœuds (format Python):`, 'info');
      addLog(pythonList, 'code');

      console.log('📋 Liste complète des nœuds (format Python):');
      console.log(pythonList);
      console.log('\n🔢 Tableau JavaScript:');
      console.log(response.nodes_found);

    } catch (error) {
      addLog(`❌ Erreur: ${error.response?.data?.detail || error.message}`, 'error');
    } finally {
      setIsLoading(false);
      setLoadingMessage('');
    }
  };

  // Désélectionner l'ad
  const handleClearSelection = () => {
    setSelectedAd(null);
    setSearchResults([]);
    setHighlightedNodes([]);
    setHighlightedLinks([]);
    addLog('🔄 Sélection réinitialisée', 'info');
  };

  // Clic sur un nœud
  const handleNodeClick = (node) => {
    if (!node || !node.id) {
      console.error('Node invalide:', node);
      return;
    }

    addLog(`👆 Nœud cliqué: ${node.id}`, 'info');

    if (node.type === 'ad') {
      handleSearch(node.id);
    }
  };

  return (
    <div className="app">
      {isLoading && <LoadingOverlay message={loadingMessage} />}

      {/* Header */}
      <header className="app-header">
        <h1>🌐 Visualiseur de Graphe Publicitaire 3D</h1>
        <div className="header-info">
          {stats && (
            <span className="badge">
              {stats.total_nodes} nœuds • {stats.ad_nodes} ads
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
            graphData={graphData}
            selectedAd={selectedAd}
            searchResults={searchResults}
            onUploadFiles={handleUploadFiles}
            onBuildGraph={handleBuildGraph}
            onRegenerateView={handleRegenerateView}
            onSearch={handleSearch}
            onClearSelection={handleClearSelection}
            isLoading={isLoading}
          />
        </aside>

        {/* Center - 3D viewer */}
        <main className="main-viewer">
          <GraphViewer3D
            graphData={graphData}
            selectedAd={selectedAd}
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