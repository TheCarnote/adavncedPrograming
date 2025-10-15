import { useEffect, useRef } from 'react';
import './LogConsole.css';

const LogConsole = ({ logs }) => {
    const consoleRef = useRef(null);

    useEffect(() => {
        // Auto-scroll vers le bas
        if (consoleRef.current) {
            consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
        }
    }, [logs]);

    const getLogClass = (type) => {
        switch (type) {
            case 'success': return 'log-success';
            case 'error': return 'log-error';
            case 'warning': return 'log-warning';
            case 'step': return 'log-step';
            default: return 'log-info';
        }
    };

    return (
        <div className="log-console">
            <div className="console-header">
                <span>📋 Console de Logs</span>
            </div>
            <div className="console-content" ref={consoleRef}>
                {logs.map((log, index) => (
                    <div key={index} className={`log-entry ${getLogClass(log.type)}`}>
                        <span className="log-time">[{log.time}]</span>
                        <span className="log-message">{log.message}</span>
                    </div>
                ))}
                {logs.length === 0 && (
                    <div className="log-entry log-info">
                        <span className="log-message">Bienvenue ! Les logs s'afficheront ici.</span>
                    </div>
                )}
            </div>
        </div>
    );
};

export default LogConsole;