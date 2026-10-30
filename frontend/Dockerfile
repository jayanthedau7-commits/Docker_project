# Use lightweight official Node image
FROM node:20-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all frontend files
COPY . .

# Expose port 3000
EXPOSE 3000

# Start Express server
CMD ["node", "server.js"]