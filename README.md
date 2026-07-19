# Local Food Wastage Management System

A full-stack web application built with Streamlit to help reduce food waste by connecting food providers with receivers in need.

## Tech Stack

- **Frontend**: Streamlit (multi-page app)
- **Backend**: Python (business logic, SQL queries, helper functions)
- **Database**: SQLite (food_wastage.db)
- **Libraries**: streamlit, pandas, plotly, streamlit-option-menu, streamlit-extras, sqlite3

## Features

- **Dashboard**: Real-time KPIs, interactive charts, recent listings and claims
- **Food Listings**: Browse, filter, and claim available food items
- **Add Food Listing**: Form to post surplus food with expiry tracking
- **My Listings**: Manage your own food postings
- **Claims Management**: Track and manage food claims with approval workflow
- **Providers**: View and manage registered food providers
- **Receivers**: View and manage registered receivers/organizations
- **Analytics**: Detailed charts and insights on food distribution
- **Reports**: Generate and export comprehensive reports (CSV)
- **Profile & Settings**: User profile management and app preferences

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database with seed data**:
   ```bash
   python db/seed_data.py
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
food waste/
├── app.py                          # Entry point with sidebar navigation
├── requirements.txt                # Python dependencies
├── db/
│   ├── database.py                 # Database connection and CRUD functions
│   ├── seed_data.py                # Mock data generator
│   └── food_wastage.db             # SQLite database (created after seeding)
├── pages/
│   ├── 1_Dashboard.py              # Main dashboard with KPIs and charts
│   ├── 2_Add_Food_Listing.py       # Form to add new food listings
│   ├── 3_Food_Listings.py          # Browse all food listings
│   ├── 4_My_Listings.py            # Manage your own listings
│   ├── 5_Claims.py                 # Manage food claims
│   ├── 6_Providers.py              # View providers
│   ├── 7_Receivers.py              # View receivers
│   ├── 8_Analytics.py              # Detailed analytics
│   ├── 9_Reports.py                # Generate reports
│   └── 10_Profile_Settings.py      # User profile and settings
├── utils/
│   ├── styles.py                   # Custom CSS theme
│   └── helpers.py                  # Utility functions
└── assets/
    └── README.md                   # Assets documentation
```

## Database Schema

### Providers
- id, name, type, address, city, contact, verified

### Receivers
- id, name, type, city, contact

### Food Listings
- id, food_name, food_type, meal_type, quantity, unit, provider_id, location, expiry_time, image_url, status, created_at

### Claims
- id, food_id, receiver_id, quantity_claimed, status, claimed_at

## Seed Data

The seed script creates realistic mock data:
- 45 providers (restaurants, hotels, caterers, etc.)
- 78 receivers (shelters, food banks, NGOs, etc.)
- 128 food listings (weighted distribution: 35% cooked food, 22% fruits, 16% vegetables, 14% bakery, 13% others)
- 96 claims with varied statuses over the last 30 days

## Theme

The application uses a custom forest-green theme (#1B4D3E) with:
- White main background
- Dark green sidebar (#0F2E24)
- Inter/Poppins fonts
- Rounded cards with soft shadows
- Color-coded status badges

## Usage

1. **Dashboard**: View overview statistics and recent activity
2. **Add Food Listing**: Fill out the form to post surplus food
3. **Food Listings**: Browse and filter available food, claim items
4. **My Listings**: View and manage your posted food items
5. **Claims**: Review and approve/reject claim requests
6. **Analytics**: Explore detailed charts and trends
7. **Reports**: Generate and export summary reports

## Notes

- The application uses session state for basic user authentication simulation
- All data is stored locally in SQLite
- Images use placeholder URLs from via.placeholder.com
- The app is designed for demonstration and can be extended with real authentication, image uploads, and notifications
