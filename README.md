# Financial Sentiment Analysis with BERT

In progress. Sentiment Analysis and Portfolio Creation of WallStreetBets opinions.

## Notes

[TF Colab](https://colab.research.google.com/drive/1CHJLsqOmoFE-XMrNtOxTXs4k2cvefgSh#scrollTo=1B8tFfYpGGPU)

## Approach

- Scrape data via scrape.py, write to csv, and preprocess
  - Preprocess: Label data and throw out bad data via label.py
  - Associate signals with stock tickers
- Train and store model (BERT)
- Design frontend for ghpages
- CRON job to run daily and update portfolio?
- Portion size by [HRP](https://www.mathworks.com/help/finance/create-hierarchical-risk-parity-portfolio.html) model (create WSB index)
