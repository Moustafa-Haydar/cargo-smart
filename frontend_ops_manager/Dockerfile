# Use Node.js 20 (non-Alpine) to avoid rollup dependency issues
FROM node:20

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Clean install to fix rollup dependency issues
RUN rm -rf node_modules package-lock.json && npm install

# Copy source code
COPY . .

# Build the Angular application for Docker (no SSR, no prerendering)
RUN npx ng build --configuration=docker

# Expose port 4200
EXPOSE 4200

# Disable Angular analytics and start the application
ENV NG_CLI_ANALYTICS=false
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--port", "4200"]
