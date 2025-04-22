import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import FormInput from '../components/FormInput';

const EmailVerificationPage = () => {
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [resendDisabled, setResendDisabled] = useState(false);
  const [countdown, setCountdown] = useState(60);
  const [email, setEmail] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Get email from location state or localStorage
    const storedEmail = localStorage.getItem('verificationEmail');
    const locationEmail = location.state?.email;
    
    if (locationEmail) {
      setEmail(locationEmail);
      localStorage.setItem('verificationEmail', locationEmail);
    } else if (storedEmail) {
      setEmail(storedEmail);
    } else {
      // If no email is found, redirect to login
      navigate('/login');
    }

    // Start countdown for resend button
    const timer = setInterval(() => {
      setCountdown((prevCount) => {
        if (prevCount <= 1) {
          clearInterval(timer);
          setResendDisabled(false);
          return 0;
        }
        return prevCount - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [navigate, location]);

  const handleChange = (e) => {
    setError('');
    setOtp(e.target.value);
  };

  const validateOtp = () => {
    if (!otp) {
      setError('Please enter the OTP');
      return false;
    }
    if (otp.length !== 6) {
      setError('OTP must be 6 digits');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateOtp()) return;

    setIsLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/auth/verify-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, 'confirmation_code':otp }),
      });

      const data = await res.json();
      
      if (res.ok) {
        toast.success(data.message || 'Email verified successfully!', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });
        localStorage.removeItem('verificationEmail');
        navigate('/login');
      } else {
        setError(data.message || 'Verification failed. Please check your OTP.');
        toast.error(data.message || 'Verification failed. Please check your OTP.', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });
      }
    } catch (err) {
      setError('An error occurred. Please try again later.');
      toast.error('An error occurred. Please try again later.', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendOtp = async () => {
    if (resendDisabled) return;
    
    setIsLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/auth/resend-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await res.json();
      
      if (res.ok) {
        toast.success(data.message || 'OTP has been resent to your email.', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });
        setResendDisabled(true);
        setCountdown(60);
        
        // Start countdown again
        const timer = setInterval(() => {
          setCountdown((prevCount) => {
            if (prevCount <= 1) {
              clearInterval(timer);
              setResendDisabled(false);
              return 0;
            }
            return prevCount - 1;
          });
        }, 1000);
      } else {
        setError(data.message || 'Failed to resend OTP. Please try again.');
        toast.error(data.message || 'Failed to resend OTP. Please try again.', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });
      }
    } catch (err) {
      setError('An error occurred. Please try again later.');
      toast.error('An error occurred. Please try again later.', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleSubmit} className="auth-form">
        <h2>Email Verification</h2>
        <p className="verification-info">
          We've sent a verification code to <strong>{email}</strong>
        </p>
        {error && <div className="error-message">{error}</div>}
        <FormInput 
          label="Enter OTP" 
          type="text" 
          name="otp" 
          value={otp} 
          onChange={handleChange}
          placeholder="Enter 6-digit code"
          required 
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Verifying...' : 'Verify Email'}
        </button>
        <div className="resend-otp">
          <p>
            Didn't receive the code?{' '}
            <button 
              type="button" 
              onClick={handleResendOtp} 
              disabled={resendDisabled || isLoading}
              className="resend-button"
            >
              {resendDisabled 
                ? `Resend in ${countdown}s` 
                : 'Resend OTP'}
            </button>
          </p>
        </div>
      </form>
    </div>
  );
};

export default EmailVerificationPage; 