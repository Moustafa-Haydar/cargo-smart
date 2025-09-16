FROM n8nio/n8n:latest

USER root

# Install system dependencies for Playwright
RUN apk add --no-cache \
    npm \
    chromium \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    nodejs \
    yarn \
    && mkdir -p /home/node/.n8n \
    && chown -R node:node /home/node/.n8n

# Set environment variables for Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 \
    CHROME_PATH=/usr/bin/chromium-browser

USER node

WORKDIR /home/node/.n8n

# Initialize and install dependencies
RUN npm init -y && \
    npm install pdfreader@3 playwright@1.54.2 --omit=dev && \
    # Create a custom module for Playwright functions
    mkdir -p /home/node/.n8n/custom && \
    echo 'const { chromium } = require("playwright"); \n\
    async function scrapeWebsite(url, selectors) { \n\
    const browser = await chromium.launch({ \n\
    executablePath: "/usr/bin/chromium-browser", \n\
    args: ["--no-sandbox", "--disable-setuid-sandbox"] \n\
    }); \n\
    const context = await browser.newContext(); \n\
    const page = await context.newPage(); \n\
    await page.goto(url); \n\
    const results = {}; \n\
    for (const [key, selector] of Object.entries(selectors)) { \n\
    results[key] = await page.locator(selector).textContent(); \n\
    } \n\
    await browser.close(); \n\
    return results; \n\
    } \n\
    module.exports = { scrapeWebsite };' > /home/node/.n8n/custom/playwright-helpers.js

CMD ["n8n", "start"]
