import { useRef, useEffect, useState } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import './GraphViewer3D.css';

const GraphViewer3D = ({ graphData, selectedAd, searchResults, highlightedNodes, highlightedLinks, onNodeClick }) => {
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

    // Focus caméra sur l'ad sélectionné
    useEffect(() => {
        if (selectedAd && fgRef.current && graphData) {
            const node = graphData.nodes.find(n => n.id === selectedAd);
            if (node) {
                // Centrer la caméra sur le nœud avec une distance de 300
                fgRef.current.cameraPosition(
                    { x: node.x, y: node.y, z: node.z + 300 }, // Position
                    node, // Regarder vers
                    1000 // Durée de l'animation en ms
                );
            }
        }
    }, [selectedAd, graphData]);

    // Couleur des nœuds
    const getNodeColor = (node) => {
        // Si un ad est sélectionné et que des nœuds sont mis en évidence
        if (selectedAd && highlightedNodes.length > 0) {
            if (node.id === selectedAd) {
                return '#357cff'; // Bleu pour l'ad sélectionné (connecté)
            }
            if (highlightedNodes.includes(node.id)) {
                return '#FFD700'; // Jaune doré pour les nœuds connectés
            }
            // Griser les autres nœuds
            return node.type === 'ad' ? '#FFA500' : '#455A64';
        }

        // Si des résultats de recherche existent (rayon D)
        if (searchResults.length > 0) {
            if (node.id === selectedAd) {
                return '#357cff'; // Bleu pour l'ad sélectionné (recherche rayon D)
            }
            if (searchResults.includes(node.id)) {
                return '#4CAF50'; // Vert pour les nœuds dans le rayon D
            }
            if (node.type === 'regular') {
                return '#B0BEC5'; // Gris clair pour les nœuds hors rayon
            }
        }

        // Couleurs par défaut
        if (node.type === 'ad') {
            return node.id === selectedAd ? '#357cff' : '#FFA500';
        }

        return '#78909C'; // Gris pour les nœuds réguliers
    };

    // Taille des nœuds
    const getNodeSize = (node) => {
        if (node.id === selectedAd) {
            return 10;
        }
        if (highlightedNodes.includes(node.id)) {
            return 6;
        }
        if (searchResults.includes(node.id)) {
            return 5;
        }
        if (node.type === 'ad') {
            return 5;
        }
        return 3;
    };

    // Couleur des arêtes
    const getLinkColor = (link) => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;

        // Mettre en évidence les arêtes connectées à l'ad sélectionné
        if (selectedAd && highlightedLinks.length > 0) {
            const isHighlighted = highlightedLinks.some(l =>
                (l.source === sourceId && l.target === targetId) ||
                (l.source === targetId && l.target === sourceId)
            );
            if (isHighlighted) {
                return '#FFD700'; // Jaune doré
            }
        }

        if (link.type === 'ad_node') {
            return '#FF7043'; // Orange pour ad-node
        }
        return '#546E7A'; // Gris pour node-node
    };

    // Largeur des arêtes
    const getLinkWidth = (link) => {
        const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
        const targetId = typeof link.target === 'object' ? link.target.id : link.target;

        if (selectedAd && highlightedLinks.some(l =>
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

        if (selectedAd && highlightedLinks.some(l =>
            (l.source === sourceId && l.target === targetId) ||
            (l.source === targetId && l.target === sourceId)
        )) {
            return 0.8;
        }
        return 0.2;
    };

    // Label des nœuds
    const getNodeLabel = (node) => {
        if (node.type === 'ad') {
            return `${node.id} (Ad)\nD = ${node.radius_D?.toFixed(2) || 'N/A'}`;
        }
        return node.id;
    };

    return (
        <div id="graph-container" style={{ width: '100%', height: '100%', background: '#263238', position: 'relative' }}>
            {/* Légende */}
            <div className="legend">
                <div className="legend-title">🎨 Légende</div>
                <div className="legend-item">
                    <div className="legend-color" style={{ background: '#FFA500' }}></div>
                    <span>Ads (Annonces)</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color" style={{ background: '#357cff' }}></div>
                    <span>Ad Sélectionné</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color" style={{ background: '#78909C' }}></div>
                    <span>Nœuds Réguliers</span>
                </div>
                {highlightedNodes.length > 0 && (
                    <div className="legend-item">
                        <div className="legend-color" style={{ background: '#FFD700' }}></div>
                        <span>Nœuds Connectés ({highlightedNodes.length})</span>
                    </div>
                )}
                {searchResults.length > 0 && (
                    <>
                        <div className="legend-item">
                            <div className="legend-color" style={{ background: '#4CAF50' }}></div>
                            <span>Dans le rayon D ({searchResults.length})</span>
                        </div>
                        <div className="legend-item">
                            <div className="legend-color" style={{ background: '#B0BEC5' }}></div>
                            <span>Hors rayon D</span>
                        </div>
                    </>
                )}
                <div className="legend-divider"></div>
                <div className="legend-item">
                    <div className="legend-line" style={{ background: '#FF7043' }}></div>
                    <span>Arêtes ad-node</span>
                </div>
                <div className="legend-item">
                    <div className="legend-line" style={{ background: '#546E7A' }}></div>
                    <span>Arêtes node-node</span>
                </div>
                {highlightedLinks.length > 0 && (
                    <div className="legend-item">
                        <div className="legend-line" style={{ background: '#FFD700' }}></div>
                        <span>Arêtes en évidence ({highlightedLinks.length})</span>
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