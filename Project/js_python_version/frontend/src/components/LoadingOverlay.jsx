import './LoadingOverlay.css';

const LoadingOverlay = ({ message = 'Chargement en cours...', progress = null }) => {
    return (
        <div className="loading-overlay">
            <div className="loading-content">
                <div className="spinner"></div>
                <div className="loading-message">{message}</div>
                {progress !== null && (
                    <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default LoadingOverlay;