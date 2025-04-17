import React, { useEffect, useState } from 'react';
import { getLanguages } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import '../styles/LanguageSelector.css';

const LanguageSelector = ({ selectedLanguage, onLanguageChange }) => {
  const [languages, setLanguages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const data = await getLanguages();
        setLanguages(data);
        if (data.length > 0 && !selectedLanguage) {
          onLanguageChange(data[0].id);
        }
      } catch (error) {
        console.error('Error fetching languages:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLanguages();
  }, []);

  if (loading) {
    return (
      <div className="language-selector">
        <h2>Language</h2>
        <div style={{ height: '40px', display: 'flex', alignItems: 'center' }}>
          <LoadingSpinner size="small" />
        </div>
      </div>
    );
  }

  return (
    <div className="language-selector">
      <h2>Language</h2>
      <div className="language-options">
        {languages.map((language) => (
          <button
            key={language.id}
            className={`language-option ${selectedLanguage === language.id ? 'selected' : ''}`}
            onClick={() => onLanguageChange(language.id)}
          >
            {language.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default LanguageSelector;