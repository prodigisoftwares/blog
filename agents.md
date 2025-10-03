# Blog Project Overview

## Project Description

This is a Django-based blog application built with modern web technologies. It provides a foundation for creating and managing blog content with a clean, responsive interface.

## Technology Stack

- **Backend**: Django 5.2.7+ (Python web framework)
- **Database**: PostgreSQL 16
- **Frontend**: Tailwind CSS for styling, HTMX for AJAX interactions, Alpine.js for lightweight JavaScript components
- **Admin Interface**: Django Unfold (enhanced admin UI)
- **Deployment**: Docker with Gunicorn for production
- **Development Tools**: Poetry for dependency management, Black for code formatting, Flake8 for linting

## Project Structure

```
/home/harlin/Sandbox/prodigi/blog/
├── pyproject.toml          # Poetry configuration and dependencies
├── poetry.lock             # Locked dependency versions
├── docker-compose.yml      # Development environment setup
├── docker-compose.prod.yml # Production environment setup
├── runtime.txt            # Python runtime version for deployment
├── dev-up.sh              # Development startup script
├── prod-up.sh             # Production startup script
├── blog/                   # Main Django application
│   ├── manage.py          # Django management script
│   ├── requirements.txt   # Python dependencies (generated)
│   ├── Dockerfile         # Development container
│   ├── Dockerfile.prod    # Production container
│   ├── entrypoint.sh      # Development entrypoint
│   ├── entrypoint.prod.sh # Production entrypoint
│   ├── createadmin.sh     # Admin user creation script
│   ├── setadminpw.py      # Admin password setup script
│   ├── test.sh            # Test runner script
│   ├── apps/              # Django apps directory (currently empty)
│   ├── config/            # Django project configuration
│   │   ├── settings.py    # Main settings file
│   │   ├── urls.py        # URL configuration
│   │   ├── wsgi.py        # WSGI application
│   │   └── asgi.py        # ASGI application
│   ├── static/            # Static files directory
│   ├── staticfiles/       # Collected static files
│   └── mediafiles/        # User-uploaded media files
├── nginx/                  # Nginx configuration for production
│   ├── Dockerfile
│   └── nginx.conf
└── tailwind/               # Tailwind CSS setup
    ├── package.json
    ├── tailwind.config.js
    └── custom.css
```

## Key Features

- PostgreSQL database integration
- Environment-based configuration management
- Docker containerization for development and production
- Tailwind CSS for responsive design
- HTMX for seamless AJAX interactions without complex JavaScript
- Alpine.js for lightweight, reactive JavaScript components
- Enhanced Django admin interface with Unfold
- Static and media file handling
- Gunicorn for production WSGI server

## Frontend Technologies

- **Tailwind CSS**: Utility-first CSS framework for rapid UI development and responsive design
- **HTMX**: Enables AJAX, WebSockets, and Server-Sent Events directly in HTML using attributes, allowing for dynamic content updates without writing JavaScript
- **Alpine.js**: Minimal JavaScript framework for adding interactivity to HTML elements, perfect for small reactive components and state management

## Static Asset Management

All third-party libraries (Tailwind CSS, HTMX, Alpine.js, and any other dependencies) are served as local static assets rather than using CDN links. This ensures:

- Better performance and reliability
- Offline capability
- No external dependencies on third-party services
- Consistent versioning and control over updates
- Compliance with content security policies

Static assets are placed in the `static/` directory and collected into the `staticfiles/` directory for production deployment.

## Environment Variables

The application uses environment variables for configuration:

- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `SQL_HOST`: Database host
- `SQL_PORT`: Database port
- `SQL_USER`: Database user
- `SQL_PASSWORD`: Database password
- `SQL_DATABASE`: Database name

## Development Setup

1. Install Poetry: `pip install poetry`
2. Install dependencies: `poetry install`
3. Set up environment variables in `.env.dev`
4. Run development environment: `./dev-up.sh` or `docker-compose up`

## Production Deployment

1. Build production containers: `docker-compose -f docker-compose.prod.yml build`
2. Run production environment: `./prod-up.sh` or `docker-compose -f docker-compose.prod.yml up`

## Development Standards

### Code Style & Organization

- **Python:** Follow Django best practices, PEP 8, 4-space indentation
- **HTML/CSS/JavaScript:** 2-space indentation for consistency
- **App Structure:** Organize Django apps as sub-packages with proper structure:
  - Create `admin/`, `models/`, `tests/`, `views/`, `utils/` as folders with `__init__.py`
  - Use explicit `__all__` exports in `__init__.py` files
  - Keep view modules focused around 70 lines when possible
- **Views:** Prefer class-based views over function-based views:
  - Use Django's generic class-based views (ListView, DetailView, CreateView, etc.)
  - Leverage mixins like LoginRequiredMixin for authentication
  - Override methods like `get_context_data()`, `get_queryset()` for custom behavior
- **Forms:** Use Django ModelForms with proper validation:
  - Implement custom `clean_[field]()` methods for field-specific validation
  - Provide user-friendly error messages via `forms.ValidationError`
  - Style forms using Tailwind classes in templates first, then widget attrs if needed

### Quality Standards

- **Documentation First:** Always read project documentation before coding
- **Minimal Viable Code:** Write just enough code to get the job done, then refactor according to best practices
- **Avoid Over-Engineering:** Don't overthink or over-architect solutions - keep them simple
- **Perfection Expected:** No shortcuts, no "good enough" - everything done right the first time
- **Issue Scope:** Keep issues small and focused - one specific task per issue when possible

### Template Standards

- **Named Endblocks:** Use named endblocks in Django templates (e.g., `{% endblock content %}`)
- **Template Length:** Keep templates under 70 lines when possible - break longer templates into includes
- **Reusable Includes:** Create template includes for common UI patterns in `templates/[app_name]/includes/`
- **Mobile-First:** Design with mobile-first responsive approach using Tailwind CSS

### Testing Philosophy

- **Custom Logic Only:** Only test custom business logic you wrote, not external code
- **No External Testing:** Never test Django's built-in functionality or third-party packages
- **Focus Areas:** Test custom model methods, form validation, view behavior, template filters/tags
- **Avoid Mocks:** Don't use patches and mocks unless absolutely necessary
- **Happy Path Focus:** Tests should generally fulfill happy path scenarios

### Frontend Interactivity

- **Local Assets Only:** All third-party libraries served as local static assets (no CDNs)
- **Alpine.js:** Use for lightweight reactive components and client-side interactions
- **HTMX:** Use for progressive enhancement and partial page updates
- **Progressive Enhancement:** Pages should work without JavaScript, enhanced with HTMX/Alpine.js

### Development Workflow

- **Pre-commit:** Use pre-commit for all linting and formatting
- **File Formatting:** All files must end with a newline character
- **Generated Files:** Exclude compiled files (like `static/css/styles.css`) from formatting
- **Consistent Indentation:** Python=4 spaces, HTML/CSS/JS=2 spaces

## Scripts

- `dev-up.sh`: Start development environment
- `prod-up.sh`: Start production environment
- `createadmin.sh`: Create Django admin user
- `setadminpw.py`: Set admin password
- `test.sh`: Run tests

## Architecture Overview

### Application Structure

```
Django Application (blog/)
├── config/                 # Project configuration
│   ├── settings.py        # Main settings
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
├── apps/                  # Django applications
│   └── [app_name]/       # Individual apps (to be created)
├── static/               # Static files (source)
├── staticfiles/          # Collected static files (production)
└── mediafiles/           # User-uploaded files
```

### Request Flow

1. **Client Request** → Nginx (production) or Django dev server
2. **Django URL Router** → View function/class
3. **View Logic** → Model queries, business logic
4. **Template Rendering** → HTML with Tailwind CSS
5. **HTMX/Alpine.js Enhancement** → Interactive features
6. **Response** → Client with static assets served locally

## Database Design

### Planned Models (Blog Application)

- **Post**: Blog posts with title, content, author, publish date, status
- **Category**: Post categories for organization
- **Tag**: Tagging system for posts
- **Comment**: User comments on posts (if enabled)
- **Author/Profile**: Extended user information for blog authors

### Database Configuration

- **Engine**: PostgreSQL 16
- **Migrations**: Django's built-in migration system
- **Backup**: Regular PostgreSQL backups in production
- **Indexing**: Add database indexes for frequently queried fields

## Security Overview

### Authentication & Authorization

- Django's built-in User model for authentication
- Session-based authentication with CSRF protection
- Admin interface protected with django-unfold
- Password validation and security settings

### Data Protection

- Environment variables for sensitive configuration
- HTTPS everywhere in production
- Secure headers and CSRF tokens
- Input validation and sanitization

### Static Asset Security

- Local hosting prevents CDN-related security risks
- Content Security Policy compliance
- No external script execution risks

## Contributing Guidelines

### Code Contribution Process

1. **Read Documentation**: Always review `agents.md` before starting work
2. **Issue Assignment**: Work on assigned GitHub issues only
3. **Branch Strategy**: Create feature branches from main
4. **Testing**: Write tests for new functionality before marking complete
5. **Code Review**: Ensure code follows established patterns
6. **Documentation**: Update documentation for significant changes

### AI Agent Guidelines

- **Documentation First**: Read all project docs before coding
- **Quality Standards**: No shortcuts - implement correctly first time
- **Simple Solutions**: Avoid over-engineering
- **Testing Required**: Create unit tests for custom logic
- **Local Assets Only**: Never use CDN links for third-party libraries

## Common Commands

### Django Management Commands

```bash
# Development
python manage.py runserver              # Start development server
python manage.py makemigrations         # Create database migrations
python manage.py migrate               # Apply database migrations
python manage.py createsuperuser       # Create admin user
python manage.py collectstatic         # Collect static files

# Testing & Quality
python manage.py test                  # Run all tests
python manage.py test --verbosity=2    # Detailed test output
python manage.py shell                 # Django shell for debugging

# Database
python manage.py dbshell               # Database shell
python manage.py showmigrations        # Show migration status
```

### Project Scripts

```bash
./dev-up.sh           # Start development environment
./prod-up.sh          # Start production environment
./blog/test.sh        # Run tests with coverage
./blog/createadmin.sh # Create Django admin user
```

## Troubleshooting

### Common Issues

**Database Connection Issues:**

- Check environment variables in `.env.dev` or `.env.prod`
- Ensure PostgreSQL container is running: `docker-compose ps`
- Verify database credentials and host settings

**Static Files Not Loading:**

- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Ensure Tailwind CSS is built: `cd tailwind && npm run build`

**Template Issues:**

- Verify template directories in `TEMPLATES['DIRS']`
- Check app template loading with `APP_DIRS: True`
- Ensure template names match file names exactly

**Migration Issues:**

- Check migration status: `python manage.py showmigrations`
- Resolve conflicts manually if needed
- Never modify existing migrations

**Testing Failures:**

- Run specific tests: `python manage.py test apps.app_name.tests.test_file`
- Check test database configuration
- Ensure test dependencies are installed

### Debug Mode

- Set `DEBUG = True` in settings for development
- Use Django Debug Toolbar if installed
- Check Django logs in terminal or Docker logs
- Use `print()` statements or Django's logging framework

## Notes for AI Agents

- This is a basic Django blog scaffold - no custom apps or models are implemented yet
- The project uses Poetry for dependency management, not pip
- Static files are built from Tailwind CSS in the `tailwind/` directory
- HTMX and Alpine.js are integrated for enhanced user interactions without heavy JavaScript frameworks
- HTMX attributes are used in Django templates for AJAX functionality
- Alpine.js is used for client-side reactivity and component state management
- **Always use local static assets instead of CDN links** for Tailwind CSS, HTMX, Alpine.js, and any third-party libraries
- Static assets are placed in the `static/` directory and must be collected using `python manage.py collectstatic` before deployment
- **Testing**: Create unit tests after finishing work on issues (when appropriate), focus on happy path scenarios, prefer Django TestCase over pytest, avoid patches/mocks unless necessary
- **Documentation First**: Always read project documentation before coding
- **Quality Standards**: No shortcuts - do it right the first time, keep issues small and focused
- **Simple Solutions**: Write minimal code first, then refactor - avoid over-engineering
- Database migrations need to be created and run after adding models
- The admin interface is enhanced with django-unfold for better UX
- Environment variables are required for database and secret key configuration</content>
  <parameter name="filePath">/home/harlin/Sandbox/prodigi/blog/agents.md
