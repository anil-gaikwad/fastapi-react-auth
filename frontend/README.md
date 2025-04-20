# FastAPI Authentication Frontend

This is the frontend part of the FastAPI Authentication System, built with React.

## Features

- User registration and login
- Email verification
- Password reset functionality
- Protected dashboard
- Responsive design
- Toast notifications for user feedback

## Project Structure

```
frontend/
├── public/            # Static files
│   ├── index.html     # HTML template
│   ├── welcome-dashboard.svg  # Dashboard welcome image
│   └── ...
├── src/               # Source code
│   ├── components/    # Reusable components
│   │   ├── ProtectedRoute.js  # Route protection component
│   │   └── ...
│   ├── pages/         # Page components
│   │   ├── LoginPage.js       # Login page
│   │   ├── SignupPage.js      # Registration page
│   │   ├── DashboardPage.js   # Dashboard page
│   │   ├── EmailVerificationPage.js  # Email verification page
│   │   ├── ForgotPasswordPage.js     # Forgot password page
│   │   ├── ResetPasswordPage.js      # Reset password page
│   │   └── ...
│   ├── styles/        # CSS styles
│   │   ├── Dashboard.css      # Dashboard styles
│   │   └── ...
│   ├── App.js         # Main application component
│   ├── App.css        # Main application styles
│   ├── index.js       # Application entry point
│   └── ...
└── package.json       # Dependencies and scripts
```

## Prerequisites

- Node.js 14+
- npm 6+

## Installation

1. Install dependencies:
   ```
   npm install
   ```

2. Create a `.env` file in the frontend directory with the following variables:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

## Available Scripts

### `npm start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### `npm test`

Launches the test runner in interactive watch mode.

### `npm run build`

Builds the app for production to the `build` folder.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

## API Integration

The frontend communicates with the FastAPI backend using the following endpoints:

- `POST /auth/signup` - Register a new user
- `POST /auth/login` - User login
- `POST /auth/verify-email` - Verify email address
- `POST /auth/resend-otp` - Resend verification code
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password
- `POST /auth/logout` - Logout user

## Authentication Flow

1. **Registration**: User registers with email, username, and password
2. **Email Verification**: User receives an OTP and verifies their email
3. **Login**: User logs in with email and password
4. **Dashboard**: User accesses the protected dashboard
5. **Password Reset**: User can reset their password if forgotten

## Protected Routes

The application uses the `ProtectedRoute` component to protect routes that require authentication. If a user tries to access a protected route without being authenticated, they will be redirected to the login page.

## Styling

The application uses CSS for styling. Each component has its own CSS file in the `styles` directory.

## Development

To start the development server:

```
npm start
```

## Building for Production

To build the application for production:

```
npm run build
```

This will create a `build` directory with optimized production files.
