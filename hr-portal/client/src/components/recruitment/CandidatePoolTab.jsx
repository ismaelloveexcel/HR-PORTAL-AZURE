import React from 'react';
import { Box, Typography } from '@mui/material';
import { People as PeopleIcon } from '@mui/icons-material';

const CandidatePoolTab = () => {
  return (
    <Box sx={{ textAlign: 'center', py: 8 }}>
      <PeopleIcon sx={{ fontSize: 64, color: '#bdc3c7', mb: 2 }} />
      <Typography variant="h6" color="text.secondary">
        Candidate Pool Coming Soon
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Search and match candidates from your talent pool
      </Typography>
    </Box>
  );
};

export default CandidatePoolTab;
