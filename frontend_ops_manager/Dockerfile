# Use Node.js 18 as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the Angular application
RUN npm run build

# Expose port 4200
EXPOSE 4200

# Start the development server
CMD ["npm", "start"]
