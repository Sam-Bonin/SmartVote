import React, { useState, useEffect } from 'react';
import SearchBox from './SearchBox';
import Sidebar from './Sidebar';
import Results from './Results';
import { useQuery } from '../hooks/useQuery';

const App: React.FC = () => {
  const [menuOpen, setMenuOpen] = useState<boolean>(false);
  const { query, results, loading, step, error, submitQuery } = useQuery();
  
  // Close menu when clicking outside on mobile
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (window.innerWidth <= 768 && menuOpen) {
        const target = e.target as HTMLElement;
        if (!target.closest('.sidebar') && !target.closest('.menu-toggle')) {
          setMenuOpen(false);
        }
      }
    };
    
    document.addEventListener('mousedown', handleOutsideClick);
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [menuOpen]);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleSearch = (searchQuery: string) => {
    submitQuery(searchQuery);
    
    // Close sidebar on mobile after search
    if (window.innerWidth <= 768) {
      setMenuOpen(false);
    }
  };

  return (
    <div className="app-container">
      {/* Mobile menu toggle */}
      <button 
        className="menu-toggle" 
        onClick={toggleMenu}
        aria-label={menuOpen ? 'Close menu' : 'Open menu'}
        style={{
          display: window.innerWidth <= 768 ? 'flex' : 'none',
          backgroundColor: 'var(--foreground-color)',
          boxShadow: 'var(--shadow-md)',
          border: 'none',
          borderRadius: '50%',
          width: '44px',
          height: '44px',
          position: 'fixed',
          top: 'var(--spacing-md)',
          left: 'var(--spacing-md)',
          zIndex: 1000,
          justifyContent: 'center',
          alignItems: 'center',
          cursor: 'pointer',
          transition: 'background-color 0.2s ease'
        }}
      >
        <span className="material-icons" style={{ color: 'var(--primary-accent)' }}>
          {menuOpen ? 'close' : 'menu'}
        </span>
      </button>
      
      {/* Sidebar */}
      <Sidebar 
        onTopicSelect={handleSearch} 
        className={menuOpen ? 'open' : ''}
      />
      
      {/* Main content */}
      <div className="main-content">
        <SearchBox onSearch={handleSearch} />
        
        {/* Error message if there's an error */}
        {error && (
          <div className="results-container" style={{
            padding: 'var(--spacing-lg)',
            backgroundColor: '#FEF2F2', // Light red background
            borderLeft: '4px solid var(--primary-accent)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 'var(--spacing-md)' }}>
              <span className="material-icons" style={{ color: 'var(--primary-accent)', marginRight: 'var(--spacing-md)', fontSize: '24px' }}>
                error
              </span>
              <p style={{ color: 'var(--primary-accent)', fontWeight: 'var(--font-weight-bold)' }}>
                Error: {error}
              </p>
            </div>
            <p>Please make sure the server is running and the embeddings file exists.</p>
          </div>
        )}
        
        {/* Placeholder when no results */}
        {!query && !loading && !error && (
          <div className="placeholder-container" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 'var(--spacing-xl)',
            textAlign: 'center',
            color: 'var(--text-secondary)',
            margin: 'var(--spacing-xl) 0'
          }}>
            <span className="material-icons" style={{ fontSize: '60px', marginBottom: 'var(--spacing-lg)', opacity: 0.7 }}>
              search
            </span>
            <h2 style={{ marginBottom: 'var(--spacing-md)', fontWeight: 'var(--font-weight-medium)' }}>
              Start exploring the Liberal Party Platform
            </h2>
            <p>
              Enter a query in the search box above or select a topic from the sidebar
            </p>
          </div>
        )}
        
        {/* Results display */}
        {(query || loading) && !error && (
          <Results 
            query={query}
            results={results}
            loading={loading}
            step={step}
          />
        )}
      </div>
    </div>
  );
};

export default App; 