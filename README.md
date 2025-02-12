

# **Travel Book System**

## **Overview**

The **Travel Book System** is a Django-based application that allows users to book travel packages. Users can browse available packages, make bookings, and track their booking status.

## **Features**

- **Travel Packages**: Browse available destinations with pricing and travel dates.
- **Booking System**: Users can book a travel package and receive a status update.
- **Booking Status**: Track bookings with statuses: *Pending, Confirmed, Cancelled, Completed*.
- **Validation**: Ensures travel dates are not in the past.
- **Hotel Details**: Stores additional hotel information as JSON.

## **Models**

- **TravelPackage**: Represents a travel package with a destination, price, slots, and date.
- **Booking**: Represents user bookings linked to a travel package with status tracking.

## **Installation & Setup**

1. **Clone the Repository**
    
    ```
    git clone <https://github.com/your-repo/travel-book-system.git>
    cd travel-book-system
    
    ```
    
2. **Install Dependencies**
    
    ```
    pip install -r requirements.txt
    
    ```
    
3. **Run Migrations**
    
    ```
    python manage.py migrate
    
    ```
    
4. **Create a Superuser** (For Admin Access)
    
    ```
    python manage.py createsuperuser
    
    ```
    
5. **Start the Development Server**
    
    ```
    python manage.py runserver
    
    ```
    

## **Usage**

- Admins can add **travel packages** via the Django admin panel.
- Users can **book packages** and track their booking status.
- The system ensures data validation and prevents duplicate bookings.

