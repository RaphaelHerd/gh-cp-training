## User Registration Form - Feature Requirements

### Feature overview

Introduce a User Registration capability that enables prospective customers or users to create an account on the site, establishing the foundation for authenticated experiences (e.g., login, profile, and future personalization). The registration flow must be reliable, secure, and easy to use, reducing friction at onboarding and supporting measurable conversion goals.

Business objectives:
- Increase onboarding completion by providing a clear, accessible registration journey
- Ensure data integrity and account uniqueness with robust validation
- Protect customer information with industry-standard password hashing
- Provide deterministic, testable outcomes to support quality assurance and TDD
- Align with existing site navigation and branding for a consistent experience

## User stories and acceptance criteria

### Story 1: As a visitor, I can open the registration form from the main navigation

Acceptance criteria:
- A new navigation link is present: "Form 7 - User Registration" pointing to `index.php?action=form7`
- The registration page renders a heading "Register New User" and a form with labeled inputs
- Form is reachable and loads in under 2 seconds

### Story 2: As a visitor, I can enter my details to register a new account

Acceptance criteria:
- Required fields: First Name, Last Name, Email, Password, Confirm Password
- Optional fields: Username (if not provided, system derives from email local-part)
- All inputs have labels and placeholders where appropriate
- Password must be at least 8 characters, include at least one letter and one number
- Confirm Password must match Password
- Email must be valid per RFC-like regex and normalized to lowercase for uniqueness check
- Submit button labeled "Create account"

### Story 3: As a visitor, I receive helpful validation messages on invalid submissions

Acceptance criteria:
- Inline validation messages appear under/near invalid fields
- A general error summary appears at the top if multiple fields are invalid
- Client-side validation (HTML5 + JS hints) prevents obvious invalid submissions
- Server-side validation re-checks and returns deterministic error messages

### Story 4: As a visitor, I am prevented from registering with an email that already exists

Acceptance criteria:
- If the email is already in use, the form returns a clear error message: "An account with this email already exists."
- No user record is created in this case
- The previously entered valid fields remain populated, except for passwords

### Story 5: As a visitor, I see a success confirmation after a valid registration

Acceptance criteria:
- On success, display a confirmation page or message block: "Registration successful. You can now log in."
- The success state includes the new username (if applicable) and a link to "Form 4 - Login Form"
- The created user is persisted with a hashed password and created_at timestamp

## Detailed implementation tasks for TDD and test planning

Below, tasks are grouped under each story. Each task includes expected behavior, sample test cases, and any data set-up required, to enable testers to write tests first and developers to implement to make those tests pass.

### Story 1 - Navigation and routing

Tasks:
1. Add navigation link
   - Update the site’s navigation bar to include: "Form 7 - User Registration" → `index.php?action=form7`
   - Test cases:
     - Link is present on the homepage and other form pages
     - Clicking the link loads the registration page (HTTP 200)
2. Add route/controller action
   - Extend `index.php` routing to handle `action=form7` and render `views/form7_register.php`
   - Test cases:
     - GET `index.php?action=form7` returns the form page
     - Unknown actions continue to behave as they do currently

### Story 2 - Registration form UI

Tasks:
1. Create view `views/form7_register.php`
   - Render labeled inputs: first_name, last_name, email, username (optional), password, confirm_password
   - Include required attributes and minimal HTML5 validation (type="email" etc.)
   - Submit button: "Create account"
   - Test cases:
     - All fields render with labels
     - Required attributes present for required fields
2. Accessibility checks
   - Ensure labels are associated with inputs via `for`/`id`
   - Ensure tab order is logical, and form is usable with keyboard
   - Test cases:
     - Axe/lighthouse-like checks (if available) or manual verification

### Story 3 - Validation (client and server)

Tasks:
1. Client-side hints
   - Use HTML5 validation and optional JS helpers for instant feedback
   - Test cases:
     - Invalid email prevents submission (browser validation)
     - Mismatched passwords show message before/after submit
2. Server-side validation endpoint
   - POST `index.php?action=form7_submit`
   - Validate:
     - first_name, last_name: non-empty
     - email: valid format, normalized lowercase
     - password: min 8 chars, at least one letter and one number
     - confirm_password: must match password
   - Return errors in a structured array; re-render form with messages
   - Test cases:
     - Each invalid field produces the correct error message text
     - Multiple invalid fields show a top-level summary plus inline messages

### Story 4 - Email uniqueness and persistence

Tasks:
1. User repository
   - Implement `UserRepository` interface with methods:
     - `findByEmail(emailLowercased)`
     - `create({ firstName, lastName, email, username, passwordHash, createdAt })`
   - Backing store can be PDO/SQLite/MySQL or in-memory for test runs
   - Test cases:
     - `findByEmail` returns existing user when present
     - `create` persists and returns the new user with id
2. Uniqueness check
   - In submit handler, call `findByEmail` before creating
   - If found, return the specific error message and do not create user
   - Repopulate non-sensitive fields; clear password inputs
   - Test cases:
     - Submitting with an existing email returns the exact error message
     - No new row is added

### Story 5 - Success flow and confirmation

Tasks:
1. Success page / block
   - On successful creation, render `views/form7_success.php`
   - Show: "Registration successful. You can now log in." and link to `index.php?action=form4`
   - Display username (derived or provided)
   - Test cases:
     - After valid submission, user sees success message and login link
     - Newly created user can subsequently be found by repository
2. Data integrity
   - Ensure saved record includes `created_at` timestamp and normalized email
   - Test cases:
     - Assert timestamp is present and within reasonable bounds
     - Email stored in lowercase



## Out of scope / future enhancements

- Email verification flow
- Password strength meter UI
- CAPTCHA or advanced rate limiting
- Profile completion after registration


## Definition of Done

- All acceptance criteria pass via automated tests
- Repeatable test runs with deterministic outcomes
- Code reviewed and matches existing style patterns
- Basic accessibility and security checks completed
