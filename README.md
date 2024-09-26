
```markdown
# Django Book Management Project

This project is a Django application for managing books and authors, including functionalities for user authentication and managing favorite books.

## Getting Started

Follow the instructions below to set up your environment, install dependencies, and run the project.

### Prerequisites

- Python 3.x installed on your machine
- Git installed on your machine

### Setting Up the Virtual Environment

#### For Windows

1. Open Command Prompt.
2. Navigate to your project directory:
   ```bash
   cd path\to\your\project
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

#### For macOS/Linux

1. Open Terminal.
2. Navigate to your project directory:
   ```bash
   cd path/to/your/project
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

### Installing Dependencies

With your virtual environment activated, install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Running Test Data

To populate the database with test data, use the included management command. First, ensure your migrations are applied, then run:

```bash
python manage.py insert_test_data
```

### Starting the Server

1. Make migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Start the development server:
   ```bash
   python manage.py runserver
   ```

Your server should now be running at `http://127.0.0.1:8000/`.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request.


