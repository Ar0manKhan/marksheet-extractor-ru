import asyncio
from playwright.async_api import async_playwright, Playwright, Page


async def run(page: Page, rollno):
    # setting course
    await page.wait_for_timeout(100)
    # await page.wait_for_selector('select[ng-model="search.course"]')
    await page.select_option('select[ng-model="search.course"]', 'PG')
    # setting semester
    # await page.wait_for_selector('select[ng-model="search.semester"]')
    await page.select_option('select[ng-model="search.semester"]', '1')
    # setting stream
    # await page.wait_for_selector('select[ng-model="search.stream"]')
    await page.select_option('select[ng-model="search.stream"]', 'M.C.A.')
    # setting rollno
    # await page.wait_for_selector('input[ng-model="search.rollno"]')
    await page.fill('input[ng-model="search.rollno"]', rollno)
    # click button #btn_result
    # await page.wait_for_selector('#btn_result')
    await page.click('#btn_result')
    await page.wait_for_load_state('networkidle')
    # print pdf
    await page.pdf(path=f"results/{rollno}.pdf", format="A4", print_background=True)
    print("PDF downloaded")
    # go back to previous page
    # await page.go_back()
    await page.close()


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        tasks = []
        rollnos = []
        # reading roll number file
        with open("roll_numbers.txt") as f:
            rollnos = f.read().splitlines()
        async def process_in_new_tab(rollno):
            page = await context.new_page()
            await page.goto("https://www.exam.ranchiuniversity.co.in/result")
            await page.wait_for_load_state('networkidle')
            print(f"Processing {rollno=}")
            await run(page, rollno)
        tasks = [process_in_new_tab(rollno) for rollno in rollnos]
        await asyncio.gather(*tasks)
        await browser.close()


if __name__ == "__main__":  
    asyncio.run(main())