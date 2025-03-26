import { useState } from 'react';
import { QueryResults, StreamResponsePartial } from '../types';

/**
 * Custom hook to handle query submission and streaming responses
 */
export const useQuery = () => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<QueryResults | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [step, setStep] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submitQuery = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    
    // Update state
    setQuery(searchQuery);
    setLoading(true);
    setResults(null);
    setError(null);
    setStep('retrieval');
    
    try {
      const response = await fetch('/query-stream', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ text: searchQuery }),
        cache: 'no-store',
        credentials: 'same-origin',
        mode: 'cors',
        redirect: 'follow',
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error("API Error:", errorText);
        throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
      }
      
      // Set up reader for streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      
      if (!reader) {
        throw new Error("Response body reader could not be created");
      }
      
      // Process the stream
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }
        
        // Decode and process the chunk
        buffer += decoder.decode(value, { stream: true });
        
        // Process complete lines
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep the last incomplete line in the buffer
        
        for (const line of lines) {
          if (line.trim() === '') continue;
          
          try {
            const data = JSON.parse(line) as StreamResponsePartial;
            console.log("Received streaming data:", data);
            
            // Handle different response types
            if (data.status === 'partial' && data.step === 'documents_ready' && data.similar_documents) {
              // Update results with documents
              setResults(prev => ({
                ...prev,
                similar_documents: data.similar_documents
              }));
            } 
            else if (data.status === 'complete' && data.analysis) {
              // Update results with analysis and complete
              setResults(prev => ({
                ...prev,
                analysis: data.analysis
              }));
              setLoading(false);
              setStep(null);
            } 
            else if (data.status === 'processing' && data.step) {
              // Update processing step
              setStep(data.step);
            } 
            else if (data.status === 'error') {
              throw new Error(data.message || 'Unknown error');
            }
          } catch (error) {
            console.error("Error parsing streaming data:", error);
            if (error instanceof Error) {
              setError(error.message);
            } else {
              setError('Unknown error occurred');
            }
          }
        }
      }
    } catch (error) {
      console.error('Query error:', error);
      setLoading(false);
      setStep(null);
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('Unknown error occurred');
      }
    }
  };

  const clearResults = () => {
    setResults(null);
    setQuery('');
    setStep(null);
    setLoading(false);
    setError(null);
  };

  return {
    query,
    results,
    loading,
    step,
    error,
    submitQuery,
    clearResults
  };
}; 