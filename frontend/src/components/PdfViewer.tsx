import React, { useState, useEffect, useRef } from 'react';
import { PdfViewerProps } from '../types';

const PdfViewer: React.FC<PdfViewerProps> = ({ page, isVisible }) => {
  const [expanded, setExpanded] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Toggle expanded state
  const toggleExpanded = () => {
    setExpanded(!expanded);
    if (!expanded) {
      setLoading(true);
    }
  };

  // Update PDF source when page changes or when expanded
  useEffect(() => {
    if (iframeRef.current && (expanded || isVisible)) {
      iframeRef.current.src = `/data/Liberal.pdf#page=${page}`;
    }
  }, [page, expanded, isVisible]);

  // Handle iframe load event
  const handleIframeLoad = () => {
    setLoading(false);
  };

  return (
    <div 
      id="pdfSection" 
      className={`pdf-section ${expanded ? 'expanded' : ''}`}
      style={{
        transition: 'box-shadow 0.3s ease',
        boxShadow: expanded ? 'var(--shadow-md)' : 'var(--shadow-sm)'
      }}
    >
      <div 
        id="pdfHeader" 
        className="pdf-header" 
        onClick={toggleExpanded}
        style={{
          cursor: 'pointer',
          transition: 'background-color 0.2s ease',
          backgroundColor: expanded ? 'var(--active-background)' : 'var(--hover-gray)',
          borderLeft: expanded ? '4px solid var(--primary-accent)' : 'none',
          paddingLeft: expanded ? 'calc(var(--spacing-lg) - 4px)' : 'var(--spacing-lg)'
        }}
      >
        <h2 className="pdf-title">
          <span id="pdfTitleText">
            <span className="material-icons" style={{ fontSize: '20px', verticalAlign: 'middle', marginRight: '8px' }}>
              picture_as_pdf
            </span>
            PDF Page {page}
          </span>
        </h2>
        <span className="material-icons expand-icon" style={{ transition: 'transform 0.3s ease' }}>
          {expanded ? 'expand_less' : 'expand_more'}
        </span>
      </div>
      <div 
        id="pdfViewerContainer" 
        ref={containerRef}
        className={`pdf-viewer-container ${expanded ? 'expanded' : ''}`}
        style={{
          height: expanded ? '600px' : '0',
          transition: 'height 0.3s ease',
          overflow: 'hidden',
          position: 'relative'
        }}
      >
        {loading && expanded && (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'var(--background-color)',
            zIndex: 1
          }}>
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <iframe 
          id="pdfViewer"
          ref={iframeRef}
          className="pdf-frame" 
          title="Liberal Party Platform PDF"
          onLoad={handleIframeLoad}
          style={{ 
            width: '100%', 
            height: '100%',
            border: 'none',
            opacity: loading ? 0 : 1,
            transition: 'opacity 0.3s ease'
          }}
        />
      </div>
    </div>
  );
};

export default PdfViewer; 