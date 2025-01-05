# E-Commerce Shop Project

This project is a comprehensive **e-commerce platform** designed with modularity and scalability in mind. To maintain code organization and ensure future scalability, different sections of the project are divided into separate applications (apps). Key features include user account management, shopping cart functionality, order processing, and product management. The project also demonstrates integration with APIs, showcasing advanced knowledge of backend development.

## Features

### Account Management
- **User Roles**: Two types of users - admin and customer.
- **Admin Panel**:
  - Sort users by phone number, name, active status, and admin privileges.
  - Display detailed user information such as last login, join date, and permissions.
- **Default Passwords**: For newly registered users, the system automatically generates a default password, which users can manually change later.

### Shopping Cart (Cart)
- **Add and Remove Items**: Users can add or remove items from the cart.
- **Shipping Costs**: Shipping fees are calculated based on the total weight and value of the items in the cart.
- **Inventory Check**: If a user attempts to add more items than are available in stock, an error will be displayed.
- **Clear Cart**: Users have the option to clear their cart entirely.

### Order Management (Order)
- Inherits information from the user's account and includes details about the buyer and the items in their cart.
  
### Product Management (Shop)
- **Product Information**:
  - Each product has a category, price, stock availability, weight, and discount (if applicable).
- **Discount Codes**: Implemented using `Django signals` to handle discount code applications.
- **Product Interaction**:
  - Users can like products and leave comments.
  - Suggestions for related products are offered based on the buyer’s cart contents.
  
### Additional Features
- **Support Tickets**: Users can submit tickets to support.
- **Profile Editing**: Users can update their profile information.
- **Account Deletion**: Users can delete their accounts.
- **Purchase History**: Users can view and edit their purchase information.
- **Product Recommendations**: Similar products are suggested based on the user’s shopping behavior.

### API Integration
- This project includes an API layer, demonstrating proficiency in backend API development for data interaction and external integration.

## Technologies Used

- **Backend**: [Django] - A Python web framework.
- **Frontend**: HTML, CSS, JavaScript.
- **Database**: SQLite (can be upgraded to PostgreSQL or MySQL as needed).
- **Authentication**: Custom authentication for user and admin roles.
- **Signals**: `Django signals` used for tasks such as applying discount codes and sending notifications.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ashkanhajian/your-repo.git
   cd your-repo
