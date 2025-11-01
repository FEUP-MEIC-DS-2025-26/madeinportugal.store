# MadeInPortugal Store

A Node.js + PostgreSQL + Docker project for a marketplace of traditional Portuguese products.

This guide explains how to set up the project **locally** for development.

---

## **Prerequisites**

Make sure you have the following installed on your machine:

* [Node.js](https://nodejs.org/) (v22+ recommended)
* [npm](https://www.npmjs.com/)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

---

## **Folder Structure**

```
madeinportugal-store/
├── app/
│   ├── index.js
│   ├── db.js
│   ├── routes/
│   │   └── products.js
│   ├── controllers/
│   │   └── productController.js
│   ├── db/
│   │   ├── mip-s_schema.sql
│   │   └── populate.sql
│   ├── public/
│   │   ├── index.html
│   ├── .env
│   ├── package.json
│   ├── package.lock.json
│   ├── Dockerfile
│   └── start.sh
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   └── api.js
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── package.lock.json
│   ├── Dockerfile
│   └── start.sh
├── nginx/
│   └── default.conf
├── docker-compose.yml
└── start.sh
```

Backend:
  * `app/` → Node.js backend
  * `app/routes/` → Express API routes
  * `app/.env` → environment variables
  * `app/package.json` → Node.js dependencies and scripts

Frontend:
  * `frontend/` → React backend
  * `frontend/public/` → Production frontend files
  * `frontend/src/` → Frontend source code
  * `frontend/package.json` → React and Vite dependencies and scripts
  * `frontend/index.html` → Frontend development phase HTML file
  * `frontend/vite.config.js` → Vite configuration file
  * `frontend/Dockerfile` → Frontend docker image dockerfile
  * `frontend/start.sh` → Frontend docker image shell file

Root:
  * `docker-compose.yml` → Docker services configuration
  * `nginx/` → Nginx configuration
  * `start.sh` → Shell file that builds the production environment and Docker containers

---

## **1. Clone the Repository**

```bash
git clone git@github.com:FEUP-MEIC-DS-2025-26/madeinportugal.store.git
cd madeinportugal-store
```

---

## **2. Install Node.js and React Dependencies**

From root, go to backend folder and install:

```bash
cd app
npm install
```

From root, go to frontend folder and install:

```bash
cd frontend
npm install
```

---

## **3. Start PostgreSQL via Docker**

```bash
docker run --name postgres_local \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=madeinportugal \
  -p 5432:5432 \
  -d postgres:18
```

* This starts a local PostgreSQL container on port `5432`.


---

## **4. Create and Populate the Database (development phase)**

1. **Go to backend folder:**

```bash
cd app
```

2. **Run the schema SQL file:**

```bash
docker exec -i postgres_local psql -U postgres -d madeinportugal < app/db/mip-s_schema.sql
```

3. **Run the populate SQL file:**

```bash
docker exec -i postgres_local psql -U postgres -d madeinportugal < app/db/populate.sql
```

4. **(If needed) Verify tables and data:**

```bash
docker exec -it postgres_local psql -U postgres -d madeinportugal
```

---

## **5. Start the Backend Locally**

**<ins>IMPORTANT<ins>**: Must set `DB_HOST` in `.env` file to `localhost`.

From root folder:

```bash
cd app
npm run dev
```

* Starts the backend with `nodemon` on `http://localhost:3000`.
* Auto-restarts on code changes.

---

## **6. Start the Frontend Locally**

From root folder:

```bash
cd frontend
npm run dev
```

* Starts the frontend on `http://localhost:5173`.
* Auto-restarts on code changes.

---

## **7. Access the App (Dev phase)**

* Frontend: `http://localhost:5173`.

---

## **8. Test in Production phase**

**<ins>IMPORTANT<ins>**: Must set `DB_HOST` in `.env` file to `db`.

From root folder, simply run:

```bash
./start.sh
```

This will build and run the containers (frontend, backend and db).

* Check production frontend at `http://localhost:5173`.
* Verify that production backend is running at `http://localhost:3000`.
* Does **not** auto-restart on code changes. Must build again to see changes.

---

## **9. Next Steps**

* Implement frontend pages in `frontend/src`.
* Add new API routes in `app/routes`.
* Use Docker Compose to run locally with the same environment as the server.

---

**Good luck coding!**
