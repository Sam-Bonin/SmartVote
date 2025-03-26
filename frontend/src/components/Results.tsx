import React, { useState } from 'react';
import { ResultsProps, Document } from '../types';
import Analysis from './Analysis';
import PdfViewer from './PdfViewer';
import EvidenceCard from './EvidenceCard';

const Results: React.FC<ResultsProps> = ({ query, results, loading, step }) => {
  const [moreVisible, setMoreVisible] = useState<boolean>(false);
  
  if (!query) return null;
  
  // Calculate which documents to show initially and which to hide behind "View More"
  const initialDisplayCount = 5;
  const hasMoreDocuments = results?.similar_documents && results.similar_documents.length > initialDisplayCount;
  
  // Get the current page for the PDF viewer
  const currentPage = results?.similar_documents && results.similar_documents.length > 0
    ? results.similar_documents[0].page
    : 1;
  
  // Handle view more button click
  const handleViewMore = () => {
    setMoreVisible(!moreVisible);
  };
  
  return (
    <div className="results-wrapper">
      <div className="results-container" style={{
        position: 'relative',
        boxShadow: 'var(--shadow-sm)',
        border: '1px solid var(--border-color)'
      }}>
        {/* Query indicator with search icon */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          marginBottom: 'var(--spacing-lg)'
        }}>
          <span className="material-icons" style={{
            color: 'var(--primary-accent)',
            marginRight: 'var(--spacing-sm)',
            fontSize: '24px'
          }}>search</span>
          <h2 className="query-display">"{query}"</h2>
        </div>
        
        {/* Analysis section */}
        <Analysis 
          analysis={results?.analysis}
          loading={loading}
          step={step}
        />
      </div>
      
      {/* PDF Viewer section */}
      <PdfViewer 
        page={currentPage} 
        isVisible={!!(results?.similar_documents && results.similar_documents.length > 0)}
      />
      
      {/* Evidence Section */}
      {(results?.similar_documents || loading) && (
        <div className="evidence-section animate-fade-in-delay-3" style={{
          boxShadow: 'var(--shadow-sm)',
          border: '1px solid var(--border-color)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: 'var(--spacing-lg)'
          }}>
            <span className="material-icons" style={{
              color: 'var(--secondary-accent)',
              marginRight: 'var(--spacing-sm)',
              fontSize: '24px'
            }}>fact_check</span>
            <h2 className="evidence-title">Supporting Evidence</h2>
          </div>
          
          {loading && !results?.similar_documents ? (
            <div className="loading-container" style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              padding: 'var(--spacing-xl)',
              color: 'var(--text-secondary)'
            }}>
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <p style={{ marginTop: 'var(--spacing-md)' }}>
                Retrieving relevant documents...
              </p>
            </div>
          ) : (
            <>
              <div className="evidence-grid">
                {results?.similar_documents?.slice(0, initialDisplayCount).map((doc, index) => (
                  <EvidenceCard key={index} document={doc} index={index} />
                ))}
                
                {moreVisible && results?.similar_documents?.slice(initialDisplayCount).map((doc, index) => (
                  <EvidenceCard 
                    key={index + initialDisplayCount} 
                    document={doc} 
                    index={index + initialDisplayCount} 
                  />
                ))}
              </div>
              
              {hasMoreDocuments && (
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'center', 
                  marginTop: 'var(--spacing-lg)' 
                }}>
                  <button 
                    className="search-button" 
                    onClick={handleViewMore}
                    style={{ 
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: 'var(--spacing-xs)',
                      padding: 'var(--spacing-sm) var(--spacing-lg)',
                      fontSize: 'var(--font-size-sm)',
                      backgroundColor: 'var(--foreground-color)',
                      color: 'var(--secondary-accent)',
                      border: '1px solid var(--secondary-accent)',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.backgroundColor = 'var(--secondary-accent)';
                      e.currentTarget.style.color = 'white';
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.backgroundColor = 'var(--foreground-color)';
                      e.currentTarget.style.color = 'var(--secondary-accent)';
                    }}
                  >
                    <span className="material-icons" style={{ fontSize: '18px' }}>
                      {moreVisible ? 'visibility_off' : 'visibility'}
                    </span>
                    {moreVisible 
                      ? 'Show Less' 
                      : `View ${results.similar_documents!.length - initialDisplayCount} More Results`}
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default Results; 