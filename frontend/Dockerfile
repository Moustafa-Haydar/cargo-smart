# ========================
# Build stage
# ========================
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application (React/Vite/etc. -> outputs to /app/build)
RUN npm run build


# ========================
# Production stage
# ========================
FROM nginx:alpine

# Install curl for healthcheck
RUN apk --no-cache add curl

# ❌ Do NOT create the nginx user; it already exists in this base image
# (Removed the adduser/chown of system directories)

# Copy nginx configuration
# (OK to chown the file to nginx for readability if you want)
COPY --chown=nginx:nginx nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder --chown=nginx:nginx /app/build /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:80/ || exit 1

# Expose port
EXPOSE 80

# Start nginx (default config drops workers to 'nginx' user)
CMD ["nginx", "-g", "daemon off;"]
