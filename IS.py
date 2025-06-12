import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_espn_nba_teams_with_logos():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("🔍 Navigating to ESPN NBA Teams page...")
        await page.goto("https://www.espn.com/nba/teams", timeout=60000)
        await page.wait_for_selector(".TeamLinks")

        teams = await page.query_selector_all(".TeamLinks")
        data = []

        for team in teams:
            try:
                name_el = await team.query_selector("h2")
                team_name = (await name_el.inner_text()).strip() if name_el else "N/A"

                img_el = await team.query_selector("img")
                img_url = await img_el.get_attribute("src") if img_el else "N/A"

                data.append({
                    "Team Name": team_name,
                    "Logo URL": img_url
                })

            except Exception as e:
                print(f"⚠️ Skipping due to error: {e}")

        await browser.close()

        # Save to Excel
        df = pd.DataFrame(data)
        df.to_excel("nba_teams_with_logos.xlsx", index=False)
        print("✅ NBA teams + logos saved to nba_teams_with_logos.xlsx")

if __name__ == "__main__":
    asyncio.run(scrape_espn_nba_teams_with_logos())
