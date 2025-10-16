import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const graphAPI = {
    // Uploader les fichiers CSV
    uploadFiles: async (nodesFile, adsFile) => {
        const formData = new FormData();
        formData.append('nodes_file', nodesFile);
        formData.append('ads_file', adsFile);

        const response = await axios.post(`${API_BASE_URL}/upload-files`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    // Construire un nouveau graphe
    buildGraph: async (k = 10) => {
        const response = await axios.post(`${API_BASE_URL}/build-graph`, { k }, {
            headers: { 'Content-Type': 'application/json' }
        });
        return response.data;
    },

    // Charger un graphe existant
    loadGraph: async () => {
        const response = await axios.post(`${API_BASE_URL}/load-graph`);
        return response.data;
    },

    // Rechercher dans le rayon
    searchInRadius: async (nodeId, adId, method = 'hybrid') => {
        const response = await axios.post(`${API_BASE_URL}/search`, {
            node_id: nodeId,
            ad_id: adId,
            method
        }, {
            headers: { 'Content-Type': 'application/json' }
        });
        return response.data;
    },

    // Récupérer les stats du graphe
    fetchGraphStats: async () => {
        const response = await axios.get(`${API_BASE_URL}/graph-stats`);
        return response.data;
    },

    // Récupérer les données des ads
    fetchAdsData: async () => {
        const response = await axios.get(`${API_BASE_URL}/ads-data`);
        return response.data;
    },

    // Récupérer les données 3D du graphe
    fetchGraphData: async (fx = 0, fy = 1, fz = 2) => {
        const response = await axios.get(`${API_BASE_URL}/graph-data`, {
            params: { fx, fy, fz }
        });
        return response.data;
    }
};

export default graphAPI;
