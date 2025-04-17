import React, { useState } from 'react';
import '../styles/GeneratedPost.css';

const GeneratedPost = ({ post, isLoading }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(post);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isLoading) {
    return (
      <div className="generated-post post-loading">
        <div className="loading-line"></div>
        <div className="loading-line"></div>
        <div className="loading-line"></div>
        <div className="loading-line"></div>
      </div>
    );
  }

  if (!post) {
    return null;
  }

  return (
    <div className="generated-post">
      <div className="post-header">
        <h2>Generated Post</h2>
        <button
          onClick={copyToClipboard}
          className="copy-button"
        >
          {copied ? 'Copied!' : 'Copy to clipboard'}
        </button>
      </div>
      <div className="post-content">
        {post}
      </div>
    </div>
  );
};

export default GeneratedPost;