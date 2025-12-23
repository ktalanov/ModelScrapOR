# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned (v0.2.0)
- Interactive cost calculator widget
- Cost effectiveness summary section
- Historical price tracking with SQLite
- Model search and filtering
- Mobile optimization improvements

## [0.1.0-alpha] - 2025-12-23

### Added
- Complete `scrape.py` script (835+ lines) with full OpenRouter API integration
- `OpenRouterClient` class for API interactions with error handling
- Model data fetching from OpenRouter API (353 models successfully retrieved)
- Heuristic keyword-based categorization across 12 categories
- Price-based ranking algorithm with cross-referencing
- Free model identification ($0/$0 pricing)
- HTML report generation with date-stamped filenames (`models-YYYY-MM-DD.html`)
- `style.css` (4.4KB+) with dark/light mode theming
- Dark/light mode toggle with localStorage persistence
- System color scheme preference detection
- 10-turn conversation cost calculator (125 input + 375 output tokens × 10 turns)
- Date navigation with Previous/Next Day buttons
- Expandable model lists (5→10→25 with progressive disclosure)
- Category quick navigation bar
- "Go to Top" buttons for easy page navigation
- Responsive design for mobile and desktop
- Initial project structure and documentation
- `README.md` with comprehensive project overview, usage instructions, and .env setup
- `PLAN.md` with detailed project roadmap, 5 completed milestones, and 10 future enhancement ideas
- `CHANGELOG.md` following Keep a Changelog format
- Updated `.github/copilot-instructions.md` with proper AI assistant guidance
- Project specifications for OpenRouter API integration
- Documentation for 12 tracked categories (Programming, Roleplay, Marketing, SEO, Technology, Science, Translation, Legal, Finance, Health, Trivia, Academia)
- Output format specifications for 4 subsections per category:
  - Daily Rankings
  - Rankings by Price (Highest) - with ranking numbers
  - Rankings by Price (Lowest) - with ranking cross-references
  - Best FREE Models (maximum 3 per category)
- Technical requirements for HTML/CSS output with dark/light mode support
- Environment variable configuration via `.env` file (`OPENROUTER_API_KEY`)
- `requirements.txt` with dependencies (requests, python-dotenv)

### Changed
- Standardized API key environment variable name to `OPENROUTER_API_KEY` (from inconsistent `API_KEY` and `OPENAI_SCRAPE_TOKEN`)
- Reorganized project documentation structure

### Fixed
- Resolved environment variable naming inconsistency in documentation

## Project Status Notes

### Current Phase: ✅ Complete Implementation
- **Version**: 0.1.0-alpha
- **Status**: All 5 milestones completed, fully functional
- **Features**: Core functionality + UI enhancements (expandable lists, date navigation, cost calculator)

### Completed Milestones
1. ✅ Milestone 1 - Project Setup & API Research
2. ✅ Milestone 2 - Core Data Fetching
3. ✅ Milestone 3 - Data Processing & Analysis
4. ✅ Milestone 4 - HTML & CSS Generation
5. ✅ Milestone 5 - Integration & Polish

### Next Steps
1. Implement v0.2.0 enhancements (interactive cost calculator, historical tracking)
2. Consider automated daily execution (cron job)
3. Add export functionality (CSV/JSON)

---

## Version History Summary

| Version | Date | Status | Description |
|---------|------|--------|-------------|
| 0.1.0-alpha | 2025-12-23 | ✅ Complete | Core implementation with all milestones finished + UI enhancements |

---

## Notes on Versioning

- **Alpha** (0.x.x-alpha): Project structure and planning phase
- **Beta** (0.x.x-beta): Core functionality implemented, testing in progress
- **Release Candidate** (x.x.x-rc.x): Feature-complete, final testing
- **Stable** (x.x.x): Production-ready releases

### Semantic Versioning Guide

Given a version number MAJOR.MINOR.PATCH:
- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

---

**Last Updated**: December 23, 2025
