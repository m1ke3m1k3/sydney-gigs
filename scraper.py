name: Scraper diario

on:
  schedule:
    # Cada día a las 8:00 AM hora Sydney (AEST = UTC+10)
    - cron: '0 22 * * *'
  workflow_dispatch: # permite correrlo manualmente desde GitHub

jobs:
  scrape:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r scraper/requirements.txt
          playwright install chromium

      - name: Run scraper
        run: |
          cd scraper
          python scraper.py

      - name: Commit y push datos actualizados
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add web/data/opportunities.json
          git diff --staged --quiet || git commit -m "chore: actualizar oportunidades $(date -u +'%Y-%m-%d')"
          git push
