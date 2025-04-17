import React, { useState } from 'react';
import { generatePost } from '../services/api';
import ModelSelector from './ModelSelector';
import LanguageSelector from './LanguageSelector';
import LengthSelector from './LengthSelector';
import TagSelector from './TagSelector';
import GeneratedPost from './GeneratedPost';
import SimilarPosts from './SimilarPosts';
import '../styles/PostGenerator.css';

const PostGenerator = () => {
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [selectedLength, setSelectedLength] = useState('');
  const [selectedTag, setSelectedTag] = useState('');
  const [customInput, setCustomInput] = useState('');
  const [generatedPost, setGeneratedPost] = useState('');
  const [similarPosts, setSimilarPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGeneratePost = async () => {
    if (!selectedModel || !selectedLanguage || !selectedLength || !selectedTag) {
      setError('Please select all required options');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      const result = await generatePost({
        model_name: selectedModel,
        language: selectedLanguage,
        length: selectedLength,
        tag: selectedTag,
        custom_input: customInput,
      });

      setGeneratedPost(result.post);
      setSimilarPosts(result.similar_posts);
    } catch (err) {
      console.error('Error generating post:', err);
      setError('Failed to generate post. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container post-generator">
      <div className="card">
        <ModelSelector selectedModel={selectedModel} onModelChange={setSelectedModel} />
        
        <div className="form-grid">
          <div>
            <LanguageSelector selectedLanguage={selectedLanguage} onLanguageChange={setSelectedLanguage} />
            <LengthSelector selectedLength={selectedLength} onLengthChange={setSelectedLength} />
          </div>
          <div>
            <TagSelector selectedTag={selectedTag} onTagChange={setSelectedTag} />
          </div>
        </div>
        
        <div className="custom-input">
          <h2>Additional Context (Optional)</h2>
          <textarea
            placeholder="Add any specific details or context for your post..."
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
          ></textarea>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-actions">
          <button
            className="btn btn-primary"
            onClick={handleGeneratePost}
            disabled={isLoading}
          >
            {isLoading ? 'Generating...' : 'Generate LinkedIn Post'}
          </button>
        </div>
      </div>
      
      <GeneratedPost post={generatedPost} isLoading={isLoading} />
      <SimilarPosts posts={similarPosts} />
    </div>
  );
};

export default PostGenerator;