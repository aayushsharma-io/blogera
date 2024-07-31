# Blogera

Blogera is a minimalistic blogging platform built with Flask, allowing users to write and host their own blogs for free. The platform offers HTML and CSS customization to match your style and preferences. 

## Features

- Admin can write and manage blogs via the `/admin` route.
- Blog data is stored in JSON files for simplicity.
- Supports thumbnail images for blog posts.
- Allows custom HTML tags within blog content.
- Blog comments functionality.
- Dark mode and glassmorphism design (initially using basic HTML, with plans to integrate Tailwind CSS).

## Requirements

- Python 3.10+
- Flask
- Flask-Login

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aayushsharma-io/blogera.git
    cd blogera
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create necessary directories:
    ```bash
    mkdir -p app/static/uploads
    mkdir -p app/blogs
    ```

5. Run the application:
    ```bash
    python run.py
    ```

## Usage

### Admin Registration and Login

1. Access the admin registration page at `/admin/register`.
2. Register an admin account.
3. Login to the admin panel at `/admin/login`.

### Writing a Blog Post

1. After logging in, navigate to `/admin/write` to create a new blog post.
2. Fill in the title, description, and content fields. Use the provided buttons to insert images by URL or upload images.
3. Upload a thumbnail image for the blog post.
4. Choose whether to allow comments.
5. Submit the form to create the blog post.

### Viewing Blogs

1. Access the homepage at `/` to see the list of blog posts.
2. Click on a blog post title or thumbnail to view the full content of the blog.
3. If comments are enabled, users can add comments to the blog post.

## Directory Structure
```
blogera/
│
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── admin.html
│ │ ├── write_blog.html
│ │ ├── blog_detail.html
│ ├── static/
│ │ └── uploads/
│ ├── blogs/
│ ├── models.py
│ └── forms.py
│
├── venv/
│
├── run.py
│
├── requirements.txt
│
└── README.md
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## Acknowledgements

- Flask: [Flask](https://flask.palletsprojects.com/)
- Flask-Login: [Flask-Login](https://flask-login.readthedocs.io/)

---

Feel free to reach out with any questions or feedback. Happy blogging with Blogera!
Project is in it's early stages of development. 
-Aayush Sharma

