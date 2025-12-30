import React from 'react';
import { Box, Typography } from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';

const ExternalSubmissionsTab = ({ onRefresh }) => {
  return (
    <Box sx={{ textAlign: 'center', py: 8 }}>
      <CloudUploadIcon sx={{ fontSize: 64, color: '#bdc3c7', mb: 2 }} />
      <Typography variant="h6" color="text.secondary">
        External Submissions Coming Soon
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Review candidate submissions from external recruiters and agencies
      </Typography>
    </Box>
  );
};

export default ExternalSubmissionsTab;
