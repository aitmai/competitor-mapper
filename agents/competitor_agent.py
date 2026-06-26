"""
Competitor Agent
Web searches each startup's competitive landscape and scores it using Claude
"""
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()


class CompetitorAgent:

    def analyze(self, startup: dict) -> dict:
        """Full competitor analysis for one startup."""
        search_results = self._web_search(startup)
        analysis      = self._analyze_with_claude(startup, search_results)

        return {
            "company_name":     startup["company_name"],
            "sector":           startup["sector"],
            "stage":            startup["stage"],
            "website":          startup["website"],
            "description":      startup["description"],
            "competitors":      analysis.get("competitors", []),
            "moat_rating":      analysis.get("moat_rating", "Unknown"),
            "moat_explanation": analysis.get("moat_explanation", ""),
            "market_summary":   analysis.get("market_summary", ""),
        }

    def _web_search(self, startup: dict) -> str:
        """Search for competitors using SerpAPI or fallback to DuckDuckGo."""
        query = f"{startup['company_name']} competitors {startup['sector']} startup funding 2024 2025"

        # Try DuckDuckGo instant answer API (free, no key needed)
        try:
            resp = requests.get(
                "https://api.duckduckgo.com/",
                params={
                    "q":      query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1,
                },
                timeout=10
            )
            data = resp.json()
            text = data.get("AbstractText", "") or ""
            related = " ".join(
                r.get("Text", "") for r in data.get("RelatedTopics", [])[:5]
            )
            return f"{text} {related}".strip() or f"No search results found for {startup['company_name']}"
        except Exception as e:
            return f"Search unavailable: {e}"

    def _analyze_with_claude(self, startup: dict, search_context: str) -> dict:
        """Send startup info + search results to Claude for competitor analysis."""

        prompt = f"""You are a venture capital analyst specializing in competitive landscape analysis.

Analyze the competitive landscape for this startup:

Company: {startup['company_name']}
Sector: {startup['sector']}
Stage: {startup['stage']}
Description: {startup['description']}
Website: {startup['website']}

Search context:
{search_context}

Based on your knowledge of this sector, identify the top 5 competitors.

Return ONLY valid JSON with no markdown or backticks:
{{
  "competitors": [
    {{
      "name": "Competitor Name",
      "funding": "$XXM Series X or Public or Bootstrapped",
      "threat": "High|Medium|Low",
      "why": "one sentence on why they are a threat"
    }}
  ],
  "moat_rating": "Strong|Medium|Weak",
  "moat_explanation": "one sentence explaining the competitive moat",
  "market_summary": "two sentences summarizing the competitive landscape"
}}"""

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key":         os.getenv("ANTHROPIC_API_KEY"),
                    "anthropic-version": "2023-06-01",
                    "content-type":      "application/json"
                },
                json={
                    "model":      "claude-haiku-4-5-20251001",
                    "max_tokens": 1000,
                    "messages":   [{"role": "user", "content": prompt}]
                },
                timeout=30
            )

            raw = response.json()["content"][0]["text"].strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw.strip())

        except Exception as e:
            print(f"Claude error for {startup['company_name']}: {e}")
            return {
                "competitors":      [],
                "moat_rating":      "Unknown",
                "moat_explanation": "Analysis unavailable",
                "market_summary":   "Analysis unavailable"
            }
