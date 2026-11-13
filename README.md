# mongodb-restaurant-manager

Console app for managing restaurant records in MongoDB with PyMongo: import from JSON, list, search by name, delete by code.

## Requirements
- Python 3.10+ (uses `match`)
- A running MongoDB server (default `mongodb://localhost:27017`, override with the `MONGO_URI` environment variable)

```bash
pip install -r requirements.txt
python restaurant_manager.py
python tests/test_manager.py      # logic test with an in-memory fake, no MongoDB needed
```

Database `dbRestaurantsAds`, collection `restaurant`. Importing is an upsert by `code`, so running option 1 twice does not create duplicates.

## Data
`data/restaurants.json` has 15 sample records. Known quirks (kept for practice): ratings above 5 (5.5, 6), `postcode` stored as number or string, missing optional fields, record 7's `name` looks like an address.
