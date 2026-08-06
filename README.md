Market Pulse

A real-time price monitoring dashboard that scrapes and displays data from multiple markets simultaneously. Built with Flask, Vue 3, and Three.js.

Overview

Market Pulse monitors prices across two markets: retail goods and digital assets. It scrapes live data, stores it, and displays it through a single-page dashboard with search, filters, watchlist, top movers, and export capabilities.

The application is designed to be extendable to other markets such as forex, commodities, or any other data source that can be scraped or accessed via API.

Team

Role	         Name	              Responsibilities
Team Lead	     Ihtishaam Johnson	Architecture, code reviews, approvals
Scrum Master	 Owam	              Standups, blockers, team velocity
Backend	       Zaarah	            Flask server, API endpoints
Backend	       Adam	              Web scrapers, data extraction
Backend	       Purrity	          Storage layer, search, history
Frontend	     Caleb	            Navigation, layout, dashboard
Frontend	     Chad	              Stores, watchlist, export
Frontend	     Likona	            Three.js 3D visualizations
QA	           Azhar	            Testing, bug logging

Tech Stack:

Backend:
Flask 3.1.3
SQLite
APScheduler (background scraping)
Requests + BeautifulSoup4 (web scraping)
Flask-CORS
Gunicorn (production)

Frontend:
Vue 3
Pinia (state management)
Vue Router
Three.js (3D bar chart)
Axios
Vite

Features:
Dashboard — Live prices, total items, success rate, market overview

3D Bar Chart — Interactive visualization of market health

Top Movers — View the five biggest price changes across both markets

Watchlist — Save and track specific items

History — Full log of all scraping runs

Search & Filters — Find items by name, filter by source or price range

Export — CSV export for history and data tables

Websites Manager — Add or remove scraping targets

Dark Mode — Toggle between light and dark themes

Data Sources:
Source	        Type	              Items
WebScraper.io	  Retail electronics	21
CoinPaprika	    Cryptocurrencies	  10

Both sources are configurable. Additional sources can be added through the Websites Manager or by extending the scraper code.

Running Locally

Prerequisites

Python 3.10+
Node.js 18+
npm 9+
Git
Backend Setup

bash
# Clone the repository
git clone https://github.com/adamjattiem12-gif/-Flask-Web-Scraping-Dashboard.git
cd -Flask-Web-Scraping-Dashboard

# Create and activate a virtual environment
cd backend
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
The backend will be available at http://127.0.0.1:5000.

Frontend Setup

bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
The frontend will be available at http://localhost:5173.

Environment Variables

Create a .env file in the frontend directory (optional):

env
VITE_API_URL=http://127.0.0.1:5000
API Endpoints

Endpoint	Method	Description
/api/health	GET	Health check
/api/items	GET	Get all items (paginated)
/api/statistics	GET	Market statistics
/api/scrape	POST	Trigger a scrape
/api/clear-all	POST	Clear all data
/api/history	GET	Scrape history
/api/search	GET	Search items
/api/websites	GET	Registered websites
/api/websites	POST	Add a website
/api/websites/<id>	DELETE	Remove a website
Deployment

The application is deployed on Render. The backend runs as a Web Service and the frontend as a Static Site.

Backend

Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && gunicorn app:app
Frontend

Build Command: cd frontend && npm install && npm run build
Publish Directory: frontend/dist
Environment Variable: VITE_API_URL = backend URL
Code Structure

text
project/
├── backend/
│   ├── app.py                 # Flask entry point
│   ├── routes/                # API routes
│   │   ├── items.py
│   │   ├── statistics.py
│   │   ├── scrape.py
│   │   ├── history.py
│   │   ├── search.py
│   │   └── websites.py
│   ├── scrapers/              # Data scrapers
│   │   ├── ecommerce_scraper.py
│   │   └── crypto_scraper.py
│   ├── services/              # Storage and scheduling
│   │   ├── storage.py
│   │   ├── db.py
│   │   └── scheduler.py
│   ├── models/                # Data models
│   └── utils/                 # Helpers
├── frontend/
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── views/             # Page views
│   │   ├── stores/            # Pinia stores
│   │   ├── services/          # API client
│   │   └── utils/             # Helpers
│   ├── package.json
│   └── vite.config.js
└── data/                      # SQLite database
Contributing

Check the branch merge-backend-frontend
Pull latest changes
Make your changes and test locally
Commit and push
Render auto-deploys from the merge-backend-frontend branch
Do not commit node_modules/ or venv/. Both are listed in .gitignore.

License

This project was developed as part of a team sprint exercise.
