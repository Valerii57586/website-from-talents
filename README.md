Here is a suggested **README.md** file for the provided Flask application:

---

# Flask Blog Application

This is a Flask-based web application that serves as a blogging platform. Users can register, log in, create posts, comment on posts, reply to comments, and manage their profiles. The application uses SQLite as the database and includes features like session management, markdown rendering, and user authentication.

---

## Features

- **User Authentication**:
  - Register new accounts with username, email, and password.
  - Log in and log out securely using Flask sessions.
  - Password validation during registration.

- **User Profiles**:
  - View user profiles with details like name, surname, avatar, header photo, and bio.
  - Display a list of posts authored by the user.

- **Blog Posts**:
  - Create, edit, and delete blog posts.
  - Posts support markdown formatting for content, including fenced code blocks.
  - Add tags and code themes to posts.

- **Comments and Replies**:
  - Add comments to posts.
  - Reply to comments on posts.

- **Post Viewing**:
  - Track the number of unique viewers for each post.
  - Render markdown content for posts.

- **Search**:
  - Search functionality for posts (basic implementation).

- **Session Management**:
  - Track active users using Flask sessions and a set of active IPs.

---

## Technologies Used

- **Backend**:
  - Flask: Web framework.
  - Werkzeug: Middleware for proxy handling.
  - Redis: Session management (optional, for scalability).
  - SQLite: Database for storing user, post, comment, and reply data.

- **Frontend**:
  - Jinja2: Templating engine for rendering HTML pages.

- **Other Libraries**:
  - `markdown2`: For rendering markdown content.
  - `sqltools`: Custom library for database operations.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Database Structure

The application uses an SQLite database (`data.db`) with the following tables:

1. **Users**:
   - `id`: Primary key.
   - `username`: User's username.
   - `password`: User's password.
   - `email`: User's email.
   - `name`: User's first name.
   - `surname`: User's last name.
   - `avatar`: URL or path to the user's avatar.
   - `header_photo`: URL or path to the user's header photo.
   - `status`: User's status message.
   - `about`: User's bio.
   - `git_link`: GitHub profile link.
   - `other_links`: Other social or personal links.

2. **Posts**:
   - `id`: Primary key.
   - `email`: Author's email.
   - `title`: Post title.
   - `content`: Post content (supports markdown).
   - `date`: Date of creation or last update.
   - `files`: Associated files (optional).
   - `images`: Associated images (optional).
   - `author_username`: Author's username.
   - `code_theme`: Code theme for syntax highlighting.
   - `tags`: Tags associated with the post.
   - `veiwers`: List of usernames who have viewed the post.

3. **Comments**:
   - `id`: Primary key.
   - `username`: Commenter's username.
   - `post_id`: ID of the post the comment belongs to.
   - `content`: Comment content.
   - `date`: Date of the comment.

4. **Replies**:
   - `id`: Primary key.
   - `username`: Replier's username.
   - `comment_id`: ID of the comment the reply belongs to.
   - `content`: Reply content.

---

## Routes

### Public Routes
- `/`: Main page displaying all posts.
- `/login`: Log in to an existing account.
- `/reg`: Register a new account.

### User Routes
- `/profile/<username>`: View a user's profile.
- `/logout`: Log out of the current session.

### Post Routes
- `/create_post`: Create a new post.
- `/post/<int:id>`: View a specific post.
- `/edit/<int:id>`: Edit an existing post (if the user is the author).
- `/delete/<int:id>`: Delete a post (if the user is the author).

### Comment and Reply Routes
- `/add_reply/<int:comment_id>/<int:post_id>`: Add a reply to a comment.

---

## Known Issues

1. **Typographical Errors**:
   - The `veiwers` column in the `posts` table is misspelled (should be `viewers`).
   - Some variable names like `reply_cntent` have typos.

2. **Error Handling**:
   - Limited error handling for database operations.
   - Exceptions are caught but not logged or displayed to the user.

3. **Security**:
   - Passwords are stored in plaintext. Use hashing (e.g., `bcrypt`) for secure password storage.
   - No CSRF protection for forms.

4. **Scalability**:
   - The application uses an in-memory set (`active_users`) for tracking active users, which may not scale well.

---

## Future Improvements

- Implement password hashing for secure authentication.
- Add CSRF protection for forms.
- Improve error handling and logging.
- Fix typos in variable names and database schema.
- Enhance the search functionality.
- Add pagination for posts and comments.
- Use a more scalable session management system (e.g., Redis).

---
