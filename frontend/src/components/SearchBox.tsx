import React, { useState, FormEvent, useRef, useEffect } from 'react';
import { SearchProps } from '../types';

const SearchBox: React.FC<SearchProps> = ({ onSearch }) => {
  const [searchText, setSearchText] = useState<string>('');
  const [isFocused, setIsFocused] = useState<boolean>(false);
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
    <div className="search-container">
      <form className="search-form" onSubmit={handleSubmit}>
        <div className="search-input-container" style={{ position: 'relative', flex: 1 }}>
          <input
            ref={inputRef}
            type="text"
            className="search-input"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Ask about the Liberal Platform..."
            aria-label="Search query"
          />
          {searchText && (
            <button 
              type="button" 
              onClick={handleClear}
              className="search-clear-button"
              aria-label="Clear search"
              style={{
                position: 'absolute',
                right: '12px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                color: 'var(--text-secondary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <span className="material-icons" style={{ fontSize: '20px' }}>clear</span>
            </button>
          )}
        </div>
        <button 
          type="submit" 
          className="search-button"
          disabled={!searchText.trim()}
        >
          <span className="material-icons" style={{ fontSize: '20px', marginRight: '4px' }}>search</span>
          Search
        </button>
      </form>
    </div>
  );
};

export default SearchBox; 