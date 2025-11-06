

class StonkSet:
    def __init__(self):
        """Initialize the set with ticker data"""
        self._stonkset = set()
    
        ticker_files = [
            "resources/nasdaq_tickers.txt",
            "resources/nyse_tickers.txt"
            ]
        for tf in ticker_files:
            with open(tf) as ticker_file:
                for ticker in ticker_file.readlines():
                    self._stonkset.add(ticker.rstrip())

    def contains(self, stonk):
        """Test if the stonk ticker is in the set"""
        return stonk in self._stonkset


    def size(self):
        """Return the number of tickers in the set"""
        return len(self._stonkset)


if __name__ == "__main__":
    stonks = StonkSet()
    print(f"StonkSet contains {stonks.size()} tickers")

    good_tickers = ["NVDA", "MSI", "RXT", "V", "O"]
    bad_tickers = ["banana", "nvda", "1", "TORC"]

    for ticker in good_tickers:
        print(f"Is {ticker} in StonkSet? {stonks.contains(ticker)}")
    for ticker in bad_tickers:
        print(f"Is {ticker} in StonkSet? {stonks.contains(ticker)}")
