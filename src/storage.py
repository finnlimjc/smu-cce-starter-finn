"""Save, list and read analyses as Markdown files in the analyses-data/ folder."""

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

# Anchored to this file (not the working directory) so it is identical in Codespaces, EC2 and local runs.
ANALYSES_DIR = Path(__file__).resolve().parent.parent / "analyses-data"
FILENAME_PATTERN = re.compile(r"^(?P<ticker>[^_]+)_(?P<kind>[^_]+)_(?P<stamp>\d{8}-\d{6})(?:_\d+)?\.md$")

def _slug(text:str) -> str:
    """Text reduced to letters, digits, dots and hyphens, safe in a filename."""
    slug = re.sub(r"[^A-Za-z0-9.]+", "-", text.strip()).strip("-.")
    return slug or "unknown"

def make_filename(ticker:str, analysis_type:str, created:datetime) -> str:
    """Build a filename such as MU_stock-price-ratings_20261017-140322.md."""
    stamp = created.strftime("%Y%m%d-%H%M%S")
    return f"{_slug(ticker).upper()}_{_slug(analysis_type).lower()}_{stamp}.md"

def _df_to_markdown(df:pd.DataFrame) -> str:
    """Render a DataFrame as a Markdown table (index included)."""
    def cell(value) -> str:
        text = "" if pd.isna(value) else str(value)
        return text.replace("|", "\\|").replace("\n", " ")
    
    headers = [cell(df.index.name or "")] + [cell(col) for col in df.columns]
    lines = ["| " + " | ".join(headers) + " |", "|" + " --- |" * len(headers)]
    for index_value, row in df.iterrows():
        cells = [cell(index_value)] + [cell(value) for value in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

def build_body(analysis_type:str, data) -> str:
    """Convert the data returned by src.analysis into Markdown for the given analysis type."""
    if analysis_type == "filings":
        sections = []
        for name, df in data.items():
            table = "No data available." if df is None or df.empty else _df_to_markdown(df)
            sections.append(f"### {name}\n\n{table}")
        return "\n\n".join(sections)
    if analysis_type == "news":
        items = [f"{i}. **{article['title']}**\n   {article['description']}" for i, article in enumerate(data, 1)]
        return "\n\n".join(items)
    price, ratings = data
    return f"**Current price (USD):** {price:,.2f}\n\n### Analyst recommendations\n\n{_df_to_markdown(ratings)}"

def build_markdown(ticker:str, analysis_type:str, params:dict, body:str, created:datetime) -> str:
    """Wrap an analysis body with a header listing ticker, type, parameters and creation date."""
    param_text = ", ".join(f"{key}: {value}" for key, value in params.items()) or "none"
    created_text = created.strftime("%Y-%m-%d %H:%M:%S")
    header = (
        f"# {ticker} - {analysis_type}\n\n"
        f"- **Ticker:** {ticker}\n"
        f"- **Analysis type:** {analysis_type}\n"
        f"- **Parameters:** {param_text}\n"
        f"- **Created:** {created_text}\n"
    )
    return f"{header}\n---\n\n{body}\n"

def save_analysis(ticker:str, analysis_type:str, params:dict, body:str) -> str:
    """
    Write an analysis to analyses-data/ and return the filename used.
    
    Inputs:
    - ticker, analysis_type, params: shown in the file header and used in the filename.
    - body: the Markdown contents of the analysis.
    
    Outputs:
    - Filename of the new file. Raises OSError if it cannot be written.
    """
    created = datetime.now()
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    content = build_markdown(ticker, analysis_type, params, body, created)
    base = make_filename(ticker, analysis_type, created)
    for attempt in range(1, 1000):
        filename = base if attempt == 1 else f"{base[:-3]}_{attempt}.md"
        try:
            with open(ANALYSES_DIR / filename, "x", encoding="utf-8") as f: #"x" refuses to overwrite an existing file
                f.write(content)
        except FileExistsError:
            continue
        return filename
    raise OSError("Could not find an unused filename.")

def label_for(filename:str) -> str:
    """Readable label such as 'MU | stock-price-ratings | 2026-10-17 14:03:22'."""
    match = FILENAME_PATTERN.match(filename)
    if match is None:
        return filename
    stamp = datetime.strptime(match["stamp"], "%Y%m%d-%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    return f"{match['ticker']} | {match['kind'].replace('-', ' ')} | {stamp}"

def list_analyses() -> list[str]:
    """Saved filenames, newest first. Empty if nothing has been saved yet. Raises OSError on read errors."""
    if not ANALYSES_DIR.is_dir():
        return []
    files = [path for path in ANALYSES_DIR.glob("*.md") if path.is_file()]
    files.sort(key=lambda path: (path.stat().st_mtime, path.name), reverse=True)
    return [path.name for path in files]

def read_analysis(filename:str) -> str:
    """Return the Markdown text of a saved analysis. Raises OSError if it cannot be read."""
    path = ANALYSES_DIR / Path(filename).name #drops any directory part so only analyses-data/ is readable
    return path.read_text(encoding="utf-8")
