import React, { useState } from 'react';
import { EvidenceCardProps } from '../types';
import { formatScore, getAnimationDelay } from '../utils/formatters';

const EvidenceCard: React.FC<EvidenceCardProps> = ({ document, index }) => {
  const [isHovered, setIsHovered] = useState<boolean>(false);
  
  const handleViewPage = () => {
    // Create URL for the PDF page
    const pdfUrl = `/data/Liberal.pdf#page=${document.page}`;
    
    // Update PDF viewer if it exists on page
    const pdfViewer = window.document.getElementById('pdfViewer') as HTMLIFrameElement | null;
    const pdfTitleText = window.document.getElementById('pdfTitleText');
    const pdfViewerContainer = window.document.getElementById('pdfViewerContainer');
    const pdfSection = window.document.getElementById('pdfSection');
    
    if (pdfViewer && pdfTitleText && pdfViewerContainer && pdfSection) {
      // Update the PDF source
      pdfViewer.src = pdfUrl;
      
      // Update title
      pdfTitleText.textContent = `PDF Page ${document.page}`;
      
      // Expand the viewer if it's not already expanded
      if (!pdfViewerContainer.classList.contains('expanded')) {
        pdfViewerContainer.classList.add('expanded');
        pdfSection.classList.add('expanded');
      }
      
      // Scroll to the PDF viewer
      pdfSection.scrollIntoView({ behavior: 'smooth' });
    } else {
      // Fallback to opening in a new tab if viewer not available
      window.open(pdfUrl, '_blank');
    }
  };

  // Calculate confidence level for visual indicator
  const confidenceLevel = () => {
    if (document.score >= 0.9) return 'high';
    if (document.score >= 0.7) return 'medium';
    return 'low';
  };
  
  // Get confidence color
  const confidenceColor = () => {
    switch (confidenceLevel()) {
      case 'high': return 'var(--tertiary-accent)';
      case 'medium': return '#F59E0B'; // Amber
      case 'low': return 'var(--text-secondary)';
      default: return 'var(--text-secondary)';
    }
  };

  return (
    <div 
      className="evidence-card" 
      style={{ 
        animationDelay: getAnimationDelay(index),
        boxShadow: isHovered ? 'var(--shadow-md)' : 'var(--shadow-sm)',
        transform: isHovered ? 'translateY(-2px)' : 'translateY(0)'
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <p className="document-text">{document.text}</p>
      <div className="document-meta">
        <div className="document-page">
          <span className="material-icons" style={{ fontSize: '16px' }}>description</span>
          <span>PDF Page {document.page}</span>
        </div>
        <div className="document-score" style={{ color: confidenceColor() }}>
          <span className="material-icons" style={{ fontSize: '16px' }}>
            {document.score >= 0.8 ? 'thumb_up' : 'thumbs_up_down'}
          </span>
          <span>{formatScore(document.score)} match</span>
        </div>
      </div>
      <div className="document-actions">
        <button 
          className="view-page-button" 
          onClick={handleViewPage}
          style={{
            transform: isHovered ? 'scale(1.025)' : 'scale(1)',
            transition: 'transform 0.2s ease'
          }}
        >
          <span className="material-icons" style={{ fontSize: '16px', marginRight: '4px' }}>visibility</span>
          View Page
        </button>
      </div>
    </div>
  );
};

export default EvidenceCard; 