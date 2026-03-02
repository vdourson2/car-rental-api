# car-rental-api

Backend project linked to "IA for developpers" training from Technofutur tic

## GPT chat used to generate the requirements.md and user_stories.md files

<https://chatgpt.com/share/69a5af2d-3dd8-800b-8a0a-3834d6343c52>

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
