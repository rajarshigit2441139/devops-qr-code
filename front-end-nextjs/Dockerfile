# FROM node:20-alpine as base

# WORKDIR /app

# COPY package.json package-lock.json ./

# RUN npm ci

# COPY . .
# RUN npm run build

# EXPOSE 3000

# CMD ["npm", "run", "start"]

# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies (dev + prod)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source and build the app
COPY . .
RUN npm run build

# Stage 2: Final (lighter) image
FROM node:20-alpine AS final

WORKDIR /app

# Only copy production dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Copy built output from builder
COPY --from=builder /app/.next ./.next        
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./      



EXPOSE 3000

CMD ["npm", "start"]
