"""
Writes competitor analysis results to Google Sheets "Competitor-Map"
"""
from sheets.sheets_reader import get_client


def write_competitor_map(results):
    client = get_client()
    sheet  = client.open("Competitor-Map").sheet1
    sheet.clear()

    headers = [
        "Company", "Sector", "Stage", "Moat Rating", "Moat Explanation",
        "Competitor 1", "Funding 1", "Threat 1",
        "Competitor 2", "Funding 2", "Threat 2",
        "Competitor 3", "Funding 3", "Threat 3",
        "Competitor 4", "Funding 4", "Threat 4",
        "Competitor 5", "Funding 5", "Threat 5",
    ]

    rows = [headers]
    for r in results:
        row = [
            r["company_name"],
            r["sector"],
            r["stage"],
            r["moat_rating"],
            r["moat_explanation"],
        ]
        for comp in r["competitors"][:5]:
            row += [
                comp.get("name", ""),
                comp.get("funding", ""),
                comp.get("threat", ""),
            ]
        # Pad if fewer than 5 competitors
        while len(row) < len(headers):
            row.append("")
        rows.append(row)

    sheet.update(rows, "A1")
    print(f"Written {len(results)} companies to Competitor-Map sheet")
