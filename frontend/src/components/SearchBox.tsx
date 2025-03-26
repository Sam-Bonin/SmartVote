import React, { useState, FormEvent, useRef, useEffect } from 'react';
import { SearchProps } from '../types';
import { TextField, Button, InputAdornment, Box, Paper } from '@mui/material';
import { Search as SearchIcon, Clear as ClearIcon } from '@mui/icons-material';
import { motion } from 'framer-motion';

const SearchBox: React.FC<SearchProps> = ({ onSearch }) => {
  const [searchText, setSearchText] = useState<string>('');
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus the input when component mounts
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (searchText.trim()) {
      onSearch(searchText);
    }
  };

  const handleClear = () => {
    setSearchText('');
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Paper 
        elevation={2}
        sx={{ 
          p: 3, 
          mb: 4,
          borderRadius: 2,
          background: 'white',
        }}
      >
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            inputRef={inputRef}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="Ask about the Liberal Platform..."
            variant="outlined"
            sx={{ 
              '& .MuiOutlinedInput-root': {
                transition: 'all 0.3s ease',
                '&:hover, &.Mui-focused': {
                  '& fieldset': {
                    borderColor: 'primary.main',
                    borderWidth: '2px',
                  },
                },
              },
            }}
            InputProps={{
              endAdornment: searchText ? (
                <InputAdornment position="end">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    exit={{ scale: 0 }}
                  >
                    <Button 
                      onClick={handleClear}
                      size="small"
                      sx={{ minWidth: 'auto', p: 0.5 }}
                    >
                      <ClearIcon fontSize="small" />
                    </Button>
                  </motion.div>
                </InputAdornment>
              ) : null,
            }}
          />
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              type="submit"
              variant="contained"
              color="secondary"
              disabled={!searchText.trim()}
              disableElevation
              sx={{ 
                px: 3,
                height: '100%',
                whiteSpace: 'nowrap',
              }}
              startIcon={<SearchIcon />}
            >
              Search
            </Button>
          </motion.div>
        </Box>
      </Paper>
    </motion.div>
  );
};

export default SearchBox; 