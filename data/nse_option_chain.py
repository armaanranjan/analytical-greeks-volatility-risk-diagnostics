import requests
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent

def get_nse_option_chain(symbol="NIFTY"):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/"
    }

    session = requests.Session()

    try:
        session.get("https://www.nseindia.com", headers=headers, timeout=5)
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()

        if "records" not in data or "data" not in data["records"]:
            raise RuntimeError("Blocked")

        rows = []
        for item in data["records"]["data"]:
            strike = item.get("strikePrice")
            if "CE" in item:
                rows.append({"strike": strike, "price": item["CE"]["lastPrice"]})

        df = pd.DataFrame(rows).set_index("strike")
        if not df.empty:
            return df

    except Exception:
        pass

    # 🔁 FALLBACK
    fallback = DATA_DIR / "sample_option_chain.csv"
    df = pd.read_csv(fallback)

    # 🔒 Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # 🔒 Handle common variants
    if "strike" not in df.columns:
        if "strikes" in df.columns:
            df.rename(columns={"strikes": "strike"}, inplace=True)
        elif "k" in df.columns:
            df.rename(columns={"k": "strike"}, inplace=True)

    if "price" not in df.columns:
        if "lastprice" in df.columns:
            df.rename(columns={"lastprice": "price"}, inplace=True)
        elif "close" in df.columns:
            df.rename(columns={"close": "price"}, inplace=True)

    # 🔒 Final validation
    if "strike" not in df.columns or "price" not in df.columns:
        raise RuntimeError(
            f"Fallback CSV must contain columns ['strike','price'], found {df.columns.tolist()}"
        )

    return df.set_index("strike")

