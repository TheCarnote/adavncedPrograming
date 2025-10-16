import { useRef, useEffect, useState } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import './GraphViewer3D.css';

const GraphViewer3D = ({ graphData, selectedNode, searchResults, highlightedNodes, highlightedLinks, onNodeClick }) => {  // RENOMMÉ selectedAd -> selectedNode
    const fgRef = useRef();
    const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

    useEffect(() => {
        const updateSize = () => {
            const container = document.getElementById('graph-container');
            if (container) {
                setDimensions({
                    width: container.clientWidth,
                    height: container.clientHeight
                });
            }
        };

        updateSize();
        window.addEventListener('resize', updateSize);
        return () => window.removeEventListener('resize', updateSize);
    }, []);

    // Focus caméra sur le node sélectionné (de départ)
    useEffect(() => {
        if (fgRef.current && graphData) {
            if (selectedNode) {
                const node = graphData.nodes.find(n => n.id === selectedNode);
                if (node) {
                    // Centrer sur le node sélectionné
                    fgRef.current.cameraPosition(
                        { x: node.x, y: node.y, z: node.z + 300 },
                        node,
                        1000
                    );
                }
            } else {
                // AJOUTÉ : Recenter sur la vue de départ quand selectedNode est vide
                fgRef.current.cameraPosition(
                    { x: 0, y: 0, z: 1000 },  // Position par défaut
                    { x: 0, y: 0, z: 0 },    // Regarder vers le centre
                    1000
                );
            }
        }
    }, [selectedNode, graphData]);

    // Couleur des nœuds
    const getNodeColor = (node) => {
        // Si un node de départ est sélectionné et des résultats existent
        if (selectedNode && searchResults.length > 0) {
            if (node.id === selectedNode) {
                return '#357cff'; // Bleu pour le node de départ
            }
            if (searchResults.includes(node.id)) {
                return '#4CAF50'; // Vert pour les nœuds dans le rayon D
            }
            return '#B0BEC5'; // Gris clair pour les nœuds hors rayon
        }

        // Si des nœuds mis en évidence (ex. : connexions)
        if (highlightedNodes.length > 0) {
            if (highlightedNodes.includes(node.id)) {
                return '#FFD700'; // Jaune doré pour les nœuds en évidence
            }
        }

        // Couleur par défaut pour nodes réguliers
        return '#78909C';
    };

    // Taille des nœuds
    const getNodeSize = (node) => {
        if (node.id === selectedNode) {
            return 10;  // Plus grand pour le node de départ
        }
        if (highlightedNodes.includes(node.id)) {
            return 6;
        }
        if (searchResults.includes(node.id)) {
            return 5;
        }
        return 3;
    };

    // Couleur des arêtes
    const getLinkColor = (link) => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;

        // Mettre en évidence les arêtes connectées
        if (selectedNode && highlightedLinks.length > 0) {
            const isHighlighted = highlightedLinks.some(l =>
                (l.source === sourceId && l.target === targetId) ||
                (l.source === targetId && l.target === sourceId)
            );
            if (isHighlighted) {
                return '#FFD700'; // Jaune doré
            }
        }

        return '#546E7A'; // Gris pour node-node (seules arêtes restantes)
    };

    // Largeur des arêtes
    const getLinkWidth = (link) => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;

        if (selectedNode && highlightedLinks.some(l =>
            (l.source === sourceId && l.target === targetId) ||
            (l.source === targetId && l.target === sourceId)
        )) {
            return 2;
        }
        return 0.5;
    };

    // Opacité des arêtes
    const getLinkOpacity = (link) => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;

        if (selectedNode && highlightedLinks.some(l =>
            (l.source === sourceId && l.target === targetId) ||
            (l.source === targetId && l.target === sourceId)
        )) {
            return 0.8;
        }
        return 0.2;
    };

    // Label des nœuds (simplifié, pas d'ads)
    const getNodeLabel = (node) => {
        return node.id;  // Seulement l'ID, pas de type ad
    };

    return (
        <div id="graph-container" style={{ width: '100%', height: '100%', background: '#263238', position: 'relative' }}>
            {/* Légende CORRIGÉE */}
            <div className="legend">
                <div className="legend-title">🎨 Légende</div>
                <div className="legend-item">
                    <div className="legend-color" style={{ background: '#78909C' }}></div>
                    <span>Nœuds Réguliers</span>
                </div>
                {selectedNode && (
                    <div className="legend-item">
                        <div className="legend-color" style={{ background: '#357cff' }}></div>
                        <span>Node de Départ</span>
                    </div>
                )}
                {searchResults.length > 0 && (
                    <>
                        <div className="legend-item">
                            <div className="legend-color" style={{ background: '#4CAF50' }}></div>
                            <span>Dans le Rayon D ({searchResults.length})</span>
                        </div>
                        <div className="legend-item">
                            <div className="legend-color" style={{ background: '#B0BEC5' }}></div>
                            <span>Hors Rayon D</span>
                        </div>
                    </>
                )}
                {highlightedNodes.length > 0 && (
                    <div className="legend-item">
                        <div className="legend-color" style={{ background: '#FFD700' }}></div>
                        <span>Nœuds en Évidence ({highlightedNodes.length})</span>
                    </div>
                )}
                <div className="legend-divider"></div>
                <div className="legend-item">
                    <div className="legend-line" style={{ background: '#546E7A' }}></div>
                    <span>Arêtes Node-Node</span>
                </div>
                {highlightedLinks.length > 0 && (
                    <div className="legend-item">
                        <div className="legend-line" style={{ background: '#FFD700' }}></div>
                        <span>Arêtes en Évidence ({highlightedLinks.length})</span>
                    </div>
                )}
            </div>

            {graphData && graphData.nodes && graphData.nodes.length > 0 ? (
                <ForceGraph3D
                    ref={fgRef}
                    graphData={graphData}
                    width={dimensions.width}
                    height={dimensions.height}
                    backgroundColor="#263238"

                    // Configuration des nœuds
                    nodeLabel={getNodeLabel}
                    nodeColor={getNodeColor}
                    nodeVal={getNodeSize}
                    nodeOpacity={0.9}
                    nodeResolution={16}

                    // Configuration des arêtes
                    linkColor={getLinkColor}
                    linkOpacity={getLinkOpacity}
                    linkWidth={getLinkWidth}

                    // Interactions
                    onNodeClick={(node) => {
                        if (node && node.id && onNodeClick) {
                            onNodeClick(node);
                        }
                    }}

                    // Forces
                    d3AlphaDecay={0.01}
                    d3VelocityDecay={0.3}
                    warmupTicks={100}
                    cooldownTicks={1000}

                    // Camera
                    enableNavigationControls={true}
                    showNavInfo={false}
                />
            ) : (
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '100%',
                    color: '#B0BEC5',
                    fontSize: '18px'
                }}>
                    Aucun graphe chargé
                </div>
            )}
        </div>
    );
};

export default GraphViewer3D;