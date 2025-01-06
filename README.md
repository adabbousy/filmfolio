# FilmFolio

### Video Demo: https://youtu.be/QBqwWArz-RA

## Description:
**FilmFolio** is a Flask-based web application tailored for movie enthusiasts, allowing them to manage their movie collections, including watchlists and watched movies. Built using Python, Flask, HTML, CSS, JavaScript, sqlite3, and Bootstrap, it offers features like searching for films, viewing detailed information, and receiving personalized movie recommendations. The application utilizes a user-friendly interface and a responsive design powered by Bootstrap, ensuring seamless usability across all devices. FilmFolio integrates with The Movie Database (TMDb) API to provide up-to-date information on movies, including titles, overviews, ratings, release dates, and posters.

### How to Run FilmFolio Locally (Step-by-Step Guide):

#### 1. Install Required Software:
   - **Install Python:**
     - Download and install Python from [python.org](https://www.python.org/downloads/). Ensure you check the box to add Python to your PATH during installation.
   - **Install Git (Optional):**
     - Download and install Git from [git-scm.com](https://git-scm.com/). This step is optional if you prefer downloading the ZIP file instead of cloning the repository.
   - **Install an IDE/Text Editor:**
     - Install an IDE such as [Visual Studio Code](https://code.visualstudio.com/) or use any text editor of your choice.

#### 2. Get the Code:
   - Option 1: **Clone the Repository (requires Git):**
     ```bash
     git clone https://github.com/adabbousy/filmfolio
     cd FilmFolio
     ```
   - Option 2: **Download as ZIP:**
     - Go to the repository page, click on the "Code" button, and select "Download ZIP."
     - Extract the ZIP file to a folder on your computer.

#### 3. Set Up the Environment:
   - Open a terminal or command prompt in the project folder.
   - Create a virtual environment to isolate dependencies:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - For Windows:
       ```bash
       venv\Scripts\activate
       ```
     - For macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

#### 4. Install Dependencies:
   - Use the following command to install the necessary libraries:
     ```bash
     pip install -r requirements.txt
     ```

#### 5. Configure the API Key:
   - The TMDb API key is **already hardcoded** in the code. You **do not** need to create a `.env` file or add the API key manually.
   - Simply proceed with running the application as outlined below.


#### 6. Run the Application:
   - Start the Flask development server:
     ```bash
     flask run
     ```
   - If `flask run` doesn't work, use:
     ```bash
     python app.py
     ```

#### 7. Access the Application:
   - Open your web browser and go to: `http://127.0.0.1:5000`.

## Key Features
- **User Authentication**: Secure registration and login functionality to provide a unique and personalized user experience while protecting user data.
- **Movie Search and Recommendations**: Offers movie search and provides movie recommendations based on popularity and with the help of TMDb API.
- **Watchlist and Watched Movies**: Users can add movies to their watchlist or mark them as watched, with both lists being easily accessible.
- **Responsive Design**: Designed to work seamlessly across all devices, from desktops to mobile phones.

## Project Structure
### **`app.py`**
This file serves as the backbone of the program. Built using the Flask framework, this file is responsible for handling all routes, user authentication, managing user sessions, handling potential errors, and managing the watchlist and watched movies. The routes interact with the database to store, retrieve, and update user-specific data as needed. Key functions and routes:
- **`@login_required`**: A decorator used to protect certain routes, ensuring that only authenticated users can access specific features.
- **`apology()`**: Returns an apology message with a meme in case of an error or issue.
- **`/` (Homepage)**: Dynamically loads recommended movies from the TMDb API and displays them on the home page with a personalized greeting based on the logged-in user.
- **`/register`**: Handles user registration and catches all potential errors, allowing new users to create an account by providing their details, which are then stored in the database.
- **`/login`**: Manages user login. If the provided credentials are valid, users are directed to the home page.
- **`/logout`**: Logs the user out of the application by clearing their session.
- **`/search`**: Processes search queries submitted by the user, returns a list of movies matching the search term, and renders the results on the search results page.
- **`/watchlist`**: Retrieves and displays movies the user has added to their watchlist but hasn't watched yet.
- **`/watched`**: Moves movies from the watchlist to the "Watched" list and displays them on the "My Watched" page, helping users track their viewing history.
- **`/add-to-watchlist`**: Adds selected movies to the user's watchlist and stores the movies' data in the database.
- **`/add-to-watched`**: Marks selected movies as watched, updates the user's list of watched movies, and updates movies' statuses in the database.
- **`/password`**: Allows users to change their password. Once the current password is validated, the database is updated with the new password.

### **`movies.db`**
A SQLite database that stores user data, including login credentials, watchlists, and watched movies. This ensures that each user’s movie preferences are saved and accessible upon subsequent logins. The database is divided into 4 related tables:
- **`users`**: Contains user credentials such as the user's unique ID, username, first name, last name, and hashed password.
- **`movies`**: Contains detailed information about the movies in the database, including their unique IDs, titles, overviews, poster paths, release dates, and average ratings. This table serves as the primary source of movie data used throughout the application, providing the necessary details for both the watchlist and watched tables.
- **`watchlist`**: Keeps track of the movies users have marked to watch later. This table stores user IDs along with the movie IDs added to each user's watchlist.
- **`watched`**: Records the movies users have already watched. Similar to `watchlist`, this table stores user IDs along with the movie IDs that have been marked as watched by each user.

### **`static/`**
A folder that contains all the static assets used by the application. It ensures a consistent and visually appealing user interface across all pages of the website. The folder consists of 2 files:
- **`logo.png`**: The website logo, representing the theme of movies, serves as both a favicon and a header element on each page, reinforcing the site's focus.
- **`styles.css`**: Customizes the visual appearance of the website. It implements a dark, starry background for the entire site, contributing to the cinematic theme. The file ensures consistency in design through the use of custom background effects, gradients, specific modern fonts, rounded corners, and form layout making the interface visually appealing and cohesive across the site.

### **`templates/`**
A folder that contains all the HTML layouts that structure the pages of the FilmFolio website. Each file serves a specific purpose in the application's user interface, with links referencing stylesheets such as Bootstrap and JavaScript integrated within certain files to enable dynamic functionality. The folder consists of 11 files:
- **`layout.html`**: This is the base template for the site. It includes common elements like the navbar, header, and links to CSS and Bootstrap files. Other templates extend this file to maintain a consistent design across pages.
- **`search_temp.html`**: A partial template included within other pages, it provides the search bar interface that allows users to look for specific movies.
- **`modal.html`**: A reusable template that defines the structure of a modal window, which is used across the site to display detailed movie information dynamically when a user clicks on a movie card.
- **`index.html`**: Serves as the homepage, displaying a greeting and a selection of popular movies. It inherits from `layout.html` and uses JavaScript to fetch and display movie data dynamically.
- **`search.html`**: Displays search results for movies. It extends `layout.html` and processes user queries to show relevant movie titles and details.
- **`watchlist.html`**: This template, which also extends `layout.html` showcases the user's personalized watchlist. The template dynamically loads the movies added by the user, displaying them in a structured layout, while offering features for managing the watchlist.
- **`watched.html`**: Extending `layout.html`, this template displays the list of movies users marked as watched. It retrieves data from the database specific to the user's watched movies and presents it in a clean, organized format.
- **`register.html`**: The user registration template which extends `layout.html` for a consistent look. It includes input fields for first name, last name, username, password, and password confirmation, along with instructions on password requirements.
- **`login.html`**: The login page template where users can enter their usernames and passwords to access their accounts. Like other templates, it extends `layout.html`.
- **`password.html`**: Extending `layout.html`, this interface allows users to change their password. It includes input fields for the current password, new password, and password confirmation, along with instructions on password requirements.
- **`apology.html`**: Displays error messages in a user-friendly format when something goes wrong or the user doesn't comply with the requirements. It also extends `layout.html` to maintain the website design.

## Final Notes
FilmFolio is designed to offer a seamless experience for movie enthusiasts looking to organize their movie collections and explore new films. This project demonstrates how Flask, Bootstrap, and the TMDb API can be integrated to create a dynamic, responsive web application. As the project evolves, there may be opportunities to add new features, such as enhanced recommendation algorithms or integration with additional APIs.

If you encounter any issues or have suggestions for improvements, please feel free to reach out at [abdullah.dabbousy6@gmail.com](mailto:abdullah.dabbousy6@gmail.com). Contributions are welcome, and I encourage you to explore the codebase, customize it to your needs, or even extend its functionality.

Thank you for checking out FilmFolio, and happy movie watching!
