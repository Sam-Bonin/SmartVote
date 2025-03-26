import React, { useEffect, useRef } from 'react';
import { Analysis as AnalysisType } from '../types';
import { processMarkdown } from '../utils/formatters';

interface AnalysisProps {
  analysis: AnalysisType | undefined;
  loading: boolean;
  step: string | null;
}

const Analysis: React.FC<AnalysisProps> = ({ analysis, loading, step }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  // Apply fade-in animation when content changes
  useEffect(() => {
    if (!loading && analysis && containerRef.current) {
      containerRef.current.style.opacity = '0';
      setTimeout(() => {
        if (containerRef.current) {
          containerRef.current.style.transition = 'opacity 0.5s ease-in-out';
          containerRef.current.style.opacity = '1';
        }
      }, 50);
    }
  }, [analysis, loading]);

  // Determine what to display based on loading state and step
  const renderContent = () => {
    if (loading) {
      return (
        <div className="loading-container">
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          {step && (
            <p className="loading-message">
              <span className="material-icons loading-icon" style={{ 
                fontSize: '20px', 
                verticalAlign: 'middle', 
                marginRight: '8px',
                color: 'var(--primary-accent)'
              }}>
                {step === 'retrieval' ? 'search' : 'psychology'}
              </span>
              {step === 'retrieval' ? 'Retrieving relevant documents...' : 'Generating analysis...'}
            </p>
          )}
        </div>
      );
    }

    if (!analysis) {
      return null;
    }

    // Process the markdown and render as HTML
    const processedHtml = processMarkdown(analysis.response);
    
    return (
      <div>
        <div className="analysis-header" style={{
          marginBottom: 'var(--spacing-md)',
          paddingBottom: 'var(--spacing-sm)',
          borderBottom: '1px solid var(--border-color)'
        }}>
          <h3 style={{ 
            fontSize: 'var(--font-size-lg)',
            fontWeight: 'var(--font-weight-bold)',
            color: 'var(--text-color)',
            display: 'flex',
            alignItems: 'center'
          }}>
            <span className="material-icons" style={{ marginRight: '8px', color: 'var(--secondary-accent)' }}>
              analytics
            </span>
            AI Analysis
          </h3>
        </div>
        <div 
          className="analysis-content"
          dangerouslySetInnerHTML={{ __html: processedHtml }} 
        />
      </div>
    );
  };

  return (
    <div 
      className="analysis-container" 
      ref={containerRef}
      style={{
        backgroundColor: 'var(--hover-gray)',
        padding: 'var(--spacing-lg)',
        borderRadius: 'var(--border-radius)',
        boxShadow: 'var(--shadow-sm)',
        transition: 'opacity 0.5s ease-in-out'
      }}
    >
      {renderContent()}
    </div>
  );
};

export default Analysis; 