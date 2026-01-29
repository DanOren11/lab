FROM node:20-alpine

WORKDIR /app

# Copy only dependency files first (better cache)
COPY package.json package-lock.json ./

# Install prod dependencies
RUN npm ci --omit=dev

# Copy app source
COPY . .

USER node
ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "start"]
