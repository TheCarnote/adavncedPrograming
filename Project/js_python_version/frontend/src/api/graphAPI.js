import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const graphAPI = {
    /**
     * Uploader les fichiers CSV
     */
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

    /**
     * Construire un nouveau graphe
     */
    buildGraph: async (k = 10) => {
        const response = await axios.post(`${API_BASE_URL}/build-graph`, { k });
        return response.data;
    },

    /**
     * Obtenir les données du graphe pour visualisation 3D
     */
    getGraphData: async (featureIndices = [0, 1, 2]) => {
        const [x, y, z] = featureIndices;
        const response = await axios.get(`${API_BASE_URL}/graph-data`, {
            params: {
                feature_x: x,
                feature_y: y,
                feature_z: z
            }
        });
        return response.data;
    },

    /**
     * Rechercher les nœuds dans le rayon D d'un ad
     */
    search: async (adId, method = 'hybrid') => {
        const response = await axios.post(`${API_BASE_URL}/search`, {
            ad_id: adId,
            method: method
        });
        return response.data;
    }
};

export default graphAPI;