# Development Dockerfile for Angular
FROM node:20

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Expose Angular dev server port
EXPOSE 4200

# Disable Angular analytics
ENV NG_CLI_ANALYTICS=false
ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true

# Run Angular dev server
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--port", "4200", "--poll", "2000"]
