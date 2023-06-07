# ecom
A django  based management system to handle the purchase and sale of commodities 

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation on Localhost

1. Clone the repo
   ```sh
   git clone https://github.com/string-eureka/ecom
   ```
2. Install Relevent Packages
   ```sh
   pip install -r Requirements.txt 
   ```
3. Connect to the database 
   ```sh
   Link it with your Postgresql database
   Create an .env file to store all secrets
   ```
4. Migrations 
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create Superuser
   ```sh
   python manage.py createsuperuser
   ```
6. You'll all set to use EurekaMart!
