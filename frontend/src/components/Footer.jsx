import React from 'react';
import '../styles/Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <p>LinkedIn Post Generator &copy; {new Date().getFullYear()}</p>
          <p>Powered by AI to help you create engaging content</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;