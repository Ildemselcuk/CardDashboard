# CardDashboard

CardDashboard is a simple backend application for card management, developed using Flask and Python. It allows users to manage their financial transactions, add and remove cards, list them, update card information, and securely log in or register.

## Installation and Setup

### Prerequisites

Make sure you have the following programs installed on your computer:

- Python 3.11
- pip package manager
- Docker (with docker-compose)

### Getting Started

Clone the project repository to your local machine:

```bash
git clone https://github.com/Ildemselcuk/CardDashboard.git
cd CardDashboard
```

Start the Docker containers for the database, database viewer, and Flask application:

```bash
docker-compose up -d
```

Alternatively, if you prefer to run the backend locally:

```bash
docker-compose up db adminer -d
python3 -m venv ./venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
cd app
flask db init
flask db migrate
flask db upgrade
cd ..
python3 main.py
```

## Usage

Access the Flask application by navigating to `http://localhost:5001` if you have run the backend locally or `http://localhost:8001` if you used docker compose, in your web browser. Perform financial transactions, add or remove cards, and manage your financial data securely.

## Contributing

Feel free to contribute to the development of CardDashboard. Create a fork of the repository, make your changes, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).


