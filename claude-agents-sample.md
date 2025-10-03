# Claude Development Guide for ProofAndQuote.com

This document provides context and guidelines for Claude when working on the ProofAndQuote.com project.

As we work on Features/Bugs/Tasks, I will occasionally give info on how I want things done (usually quality or technique-wise) and I need you to update this CLAUDE.md document with that info.

## Project Context

### Mission

ProofAndQuote.com is the **client-facing portal** that works alongside ProofQuoteFlow.com (contractor workspace). The goal is to make contractors look professional while giving clients a transparent, trustworthy experience.

### Platform Strategy

- **Current Focus:** Desktop/web implementation (Django + Tailwind CSS)
- **Future Mobile Stack (Proposed):**
  - **Framework:** React Native with Expo
  - **Styling:** NativeWind (Tailwind for React Native)
  - **Backend:** Django REST API (shared with web)
  - **Location:** Top-level `mobile/` directory (to be created when ready)
  - **Rationale:** Single codebase for iOS/Android, maintains Tailwind design system, excellent camera/photo handling, native push notifications, aligns with existing mobile-first philosophy

### Target Users

- **Primary:** Homeowners and property owners who hired contractors
- **Secondary:** Small business owners needing contractor services
- **Tertiary:** Property managers overseeing contractor work

### Core Value Proposition

Transform typical contractor-client interactions from:

- ❌ Photos buried in text messages
- ❌ Hand-written quotes on napkins
- ❌ Awkward Excel invoices
- ❌ "Trust me" communication

To:

- ✅ Professional branded galleries
- ✅ Clean, detailed estimates
- ✅ Secure payment processing
- ✅ Transparent job tracking

## Development Standards

### Code Style

- **Python:** Follow Django best practices, PEP 8, 4-space indentation
- **HTML/CSS:** Mobile-first responsive design, **2-space indentation** (not 4-space)
- **JavaScript:** Minimal, progressive enhancement, **2-space indentation**
- **Database:** PostgreSQL with proper migrations

We want firstly to write just enough code to get the job done (based on the issue) and then as we work the issue, we'll come back and refactor according to best practices. We will do everything possible to avoid overthinking or over-architecting solutions. The solutions should be simple.

### Developer Preferences & Best Practices

- **App Structure:** All Django apps must be organized as sub-packages, not single files:
  - Create `admin/`, `models/`, `tests/`, `views/`, `utils/` as folders with `__init__.py`
  - Each package should import from its submodules and use explicit `__all__` exports
  - Name submodules appropriately: `admin/galleries.py`, `models/galleries.py`, `tests/test_galleries.py`
  - For views, organize by functionality: `views/contractor.py`, `views/photos.py`, `views/public.py`
  - Keep view modules focused and around 70 lines when possible (same as templates)
  - Remove original single `.py` files after converting to packages
- **Views:** Prefer class-based views over function-based views:
  - Use Django's generic class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView, etc.)
  - Leverage mixins like LoginRequiredMixin for authentication
  - Override methods like get_context_data(), get_queryset() for custom behavior
  - Organize views into logical modules by functionality (contractor views, public views, photo views, etc.)
  - Keep view modules focused around 70 lines when possible (same guideline as templates)
  - Use explicit imports and `__all__` in `views/__init__.py` for clear API
  - Class-based views provide better code organization and reusability
- **Forms:** Use Django ModelForms with proper validation:
  - **Styling preference order:** 1) Tailwind classes in templates first, 2) Form widget attrs if template styling not feasible, 3) Form Media definitions last resort
  - Implement custom `clean_[field]()` methods for field-specific validation
  - Use `form.cleaned_data.get()` to safely access validated data
  - Handle file uploads with request.FILES.getlist() for multiple files
  - Provide user-friendly error messages via forms.ValidationError
  - **Extending Built-in Forms:** When extending Django's built-in forms (e.g., `UserCreationForm`), add required fields in the extended class and override `save()` method if needed
  - **Uniqueness Validation:** Check for duplicate values in `clean_[field]()` using `Model.objects.filter(field=value).exists()` and raise `forms.ValidationError` with clear message
  - **Form Organization:** Create forms in `[app_name]/forms.py` file, import in views as needed
- **App Location:** Apps live in `pqw/apps/[app_name]/` directory structure
- **INSTALLED_APPS:** Reference apps as `"apps.[app_name]"` in settings
- **App Configuration:** Set `name = "apps.[app_name]"` in the app's `apps.py` file
- **URL Routing:** Create `urls.py` in each app with `app_name` namespace and include in main URLs
- **Documentation:** Maintain `CHANGELOG.md` documenting all changes made for each issue
- **File Formatting:** All files must end with a newline character (actual `\n`, not just empty space) - let pre-commit handle formatting
- **Generated Files:** Compiled/generated files (like `static/css/styles.css`) should be excluded from pre-commit formatting
- **Markdown Files:** Markdown files are excluded from Prettier formatting to preserve specific formatting requirements
- **Indentation Standards:** Python=4 spaces, HTML/CSS/JS=2 spaces (strictly enforced)
- **Template Standards:** Django templates must use named endblocks (e.g., `{% endblock content %}` not `{% endblock %}`)
- **Template Length:** Keep templates under 70 lines when possible - break longer templates into appropriate includes for better maintainability
- **Template Organization:** Create reusable template includes for common UI patterns:
  - Store includes in `templates/[app_name]/includes/` directory
  - Prefix include filenames with underscore (e.g., `_messages.html`, `_back_link.html`)
  - Make includes flexible with context variables (e.g., `submit_text|default:"Submit"`)
  - Common patterns to extract: navigation elements, form actions, messages, complex interactive components, headers, empty states
  - Name includes descriptively based on functionality (e.g., `_gallery_detail_header.html`, `_gallery_detail_actions.html`)
  - Benefits: DRY code, consistent UI, easier maintenance across multiple views, improved testability
- **User Model vs Profile Model Pattern:** Separate account data from profile/business data:
  - **User Model (Django's built-in):** Username, email (for login/notifications), password - account-level data
  - **Profile Model (OneToOne with User):** Business information, preferences, optional contact details
  - Display read-only account information (username, email) separately from editable profile forms
  - Use gray background box at top of profile page to show non-editable User fields
  - Profile can have optional business email separate from account email for flexibility
  - Pattern: Account email = system notifications, Business email = public contact on galleries
- **Navigation Consistency:** ALL authenticated pages must include navigation for consistent UX:
  - Every app's base template must include the navigation component (e.g., `{% include "dashboard/includes/_navigation.html" %}`)
  - Navigation should appear at the top of every authenticated page
  - Users must always be able to navigate back to Dashboard, Galleries, and Profile from any page
  - Never create isolated pages without navigation - users should never feel "stuck" on a page
  - Public/unauthenticated pages can have different navigation appropriate for their context
- **Django URL Template Tags:** Always use keyword arguments for URL patterns with named groups:
  - Correct: `{% url 'galleries:public' share_slug=gallery.share_slug %}`
  - Incorrect: `{% url 'galleries:public' gallery.share_slug %}`
  - Use conditional checks before rendering URLs if field might be empty: `{% if gallery.share_slug %}...{% endif %}`
- **CSS Standards:** Custom styles that cannot be handled by Tailwind classes should be placed in `tailwind/custom.css` using proper `@layer` directives, not inline `<style>` tags in templates
- **Button Philosophy (CRITICAL):**
  - **NO buttons should EVER be significantly wider than their text content**
  - Buttons size to content automatically via `inline-flex` in `.btn-base`
  - NEVER use `w-full`, `btn-full`, or `flex-1` on buttons - these make buttons unprofessionally wide
  - Button component classes: `.btn-primary`, `.btn-secondary`, `.btn-tertiary`, `.btn-danger`, `.btn-success`
  - Size variants: `.btn-sm`, `.btn-lg` (adjust padding, not width)
  - All buttons must include `hover:text-white` (or appropriate color) to prevent text from disappearing on hover
  - Clean, simple design: no animations, no lift effects, just solid color transitions (200ms)
  - Use `flex flex-wrap gap-3` for button groups so they wrap naturally
  - This applies to ALL buttons: form submits, action buttons, CTAs, everything
- **Quality Standards:** Tech lead expects perfection - doing exactly like he says and never forgetting when he says it even if you have to write it down right then. No shortcuts, no "good enough", everything done right the first time
- **Issue Scope:** When creating GitHub issues, keep them small and focused - one specific task or change per issue rather than large multi-step features. Limit scope to 10 files or less whenever possible
- **Test Organization:** Organize tests into logical modules mirroring code structure:
  - Create `tests/test_forms.py`, `tests/test_contractor_views.py`, `tests/test_photo_views.py`, etc.
  - Keep test files focused around 70 lines when possible (same guideline as views/templates)
  - Extract shared test utilities to `tests/helpers.py` (e.g., `create_test_image()`)
  - Import all test modules in `tests/__init__.py` for test discovery
  - Benefits: Easier to find tests, faster test execution, better organization
- **Test Coverage Exclusions:** Use `# pragma: no cover` for code that doesn't need coverage:
  - Model `__str__()` methods: `def __str__(self): # pragma: no cover`
  - Admin display methods that are simple property accessors or counts
  - Simple one-line methods that just return formatted strings or counts
- **Testing Philosophy - DO NOT TEST EXTERNAL CODE:**
  - **NEVER write tests for Django's built-in functionality** - Django is already well-tested
  - **NEVER write tests for third-party packages** - They have their own test suites
  - **DO NOT test basic model field behavior** (CharField, IntegerField, ForeignKey, etc.)
  - **DO NOT test ORM operations** (create, save, filter, get)
  - **DO NOT test framework validators** (EmailValidator, URLValidator, etc.)
  - **ONLY test custom business logic we wrote:**
    - Custom model methods (e.g., `get_formatted_display()`, `calculate_total()`)
    - Custom form validation logic (e.g., `clean_logo()` with file size/format checks)
    - Custom view behavior (e.g., auto-creating profiles, special permissions)
    - Custom template filters and tags (e.g., `format_phone`)
    - Integration points between our components
  - **When in doubt, ask:** "Am I testing my code or someone else's code?" If it's external code, delete the test
  - **Example - BAD tests (testing external code):**
    - Testing that a CharField can be created ❌
    - Testing that OneToOneField enforces uniqueness ❌
    - Testing that blank=True makes a field optional ❌
    - Testing that Pillow can resize images ❌
  - **Example - GOOD tests (testing our code):**
    - Testing custom validation logic in `clean_logo()` ✅
    - Testing custom phone formatting template filter ✅
    - Testing view creates profile automatically on first access ✅
- **Alpine.js Components:** Create reusable Alpine.js components using function-based pattern:
  - Define components as functions in `<script>` tags: `function componentName() { return { ... } }`
  - Initialize with `x-data="componentName()"` on container element
  - Keep component logic focused and single-responsibility
  - Use descriptive method names: `handleSubmit()`, `validateFile()`, `handleDrop()`
  - Store component state in data properties: `uploading`, `validFiles`, `errors`
  - Provide immediate user feedback with reactive UI updates
  - Example patterns: file validation, upload progress, drag-and-drop
- **Form Validation Strategy:** Implement both client-side and server-side validation:
  - **Client-side (JavaScript):** Immediate feedback before form submission using Alpine.js
    - Validate file types, sizes, and formats before upload
    - Display validation errors inline with clear messaging
    - Filter out invalid files automatically
    - Prevent form submission if validation fails
  - **Server-side (Django):** Authoritative validation in form clean methods
    - Always validate on server even if client-side validation exists
    - Use `forms.ValidationError` for user-friendly error messages
    - Handle edge cases and security concerns
    - Wrap operations in try-catch for graceful error handling
  - **User Feedback:** Provide clear messages at every stage
    - Show validation errors with specific file names and reasons
    - Display progress indicators during long operations
    - Confirm successful operations with counts and details
    - Enable retry via back navigation after errors

### Key Commands

- **Linting:** We're using pre-commit to handle all of the linting.
- **Tests:** `./pqw/test.sh`
- **Type checking:** `mypy pqw/`
- **CSS:** `npm run build` in `tailwind/` directory
- **Email Testing:** `cd pqw && python manage.py test_email --type all --email test@example.com`

### Development Environment

- Use `./dev-up.sh` to start development containers
- Application runs on http://localhost:8000
- Admin interface at http://localhost:8000/admin
- Use `./pqw/createadmin.sh` for initial superuser
- **Virtual Environment:** Source `.venv/bin/activate` from project root when running Django commands
- **Project Structure:** All Django commands should be run from `pqw/` directory
- **Media Files:**
  - Uploaded files stored in `MEDIA_ROOT` (pqw/mediafiles/)
  - Served at `MEDIA_URL` (/media/) in development
  - Must add `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` to urls.py in DEBUG mode
  - Images stored with date-based paths: `gallery_photos/%Y/%m/%d/`

## Architecture Principles

### Two-Platform Philosophy

```
ProofQuoteFlow.com (Contractors)    ProofAndQuote.com (Clients)
├─ Photo uploads                 ←→ ├─ Photo galleries
├─ Estimate creation            ←→ ├─ Quote viewing
├─ Job management               ←→ ├─ Progress tracking
└─ Invoice generation           ←→ └─ Payment processing
```

### Shared Backend, Separate Frontends

- Common Django models and API endpoints
- Different views/templates for each platform
- Unified user management with role separation

### Mobile-First Design

- Clients primarily use smartphones
- Touch-friendly interfaces
- Fast loading on mobile data
- Offline-friendly where possible

### Frontend Interactivity

- **Third-Party Assets Policy:** ALL external libraries and assets must be stored locally in the project
  - NO CDN dependencies in production (reliability, security, performance, offline development)
  - Store JavaScript libraries in `pqw/static/js/`
  - Store CSS libraries in `pqw/static/css/`
  - Store fonts/icons in appropriate static directories
  - Version control ensures consistency across all environments
- **Alpine.js:** Lightweight JavaScript framework for reactive components
  - Served as local static asset from `pqw/static/js/alpine.min.js`
  - Use for: drag-and-drop, auto-dismissing messages, show/hide toggles, dynamic UI updates
  - Syntax: `x-data`, `x-show`, `x-transition`, `x-init`, `@click`, `@dragover`, etc.
  - Keep JavaScript logic minimal and progressive - pages should work without JS
  - Example patterns:
    - File upload with drag-and-drop: `x-data="{ dragging: false, files: [] }"`
    - Auto-dismissing notifications: `x-init="setTimeout(() => show = false, 5000)"`
- **HTMX:** For progressive enhancement and partial page updates (minimal framework, stored locally)
- **Tailwind CSS:** Utility-first styling, mobile-first breakpoints (built locally via npm)

## Feature Development Guidelines

### Phase 1: Photo Galleries

**Priority:** Foundation for contractor credibility

- Before/after photo collections
- Contractor branding customization
- Simple sharing via links
- **Focus:** Visual impact and professional presentation

### Phase 2: Quotes & Estimates

**Priority:** Replace informal quote delivery

- Professional PDF generation
- Client review and approval workflow
- Estimate comparison tools
- **Focus:** Trust-building and clear communication

### Phase 3: Payment Processing

**Priority:** Complete transaction cycle

- Secure payment integration
- Invoice delivery and tracking
- Payment history and receipts
- **Focus:** Convenience and security

### Phase 4: Job Transparency

**Priority:** Ongoing relationship building

- Real-time status updates
- Progress photos and milestones
- Completion notifications
- **Focus:** Transparency and satisfaction

## Email Notification System

### Overview

Professional email notification system with Tailwind CSS styling and contractor branding support.

### Configuration

- **Development:** Console backend (emails printed to terminal)
- **Production:** SMTP backend configurable via environment variables
- **Templates:** HTML emails with automatic plain text fallback
- **Styling:** Uses Tailwind CSS classes with mobile-responsive design

### Email Types

- **Client Invitations:** Invite clients to view their project
- **Gallery Sharing:** Notify clients of new photos
- **Extensible:** Easy to add new notification types

### Usage Examples

```python
from apps.notifications.utils import (
    send_client_invitation_email,
    send_gallery_sharing_email
)

# Send client invitation
success = send_client_invitation_email(
    contractor=contractor_user,
    client_email='client@example.com',
    invitation_link='https://proofandquote.com/project/123',
    project=project_obj
)

# Send gallery notification
success = send_gallery_sharing_email(
    contractor=contractor_user,
    client_email='client@example.com',
    gallery_link='https://proofandquote.com/gallery/456',
    gallery=gallery_obj,
    project=project_obj
)
```

### Testing

- **Management Command:** `python manage.py test_email --type all --email test@example.com`
- **Unit Tests:** Located in `apps/notifications/tests/test_email.py`
- **Template Testing:** Templates render with mock data for development

## UI/UX Guidelines

### Design Principles

- **Clean:** Minimal clutter, focused content
- **Professional:** Builds contractor credibility
- **Trustworthy:** Clear pricing, secure transactions
- **Responsive:** Works perfectly on all devices

### Design System (Issue #73)

**Professional design system with sophisticated typography and color palette for elite UI/UX.**

#### Typography

**Font Family:**

- **Primary:** Inter (variable font, locally hosted)
- **Fallback stack:** system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif
- **Location:** `/pqw/static/fonts/web/InterVariable.woff2`

**Typography Scale:**

```
h1: text-6xl (60px) / font-extrabold (800) / tracking-tight
h2: text-5xl (48px) / font-bold (700) / tracking-tight
h3: text-4xl (36px) / font-bold (700)
h4: text-3xl (30px) / font-semibold (600)
h5: text-2xl (24px) / font-semibold (600)
h6: text-xl (20px) / font-semibold (600)
Body: text-base (16px) / font-normal (400) / line-height 1.5
Small: text-sm (14px) / Secondary text
Caption: text-xs (12px) / Labels and metadata
```

**Utility Classes:**

- `.text-display` - Large display text (48px/extrabold)
- `.text-heading` - Section headings (30px/bold)
- `.text-subheading` - Subsection headings (20px/semibold)
- `.text-body` - Body text (16px/normal)
- `.text-body-emphasized` - Emphasized body (16px/medium)
- `.text-small` - Small text (14px)
- `.text-caption` - Captions and labels (12px)
- `.text-label` - Form labels (14px/medium)

#### Color Palette

**WCAG 2.1 AA compliant color system with semantic tokens.**

**Primary (Professional Blue):**

```
primary-50: #eff6ff   (Lightest backgrounds)
primary-100: #dbeafe  (Light hover states)
primary-500: #3b82f6  (Main primary - buttons, links)
primary-600: #2563eb  (Hover - interactive elements)
primary-700: #1d4ed8  (Active states)
primary-900: #1e3a8a  (Darkest - text on light bg)
```

**Secondary (Warm Gray - Sophisticated Neutral):**

```
secondary-50: #fafaf9   (Lightest backgrounds)
secondary-100: #f5f5f4  (Card backgrounds)
secondary-200: #e7e5e4  (Borders, dividers)
secondary-300: #d6d3d1  (Disabled states)
secondary-400: #a8a29e  (Placeholder text)
secondary-500: #78716c  (Secondary text)
secondary-600: #57534e  (Body text)
secondary-700: #44403c  (Headings)
secondary-800: #292524  (Dark headings)
secondary-900: #1c1917  (Darkest text)
```

**Semantic Colors:**

```
success-500: #22c55e  (Green - success states)
success-600: #16a34a  (Hover)
warning-500: #f59e0b  (Amber - warnings)
warning-600: #d97706  (Hover)
error-500: #ef4444    (Red - errors)
error-600: #dc2626    (Hover)
neutral-*: Cool gray  (UI elements)
```

**Usage Guidelines:**

- Use `primary-*` for interactive elements (buttons, links, focus states)
- Use `secondary-*` for text hierarchy and neutral UI
- Use semantic colors (success/warning/error) for states and feedback
- Ensure 4.5:1 contrast ratio for text (WCAG AA)
- Ensure 3:1 contrast ratio for UI components

#### Spacing & Layout (Issue #83)

**Spacing Scale:**
Tailwind's default 4px scale: 0, 1(4px), 2(8px), 3(12px), 4(16px), 5(20px), 6(24px), 8(32px), 10(40px), 12(48px), 16(64px), 20(80px), 24(96px), 32(128px)

**Standard Spacing Conventions:**

- **Page padding (mobile):** `px-4` (16px)
- **Page padding (desktop):** `px-6 lg:px-8` (24px/32px)
- **Section vertical spacing:** `py-12 lg:py-16` (48px/64px)
- **Section gaps:** `space-y-8` or `space-y-12` (32px/48px)
- **Card padding:** `p-6` (24px)
- **Form spacing:** `space-y-6` (24px between fields)
- **Grid gaps:** `gap-4` (16px) or `gap-6` (24px)
- **Element margins:** `mb-8` (32px) or `mb-12` (48px)

**Container Widths:**

- `max-w-7xl` (1280px) - Main dashboard/app pages
- `max-w-4xl` (896px) - Public gallery pages, forms
- `max-w-2xl` (672px) - Narrow forms, profile pages
- `max-w-md` (448px) - Authentication forms

**Layout Utility Classes:**

- `.container-page` - Full-width page container (`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`)
- `.container-narrow` - Narrow content container (`max-w-4xl mx-auto px-4 sm:px-6 lg:px-8`)
- `.container-form` - Form container (`max-w-md mx-auto px-4`)
- `.section-spacing` - Standard section spacing (`py-12 lg:py-16`)
- `.section-spacing-sm` - Small section spacing (`py-8 lg:py-12`)
- `.section-spacing-lg` - Large section spacing (`py-16 lg:py-24`)

**Border Radius:**

- `rounded` (default): 8px - Cards, buttons
- `rounded-lg`: 12px - Larger cards
- `rounded-xl`: 16px - Feature sections
- `rounded-full`: Pills, avatars

**Shadows:**

- `shadow-sm`: Subtle card elevation
- `shadow` (default): Standard cards
- `shadow-md`: Hover states, dropdowns
- `shadow-lg`: Modals, popovers

#### Transitions & Animations

**Timing:**

- Default: 200ms (quick feedback)
- Smooth: 300ms (page transitions, modals)
- Timing function: cubic-bezier(0.4, 0, 0.2, 1) - ease-in-out

**Utility Classes:**

- `.transition-smooth` - 200ms transitions
- `.transition-smooth-300` - 300ms transitions
- `.text-crisp` - Optimized text rendering

**Best Practices:**

- Keep animations subtle and fast (200-300ms)
- Use transitions for hover, focus, active states
- Respect `prefers-reduced-motion` setting

## Authentication & Security

### Client Access Pattern

- **Invitation-based:** Contractors invite clients
- **Lightweight auth:** Email + simple password
- **Session-based:** Standard Django sessions
- **Privacy-focused:** Clients see only their projects

### Security Requirements

- HTTPS everywhere
- Secure payment processing
- Image upload validation
- Rate limiting on public endpoints
- CSRF protection on all forms

## Database Design

### Key Models

```python
# Core entities
Contractor (extends User)
Client (extends User)
Project
PhotoGallery
Estimate
Invoice
Payment

# Relationships
Contractor -> Projects -> Clients
Projects -> PhotoGalleries, Estimates, Invoices
```

### Migration Strategy

- Always create reversible migrations
- Test migrations on sample data
- Document breaking changes
- Coordinate with ProofQuoteFlow.com schema

## Testing Strategy

### Test Coverage Areas

- **Models:** Business logic and relationships
- **Views:** Authentication and permissions
- **Forms:** Validation and error handling
- **Integration:** Payment processing
- **E2E:** Critical user journeys

### Test Commands

- `./pqw/test.sh` - Run full test suite
- `pytest pqw/apps/` - Run specific app tests
- Coverage reports generated automatically

## Deployment Notes

### Production Environment

- Docker containers with Nginx proxy
- PostgreSQL database
- Redis for caching/sessions
- S3 for file storage
- CDN for static assets

### Environment Variables

- **Development:** `.env.dev`
- **Production:** `.env.prod`
- **Database:** `.env.prod.db`
- Never commit environment files to git

## Common Tasks

### Adding New Features

1. **Django App Structure:** Create apps in `pqw/apps/[app_name]` folder structure
   - Use: `python manage.py startapp [app_name] apps/[app_name]`
   - Update `apps.py`: Set `name = "apps.[app_name]"`
   - Add to `INSTALLED_APPS` as: `"apps.[app_name]"`
2. **App Organization:** Convert single files to sub-packages:
   - Create folders: `admin/`, `models/`, `tests/`, `views/`, `utils/`
   - Each folder gets `__init__.py` with imports from submodules
   - Move content to appropriately named submodules (e.g., `admin/galleries.py`, `models/galleries.py`)
   - Remove original single `.py` files after migration
3. Add models with proper migrations
4. Create views with authentication checks
5. Design mobile-first templates
6. Add comprehensive tests
7. Update this documentation

### Debugging Issues

- Check Django logs in docker logs
- Use Django Debug Toolbar in development
- Test responsive design on actual devices
- Verify payment flows in sandbox mode

### Performance Optimization

- Database query optimization (select_related, prefetch_related)
- Image optimization and CDN usage
- CSS/JS minification via Tailwind
- Caching strategy for galleries and estimates

## Integration Points

### With ProofQuoteFlow.com

- Shared user authentication
- Common photo storage
- Synchronized project data
- Unified notification system

### External Services

- Payment processors (Stripe/Square)
- Email delivery (SendGrid/Mailgun)
- SMS notifications (Twilio)
- File storage (AWS S3)

---

## Working with Issues

### Issue Workflow for AI Agents

When assigned to work on a GitHub issue, follow these steps:

1. **Pre-Work Assessment:**
   - Read the issue description and acceptance criteria thoroughly
   - Check if the issue has already been completed by searching the codebase
   - If already implemented, inform the user immediately and provide evidence
   - Never duplicate work that's already been done

2. **Documentation Review (MANDATORY):**
   - **ALWAYS** read ALL project documentation files first:
     - `CLAUDE.md` - Development guidelines and best practices
     - `DEVELOPMENT.md` - Technical implementation details
     - `README.md` - Project overview and setup
     - `CHANGELOG.md` - Recent changes and patterns
   - Understanding the project context prevents mistakes and ensures consistency
   - Look for similar work patterns in existing code and documentation

3. **Implementation Standards:**
   - Follow ALL best practices mentioned in project documentation
   - Use the TodoWrite tool for complex multi-step tasks
   - Apply established code style and architectural patterns
   - Maintain proper app structure (sub-packages, not single files)
   - Update tests and ensure they pass
   - Use Tailwind CSS classes appropriately
   - Follow template formatting standards (named endblocks)

4. **Documentation Updates:**
   - Update `CHANGELOG.md` with detailed changes made
   - Update relevant documentation (CLAUDE.md, DEVELOPMENT.md, README.md)
   - Add usage examples where appropriate
   - Document new commands, utilities, or patterns created

5. **Quality Assurance:**
   - Run all linting and formatting checks
   - Ensure all tests pass
   - Verify acceptance criteria are met
   - Check that implementation follows project conventions

6. **Issue Completion:**
   - Verify all acceptance criteria are fulfilled
   - Provide clear summary of work completed
   - Note any related issues or follow-up work needed
   - Ensure code is ready for production use

### Key Principles

- **Documentation First:** Always read docs before coding
- **Consistency:** Follow established patterns and conventions
- **Quality:** No shortcuts - do it right the first time
- **Communication:** Keep user informed of progress and decisions
- **Evidence-Based:** Check existing code before claiming work is needed

## Quick Reference

**Start Development:** `./dev-up.sh`
**Run Tests:** `./pqw/test.sh`
**Format Code:** `ruff format pqw/`
**Build CSS:** `cd tailwind && npm run build`
**Create Migration:** `python manage.py makemigrations`
**Apply Migrations:** `python manage.py migrate`

Remember: Every feature should make contractors look more professional and give clients more confidence in their choice of contractor.
