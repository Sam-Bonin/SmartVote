export interface Document {
  text: string;
  score: number;
  page: number;
  page_num?: number;
  similarity?: number;
}

export interface Analysis {
  response: string;
}

export interface QueryResults {
  analysis?: Analysis;
  similar_documents?: Document[];
}

export interface StreamResponsePartial {
  status: 'partial' | 'processing' | 'complete' | 'error';
  step?: 'retrieval' | 'documents_ready' | 'analysis';
  similar_documents?: Document[];
  analysis?: Analysis;
  message?: string;
  padding?: string;
}

export interface Topic {
  title: string;
  query: string;
}

export interface SearchProps {
  onSearch: (query: string) => void;
}

export interface SidebarProps {
  onTopicSelect: (query: string) => void;
  className?: string;
}

export interface ResultsProps {
  query: string;
  results: QueryResults | null;
  loading: boolean;
  step: string | null;
}

export interface EvidenceCardProps {
  document: Document;
  index: number;
}

export interface PdfViewerProps {
  page: number;
  isVisible: boolean;
} 