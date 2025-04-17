import React, { useEffect, useState } from 'react';
import { getTags } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import '../styles/TagSelector.css';

const TagSelector = ({ selectedTag, onTagChange }) => {
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await getTags();
        setTags(response);
        if (response.length > 0 && !selectedTag) {
          onTagChange(response[0]);
        }
      } catch (error) {
        console.error('Error fetching tags:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTags();
  }, []);

  const filteredTags = tags.filter(tag => 
    tag.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="tag-selector">
        <h2>Topic/Tag</h2>
        <div style={{ height: '40px', display: 'flex', alignItems: 'center' }}>
          <LoadingSpinner size="small" />
        </div>
      </div>
    );
  }

  return (
    <div className="tag-selector">
      <h2>Topic/Tag</h2>
      <input
        type="text"
        className="tag-search"
        placeholder="Search for a tag or enter a custom topic"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="tag-list">
        {filteredTags.map((tag) => (
          <button
            key={tag}
            className={`tag-option ${selectedTag === tag ? 'selected' : ''}`}
            onClick={() => onTagChange(tag)}
          >
            {tag}
          </button>
        ))}
      </div>
      {filteredTags.length === 0 && searchTerm && (
        <button
          className="custom-tag-button"
          onClick={() => onTagChange(searchTerm)}
        >
          Use "{searchTerm}" as custom topic
        </button>
      )}
    </div>
  );
};

export default TagSelector;