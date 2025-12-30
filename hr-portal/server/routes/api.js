const express = require('express');
const router = express.Router();
const db = require('../db');

// ============================================
// PASS ROUTES
// ============================================

// Get pass by ID (Universal endpoint)
router.get('/pass/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const pass = await db.query(
      'SELECT * FROM passes WHERE id = $1',
      [id]
    );

    if (pass.rows.length === 0) {
      return res.status(404).json({ error: 'Pass not found' });
    }

    res.json(pass.rows[0]);
  } catch (error) {
    console.error('Error fetching pass:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create new pass
router.post('/pass', async (req, res) => {
  try {
    const { type, enabled_modules, data } = req.body;

    const result = await db.query(
      `INSERT INTO passes (type, enabled_modules, data, created_at, updated_at)
       VALUES ($1, $2, $3, NOW(), NOW())
       RETURNING *`,
      [type, JSON.stringify(enabled_modules), JSON.stringify(data)]
    );

    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Error creating pass:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update pass
router.patch('/pass/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { enabled_modules, data } = req.body;

    const result = await db.query(
      `UPDATE passes
       SET enabled_modules = $1, data = $2, updated_at = NOW()
       WHERE id = $3
       RETURNING *`,
      [JSON.stringify(enabled_modules), JSON.stringify(data), id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Pass not found' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error updating pass:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================
// EMPLOYEE ROUTES
// ============================================

router.get('/employees', async (req, res) => {
  try {
    const employees = await db.query('SELECT * FROM employees ORDER BY employee_id');
    res.json(employees.rows);
  } catch (error) {
    console.error('Error fetching employees:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/employees/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const employee = await db.query(
      'SELECT * FROM employees WHERE employee_id = $1',
      [id]
    );

    if (employee.rows.length === 0) {
      return res.status(404).json({ error: 'Employee not found' });
    }

    res.json(employee.rows[0]);
  } catch (error) {
    console.error('Error fetching employee:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================
// ATTENDANCE ROUTES
// ============================================

router.post('/attendance/clock-in', async (req, res) => {
  try {
    const { employee_id, location, gps_coordinates } = req.body;

    const result = await db.query(
      `INSERT INTO attendance_records
       (employee_id, date, clock_in_time, work_location, gps_coordinates, attendance_status)
       VALUES ($1, CURRENT_DATE, CURRENT_TIME, $2, $3, 'Present')
       RETURNING *`,
      [employee_id, location, gps_coordinates]
    );

    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Error clocking in:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/attendance/clock-out', async (req, res) => {
  try {
    const { employee_id } = req.body;

    const result = await db.query(
      `UPDATE attendance_records
       SET clock_out_time = CURRENT_TIME
       WHERE employee_id = $1 AND date = CURRENT_DATE AND clock_out_time IS NULL
       RETURNING *`,
      [employee_id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'No active clock-in found' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error clocking out:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.get('/attendance/:employee_id', async (req, res) => {
  try {
    const { employee_id } = req.params;
    const { month, year } = req.query;

    let query = 'SELECT * FROM attendance_records WHERE employee_id = $1';
    const params = [employee_id];

    if (month && year) {
      query += ' AND EXTRACT(MONTH FROM date) = $2 AND EXTRACT(YEAR FROM date) = $3';
      params.push(month, year);
    }

    query += ' ORDER BY date DESC';

    const records = await db.query(query, params);
    res.json(records.rows);
  } catch (error) {
    console.error('Error fetching attendance:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================
// HR REQUESTS ROUTES
// ============================================

router.get('/requests', async (req, res) => {
  try {
    const { employee_id, status } = req.query;

    let query = 'SELECT * FROM hr_requests';
    const params = [];
    const conditions = [];

    if (employee_id) {
      params.push(employee_id);
      conditions.push(`employee_id = $${params.length}`);
    }

    if (status) {
      params.push(status);
      conditions.push(`status = $${params.length}`);
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }

    query += ' ORDER BY request_date DESC';

    const requests = await db.query(query, params);
    res.json(requests.rows);
  } catch (error) {
    console.error('Error fetching requests:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/requests', async (req, res) => {
  try {
    const { employee_id, request_type, description, leave_type_id } = req.body;

    const result = await db.query(
      `INSERT INTO hr_requests
       (employee_id, request_type, description, leave_type_id, request_date, status)
       VALUES ($1, $2, $3, $4, NOW(), 'Submitted')
       RETURNING *`,
      [employee_id, request_type, description, leave_type_id]
    );

    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Error creating request:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.patch('/requests/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { status, manager_comments } = req.body;

    const result = await db.query(
      `UPDATE hr_requests
       SET status = $1, manager_comments = $2, date_actioned = NOW()
       WHERE id = $3
       RETURNING *`,
      [status, manager_comments, id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Request not found' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Error updating request:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================
// LEAVE ROUTES
// ============================================

router.get('/leave-types', async (req, res) => {
  try {
    const leaveTypes = await db.query('SELECT * FROM leave_types WHERE active = true');
    res.json(leaveTypes.rows);
  } catch (error) {
    console.error('Error fetching leave types:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================
// COMPLIANCE ROUTES
// ============================================

router.get('/compliance/expiring', async (req, res) => {
  try {
    const { days = 30 } = req.query;

    const query = `
      SELECT employee_id, full_name,
             emirates_id_expiry, uae_visa_expiry, labor_card_expiry, medical_fitness_expiry
      FROM employees
      WHERE emirates_id_expiry <= CURRENT_DATE + INTERVAL '${days} days'
         OR uae_visa_expiry <= CURRENT_DATE + INTERVAL '${days} days'
         OR labor_card_expiry <= CURRENT_DATE + INTERVAL '${days} days'
         OR medical_fitness_expiry <= CURRENT_DATE + INTERVAL '${days} days'
      ORDER BY emirates_id_expiry, uae_visa_expiry
    `;

    const result = await db.query(query);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching compliance data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Health check
router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

module.exports = router;
