import React, { useState } from 'react';
import { SidebarProps, Topic } from '../types';

const Sidebar: React.FC<SidebarProps> = ({ onTopicSelect, className = '' }) => {
  const [activeTopic, setActiveTopic] = useState<string | null>(null);
  const [hoveredTopic, setHoveredTopic] = useState<string | null>(null);

  // Predefined topics with queries
  const topics: Topic[] = [
    { title: "Climate Change", query: "What is the Liberal plan for climate change?" },
    { title: "Housing Crisis", query: "How will Liberals address the housing crisis?" },
    { title: "Healthcare", query: "What are the Liberal healthcare policies?" },
    { title: "Economic Growth", query: "What is the Liberal plan for economic growth?" },
    { title: "Indigenous Reconciliation", query: "What is the Liberal approach to Indigenous reconciliation?" },
    { title: "Immigration", query: "What is the Liberal immigration policy?" },
    { title: "Education", query: "What are the Liberal education policies?" },
    { title: "Taxes", query: "What tax changes are Liberals proposing?" }
  ];

  const handleTopicClick = (query: string, index: number) => {
    setActiveTopic(topics[index].title);
    onTopicSelect(query);
  };

  // Generate a relevant icon for each topic
  const getTopicIcon = (topic: string): string => {
    switch (topic.toLowerCase()) {
      case 'climate change': return 'eco';
      case 'housing crisis': return 'home';
      case 'healthcare': return 'medical_services';
      case 'economic growth': return 'trending_up';
      case 'indigenous reconciliation': return 'people';
      case 'immigration': return 'public';
      case 'education': return 'school';
      case 'taxes': return 'paid';
      default: return 'category';
    }
  };

  return (
    <div className={`sidebar ${className}`}>
      <div className="sidebar-header">
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          backgroundColor: 'var(--primary-accent)',
          color: 'white',
          width: '48px',
          height: '48px',
          borderRadius: '50%',
          marginRight: '12px'
        }}>
          <span className="material-icons" style={{ fontSize: '28px' }}>how_to_vote</span>
        </div>
        <h1 className="sidebar-title">SmartVote</h1>
      </div>
      
      <div className="topics-container">
        <h2 className="topics-title">
          <span className="material-icons" style={{ 
            fontSize: '20px', 
            verticalAlign: 'middle', 
            marginRight: '8px',
            color: 'var(--text-secondary)'
          }}>
            topic
          </span>
          Popular Topics
        </h2>
        <ul className="topics-list">
          {topics.map((topic, index) => (
            <li 
              key={index}
              className={`topic-item ${activeTopic === topic.title ? 'active' : ''}`}
              onClick={() => handleTopicClick(topic.query, index)}
              onMouseEnter={() => setHoveredTopic(topic.title)}
              onMouseLeave={() => setHoveredTopic(null)}
              style={{
                display: 'flex',
                alignItems: 'center',
                backgroundColor: hoveredTopic === topic.title ? 
                  (activeTopic === topic.title ? 'var(--active-background)' : 'var(--border-color)') : 
                  (activeTopic === topic.title ? 'var(--active-background)' : 'var(--hover-gray)'),
                transition: 'background-color 0.2s ease'
              }}
            >
              <span className="material-icons" style={{ 
                marginRight: '12px',
                color: activeTopic === topic.title ? 'var(--primary-accent)' : 'var(--text-secondary)'
              }}>
                {getTopicIcon(topic.title)}
              </span>
              {topic.title}
            </li>
          ))}
        </ul>
      </div>
      
      <div style={{ 
        marginTop: 'var(--spacing-xl)', 
        padding: 'var(--spacing-md)',
        borderRadius: 'var(--border-radius)',
        backgroundColor: 'var(--hover-gray)',
        fontSize: 'var(--font-size-sm)',
        color: 'var(--text-secondary)'
      }}>
        <p style={{ display: 'flex', alignItems: 'center' }}>
          <span className="material-icons" style={{ fontSize: '16px', marginRight: '8px' }}>info</span>
          Ask any question about the Liberal Party platform
        </p>
      </div>
    </div>
  );
};

export default Sidebar; 