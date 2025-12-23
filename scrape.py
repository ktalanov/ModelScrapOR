#!/usr/bin/env python3
"""
ModelScrapOR - OpenRouter AI Model Rankings & Pricing Tracker

Scrapes OpenRouter API to generate daily HTML reports of AI model rankings,
pricing, and availability across multiple categories.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

import requests
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Constants
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
CATEGORIES = [
    "Programming",
    "Roleplay",
    "Marketing",
    "SEO",
    "Technology",
    "Science",
    "Translation",
    "Legal",
    "Finance",
    "Health",
    "Trivia",
    "Academia"
]


@dataclass
class Model:
    """Represents an AI model with its metadata."""
    id: str
    name: str
    pricing: Dict[str, float]
    context_length: int
    architecture: Optional[Dict] = None
    top_provider: Optional[Dict] = None
    per_request_limits: Optional[Dict] = None
    
    @property
    def display_name(self) -> str:
        """Format model name for display."""
        return self.name
    
    @property
    def input_price(self) -> float:
        """Price per million input tokens."""
        return float(self.pricing.get('prompt', 0)) * 1_000_000
    
    @property
    def output_price(self) -> float:
        """Price per million output tokens."""
        return float(self.pricing.get('completion', 0)) * 1_000_000
    
    @property
    def is_free(self) -> bool:
        """Check if model is free."""
        return self.input_price == 0 and self.output_price == 0
    
    @property
    def total_price(self) -> float:
        """Total price (input + output) for sorting."""
        return self.input_price + self.output_price
    
    def price_display(self) -> str:
        """Format pricing for display."""
        return f"(${self.input_price:.2f}/${self.output_price:.2f})"
    
    def calculate_conversation_cost(self, user_tokens: int = 125, 
                                   model_tokens: int = 375, 
                                   turns: int = 10) -> float:
        """Calculate cost for a multi-turn conversation.
        
        Args:
            user_tokens: Tokens per user message (default: 125).
            model_tokens: Tokens per model response (default: 375).
            turns: Number of turns in conversation (default: 10).
            
        Returns:
            Total cost in dollars for the conversation.
        """
        total_input_tokens = user_tokens * turns
        total_output_tokens = model_tokens * turns
        
        # Prices are per million tokens
        input_cost = (total_input_tokens / 1_000_000) * self.input_price
        output_cost = (total_output_tokens / 1_000_000) * self.output_price
        
        return input_cost + output_cost
    
    def conversation_cost_display(self) -> str:
        """Format conversation cost for display."""
        cost = self.calculate_conversation_cost()
        if cost == 0:
            return "FREE"
        elif cost < 0.01:
            return f"${cost:.4f}"
        else:
            return f"${cost:.3f}"


class OpenRouterClient:
    """Client for interacting with OpenRouter API."""
    
    def __init__(self, api_key: str):
        """Initialize the OpenRouter client.
        
        Args:
            api_key: OpenRouter API authentication key.
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'HTTP-Referer': 'https://github.com/yourusername/ModelScrapOR',
            'X-Title': 'ModelScrapOR'
        })
    
    def fetch_models(self) -> List[Model]:
        """Fetch all available models from OpenRouter API.
        
        Returns:
            List of Model objects.
            
        Raises:
            RequestException: If API request fails.
        """
        try:
            logger.info("Fetching models from OpenRouter API...")
            response = self.session.get(f"{OPENROUTER_API_BASE}/models")
            response.raise_for_status()
            
            data = response.json()
            models = []
            
            for model_data in data.get('data', []):
                try:
                    model = Model(
                        id=model_data['id'],
                        name=model_data['name'],
                        pricing=model_data.get('pricing', {}),
                        context_length=model_data.get('context_length', 0),
                        architecture=model_data.get('architecture'),
                        top_provider=model_data.get('top_provider'),
                        per_request_limits=model_data.get('per_request_limits')
                    )
                    models.append(model)
                except (KeyError, ValueError) as e:
                    logger.warning(f"Skipping model due to parsing error: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(models)} models")
            return models
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models: {e}")
            raise


def categorize_models(models: List[Model]) -> Dict[str, List[Model]]:
    """Categorize models based on their names and capabilities.
    
    This is a heuristic approach since OpenRouter doesn't provide explicit categories.
    Models can appear in multiple categories.
    
    Args:
        models: List of Model objects.
        
    Returns:
        Dictionary mapping category names to lists of models.
    """
    categorized = {category: [] for category in CATEGORIES}
    
    # Keywords for categorization (case-insensitive)
    keywords = {
        "Programming": ["code", "coder", "coding", "program", "dev", "devstral"],
        "Roleplay": ["roleplay", "rp", "character", "chat", "story", "creative"],
        "Marketing": ["marketing", "business", "content", "copywriting"],
        "SEO": ["seo", "search", "optimization"],
        "Technology": ["tech", "technical", "system", "engineering"],
        "Science": ["science", "scientific", "research", "academic"],
        "Translation": ["translate", "translation", "language", "multilingual"],
        "Legal": ["legal", "law", "compliance"],
        "Finance": ["finance", "financial", "economics", "trading"],
        "Health": ["health", "medical", "healthcare", "clinical"],
        "Trivia": ["trivia", "quiz", "general", "knowledge"],
        "Academia": ["academic", "scholar", "research", "education"]
    }
    
    for model in models:
        name_lower = model.name.lower()
        id_lower = model.id.lower()
        matched = False
        
        for category, category_keywords in keywords.items():
            if any(kw in name_lower or kw in id_lower for kw in category_keywords):
                categorized[category].append(model)
                matched = True
        
        # If no specific match, add to general categories
        if not matched:
            # Add to multiple general categories
            for general_cat in ["Technology", "Trivia", "Academia"]:
                categorized[general_cat].append(model)
    
    # Ensure each category has at least some models
    for category in CATEGORIES:
        if not categorized[category]:
            # Add top 10 general models to empty categories
            categorized[category] = sorted(models, key=lambda m: m.total_price, reverse=True)[:10]
    
    return categorized


def rank_models(models: List[Model]) -> List[Tuple[Model, int]]:
    """Rank models by a heuristic (for now, by total price as a proxy for capability).
    
    Args:
        models: List of Model objects.
        
    Returns:
        List of tuples (Model, rank).
    """
    # Sort by price (higher price often correlates with capability)
    # This is a placeholder - in production, use actual performance metrics
    sorted_models = sorted(models, key=lambda m: m.total_price, reverse=True)
    return [(model, idx + 1) for idx, model in enumerate(sorted_models)]


def generate_expandable_list(models_data: list, list_id: str, initial_count: int = 5) -> str:
    """Generate an expandable list with show more functionality.
    
    Args:
        models_data: List of HTML strings for each model
        list_id: Unique ID for this list
        initial_count: Number of items to show initially
        
    Returns:
        HTML string with expandable list
    """
    html = []
    total = len(models_data)
    
    for i, model_html in enumerate(models_data):
        # Add visibility classes based on position
        if i < initial_count:
            html.append(model_html)
        elif i < 10:
            # Hidden initially, shown when expanding to 10
            html.append(model_html.replace('<li', '<li class="hidden show-10"'))
        else:
            # Hidden initially, shown when expanding to 25
            html.append(model_html.replace('<li', '<li class="hidden show-25"'))
    
    # Add expand button if there are more than initial_count items
    if total > initial_count:
        html.append(f'''                        <li class="expand-control">
                            <button class="expand-btn" data-list="{list_id}" data-state="5" onclick="expandList('{list_id}')">
                                Show More... (5/{total})
                            </button>
                        </li>\n''')
    
    return ''.join(html)


def generate_html(categorized_models: Dict[str, List[Model]], date_str: str) -> str:
    """Generate HTML report for all categories.
    
    Args:
        categorized_models: Dictionary mapping categories to model lists.
        date_str: Date string for the report (YYYY-MM-DD format).
        
    Returns:
        Complete HTML document as string.
    """
    html_parts = [f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenRouter Models - {date_str}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header id="top">
            <h1>OpenRouter Models as of {date_str}</h1>
            <div class="header-controls">
                <button id="theme-toggle" aria-label="Toggle dark/light mode">🌓</button>
            </div>
        </header>
        <nav class="date-nav">
            <button id="prev-date" aria-label="Previous day">← Previous Day</button>
            <span id="current-date">{date_str}</span>
            <button id="next-date" aria-label="Next day">Next Day →</button>
        </nav>
        <nav class="category-nav">
            <ul>
"""]
    
    # Add category navigation
    for category in CATEGORIES:
        html_parts.append(f'                <li><a href="#{category.lower()}">{category}</a></li>\n')
    
    html_parts.append("""            </ul>
        </nav>
        <main>
""")
    
    # Generate sections for each category
    for category in CATEGORIES:
        models = categorized_models[category]
        if not models:
            continue
        
        # Rank models for this category
        ranked_models = rank_models(models)
        rankings_map = {model.id: rank for model, rank in ranked_models}
        
        # Sort by price (highest first)
        by_price_high = sorted(models, key=lambda m: m.total_price, reverse=True)
        
        # Sort by price (lowest first)
        by_price_low = sorted(models, key=lambda m: m.total_price)
        
        # Get free models (cap at 25)
        free_models = [m for m in models if m.is_free][:25]
        
        category_id = category.lower().replace(' ', '-')
        
        html_parts.append(f"""
            <section id="{category_id}" class="category-section">
                <div class="category-header">
                    <h2>{category}</h2>
                    <a href="#top" class="back-to-top-btn">↑ Go to Top</a>
                </div>
                
                <article class="subsection">
                    <h3>Daily Rankings</h3>
                    <ol class="model-list" id="{category_id}-daily">
""")
        
        # Daily Rankings - Generate all 25, but mark visibility
        daily_items = []
        for model, rank in ranked_models[:25]:
            conv_cost = model.conversation_cost_display()
            daily_items.append(f'                        <li>{model.display_name} <span class="price">{model.price_display()}</span> <span class="conv-cost">10-turn: {conv_cost}</span></li>\n')
        
        html_parts.append(generate_expandable_list(daily_items, f"{category_id}-daily"))
        
        html_parts.append("""                    </ol>
                </article>
                
                <article class="subsection">
                    <h3>Rankings by Price (Highest First)</h3>
                    <ol class="model-list" id=\"""" + f"{category_id}-high" + """\">
""")
        
        # By Price (Highest) - top 25 with ranking reference
        high_items = []
        for model in by_price_high[:25]:
            ranking = rankings_map.get(model.id, '?')
            conv_cost = model.conversation_cost_display()
            high_items.append(f'                        <li>{model.display_name} <span class="price">{model.price_display()}</span> <span class="ranking">(ranking: #{ranking})</span> <span class="conv-cost">10-turn: {conv_cost}</span></li>\n')
        
        html_parts.append(generate_expandable_list(high_items, f"{category_id}-high"))
        
        html_parts.append("""                    </ol>
                </article>
                
                <article class="subsection">
                    <h3>Rankings by Price (Lowest First)</h3>
                    <ol class="model-list" id=\"""" + f"{category_id}-low" + """\">
""")
        
        # By Price (Lowest) - top 25 with ranking reference
        low_items = []
        for model in by_price_low[:25]:
            ranking = rankings_map.get(model.id, '?')
            conv_cost = model.conversation_cost_display()
            low_items.append(f'                        <li>{model.display_name} <span class="price">{model.price_display()}</span> <span class="ranking">(ranking: #{ranking})</span> <span class="conv-cost">10-turn: {conv_cost}</span></li>\n')
        
        html_parts.append(generate_expandable_list(low_items, f"{category_id}-low"))
        
        html_parts.append("""                    </ol>
                </article>
""")
        
        # Free Models section (if any)
        if free_models:
            html_parts.append("""                <article class="subsection">
                    <h3>Best FREE Models</h3>
                    <ul class="model-list free-models" id=\"""" + f"{category_id}-free" + """\">
""")
            free_items = []
            for model in free_models:
                ranking = rankings_map.get(model.id, '?')
                free_items.append(f'                        <li><span class="free-badge">[FREE]</span> {model.display_name} <span class="ranking">({category} #{ranking})</span></li>\n')
            
            html_parts.append(generate_expandable_list(free_items, f"{category_id}-free"))
            
            html_parts.append("""                    </ul>
                </article>
""")
        
        html_parts.append("""            </section>
""")
    
    html_parts.append("""        </main>
        <footer>
            <p>Generated by <a href="https://github.com/yourusername/ModelScrapOR" target="_blank">ModelScrapOR</a></p>
            <p>Data sourced from <a href="https://openrouter.ai/" target="_blank">OpenRouter</a></p>
        </footer>
    </div>
    
    <script>
        // Expand list functionality
        function expandList(listId) {
            const list = document.getElementById(listId);
            const btn = list.querySelector('.expand-btn');
            const currentState = parseInt(btn.dataset.state);
            const allItems = list.querySelectorAll('li:not(.expand-control)');
            const totalItems = allItems.length;
            
            if (currentState === 5) {
                // Expand to 10
                list.querySelectorAll('.show-10').forEach(item => item.classList.remove('hidden'));
                btn.dataset.state = '10';
                if (totalItems > 10) {
                    btn.textContent = `Show More... (10/${totalItems})`;
                } else {
                    btn.textContent = `Show Less`;
                    btn.dataset.state = '10-max';
                }
            } else if (currentState === 10) {
                // Expand to 25
                list.querySelectorAll('.show-25').forEach(item => item.classList.remove('hidden'));
                btn.textContent = 'Show Less';
                btn.dataset.state = '25';
            } else {
                // Collapse back to 5
                list.querySelectorAll('.show-10, .show-25').forEach(item => item.classList.add('hidden'));
                btn.textContent = `Show More... (5/${totalItems})`;
                btn.dataset.state = '5';
            }
        }
        
        // Dark/Light mode toggle
        const themeToggle = document.getElementById('theme-toggle');
        const html = document.documentElement;
        
        // Check for saved theme preference or default to system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        const currentTheme = savedTheme || systemPreference;
        
        html.setAttribute('data-theme', currentTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
        
        // Smooth scroll for navigation
        document.querySelectorAll('.category-nav a').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
        
        // Date navigation
        document.getElementById('prev-date').addEventListener('click', () => {
            const date = new Date('""" + date_str + """');
            date.setDate(date.getDate() - 1);
            const newDate = date.toISOString().split('T')[0];
            window.location.href = `models-${newDate}.html`;
        });
        
        document.getElementById('next-date').addEventListener('click', () => {
            const date = new Date('""" + date_str + """');
            date.setDate(date.getDate() + 1);
            const newDate = date.toISOString().split('T')[0];
            const today = new Date().toISOString().split('T')[0];
            if (newDate <= today) {
                window.location.href = `models-${newDate}.html`;
            } else {
                alert('Future dates not available yet!');
            }
        });
    </script>
</body>
</html>
""")
    
    return ''.join(html_parts)


def generate_css() -> str:
    """Generate CSS stylesheet with dark/light mode support.
    
    Returns:
        CSS stylesheet as string.
    """
    return """/* ModelScrapOR Stylesheet */

:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --border-color: #e0e0e0;
    --accent-color: #3b82f6;
    --accent-hover: #2563eb;
    --free-badge: #10b981;
    --shadow: rgba(0, 0, 0, 0.1);
}

[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --text-primary: #f5f5f5;
    --text-secondary: #a0a0a0;
    --border-color: #404040;
    --accent-color: #60a5fa;
    --accent-hover: #3b82f6;
    --free-badge: #34d399;
    --shadow: rgba(0, 0, 0, 0.3);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 0;
    border-bottom: 2px solid var(--border-color);
    margin-bottom: 20px;
}

h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
}

.header-controls {
    display: flex;
    gap: 10px;
    align-items: center;
}

#theme-toggle {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

#theme-toggle:hover {
    transform: scale(1.1);
    border-color: var(--accent-color);
}

.date-nav {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    padding: 15px;
    background: var(--bg-secondary);
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px var(--shadow);
}

.date-nav button {
    background: var(--accent-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s ease;
}

.date-nav button:hover {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.date-nav button:active {
    transform: translateY(0);
}

#current-date {
    font-weight: 600;
    font-size: 1.1rem;
    min-width: 120px;
    text-align: center;
}

.category-nav {
    background: var(--bg-secondary);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 2px 4px var(--shadow);
}

.category-nav ul {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.category-nav li a {
    display: inline-block;
    padding: 8px 16px;
    background: var(--bg-primary);
    color: var(--text-primary);
    text-decoration: none;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
}

.category-nav li a:hover {
    background: var(--accent-color);
    color: white;
    border-color: var(--accent-color);
}

.category-section {
    margin-bottom: 50px;
    padding: 30px;
    background: var(--bg-secondary);
    border-radius: 12px;
    box-shadow: 0 4px 6px var(--shadow);
}

.category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    border-bottom: 3px solid var(--accent-color);
    padding-bottom: 10px;
}

.category-section h2 {
    font-size: 1.8rem;
    color: var(--accent-color);
    margin: 0;
}

.back-to-top-btn {
    background: var(--accent-color);
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.back-to-top-btn:hover {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.subsection {
    margin-bottom: 30px;
    padding: 20px;
    background: var(--bg-primary);
    border-radius: 8px;
    border-left: 4px solid var(--accent-color);
}

.subsection h3 {
    font-size: 1.3rem;
    margin-bottom: 15px;
    color: var(--text-primary);
}

.model-list {
    list-style-position: inside;
    padding-left: 0;
}

.model-list li {
    padding: 10px;
    margin-bottom: 8px;
    background: var(--bg-secondary);
    border-radius: 6px;
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.model-list li:not(.expand-control):hover {
    background: var(--bg-primary);
    border-color: var(--accent-color);
    transform: translateX(5px);
}

.model-list li.hidden {
    display: none;
}

.expand-control {
    list-style: none;
    background: transparent;
    border: none;
    padding: 0;
    margin-top: 10px;
}

.expand-control:hover {
    background: transparent;
    transform: none;
}

.expand-btn {
    width: 100%;
    background: var(--accent-color);
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.expand-btn:hover {
    background: var(--accent-hover);
    transform: translateY(-2px);
}

.expand-btn:active {
    transform: translateY(0);
}

.price {
    color: var(--accent-color);
    font-weight: 600;
    margin-left: 10px;
}

.ranking {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-left: 10px;
}

.conv-cost {
    margin-left: auto;
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 600;
    background: var(--bg-secondary);
    padding: 2px 8px;
    border-radius: 4px;
    white-space: nowrap;
}

.free-badge {
    background: var(--free-badge);
    color: white;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-right: 8px;
}

.free-models {
    list-style: none;
}

footer {
    text-align: center;
    padding: 30px 0;
    margin-top: 50px;
    border-top: 2px solid var(--border-color);
    color: var(--text-secondary);
}

footer a {
    color: var(--accent-color);
    text-decoration: none;
}

footer a:hover {
    text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    header {
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }
    
    h1 {
        font-size: 1.5rem;
    }
    
    .category-header {
        flex-direction: column;
        gap: 15px;
        align-items: flex-start;
    }
    
    .back-to-top-btn {
        width: 100%;
        text-align: center;
    }
    
    .date-nav {
        flex-direction: column;
        gap: 10px;
    }
    
    .date-nav button {
        width: 100%;
    }
    
    .category-nav ul {
        justify-content: center;
    }
    
    .category-section {
        padding: 20px;
    }
    
    .model-list li {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .conv-cost {
        margin-left: 0;
        margin-top: 5px;
    }
    
    .model-list li:not(.expand-control):hover {
        transform: none;
    }
}
"""


def main():
    """Main execution function."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        logger.error("OPENROUTER_API_KEY not found in environment variables")
        logger.error("Please create a .env file with: OPENROUTER_API_KEY=your_key_here")
        sys.exit(1)
    
    try:
        # Initialize client
        client = OpenRouterClient(api_key)
        
        # Fetch models
        models = client.fetch_models()
        
        if not models:
            logger.error("No models fetched from API")
            sys.exit(1)
        
        # Categorize models
        logger.info("Categorizing models...")
        categorized_models = categorize_models(models)
        
        # Generate date string
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Generate HTML
        logger.info("Generating HTML report...")
        html_content = generate_html(categorized_models, date_str)
        
        # Write HTML file
        html_filename = f"models-{date_str}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"HTML report saved to: {html_filename}")
        
        # Generate and write CSS file
        logger.info("Generating CSS stylesheet...")
        css_content = generate_css()
        with open('style.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        logger.info("CSS stylesheet saved to: style.css")
        
        logger.info("✅ Report generation complete!")
        
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
