# Laundry Management System API

This is a robust API for a Laundry Management System. It's built with Python, Flask, Flask-RESTx, and SQLAlchemy.

## Features

- User authentication
- Admin functionality
- Order management

# Laundry Management System

## Authentication Endpoints

- **DELETE** `/auth/delete_user/{user_id}`: Delete a user.
- **POST** `/auth/login`: Login a user.
- **POST** `/auth/logout`: Logout a user.
- **POST** `/auth/register`: Register a new user.
- **PATCH** `/auth/update_user_details`: Update user details.
- **GET** `/auth/users`: Get all users.

## Admin Endpoints
- **POST** `/admin/login`: Login an admin.
- **POST** `/admin/register`: Register a new admin.
- **PATCH** `/admin/update_admin_details/{admin_id}`: Update admin details.

## Order Endpoints

- **POST** `/order/create_order`: Create a new order.
- **PATCH** `/order/order/status/{order_id}`: Update order status.
- **DELETE** `/order/order/{order_id}`: Delete an order.
- **GET** `/order/user/{user_id}/orders`: Get all orders.
- **GET** `/order/user/{user_id}/orders/{order_id}`: Get a specific order.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- pip

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/FrankOnyemaOrji/laundry-mgt-system.git
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
    python -m unittest test
    ```
## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Project Software Requirement Specification
- [Software Requirement Specification](https://docs.google.com/document/d/16-_K1VLh6a5CflWScxuNFYzUSx9IDAVaHf_0zFmXDUE/edit?usp=sharing)

## Contact

If you want to contact me you can reach me at `f.orji@alustudent.com`.
