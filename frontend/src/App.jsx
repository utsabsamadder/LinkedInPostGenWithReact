import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import PostGenerator from './components/PostGenerator';
import './styles/App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <PostGenerator />
      </main>
      <Footer />
    </div>
  );
}

export default App;