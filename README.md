# car-rental-api

Backend project linked to "IA for developpers" training from Technofutur tic

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content:

   ```env
   DATABASE_URL=sqlite:///./dev.db
   ```

5. Run the development server:

   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API at `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`
