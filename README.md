# MacroForge v1

## Run locally
1. Copy `.env.example` to `.env`
2. Set `ADMIN_PASSWORD`
3. Run:
   docker compose up --build

Frontend: http://localhost:3000
Backend: http://localhost:8000

## Notes
- Login with the admin user from `.env`
- Import USDA foods by configuring `USDA_API_KEY`
- Persistent data lives in Postgres volume
- Designed for TrueNAS SCALE deployment with custom app volumes
