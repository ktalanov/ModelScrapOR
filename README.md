# ModelScrapOR

**THIS PROJECT WAS "VIBE-CODED" BY Claude Sonnet 4.5 AS A TEST**

It's a quick script I've wanted for myself and I've made it public only for educational purposes.

All contents except in this one paragraph is AI-generated.

---

> Daily OpenRouter AI Model Rankings & Pricing Tracker

ModelScrapOR is a Python script that scrapes the OpenRouter API to generate comprehensive daily reports of AI model rankings, pricing, and availability across multiple categories.

## Features

- 📊 **12 Category Coverage**: Track models across Programming, Roleplay, Marketing, SEO, Technology, Science, Translation, Legal, Finance, Health, Trivia, and Academia
- 💰 **Pricing Analysis**: Sort models by cost (high to low, low to high) with transparent per-million-token pricing
- 🏆 **Daily Rankings**: See top-performing models updated daily for each category
- 🆓 **Free Model Tracking**: Identify the best free models available in each category
- 🌓 **Dark/Light Mode**: Beautiful HTML output with automatic theme detection and manual toggle
- 📅 **Daily Archives**: Generate timestamped reports (`models-YYYY-MM-DD.html`) for historical tracking

## Prerequisites

- Python 3.8+
- OpenRouter API key
- Fedora 43 KDE Plasma (or any Linux distribution)

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/ModelScrapOR.git
cd ModelScrapOR
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up API key**:

Create a `.env` file in the project root:
```bash
echo 'OPENROUTER_API_KEY="your_api_key_here"' > .env
```

Or create it manually with your editor:
```env
OPENROUTER_API_KEY=your_api_key_here
```

To get an OpenRouter API key:
- Visit [OpenRouter](https://openrouter.ai/)
- Sign up or log in
- Navigate to API Keys section
- Generate a new key

**Note**: The `.env` file is gitignored and will not be uploaded to the repository.

## Usage

### Basic Usage

Run the script to generate today's report:
```bash
python scrape.py
```

This creates a file named `models-2025-12-23.html` (with today's date) in the current directory.

### View the Report

Open the generated HTML file in your browser:
```bash
firefox models-2025-12-23.html
# or
xdg-open models-2025-12-23.html
```

## Output Format

Each generated HTML report contains:

### Per Category (12 total):

1. **Daily Rankings** - Top models by performance
2. **Rankings by Price (Highest)** - Most expensive models
3. **Rankings by Price (Lowest)** - Most affordable models with daily ranking reference
4. **Best FREE Models** - Up to 3 free models per category

### Example Output Structure:

```
OpenRouter Models as of 2025-12-23

Programming
├── Daily Rankings
│   1) xAI: Grok Code Fast 1 ($0.20/$1.50)
│   2) Anthropic: Claude Sonnet 4.5 ($3/$15)
│   └── ...
├── Rankings by Price (Highest)
├── Rankings by Price (Lowest)
└── Best FREE Models

Roleplay
├── Daily Rankings
└── ...
```

### Pricing Format

Pricing is displayed as `($X/$Y)` where:
- **$X** = Cost per million input tokens
- **$Y** = Cost per million output tokens

## Project Structure

```
ModelScrapOR/
├── .github/
│   └── copilot-instructions.md   # AI assistant configuration
├── scrape.py                      # Main script (to be implemented)
├── style.css                      # CSS for HTML output (generated)
├── models-*.html                  # Generated reports (gitignored)
├── README.md                      # This file
├── PLAN.md                        # Project roadmap and specifications
├── CHANGELOG.md                   # Version history
├── AGENTS.md                      # Legacy documentation
├── requirements.txt               # Python dependencies
└── .gitignore                     # Git ignore rules
```

## Development Status

🚧 **Project Status**: Planning Phase

See [PLAN.md](PLAN.md) for detailed milestones and implementation roadmap.

### Milestones:
- [x] Milestone 1: Project Setup & API Research - **In Progress**
- [ ] Milestone 2: Core Data Fetching
- [ ] Milestone 3: Data Processing & Analysis
- [ ] Milestone 4: HTML & CSS Generation
- [ ] Milestone 5: Integration & Polish

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY` - Your OpenRouter API key (required)

### Categories Tracked

1. Programming
2. Roleplay
3. Marketing
4. SEO
5. Technology
6. Science
7. Translation
8. Legal
9. Finance
10. Health
11. Trivia
12. Academia

## Troubleshooting

### Permission Errors on Fedora

If you encounter permission errors, use `pkexec` instead of `sudo`:
```bash
# Instead of:
sudo dnf install python3-pip

# Use:
pkexec dnf install python3-pip
```

This will show a GUI prompt for password authentication.

### API Key Not Found

If you get an API key error:

1. **Check if `.env` file exists**:
```bash
ls -la .env
```

2. **Verify the file contents**:
```bash
cat .env
```

Should show:
```
OPENROUTER_API_KEY=your_actual_key_here
```

3. **Recreate if missing**:
```bash
echo 'OPENROUTER_API_KEY="your_api_key_here"' > .env
```

### Missing Dependencies

Install required Python packages:
```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenRouter](https://openrouter.ai/) - For providing the API
- AI model providers (Anthropic, OpenAI, Google, etc.) - For their amazing models

## Roadmap

### Current Version (v0.1.0-alpha)
- Project setup and documentation

### Planned Features
- Automated daily execution (cron job)
- Historical trend analysis
- Model comparison tool
- CSV/JSON export options
- Interactive web interface
- Email notifications

## Contact

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check [PLAN.md](PLAN.md) for technical details

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

---

**Note**: This is a local utility for personal use. Generated HTML files are designed for local viewing and are not intended for web hosting.
