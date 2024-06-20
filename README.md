# Laundry Management System API

This is a robust API for a Laundry Management System. It's built with Python, Flask, Flask-RESTx, and SQLAlchemy.

## Features

- User authentication
- Admin functionality
- Order management

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- pip

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/laundry-mgt-system.git
    ```
2. Change into the project directory:
    ```
    cd laundry-mgt-system
    ```
3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
4. Set up your environment variables in your .env file:
    ```
    export FLASK_APP=app
    export FLASK_ENV=development
    export SECRET_KEY=your_secret_key
   ```
5. Run the application:
    ```
    flask run
    ```

## Usage

The API has the following endpoints:

- `/auth/login`: Authenticate a user and return a JWT token.
- `/admin`: Perform administrative tasks.
- `/order`: Manage orders.

## Running the Tests

To run the tests, use the following command:
 - ```
    pytest
    ```
## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Contact

If you want to contact me you can reach me at `f.orji@alustudent.com`.