#!/bin/bash

# Install Dependencies
cd backend
npm install

cd ../frontend
npm install

# Setup environment variables
cd ..
cp .env.dev backend/.env
cp .env.dev frontend/.env

# Start Database
docker run --name postgres_local \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=madeinportugal \
  -p 5432:5432 \
  -d postgres:18

sleep 1 # Waiting for container to run

docker exec -i postgres_local psql -U postgres -d madeinportugal < db/mip-s_schema.sql

docker exec -i postgres_local psql -U postgres -d madeinportugal < db/populate.sql

# Start Backend
cd backend
npm run dev &

# Start Frontend
sleep 1
cd ../frontend
npm run dev
