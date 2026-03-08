# chelyzer

A python project containing a `fastapi` backend and a small `react` frontend for visualizing and analyzing chess game results.

## Installation

Requires python `3.14` or later as well as `npm`.

To install the `chelyzer_rating`, `chelyzer_lichess` and `chelyzer_api` packages run
```bash
pip install -e .
```

To install the `react` frontend run
```bash
npm install --prefix ./frontend
```

## Usage

To run the backend, run
```bash
python -m chelyzer_api
```

To run the frontend, run
```bash
rpm run dev
```
