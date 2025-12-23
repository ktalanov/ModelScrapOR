# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- OpenRouter API integration
- Model data fetching across 12 categories
- Daily ranking calculation
- Pricing analysis (high to low, low to high)
- Free model identification
- HTML report generation with dark/light mode
- CSS styling for reports
- Date-stamped output files

## [0.1.0-alpha] - 2025-12-23

### Added
- Initial project structure and documentation
- `README.md` with comprehensive project overview and usage instructions
- `PLAN.md` with detailed project roadmap, milestones, and technical specifications
- `CHANGELOG.md` following Keep a Changelog format
- Updated `.github/copilot-instructions.md` with proper AI assistant guidance
- Project specifications for OpenRouter API integration
- Documentation for 12 tracked categories (Programming, Roleplay, Marketing, SEO, Technology, Science, Translation, Legal, Finance, Health, Trivia, Academia)
- Output format specifications for 4 subsections per category:
  - Daily Rankings
  - Rankings by Price (Highest)
  - Rankings by Price (Lowest)
  - Best FREE Models
- Technical requirements for HTML/CSS output with dark/light mode support
- Environment variable configuration (`OPENROUTER_API_KEY`)

### Changed
- Standardized API key environment variable name to `OPENROUTER_API_KEY` (from inconsistent `API_KEY` and `OPENAI_SCRAPE_TOKEN`)
- Reorganized project documentation structure

### Fixed
- Resolved environment variable naming inconsistency in documentation

## Project Status Notes

### Current Phase: Planning & Setup
- **Version**: 0.1.0-alpha
- **Status**: Pre-release, no functional code yet
- **Active Milestone**: Milestone 1 - Project Setup & API Research

### Next Steps
1. Research OpenRouter API endpoints and authentication
2. Test API connectivity
3. Begin implementing core data fetching functionality

---

## Version History Summary

| Version | Date | Status | Description |
|---------|------|--------|-------------|
| 0.1.0-alpha | 2025-12-23 | Planning | Initial project setup and documentation |

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
