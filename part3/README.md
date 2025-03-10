# HBNB PROJECT

This project consists of developping a complete yet simplified web application based on AirBnb.  
 Language: Python  
 Framework: Flask

## Project Directory Structure

```
hbnb/
├── app/
│ ├── __init__.py
│ ├── api/
│ │ ├── __init__.py
│ │ ├── v1/
│ │ ├── __init__.py
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── reviews.py
│ │ ├── amenities.py
│ ├── models/
│ │ ├── __init__.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ ├── amenity.py
│ ├── services/
│ │ ├── __init__.py
│ │ ├── facade.py
│ ├── persistence/
│ ├── __init__.py
│ ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

### Explanation

The **app/** directory contains the core application code.  
The **api/** subdirectory houses the API endpoints, organized by version (v1/).  
The **models/** subdirectory contains the business logic classes (e.g., user.py, place.py).  
The **services/** subdirectory is where the Facade pattern is implemented, managing the interaction between layers.  
The **persistence/** subdirectory is where the in-memory repository is implemented. This will later be replaced by a database-backed solution using SQL Alchemy.  
**run.py** is the entry point for running the Flask application.
**config.py** will be used for configuring environment variables and application settings.  
**requirements.txt** will list all the Python packages needed for the project.

## API Layers

- Presentation Layer:
  - Handles incoming requests and outgoing responses via the API
- Business Logic Layer:
  - This contains the models and the core logic of the application
- Persistence Layer:
  - Responsible for storing and retrieving data for the application from the database

## Key Entities

### Places:

Places are the core entities of our application, representing accomodations available for rent. Each place includes attributes such as:

- Title, Description
- Adress, Latitude, Longitude
- Host (Owner)
- Price
- Amenities
- Reviews

### Users:

Users represents individuals interacting with the application. Key attributes are:

- First name, Last name
- Password
- Email (Unique ID)

### Reviews:

User-generated feedback and ratings for places. Each reviews include attributes such as:

- Rating (1-5 Stars)
- Comment
- Date of submission

### Amenities

Features available in places, such as Wi-Fi, pool, jacuzzi etc. Users can select and filter results as needed

## Test Requirements

- Dependencies
  - All required packages are listed in _requirements.txt_. Install dependencies using
  ```
  pip install -m requirements.txt
  ```
- Run the application using
  ```
  python run.py
  ```