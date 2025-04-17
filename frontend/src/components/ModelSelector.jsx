import React, { useEffect, useState } from 'react';
import { getModels } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import '../styles/ModelSelector.css';

const ModelSelector = ({ selectedModel, onModelChange }) => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await getModels();
        setModels(data);
        if (data.length > 0 && !selectedModel) {
          onModelChange(data[0].id);
        }
      } catch (error) {
        console.error('Error fetching models:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchModels();
  }, []);

  if (loading) {
    return (
      <div className="model-selector">
        <h2>Select Model</h2>
        <div style={{ height: '128px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  return (
    <div className="model-selector">
      <h2>Select Model</h2>
      <div className="model-grid">
        {models.map((model) => (
          <div
            key={model.id}
            className={`model-card ${selectedModel === model.id ? 'selected' : ''}`}
            onClick={() => onModelChange(model.id)}
          >
            <h3>{model.name}</h3>
            <p>{model.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ModelSelector;