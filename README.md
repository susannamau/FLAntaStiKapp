# My FLAntaStiKapp 🐍

This is a simple banking web application built with Flask. The application allows users to register, log in, and perform basic account management tasks such as depositing and withdrawing money.

## Features implemented so far

- User registration and login
- Admin login
- Unique account number generation for new accounts
- Account balance management
- Data storing
- Chance for the user to:
  - Deposit and withdraw money
  - Upload textual files
  - Query of a LLM (currently LLaMa3 (8B), HuggingFace) that considers the content of the textual files previously uploaded
  - Download and delete uploaded files
- Chance for the admin to:
  - See the number of registered users
  - See the distribution of the balances of the users

## Requirements

To run this application, you will need Python and Flask. The application uses JSON to store user data persistently. Also, an HuggingFace key is needed to query the LLM.

## Installation

Clone the repository to your local machine and navigate to the app directory. When running `run.py`, by default the application will we available at `http://127.0.0.1:5000/`.

## Structure of My FLAntaStiKapp

```mermaid
graph TD
    A[Access and choose authentication role] --> B[User]
    A --> B2[Administrator]

    B --> C{Do you already have an account?}
    C -- Yes --> D[Login]
    C -- No --> E[Register]
    D --> F[User dashboard]
    E --> D

    F --> G[Manage files]
    G --> H[Upload file]
    G --> I[Download file]
    G --> J[Delete file]
    G --> K[Query files via LLM]

    B2 --> L[Login]
    L --> M[Admin dashboard with graphs and queries]
    M --> N[Query all users' files via LLM]
    M --> O[Query individual user files via LLM]
