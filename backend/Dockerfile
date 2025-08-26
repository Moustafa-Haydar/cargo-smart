FROM node:18

# Create app directory
WORKDIR /app

# Copy and install dependencies
COPY package*.json ./
RUN npm install

# Install Playwright browser binaries
RUN npx playwright install --with-deps

# Copy rest of the app
COPY . .

# Expose port
EXPOSE 5000

# Start your app
CMD ["node", "server.js"]
