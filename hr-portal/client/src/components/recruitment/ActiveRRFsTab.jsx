import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Grid,
  Chip,
  Button,
  IconButton,
  Menu,
  MenuItem,
  LinearProgress,
  Tooltip,
  Avatar,
  AvatarGroup
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  Person as PersonIcon,
  Badge as BadgeIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Description as DescriptionIcon
} from '@mui/icons-material';

const ActiveRRFsTab = ({ onRefresh }) => {
  const [rrfs, setRRFs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedRRF, setSelectedRRF] = useState(null);

  useEffect(() => {
    fetchActiveRRFs();
  }, []);

  const fetchActiveRRFs = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/recruitment/rrf/active');
      const data = await response.json();
      setRRFs(data);
    } catch (error) {
      console.error('Error fetching RRFs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMenuOpen = (event, rrf) => {
    setAnchorEl(event.currentTarget);
    setSelectedRRF(rrf);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedRRF(null);
  };

  const getUrgencyColor = (urgency) => {
    const colors = {
      'Critical': '#e74c3c',
      'High': '#f39c12',
      'Normal': '#3498db',
      'Low': '#95a5a6'
    };
    return colors[urgency] || '#95a5a6';
  };

  const getStatusColor = (status) => {
    const colors = {
      'Approved': '#2ecc71',
      'Pending': '#f39c12',
      'Rejected': '#e74c3c'
    };
    return colors[status] || '#95a5a6';
  };

  if (loading) {
    return <LinearProgress />;
  }

  if (rrfs.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <DescriptionIcon sx={{ fontSize: 64, color: '#bdc3c7', mb: 2 }} />
        <Typography variant="h6" color="text.secondary">
          No active recruitment requests
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Click "Create New RRF" to get started
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {rrfs.map((rrf) => (
          <Grid item xs={12} md={6} lg={4} key={rrf.id}>
            <Card
              elevation={0}
              sx={{
                border: '1px solid #e0e0e0',
                borderRadius: 2,
                transition: 'all 0.3s ease',
                '&:hover': {
                  boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                  transform: 'translateY(-4px)'
                }
              }}
            >
              <CardContent>
                {/* Header */}
                <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 2 }}>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5, color: '#2c3e50' }}>
                      {rrf.job_title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {rrf.department}
                    </Typography>
                  </Box>
                  <IconButton
                    size="small"
                    onClick={(e) => handleMenuOpen(e, rrf)}
                  >
                    <MoreVertIcon />
                  </IconButton>
                </Box>

                {/* RRF Number & Entity */}
                <Box sx={{ mb: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Chip
                    label={rrf.rrf_number}
                    size="small"
                    sx={{ fontWeight: 500, fontSize: '0.75rem' }}
                  />
                  <Chip
                    label={rrf.entity}
                    size="small"
                    variant="outlined"
                  />
                </Box>

                {/* Location & Salary */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" sx={{ mb: 0.5 }}>
                    📍 {rrf.location}
                  </Typography>
                  {rrf.salary_range && (
                    <Typography variant="body2" sx={{ color: '#2ecc71', fontWeight: 500 }}>
                      💰 {rrf.salary_range}
                    </Typography>
                  )}
                </Box>

                {/* Status Chips */}
                <Box sx={{ mb: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <Chip
                    label={rrf.status}
                    size="small"
                    sx={{
                      backgroundColor: getStatusColor(rrf.status) + '15',
                      color: getStatusColor(rrf.status),
                      fontWeight: 500
                    }}
                  />
                  <Chip
                    label={rrf.hiring_urgency}
                    size="small"
                    sx={{
                      backgroundColor: getUrgencyColor(rrf.hiring_urgency) + '15',
                      color: getUrgencyColor(rrf.hiring_urgency),
                      fontWeight: 500
                    }}
                  />
                  {rrf.jd_status === 'Uploaded' && (
                    <Chip
                      label="JD Attached"
                      size="small"
                      icon={<DescriptionIcon />}
                      sx={{ backgroundColor: '#e3f2fd', color: '#1976d2' }}
                    />
                  )}
                </Box>

                {/* Candidates Pipeline */}
                {rrf.candidates_count > 0 && (
                  <Box sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 2,
                    p: 1.5,
                    backgroundColor: '#f8f9fa',
                    borderRadius: 1,
                    mb: 2
                  }}>
                    <AvatarGroup max={3} sx={{ '& .MuiAvatar-root': { width: 28, height: 28, fontSize: '0.875rem' } }}>
                      {[...Array(Math.min(rrf.candidates_count, 3))].map((_, i) => (
                        <Avatar key={i} sx={{ bgcolor: '#667eea' }}>
                          <PersonIcon sx={{ fontSize: 16 }} />
                        </Avatar>
                      ))}
                    </AvatarGroup>
                    <Typography variant="body2" color="text.secondary">
                      {rrf.candidates_count} {rrf.candidates_count === 1 ? 'candidate' : 'candidates'} in pipeline
                    </Typography>
                  </Box>
                )}

                {/* Requested Date */}
                <Typography variant="caption" color="text.secondary">
                  Requested: {new Date(rrf.request_date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                  })}
                </Typography>
              </CardContent>

              <CardActions sx={{ borderTop: '1px solid #f0f0f0', px: 2, py: 1.5 }}>
                <Button
                  size="small"
                  startIcon={<BadgeIcon />}
                  sx={{ textTransform: 'none' }}
                >
                  Generate Hiring Manager Pass
                </Button>
                <Button
                  size="small"
                  startIcon={<VisibilityIcon />}
                  sx={{ ml: 'auto', textTransform: 'none' }}
                >
                  View Details
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>
          <VisibilityIcon sx={{ mr: 1, fontSize: 20 }} />
          View Details
        </MenuItem>
        <MenuItem onClick={handleMenuClose}>
          <EditIcon sx={{ mr: 1, fontSize: 20 }} />
          Edit RRF
        </MenuItem>
        <MenuItem onClick={handleMenuClose}>
          <BadgeIcon sx={{ mr: 1, fontSize: 20 }} />
          Generate Pass
        </MenuItem>
        <MenuItem onClick={handleMenuClose} sx={{ color: '#e74c3c' }}>
          <DeleteIcon sx={{ mr: 1, fontSize: 20 }} />
          Close Position
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default ActiveRRFsTab;
