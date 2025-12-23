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
**Status**: ✅ Complete  
**Estimated Duration**: 1-2 hours

**Tasks**:
- [x] Create project documentation (README, PLAN, CHANGELOG)
- [x] Set up environment variable `OPENROUTER_API_KEY`
- [x] Research OpenRouter API documentation
- [x] Identify API endpoints for:
  - Model listing
  - Category filtering/tagging
  - Ranking data
  - Pricing information
- [x] Test API authentication and basic requests
- [x] Document API response structure

**Deliverables**:
- ✅ Working API connection with test script
- ✅ Documentation of API endpoints and response schemas

**Resolutions**:
- Used OpenRouter API endpoint: https://openrouter.ai/api/v1/models
- Categories implemented via heuristic keyword matching
- Rankings calculated from pricing as proxy for capability
- Free models identified by $0/$0 pricing

---

### Milestone 2: Core Data Fetching
**Status**: ✅ Complete  
**Estimated Duration**: 3-4 hours

**Tasks**:
- [x] Create `OpenRouterClient` class for API interactions
- [x] Implement model data fetching from API
- [x] Parse model metadata (name, provider, pricing)
- [x] Filter models by 12 categories
- [x] Extract daily rankings per category
- [x] Identify free models (zero cost input/output)
- [x] Add error handling and retry logic
- [x] Implement rate limiting if needed

**Deliverables**:
- ✅ Python module with API client
- ✅ Data structures for models, categories, rankings
- ✅ Successfully fetching 353 models from OpenRouter API

**Technical Implementation**:
- Used `requests` library for HTTP calls
- API key stored in .env file via `python-dotenv`
- Comprehensive error handling implemented

---

### Milestone 3: Data Processing & Analysis
**Status**: ✅ Complete  
**Estimated Duration**: 2-3 hours

**Tasks**:
- [x] Implement sorting algorithms:
  - Sort by daily ranking
  - Sort by price (high to low)
  - Sort by price (low to high)
- [x] Cross-reference rankings between sections
- [x] Filter top N models per category (configurable - 25 models with 5→10→25 expandable display)
- [x] Identify top 3 free models per category
- [x] Calculate pricing totals (input + output)
- [x] Handle edge cases:
  - Missing pricing data
  - Models in multiple categories
  - Tied rankings

**Deliverables**:
- ✅ Data processing functions
- ✅ Sorted/filtered datasets ready for output
- ✅ Progressive disclosure UI (5→10→25 models)

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
**Status**: ✅ Complete  
**Estimated Duration**: 4-5 hours

**Tasks**:
- [x] Design HTML template structure
- [x] Create `style.css` with:
  - Dark mode styles
  - Light mode styles
  - Responsive tables
  - Typography and spacing
- [x] Implement dark/light mode toggle JavaScript
- [x] Detect system color scheme preference
- [x] Generate HTML sections dynamically per category
- [x] Create subsection tables (4 per category)
- [x] Format pricing display consistently
- [x] Add metadata (generation date, timestamp)
- [x] Implement file naming with date (`models-YYYY-MM-DD.html`)

**Deliverables**:
- ✅ HTML template generator
- ✅ `style.css` file (4.4KB+)
- ✅ JavaScript for theme toggle with localStorage persistence
- ✅ Sample output file (models-2025-12-23.html, 56KB+)

**Design Implementation**:
- ✅ Clean, minimal design
- ✅ Readable tables with clear headers
- ✅ Mobile-friendly responsive layout
- ✅ Accessibility considerations (ARIA labels, semantic HTML)
- ✅ Category navigation bar
- ✅ Date navigation (Previous/Next Day buttons)
- ✅ "Go to Top" buttons for easy navigation

---

### Milestone 5: Integration & Polish
**Status**: ✅ Complete  
**Estimated Duration**: 2-3 hours

**Tasks**:
- [x] Integrate all components into main `scrape.py` script
- [x] Add command-line argument parsing (optional)
- [x] Implement logging (INFO, WARNING, ERROR levels)
- [x] Add progress indicators for long operations
- [x] Create configuration file support (optional)
- [x] Write comprehensive error messages
- [x] Add data validation
- [x] Performance optimization
- [x] Create usage documentation
- [x] Add example output to repository

**Deliverables**:
- ✅ Complete, runnable `scrape.py` script (835+ lines)
- ✅ User documentation in README
- ✅ Example output files (models-2025-12-23.html)

**Implementation**:
- Script generates today's report by default
- Console output shows progress
- Error handling throughout
- .env file for API key configuration

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

## Design Decisions Made

### 1. API Endpoint Structure ✅
- **Decision**: Use OpenRouter API endpoint: `https://openrouter.ai/api/v1/models`
- **Implementation**: Fetch all models in single request, filter client-side
- **Status**: Implemented and working (353 models fetched successfully)

### 2. Category Assignment ✅
- **Decision**: Heuristic keyword-based categorization
- **Implementation**: Search model names/descriptions for category keywords
- **Rationale**: API doesn't provide explicit category tags
- **Status**: Implemented across all 12 categories

### 3. Ranking Algorithm ✅
- **Decision**: Price-based ranking as proxy for capability
- **Implementation**: Lower total price = higher ranking (more accessible)
- **Rationale**: OpenRouter doesn't provide performance rankings
- **Status**: Implemented with cross-referencing between price sections

### 4. Free Model Detection ✅
- **Decision**: Pricing = $0/$0 for both input and output
- **Implementation**: Check `input_price == 0 and output_price == 0`
- **Status**: Implemented, showing up to 3 free models per category

### 5. Environment Variable Name ✅
- **Decision**: Use `OPENROUTER_API_KEY`
- **Implementation**: Stored in .env file, loaded via python-dotenv
- **Rationale**: Clear naming indicates OpenRouter, not OpenAI
- **Status**: Implemented and documented

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

## v0.1.0 Enhancements (Implemented)

- [x] 25 model limit per section (expandable 5→10→25)
- [x] Rankings added to "Rankings by Price (Highest)" section
- [x] 10-turn conversation cost calculator integrated into display
- [x] Date navigation (Previous Day / Next Day buttons)
- [x] Expandable lists with progressive disclosure
- [x] Prominent "Go to Top" navigation buttons
- [x] Dark/light mode with localStorage persistence
- [x] Category quick navigation bar
- [x] Responsive design for mobile/desktop

## Future Enhancements (Post-v0.1.0)

- [ ] Automated daily execution (cron job)
- [ ] Historical data tracking and trends
- [ ] Email/notification on completion
- [ ] Comparison with previous day's rankings
- [ ] Interactive filtering/sorting in HTML
- [ ] Export to CSV/JSON formats
- [ ] Multi-language support
- [ ] Model comparison tool
- [ ] Performance benchmarks display

---

## Notes

- **Local Use Only**: HTML output is for local viewing, not web hosting
- **Daily Generation**: Script should be idempotent (safe to run multiple times per day)
- **Error Recovery**: Script should handle API failures gracefully
- **Date Format**: Use ISO 8601 format (YYYY-MM-DD) consistently

---

**Last Updated**: December 23, 2025  
**Project Status**: ✅ v0.1.0-alpha Complete - All Milestones Finished  
**Current Version**: 0.1.0-alpha with enhancements  
**Next Phase**: v0.2.0 - Future Enhancement Implementation

---

## Future Enhancement Ideas (v0.2.0+)

### High Priority Enhancements

#### 1. Cost Effectiveness Summary Section
**Status**: Idea Phase  
**Description**: Add a top-of-page summary showing most cost-effective models across categories.

**Features**:
- Compare flagship models (e.g., Claude Opus vs Qwen Coder vs GPT-4o)
- Show cost per 10-turn conversation (125 input + 375 output tokens × 10 turns)
- Highlight "best value" models in each category
- Visual comparison chart/table
- Include quality-to-price ratio indicators

**Calculation Example**:
```
User: 125 tokens × 10 turns = 1,250 input tokens
Model: 375 tokens × 10 turns = 3,750 output tokens
Total cost = (1,250/1M × input_price) + (3,750/1M × output_price)
```

**Display Format**:
```
Cost-Effective Models for Programming
┌─────────────────────────────────────────────────────────┐
│ Model              │ 10-turn Conv │ Quality │ Value    │
├────────────────────┼──────────────┼─────────┼──────────┤
│ Qwen Code         │ $0.002       │ ★★★★☆   │ Excellent│
│ Claude Sonnet 4.5 │ $0.058       │ ★★★★★   │ Good     │
│ Claude Opus 4.5   │ $0.101       │ ★★★★★   │ Fair     │
└─────────────────────────────────────────────────────────┘
```

#### 2. Usage-Based Cost Calculator (Interactive)
**Status**: Idea Phase  
**Description**: Interactive JavaScript calculator on each page.

**Features**:
- Adjustable sliders for:
  - Input tokens per message (50-1000)
  - Output tokens per response (100-5000)
  - Number of turns (1-100)
  - Messages per day/month
- Real-time cost updates for selected model
- Compare up to 3 models side-by-side
- Monthly/yearly cost projections
- Export calculations as CSV

**Implementation**:
- Pure JavaScript (no external dependencies)
- Sticky calculator widget (follows scroll)
- Local storage for user preferences
- Share cost comparison via URL parameters

#### 3. Historical Price Tracking
**Status**: Idea Phase  
**Description**: Track and visualize model pricing over time.

**Features**:
- Daily snapshots of all model prices
- SQLite database for historical data
- Price change indicators (↑ ↓ →)
- 30/90/365-day price trend charts
- Email alerts on significant price changes (>10%)
- Price history CSV export per model

**Database Schema**:
```sql
CREATE TABLE price_history (
    date DATE,
    model_id TEXT,
    input_price REAL,
    output_price REAL,
    PRIMARY KEY (date, model_id)
);
```

#### 4. Model Comparison Matrix
**Status**: Idea Phase  
**Description**: Side-by-side comparison of selected models.

**Features**:
- Compare up to 5 models simultaneously
- Metrics:
  - Pricing (input/output)
  - Context length
  - 10-turn conversation cost
  - Category rankings
  - Performance indicators
- Export comparison as image/PDF
- Shareable comparison links
- "Add to comparison" button on each model

#### 5. Category-Specific Recommendations
**Status**: Idea Phase  
**Description**: Smart recommendations based on use case.

**Features**:
- Budget tiers: "Economy" ($0-$0.01), "Mid-range" ($0.01-$0.10), "Premium" ($0.10+)
- Use case presets:
  - "Student coding helper" → free/low-cost programming models
  - "Enterprise content generation" → reliable, scalable models
  - "Research assistant" → high-context, accurate models
- Filtering by:
  - Max cost per conversation
  - Minimum context length
  - Specific providers only
  - Free models only

#### 6. API Response Time Benchmarks
**Status**: Idea Phase  
**Description**: Track and display model response times.

**Features**:
- Periodic ping tests (opt-in)
- Display average response times
- Token generation speed (tokens/second)
- Uptime/availability indicators
- Regional latency differences
- Performance vs cost visualization

**Metrics Tracked**:
- Time to first token (TTFT)
- Tokens per second (TPS)
- Total request duration
- 95th percentile latency

#### 7. Weekly/Monthly Reports
**Status**: Idea Phase  
**Description**: Automated summary emails/reports.

**Features**:
- Weekly digest of:
  - New models added
  - Price changes
  - Top gainers/losers in rankings
  - Most cost-effective discoveries
- Monthly trend analysis
- Customizable report sections
- Email or Slack integration
- PDF export option

#### 8. Model Search and Filtering
**Status**: Idea Phase  
**Description**: Advanced search across all models.

**Features**:
- Full-text search by model name
- Filter by:
  - Price range (min/max)
  - Provider (Anthropic, OpenAI, etc.)
  - Context length
  - Free/paid status
  - Multiple categories
- Sort options:
  - Alphabetical
  - Price (low/high)
  - Context length
  - Recently added
- Save custom filters
- Keyword search in all categories

#### 9. Model Versioning Tracker
**Status**: Idea Phase  
**Description**: Track model version changes and deprecations.

**Features**:
- Detect new model versions
- Highlight deprecated models
- Version comparison (v1 vs v2)
- Migration recommendations
- API changelog integration
- Deprecation warnings with dates

#### 10. Mobile-Optimized View
**Status**: Idea Phase  
**Description**: Enhanced mobile experience.

**Features**:
- Swipe navigation between categories
- Collapsible sections (accordion style)
- Touch-friendly buttons and controls
- Reduced data mode (load fewer models)
- Progressive Web App (PWA) support
- Offline mode with last cached data
- Mobile-specific compact layout

---

## Implementation Priority Matrix

| Feature | Impact | Effort | Priority | Target Version |
|---------|--------|--------|----------|----------------|
| Cost Calculator (Interactive) | High | Medium | 1 | v0.2.0 |
| Cost Effectiveness Summary | High | Low | 2 | v0.2.0 |
| Historical Price Tracking | Medium | High | 3 | v0.3.0 |
| Model Search/Filtering | High | Medium | 4 | v0.3.0 |
| Mobile Optimization | Medium | Medium | 5 | v0.3.0 |
| Model Comparison Matrix | Medium | Medium | 6 | v0.4.0 |
| Category Recommendations | Medium | Low | 7 | v0.4.0 |
| API Response Benchmarks | Low | High | 8 | v0.5.0 |
| Weekly/Monthly Reports | Low | Medium | 9 | v0.5.0 |
| Model Versioning Tracker | Low | Medium | 10 | v0.6.0 |

---

## Technical Considerations

### Cost Calculator Implementation
- Use vanilla JavaScript (no frameworks)
- Store default values in localStorage
- Debounce slider changes for performance
- Add copy-to-clipboard for calculations

### Historical Data Storage
- SQLite for simplicity and portability
- Automated daily backup to Git (optional)
- Consider PostgreSQL for production scale
- Implement data retention policies (e.g., 2 years)

### Performance Optimization
- Lazy-load model lists (paginate at 25 items)
- Index HTML for faster category navigation
- Compress historical data older than 90 days
- Cache API responses (5-minute TTL)

### Mobile Considerations
- Test on iPhone SE (smallest modern screen)
- Use CSS Grid for responsive layouts
- Implement touch gestures carefully
- Consider data usage (optimize images/CSS)

---

**Last Updated**: December 23, 2025 (after v0.1.0 implementation with enhancements)
