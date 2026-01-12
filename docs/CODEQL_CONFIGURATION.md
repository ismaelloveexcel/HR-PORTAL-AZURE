# CodeQL Configuration for HR Portal

## Overview

This document explains the custom CodeQL configuration used to address false positive security alerts related to PII masking.

## The Problem

CodeQL's static analysis performs data flow tracking to detect when sensitive information (like employee IDs) might be logged in clear text. Even though we implemented masking via the `_mask_employee_id()` function, CodeQL continued to flag the code because:

1. It sees sensitive data (`request.employee_id`) being accessed
2. It tracks this data flowing through the code
3. It doesn't inherently recognize our custom masking function as a sanitizer

## The Solution

We created a custom CodeQL configuration file (`.github/codeql-config.yml`) that explicitly registers our masking functions as sanitizers.

### Configuration File

```yaml
# .github/codeql-config.yml
name: hr-portal-codeql-config

queries:
  - uses: security-extended

extensions:
  - addsTo:
      pack: codeql/python-all
      extensible: sanitizers
    data:
      - ['app.routers.auth._mask_employee_id', 'ReturnValue']
      - ['app.routers.health._mask_employee_id', 'ReturnValue']
```

This configuration tells CodeQL that:
- The return value of `_mask_employee_id()` in both routers is sanitized
- Data that flows through these functions is safe for logging

### CI Workflow Update

Updated `.github/workflows/ci.yml` to use the custom configuration:

```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@v4
  with:
    languages: python, javascript
    config-file: ./.github/codeql-config.yml
```

## Implementation Details

### Masking Function

Both routers have identical masking functions:

```python
def _mask_employee_id(employee_id: str) -> str:
    """
    Mask employee ID for logging to prevent clear-text logging of sensitive information.
    
    This function acts as a sanitizer for PII data, masking the middle characters
    while preserving the first and last 2 characters for debugging purposes.
    
    Args:
        employee_id: The employee ID to mask (sensitive PII)
    
    Returns:
        Masked employee ID safe for logging (sanitized)
    
    Examples:
        >>> _mask_employee_id("BAYN00008")
        'BA***08'
    """
    if not employee_id or len(employee_id) < 4:
        return "***"
    return f"{employee_id[:2]}***{employee_id[-2:]}"
```

### Enhanced Documentation

Added detailed docstrings that explicitly state:
- The function is a sanitizer
- Input is sensitive PII
- Output is sanitized and safe for logging
- Includes examples showing the transformation

## Why This Approach

### Alternative Approaches Considered

1. **Inline Suppression Comments** - Would work but doesn't address the root cause
   ```python
   # lgtm[py/clear-text-logging-sensitive-data]
   masked_id = _mask_employee_id(request.employee_id)
   ```
   
2. **Not Logging at All** - Would eliminate the alert but reduce debuggability

3. **Custom CodeQL Query** - More complex, requires maintaining query files

### Why Custom Configuration is Best

- ✅ Teaches CodeQL about our sanitization pattern
- ✅ Works for all instances automatically
- ✅ Doesn't suppress legitimate alerts
- ✅ Maintains code clarity
- ✅ Follows security best practices

## Testing

All tests continue to pass after implementing the custom configuration:

```bash
cd backend
pytest tests/test_security_masking.py tests/test_emergency_endpoints.py -v
# 9 passed
```

## Expected Outcome

After the next CodeQL scan runs with the custom configuration:
- ✅ Alerts should be resolved
- ✅ Future code using `_mask_employee_id()` will be recognized as safe
- ✅ CodeQL will still detect if we accidentally log `request.employee_id` directly

## Verification

To verify the configuration is working:

1. Check the next CI run's CodeQL analysis
2. Look for the message: "Using configuration from .github/codeql-config.yml"
3. Verify the security alerts are resolved

## Future Maintenance

If you add new masking functions:

1. Add them to `.github/codeql-config.yml`
2. Follow the same pattern: `['module.path.function_name', 'ReturnValue']`
3. Use clear docstrings that explicitly state the function is a sanitizer

## References

- [CodeQL Custom Configurations](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/customizing-your-advanced-setup-for-code-scanning)
- [CodeQL Python Sanitizers](https://codeql.github.com/docs/codeql-language-guides/customizing-python-analysis/)

---

**Date:** January 12, 2026  
**Status:** Implemented  
**Commit:** 42be930
