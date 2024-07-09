import streamlit as st
from googlesearch import search
import html2text
import asyncio
from playwright.async_api import async_playwright


def google_search(query):
    """
    Perform a Google search for the given query,
    and return URLs that contain "wikipedia.org" in their address.
    """
    search_results = []
    for url in search(query, num_results=2):
        if "wikipedia.org" in url:
            search_results.append(url)
    return search_results


async def scrape_and_convert_to_markdown(url):
    """
    Asynchronously scrape the HTML content from a given URL,
    convert it to Markdown format using html2text library
    and return the markdown string.

    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()

    h = html2text.HTML2Text()
    h.ignore_links = False
    markdown = h.handle(content)
    return markdown

st.title('Web Scraper')

query = st.text_input('Enter your search query:', 'Elden Ring')

if st.button('Search'):
    st.subheader('Search Results:')

    results = google_search(query)
    print(results)

    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

    for result in results:
        markdown = loop.run_until_complete(
            scrape_and_convert_to_markdown(result)
        )
        st.markdown(markdown)

    print("Done")
