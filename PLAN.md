# ModelScrapOR - Project Plan

## Project Overview

ModelScrapOR is a Python script that scrapes OpenRouter API data to generate daily HTML reports of AI model rankings across multiple categories. The output provides insights into model performance, pricing, and availability.

## Project Specifications

### Core Functionality

1. **API Integration**: Connect to OpenRouter API using authentication token
2. **Data Collection**: Fetch model data across 12 categories
3. **Data Processing**: Analyze rankings, pricing, and free model availability
4. **HTML Generation**: Create daily timestamped HTML reports with dark/light mode support

### Categories (12 Total)

- Programming
- Roleplay
- Marketing
- SEO
- Technology
- Science
- Translation
- Legal
- Finance
- Health
- Trivia
- Academia

### Output Structure

Each category contains 4 subsections:

#### 1. Daily Rankings
Top models ranked by daily performance:
```
* 1) xAI: Grok Code Fast 1 ($0.20/$1.50)
* 2) Anthropic: Claude Sonnet 4.5 ($3/$15)
* 3) Anthropic: Claude Opus 4.5 ($5/$25)
```

#### 2. Rankings by Price (Highest First)
Most expensive models first:
```
* 1) Anthropic: Claude Opus 4.5 ($5/$25)
* 2) Anthropic: Claude Sonnet 4.5 ($3/$15)
* 3) Google: Gemini 3 Pro Preview ($2/$12)
```

#### 3. Rankings by Price (Lowest First)
Least expensive models with daily ranking reference:
```
* 1) MiniMax: MiniMax M2 ($0.20/$1) (ranking: #7)
* 2) xAI: Grok Code Fast 1 ($0.20/$1.50) (ranking: #1)
* 3) Google: Gemini 3 Flash Preview ($0.50/$3) (ranking: #6)
```

#### 4. Best FREE Models
Maximum 3 free models per category:
```
* [FREE] Kwaipilot: KAT-Coder-Pro V1 (Programming #5)
* [FREE] MiniMax: MiniMax M2 (Programming #7)
* [FREE] Mistral: Devstral 2 2512 (Programming #8)
```

### Technical Requirements

**Output File**:
- Filename: `models-YYYY-MM-DD.html`
- Format: HTML + external CSS (`style.css`)
- Features: Dark/light mode toggle, system preference detection
- Layout: Separate section per category, separate table per subsection

**Pricing Format**:
- Display as: `($X/$Y)` where X = input tokens/M, Y = output tokens/M
- Ignore: Audio tokens and other non-text token types

**Authentication**:
- Environment variable: `OPENROUTER_API_KEY` (stored in `~/.zshrc`)
- Note: Original specs had inconsistency (`API_KEY` vs `OPENAI_SCRAPE_TOKEN`)

---

## Project Milestones

### Milestone 1: Project Setup & API Research
**Status**: Not Started  
**Estimated Duration**: 1-2 hours

**Tasks**:
- [x] Create project documentation (README, PLAN, CHANGELOG)
- [ ] Set up environment variable `OPENROUTER_API_KEY`
- [ ] Research OpenRouter API documentation
- [ ] Identify API endpoints for:
  - Model listing
  - Category filtering/tagging
  - Ranking data
  - Pricing information
- [ ] Test API authentication and basic requests
- [ ] Document API response structure

**Deliverables**:
- Working API connection with test script
- Documentation of API endpoints and response schemas

**Blockers/Questions**:
- How does OpenRouter categorize models?
- Are rankings provided by API or calculated from usage stats?
- What defines a "free" model in the API?

---

### Milestone 2: Core Data Fetching
**Status**: Not Started  
**Estimated Duration**: 3-4 hours

**Tasks**:
- [ ] Create `OpenRouterClient` class for API interactions
- [ ] Implement model data fetching from API
- [ ] Parse model metadata (name, provider, pricing)
- [ ] Filter models by 12 categories
- [ ] Extract daily rankings per category
- [ ] Identify free models (zero cost input/output)
- [ ] Add error handling and retry logic
- [ ] Implement rate limiting if needed

**Deliverables**:
- Python module with API client
- Data structures for models, categories, rankings
- Unit tests for data fetching

**Technical Notes**:
- Use `requests` library for HTTP calls
- Store API key in environment variable
- Implement exponential backoff for failed requests

---

### Milestone 3: Data Processing & Analysis
**Status**: Not Started  
**Estimated Duration**: 2-3 hours

**Tasks**:
- [ ] Implement sorting algorithms:
  - Sort by daily ranking
  - Sort by price (high to low)
  - Sort by price (low to high)
- [ ] Cross-reference rankings between sections
- [ ] Filter top N models per category (configurable)
- [ ] Identify top 3 free models per category
- [ ] Calculate pricing totals (input + output)
- [ ] Handle edge cases:
  - Missing pricing data
  - Models in multiple categories
  - Tied rankings

**Deliverables**:
- Data processing functions
- Sorted/filtered datasets ready for output
- Unit tests for sorting logic

**Data Structures**:
```python
@dataclass
class Model:
    id: str
    name: str
    provider: str
    input_price: float  # per M tokens
    output_price: float  # per M tokens
    categories: List[str]
    rankings: Dict[str, int]  # category -> rank
    is_free: bool
```

---

### Milestone 4: HTML & CSS Generation
**Status**: Not Started  
**Estimated Duration**: 4-5 hours

**Tasks**:
- [ ] Design HTML template structure
- [ ] Create `style.css` with:
  - Dark mode styles
  - Light mode styles
  - Responsive tables
  - Typography and spacing
- [ ] Implement dark/light mode toggle JavaScript
- [ ] Detect system color scheme preference
- [ ] Generate HTML sections dynamically per category
- [ ] Create subsection tables (4 per category)
- [ ] Format pricing display consistently
- [ ] Add metadata (generation date, timestamp)
- [ ] Implement file naming with date (`models-YYYY-MM-DD.html`)

**Deliverables**:
- HTML template generator
- `style.css` file
- JavaScript for theme toggle
- Sample output file

**Design Requirements**:
- Clean, minimal design
- Readable tables with clear headers
- Mobile-friendly responsive layout
- Accessibility considerations (ARIA labels, semantic HTML)

---

### Milestone 5: Integration & Polish
**Status**: Not Started  
**Estimated Duration**: 2-3 hours

**Tasks**:
- [ ] Integrate all components into main `scrape.py` script
- [ ] Add command-line argument parsing (optional)
- [ ] Implement logging (INFO, WARNING, ERROR levels)
- [ ] Add progress indicators for long operations
- [ ] Create configuration file support (optional)
- [ ] Write comprehensive error messages
- [ ] Add data validation
- [ ] Performance optimization
- [ ] Create usage documentation
- [ ] Add example output to repository

**Deliverables**:
- Complete, runnable `scrape.py` script
- User documentation in README
- Example output files

**Command-Line Interface** (Optional):
```bash
python scrape.py                    # Generate today's report
python scrape.py --date 2025-12-20  # Generate for specific date
python scrape.py --help             # Show usage
```

---

## Technical Architecture

### File Structure
```
ModelScrapOR/
├── .github/
│   └── copilot-instructions.md   # AI assistant instructions
├── scrape.py                      # Main script
├── style.css                      # Generated CSS file
├── models-YYYY-MM-DD.html         # Generated output (gitignored)
├── README.md                      # Project documentation
├── PLAN.md                        # This file
├── CHANGELOG.md                   # Version history
├── requirements.txt               # Python dependencies
└── .gitignore                     # Git ignore rules
```

### Dependencies
```
requests>=2.31.0
python-dateutil>=2.8.2
```

### Environment Setup
```bash
# Add to ~/.zshrc
export OPENROUTER_API_KEY="your_api_key_here"

# Install dependencies
pip install -r requirements.txt

# Run script
python scrape.py
```

---

## Open Questions & Decisions Needed

### 1. API Endpoint Structure
- **Question**: What is the exact OpenRouter API endpoint for fetching models?
- **Action**: Research OpenRouter API documentation
- **Impact**: Blocks Milestone 2

### 2. Category Assignment
- **Question**: How are models assigned to categories (Programming, Roleplay, etc.)?
- **Options**:
  - A) API provides category tags/metadata
  - B) Manual mapping based on model names
  - C) Category-specific API endpoints
- **Action**: Investigate API response structure
- **Impact**: Affects data fetching and filtering logic

### 3. Ranking Algorithm
- **Question**: How are "daily rankings" calculated?
- **Options**:
  - A) OpenRouter provides pre-calculated rankings
  - B) Calculate from usage statistics
  - C) Based on popularity/performance metrics
- **Action**: Check API documentation for ranking data
- **Impact**: Core to output generation

### 4. Free Model Detection
- **Question**: How to identify free models?
- **Options**:
  - A) Pricing = $0/$0
  - B) Specific API flag/field
  - C) Check multiple pricing fields
- **Decision**: Use pricing == 0 for both input and output
- **Status**: Decided (can revise if needed)

### 5. Environment Variable Name
- **Question**: Original docs had `API_KEY` and `OPENAI_SCRAPE_TOKEN`
- **Decision**: Use `OPENROUTER_API_KEY` for clarity
- **Status**: Decided
- **Rationale**: Clear naming indicates it's for OpenRouter, not OpenAI

---

## Success Criteria

The project is considered complete when:

1. ✅ Script successfully authenticates with OpenRouter API
2. ✅ Fetches model data for all 12 categories
3. ✅ Generates HTML file with correct naming convention
4. ✅ All 4 subsections present for each category
5. ✅ Dark/light mode toggle works correctly
6. ✅ Pricing displays in correct format ($X/$Y)
7. ✅ Rankings are accurate and consistent
8. ✅ Free models identified correctly (max 3 per category)
9. ✅ HTML renders properly in major browsers
10. ✅ Script can run daily without manual intervention

---

## Future Enhancements (Post-MVP)

- [ ] Automated daily execution (cron job)
- [ ] Historical data tracking and trends
- [ ] Email/notification on completion
- [ ] Comparison with previous day's rankings
- [ ] Interactive filtering/sorting in HTML
- [ ] Export to CSV/JSON formats
- [ ] Multi-language support
- [ ] Model comparison tool
- [ ] Performance benchmarks display
- [ ] Cost calculator based on usage estimates

---

## Notes

- **Local Use Only**: HTML output is for local viewing, not web hosting
- **Daily Generation**: Script should be idempotent (safe to run multiple times per day)
- **Error Recovery**: Script should handle API failures gracefully
- **Date Format**: Use ISO 8601 format (YYYY-MM-DD) consistently

---

**Last Updated**: December 23, 2025  
**Project Status**: Planning Phase  
**Next Milestone**: Milestone 1 - Project Setup & API Research
