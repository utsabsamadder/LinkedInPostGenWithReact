import React, { useEffect, useState } from 'react';
import { getLengths } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import '../styles/LengthSelector.css';

const LengthSelector = ({ selectedLength, onLengthChange }) => {
  const [lengths, setLengths] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLengths = async () => {
      try {
        const data = await getLengths();
        setLengths(data);
        if (data.length > 0 && !selectedLength) {
          onLengthChange(data[0].id);
        }
      } catch (error) {
        console.error('Error fetching lengths:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLengths();
  }, []);

  if (loading) {
    return (
      <div className="length-selector">
        <h2>Post Length</h2>
        <div style={{ height: '40px', display: 'flex', alignItems: 'center' }}>
          <LoadingSpinner size="small" />
        </div>
      </div>
    );
  }

  return (
    <div className="length-selector">
      <h2>Post Length</h2>
      <div className="length-options">
        {lengths.map((length) => (
          <button
            key={length.id}
            className={`length-option ${selectedLength === length.id ? 'selected' : ''}`}
            onClick={() => onLengthChange(length.id)}
          >
            {length.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default LengthSelector;