import React, { useState } from 'react';
import '../styles/SimilarPosts.css';

const SimilarPosts = ({ posts }) => {
  const [expandedPost, setExpandedPost] = useState(null);

  if (!posts || posts.length === 0) {
    return null;
  }

  return (
    <div className="similar-posts">
      <h2>Similar Posts for Inspiration</h2>
      <div className="post-list">
        {posts.map((post, index) => (
          <div key={index} className="similar-post">
            <div className="post-meta">
              <div className="post-badges">
                <span className="engagement-badge">
                  Engagement: {post.engagement}
                </span>
                <span className="language-badge">
                  {post.language}
                </span>
              </div>
              <button
                onClick={() => setExpandedPost(expandedPost === index ? null : index)}
                className="toggle-button"
              >
                {expandedPost === index ? 'Show less' : 'Show more'}
              </button>
            </div>
            <div className="post-text">
              {expandedPost === index
                ? post.text
                : `${post.text.substring(0, 150)}${post.text.length > 150 ? '...' : ''}`}
            </div>
            <div className="post-tags">
              {post.tags.map((tag, tagIndex) => (
                <span key={tagIndex} className="post-tag">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SimilarPosts;