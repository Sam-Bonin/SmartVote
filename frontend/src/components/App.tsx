import React, { useState, useEffect } from 'react';
import SearchBox from './SearchBox';
import Sidebar from './Sidebar';
import Results from './Results';
import { useQuery } from '../hooks/useQuery';
import { Box, Container, AppBar, Toolbar, IconButton, Typography, useMediaQuery, 
  useTheme, Drawer, Alert, Paper } from '@mui/material';
import { Menu as MenuIcon, Close as CloseIcon, SearchOutlined } from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const App: React.FC = () => {
  const [menuOpen, setMenuOpen] = useState<boolean>(false);
  const { query, results, loading, step, error, submitQuery } = useQuery();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Close menu when clicking outside on mobile
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (isMobile && menuOpen) {
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
  }, [menuOpen, isMobile]);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const handleSearch = (searchQuery: string) => {
    submitQuery(searchQuery);
    
    // Close sidebar on mobile after search
    if (isMobile) {
      setMenuOpen(false);
    }
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Mobile App Bar */}
      {isMobile && (
        <AppBar 
          position="fixed" 
          color="inherit" 
          elevation={1}
          sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
        >
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={toggleMenu}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ color: 'primary.main', fontWeight: 'bold' }}>
              SmartVote
            </Typography>
          </Toolbar>
        </AppBar>
      )}

      {/* Sidebar */}
      <Drawer
        variant={isMobile ? "temporary" : "permanent"}
        open={isMobile ? menuOpen : true}
        onClose={() => setMenuOpen(false)}
        sx={{
          width: 280,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: 280,
            boxSizing: 'border-box',
            border: 'none',
            boxShadow: isMobile ? 3 : 1,
          },
        }}
      >
        {isMobile && (
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 1 }}>
            <IconButton onClick={() => setMenuOpen(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        )}
        <Sidebar onTopicSelect={handleSearch} />
      </Drawer>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: '100%',
          maxWidth: '1200px',
          mx: 'auto',
          mt: isMobile ? 8 : 0, // Add margin top for mobile to account for AppBar
        }}
      >
        <Container maxWidth="xl">
          {/* Search Box */}
          <SearchBox onSearch={handleSearch} />
          
          {/* Error message if there's an error */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Alert 
                  severity="error" 
                  variant="filled"
                  sx={{ mb: 3 }}
                >
                  {error} - Please make sure the server is running and the embeddings file exists.
                </Alert>
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Placeholder when no results */}
          <AnimatePresence>
            {!query && !loading && !error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.5 }}
              >
                <Paper 
                  elevation={0}
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    p: 4,
                    textAlign: 'center',
                    bgcolor: 'transparent',
                    my: 6
                  }}
                >
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 0.7 }}
                    transition={{ delay: 0.2, duration: 0.5 }}
                  >
                    <SearchOutlined 
                      sx={{ 
                        fontSize: 80, 
                        color: 'text.secondary',
                        mb: 2,
                        opacity: 0.7
                      }} 
                    />
                  </motion.div>
                  
                  <Typography variant="h4" sx={{ mb: 2, fontWeight: 'medium' }}>
                    Start exploring the Liberal Party Platform
                  </Typography>
                  
                  <Typography variant="body1" color="text.secondary">
                    Enter a query in the search box above or select a topic from the sidebar
                  </Typography>
                </Paper>
              </motion.div>
            )}
          </AnimatePresence>
          
          {/* Results display */}
          <AnimatePresence>
            {(query || loading) && !error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Results 
                  query={query}
                  results={results}
                  loading={loading}
                  step={step}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </Container>
      </Box>
    </Box>
  );
};

export default App; 