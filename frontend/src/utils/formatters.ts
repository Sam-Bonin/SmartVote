/**
 * Formats a similarity score as a percentage
 */
export const formatScore = (score: number): string => {
  return `${Math.round(score * 100)}%`;
};

/**
 * Process markdown-like text into HTML with proper formatting
 */
export const processMarkdown = (text: string): string => {
  if (!text) return '';
  
  // First process the raw text to prevent HTML tag splitting
  let processedHtml = text
    // Bold text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Italic text
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // Headers
    .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
    .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
    .replace(/^# (.*?)$/gm, '<h1>$1</h1>');
  
  // Process lists
  const lines = processedHtml.split('\n');
  let inList = false;
  let listType = '';
  
  for (let i = 0; i < lines.length; i++) {
    // Check for bullet list items
    if (lines[i].match(/^- (.*?)$/)) {
      if (!inList || listType !== 'ul') {
        // Start a new list if not in one
        lines[i] = inList ? '</'+listType+'><ul><li>' + lines[i].substring(2) + '</li>' : '<ul><li>' + lines[i].substring(2) + '</li>';
        inList = true;
        listType = 'ul';
      } else {
        // Continue the list
        lines[i] = '<li>' + lines[i].substring(2) + '</li>';
      }
    }
    // Check for numbered list items
    else if (lines[i].match(/^\d+\. (.*?)$/)) {
      if (!inList || listType !== 'ol') {
        // Start a new list if not in one
        lines[i] = inList ? '</'+listType+'><ol><li>' + lines[i].replace(/^\d+\. /, '') + '</li>' : '<ol><li>' + lines[i].replace(/^\d+\. /, '') + '</li>';
        inList = true;
        listType = 'ol';
      } else {
        // Continue the list
        lines[i] = '<li>' + lines[i].replace(/^\d+\. /, '') + '</li>';
      }
    }
    // Not a list item - close list if we were in one
    else if (inList && lines[i].trim() !== '') {
      lines[i] = '</'+listType+'>' + lines[i];
      inList = false;
    }
  }
  
  // Close any open list at the end
  if (inList) {
    lines.push('</'+listType+'>');
  }
  
  // Reassemble the lines
  processedHtml = lines.join('\n');
  
  // Handle paragraphs - split by double newlines
  const paragraphs = processedHtml.split('\n\n');
  processedHtml = paragraphs.map(p => {
    // Skip if already wrapped in a block element
    if (p.trim().startsWith('<h') || p.trim().startsWith('<ul') || 
        p.trim().startsWith('<ol') || p.trim().startsWith('<p')) {
      return p;
    }
    // Otherwise wrap in paragraph tags
    return '<p>' + p + '</p>';
  }).join('\n');
  
  // Replace single newlines with <br> only within paragraphs
  processedHtml = processedHtml.replace(/<p>(.*?)<\/p>/gs, function(match, p1) {
    return '<p>' + p1.replace(/\n/g, '<br>') + '</p>';
  });
  
  return processedHtml;
};

/**
 * Generate delay for staggered animations
 */
export const getAnimationDelay = (index: number): string => {
  const delay = index * 100;
  return `${delay}ms`;
}; 