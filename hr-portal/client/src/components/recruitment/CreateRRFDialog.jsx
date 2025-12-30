import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  MenuItem,
  Typography,
  Box,
  Chip,
  Alert,
  CircularProgress,
  IconButton,
  Divider
} from '@mui/material';
import {
  Close as CloseIcon,
  CloudUpload as CloudUploadIcon,
  AutoAwesome as AutoAwesomeIcon
} from '@mui/icons-material';

const CreateRRFDialog = ({ open, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    entity: 'Baynunah',
    department: '',
    jobTitle: '',
    reasonForHiring: '',
    replacingWhom: '',
    location: 'Abu Dhabi',
    salaryRange: '',
    hiringUrgency: 'Normal',
    requiredSkills: '',
    jobDescription: '',
    jdStatus: 'Missing'
  });

  const [jdFile, setJdFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const entities = [
    'Baynunah',
    'Baynunah Watergeneration Technologies SP LLC',
    'Company B',
    'Company C'
  ];

  const urgencyLevels = [
    { value: 'Critical', label: 'Critical (< 2 weeks)', color: '#e74c3c' },
    { value: 'High', label: 'High (2-4 weeks)', color: '#f39c12' },
    { value: 'Normal', label: 'Normal (4-8 weeks)', color: '#3498db' },
    { value: 'Low', label: 'Low (> 8 weeks)', color: '#95a5a6' }
  ];

  const handleChange = (field) => (event) => {
    setFormData({ ...formData, [field]: event.target.value });
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setJdFile(file);
      setFormData({ ...formData, jdStatus: 'Uploaded' });
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      // Validate required fields
      if (!formData.jobTitle || !formData.department) {
        throw new Error('Please fill in all required fields');
      }

      // Create FormData for file upload
      const submitData = new FormData();
      submitData.append('data', JSON.stringify(formData));
      if (jdFile) {
        submitData.append('jd_file', jdFile);
      }

      const response = await fetch('/api/recruitment/rrf/create', {
        method: 'POST',
        body: submitData
      });

      if (!response.ok) {
        throw new Error('Failed to create RRF');
      }

      const result = await response.json();

      // Reset form
      setFormData({
        entity: 'Baynunah',
        department: '',
        jobTitle: '',
        reasonForHiring: '',
        replacingWhom: '',
        location: 'Abu Dhabi',
        salaryRange: '',
        hiringUrgency: 'Normal',
        requiredSkills: '',
        jobDescription: '',
        jdStatus: 'Missing'
      });
      setJdFile(null);

      // Call success callback
      onSuccess(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAutoFillJD = async () => {
    if (!formData.jobTitle) {
      setError('Please enter a job title first');
      return;
    }

    setLoading(true);
    try {
      // Call auto-fill API (uses open-source templates, NOT AI)
      const response = await fetch('/api/recruitment/rrf/auto-fill-jd', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jobTitle: formData.jobTitle,
          department: formData.department
        })
      });

      const data = await response.json();
      setFormData({
        ...formData,
        jobDescription: data.jobDescription,
        requiredSkills: data.requiredSkills,
        jdStatus: 'Auto-filled'
      });
    } catch (err) {
      setError('Failed to auto-fill job description');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 2,
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)'
        }
      }}
    >
      <DialogTitle sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        pb: 2
      }}>
        <Typography variant="h5" sx={{ fontWeight: 600, color: '#2c3e50' }}>
          Create Recruitment Request
        </Typography>
        <IconButton onClick={onClose} size="small">
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <Divider />

      <DialogContent sx={{ pt: 3 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* Entity */}
          <Grid item xs={12} sm={6}>
            <TextField
              select
              fullWidth
              label="Entity / Company"
              value={formData.entity}
              onChange={handleChange('entity')}
              required
            >
              {entities.map((entity) => (
                <MenuItem key={entity} value={entity}>
                  {entity}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          {/* Department */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Department / Division"
              value={formData.department}
              onChange={handleChange('department')}
              required
              placeholder="e.g., Engineering / R&D"
            />
          </Grid>

          {/* Job Title */}
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Job Title"
              value={formData.jobTitle}
              onChange={handleChange('jobTitle')}
              required
              placeholder="e.g., Electronics Engineer"
            />
          </Grid>

          {/* Reason for Hiring */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Reason for Hiring"
              value={formData.reasonForHiring}
              onChange={handleChange('reasonForHiring')}
              placeholder="e.g., Expansion, Replacement"
            />
          </Grid>

          {/* Replacing Whom */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Replacing Whom (if applicable)"
              value={formData.replacingWhom}
              onChange={handleChange('replacingWhom')}
              placeholder="Employee name or N/A"
            />
          </Grid>

          {/* Location */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Location"
              value={formData.location}
              onChange={handleChange('location')}
            />
          </Grid>

          {/* Salary Range */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Salary Range"
              value={formData.salaryRange}
              onChange={handleChange('salaryRange')}
              placeholder="e.g., 15,000 - 20,000 AED"
            />
          </Grid>

          {/* Hiring Urgency */}
          <Grid item xs={12}>
            <TextField
              select
              fullWidth
              label="Hiring Urgency"
              value={formData.hiringUrgency}
              onChange={handleChange('hiringUrgency')}
            >
              {urgencyLevels.map((level) => (
                <MenuItem key={level.value} value={level.value}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: '50%',
                        backgroundColor: level.color
                      }}
                    />
                    {level.label}
                  </Box>
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <Divider sx={{ my: 1 }}>
              <Chip label="Job Description" />
            </Divider>
          </Grid>

          {/* Required Skills */}
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Required Skills"
              value={formData.requiredSkills}
              onChange={handleChange('requiredSkills')}
              multiline
              rows={2}
              placeholder="e.g., Circuit design, embedded systems, PCB tools..."
              helperText="Separate skills with commas"
            />
          </Grid>

          {/* Job Description */}
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
              <Typography variant="body2" color="text.secondary">
                Job Description
              </Typography>
              <Button
                size="small"
                startIcon={<AutoAwesomeIcon />}
                onClick={handleAutoFillJD}
                disabled={loading || !formData.jobTitle}
                sx={{ ml: 'auto' }}
              >
                Auto-fill
              </Button>
            </Box>
            <TextField
              fullWidth
              multiline
              rows={6}
              value={formData.jobDescription}
              onChange={handleChange('jobDescription')}
              placeholder="Paste full job description or use Auto-fill..."
            />
          </Grid>

          {/* Upload JD File */}
          <Grid item xs={12}>
            <Box sx={{
              border: '2px dashed #e0e0e0',
              borderRadius: 2,
              p: 3,
              textAlign: 'center',
              backgroundColor: '#fafafa'
            }}>
              <input
                accept=".pdf,.doc,.docx"
                style={{ display: 'none' }}
                id="jd-file-upload"
                type="file"
                onChange={handleFileUpload}
              />
              <label htmlFor="jd-file-upload">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<CloudUploadIcon />}
                >
                  Upload JD Document
                </Button>
              </label>
              {jdFile && (
                <Typography variant="body2" sx={{ mt: 2, color: '#2ecc71' }}>
                  ✓ {jdFile.name}
                </Typography>
              )}
              <Typography variant="caption" display="block" sx={{ mt: 1, color: 'text.secondary' }}>
                Supported formats: PDF, DOC, DOCX
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </DialogContent>

      <Divider />

      <DialogActions sx={{ p: 3, gap: 1 }}>
        <Button onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={loading || !formData.jobTitle || !formData.department}
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            minWidth: 120
          }}
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : 'Create RRF'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreateRRFDialog;
