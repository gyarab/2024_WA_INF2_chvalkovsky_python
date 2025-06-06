# 2024_WA_INF2_chvalkovsky_python
# Info
Django cms repozitář
Currently running at [guitars.svs.gyarab.cz](https://guitars.svs.gyarab.cz/)
# Autor
brunochvalk
# Obsah
Projekt obsahuje databázi elektrických kytar

# How to run:
1. Clone the repository:
    ```sh
    git clone https://github.com/brunochvalk/2024_WA_INF2_chvalkovsky_python.git
    ```
2. Navigate to the project directory:
    ```sh
    cd 2024_WA_INF2_chvalkovsky_python
    ```
3. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```
4. Activate the virtual environment:

    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source .venv/bin/activate
        ```
5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Apply the database migrations:
    ```sh
    python manage.py migrate
    ```
7. Load data from fixture
    ```sh
    python manage.py loaddata brands.json
    python manage.py loaddata genres.json
    python manage.py loaddata guitars.json
    ```
8. Run the development server:
    ```sh
    python manage.py runserver
    ```
# Features
- Filter on the homepage by pickup configuration and shape.
- Click on a guitar to see the details page.
- Clicking on the logo in the header returns to the homepage.
- On the details page, clicking on the guitar images enlarges the image.
- On the details page, clicking on the guitar name in the header redirects to brand info and all the brand's guitars.
- On the details page, clicking on the genre redirects to the genre page with all the guitars of the selected genre.
