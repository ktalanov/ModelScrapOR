# GitHub Copilot Instructions - ModelScrapOR

## Project Overview

ModelScrapOR is a Python-based tool that scrapes OpenRouter API data to generate daily HTML reports of AI model rankings, pricing, and availability across 12 categories.

**Project Documentation**:
- [README.md](../README.md) - User-facing documentation and usage guide
- [PLAN.md](../PLAN.md) - Complete project specifications, milestones, and technical architecture
- [CHANGELOG.md](../CHANGELOG.md) - Version history and changes

## Development Environment

### Operating System: Fedora 43 KDE Plasma

**Important**: When you need elevated privileges, use `pkexec` instead of `sudo`:

```bash
# ❌ Don't use sudo (may fail silently)
sudo dnf install package-name

# ✅ Use pkexec (shows GUI password prompt)
pkexec dnf install package-name
```

This displays a GUI authentication dialog that respects KDE Plasma's privilege escalation system.

## Coding Standards

### Python Style Guide

- **PEP 8 Compliance**: Follow Python's official style guide
- **Type Hints**: Use type annotations for function parameters and return values
- **Docstrings**: Google-style docstrings for all public functions and classes
- **Line Length**: Maximum 88 characters (Black formatter standard)
- **Imports**: Group imports in order: stdlib, third-party, local

Example:
```python
from typing import List, Dict, Optional
import requests
from datetime import datetime


def fetch_models(api_key: str, category: str) -> List[Dict[str, any]]:
    """Fetch models from OpenRouter API for a specific category.
    
    Args:
        api_key: OpenRouter API authentication key.
        category: Model category (e.g., 'Programming', 'Roleplay').
        
    Returns:
        List of model dictionaries with name, pricing, and ranking data.
        
    Raises:
        RequestException: If API request fails.
    """
    # Implementation here
    pass
```

### Code Organization

- **Single Responsibility**: Each function should do one thing well
- **DRY Principle**: Don't repeat yourself - extract common logic
- **Error Handling**: Use try/except blocks with specific exceptions
- **Logging**: Use Python's `logging` module, not print statements

### File Structure

```python
# scrape.py structure
# 1. Imports (grouped: stdlib, third-party, local)
# 2. Constants and configuration
# 3. Data classes/models
# 4. API client class
# 5. Data processing functions
# 6. HTML generation functions
# 7. Main execution block
```

## Project-Specific Guidelines

### Environment Variables

- **API Key**: `OPENROUTER_API_KEY` (defined in `~/.zshrc`)
- Always check for environment variable existence before use
- Never hardcode API keys or sensitive data

```python
import os

api_key = os.getenv('OPENROUTER_API_KEY')
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")
```

### API Integration

- **Base URL**: Confirm from OpenRouter documentation
- **Authentication**: Bearer token in Authorization header
- **Rate Limiting**: Implement exponential backoff
- **Error Handling**: Gracefully handle API failures

### Data Processing

- **Pricing**: Only track input/output token costs, ignore audio/other tokens
- **Categories**: 12 categories as defined in [PLAN.md](../PLAN.md)
- **Rankings**: Cross-reference daily rankings in price-sorted sections
- **Free Models**: Max 3 per category, identified by $0/$0 pricing

### HTML/CSS Output

- **File Naming**: `models-YYYY-MM-DD.html` (ISO 8601 date format)
- **Dark/Light Mode**: Support both with toggle switch
- **External CSS**: Use separate `style.css` file
- **Accessibility**: Semantic HTML, ARIA labels where needed
- **Local Use**: No CDN dependencies, all assets local

## Testing & Validation

### Before Committing

1. Test API connectivity and authentication
2. Verify HTML renders correctly in Firefox/Chrome
3. Check dark/light mode toggle functionality
4. Validate pricing format displays correctly
5. Ensure all 12 categories appear in output

### Error Scenarios to Handle

- Missing API key
- Network failures
- Invalid API responses
- Missing category data
- Zero models in a category
- Malformed pricing data

## Common Commands

### Package Management
```bash
# Install Python dependencies
pip install -r requirements.txt

# Update a package
pip install --upgrade package-name
```

### Running the Script
```bash
# Generate today's report
python scrape.py

# Check for syntax errors
python -m py_compile scrape.py

# Run with debug logging (when implemented)
python scrape.py --debug
```

### Git Workflow
```bash
# Check status
git status

# Stage changes
git add scrape.py

# Commit with descriptive message
git commit -m "feat: implement OpenRouter API client"

# Push to remote
git push origin main
```

## AI Assistant Behavior Guidelines

### Be Concise
- Provide direct answers without unnecessary preamble
- Offer suggestions when asked or when obvious improvements exist
- Don't over-explain simple changes

### Be Precise
- Use exact file paths and line numbers
- Quote error messages accurately
- Reference specific functions/classes by name

### Be Proactive
- Suggest best practices when relevant
- Identify potential issues before they become problems
- Recommend testing strategies for new features

### File Updates
- Update this file if project requirements change
- Keep instructions synchronized with [PLAN.md](../PLAN.md)
- Document new conventions or patterns as they emerge

## Quick Reference

| Task | Command |
|------|---------|
| Install package (system) | `pkexec dnf install <package>` |
| Install package (Python) | `pip install <package>` |
| Run script | `python scrape.py` |
| Check env variable | `echo $OPENROUTER_API_KEY` |
| Open HTML output | `firefox models-2025-12-23.html` |

## Resources

- [OpenRouter API Docs](https://openrouter.ai/docs) - API reference
- [PEP 8](https://pep8.org/) - Python style guide
- [Keep a Changelog](https://keepachangelog.com/) - Changelog format
- [Semantic Versioning](https://semver.org/) - Version numbering

---

**Last Updated**: December 23, 2025  
**Current Version**: 0.1.0-alpha
