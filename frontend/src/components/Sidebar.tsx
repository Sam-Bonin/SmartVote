import React, { useState } from 'react';
import { SidebarProps, Topic } from '../types';
import { List, ListItemButton, ListItemIcon, ListItemText, Typography, Box, Paper, Divider } from '@mui/material';
import { 
  Nature as Eco, 
  Home, 
  LocalHospital, 
  TrendingUp, 
  People, 
  Public, 
  School, 
  AttachMoney as Paid, 
  Category, 
  Topic as TopicIcon, 
  Info, 
  HowToVote 
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const Sidebar: React.FC<SidebarProps> = ({ onTopicSelect }) => {
  const [activeTopic, setActiveTopic] = useState<string | null>(null);

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
  const getTopicIcon = (topic: string) => {
    switch (topic.toLowerCase()) {
      case 'climate change': return <Eco />;
      case 'housing crisis': return <Home />;
      case 'healthcare': return <LocalHospital />;
      case 'economic growth': return <TrendingUp />;
      case 'indigenous reconciliation': return <People />;
      case 'immigration': return <Public />;
      case 'education': return <School />;
      case 'taxes': return <Paid />;
      default: return <Category />;
    }
  };

  return (
    <Box sx={{ 
      height: '100%',
      display: 'flex', 
      flexDirection: 'column',
      p: 2,
      overflow: 'auto'
    }}>
      <Box 
        sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          mb: 4,
          pl: 1
        }}
      >
        <motion.div
          whileHover={{ rotate: 10 }}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 260, damping: 20 }}
        >
          <Box 
            sx={{ 
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: 'primary.main',
              color: 'white',
              width: 48,
              height: 48,
              borderRadius: '50%',
              mr: 2,
              boxShadow: 2
            }}
          >
            <HowToVote fontSize="large" />
          </Box>
        </motion.div>
        
        <Typography 
          variant="h5" 
          sx={{ 
            fontWeight: 'bold', 
            color: 'primary.main',
            letterSpacing: '-0.5px'
          }}
        >
          SmartVote
        </Typography>
      </Box>
      
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, pl: 1 }}>
          <TopicIcon fontSize="small" sx={{ mr: 1, color: 'text.secondary' }} />
          <Typography 
            variant="subtitle1" 
            sx={{ 
              fontWeight: 600, 
              color: 'text.primary' 
            }}
          >
            Popular Topics
          </Typography>
        </Box>
        
        <List sx={{ px: 0 }}>
          {topics.map((topic, index) => (
            <motion.div
              key={index}
              whileHover={{ x: 4 }}
              whileTap={{ scale: 0.98 }}
            >
              <ListItemButton
                selected={activeTopic === topic.title}
                onClick={() => handleTopicClick(topic.query, index)}
                sx={{
                  borderRadius: 1,
                  mb: 0.5,
                  transition: 'all 0.2s',
                  '&.Mui-selected': {
                    bgcolor: 'rgba(230, 57, 70, 0.1)',
                    borderLeft: 3,
                    borderColor: 'primary.main',
                    '& .MuiListItemIcon-root': {
                      color: 'primary.main',
                    },
                    '& .MuiListItemText-primary': {
                      fontWeight: 'medium',
                      color: 'text.primary',
                    },
                  },
                  '&:hover': {
                    bgcolor: activeTopic === topic.title 
                      ? 'rgba(230, 57, 70, 0.15)' 
                      : 'action.hover',
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 40, color: 'text.secondary' }}>
                  {getTopicIcon(topic.title)}
                </ListItemIcon>
                <ListItemText 
                  primary={topic.title}
                  primaryTypographyProps={{
                    fontWeight: activeTopic === topic.title ? 'medium' : 'regular'
                  }}
                />
              </ListItemButton>
            </motion.div>
          ))}
        </List>
      </Box>
      
      <Box sx={{ mt: 'auto', pt: 2 }}>
        <Divider sx={{ mb: 2 }} />
        <Paper 
          elevation={0}
          sx={{ 
            p: 2, 
            bgcolor: 'rgba(0,0,0,0.03)', 
            borderRadius: 2
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
            <Info fontSize="small" sx={{ mr: 1, mt: 0.3, color: 'text.secondary' }} />
            <Typography variant="body2" color="text.secondary">
              Ask any question about the Liberal Party platform to get AI-powered analysis
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default Sidebar; 