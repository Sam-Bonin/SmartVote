import React from 'react';
import { EvidenceCardProps } from '../types';
import { formatScore } from '../utils/formatters';
import { Card, CardContent, Typography, Button, Chip, Box, Divider } from '@mui/material';
import { Description, ThumbUp, ThumbsUpDown, Visibility } from '@mui/icons-material';
import { motion } from 'framer-motion';

const EvidenceCard: React.FC<EvidenceCardProps> = ({ document, index }) => {
  // Calculate confidence level for visual indicator
  const confidenceLevel = () => {
    if (document.score >= 0.9) return 'success';
    if (document.score >= 0.7) return 'warning';
    return 'default';
  };
  
  // Get confidence icon
  const confidenceIcon = () => {
    return document.score >= 0.8 ? <ThumbUp fontSize="small" /> : <ThumbsUpDown fontSize="small" />;
  };

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

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
    >
      <Card 
        elevation={2}
        sx={{ 
          height: '100%', 
          display: 'flex', 
          flexDirection: 'column',
          transition: 'box-shadow 0.3s ease',
          '&:hover': {
            boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          },
        }}
      >
        <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          <Typography variant="body1" component="div" sx={{ mb: 2, flexGrow: 1 }}>
            {document.text}
          </Typography>
          
          <Divider sx={{ my: 2 }} />
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Chip
              icon={<Description fontSize="small" />}
              label={`PDF Page ${document.page}`}
              size="small"
              variant="outlined"
            />
            
            <Chip
              icon={confidenceIcon()}
              label={`${formatScore(document.score)} match`}
              size="small"
              color={confidenceLevel()}
              variant="outlined"
            />
          </Box>
          
          <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
            <Button
              variant="outlined"
              color="secondary"
              startIcon={<Visibility />}
              onClick={handleViewPage}
              fullWidth
              sx={{ mt: 1 }}
            >
              View Page
            </Button>
          </motion.div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default EvidenceCard; 