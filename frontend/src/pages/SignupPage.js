import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import FormInput from '../components/FormInput';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setError('');
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateForm = () => {
    if (!formData.username || !formData.email || !formData.password) {
      setError('Please fill in all fields');
      return false;
    }
    if (!/\S+@\S+\.\S+/.test(formData.email)) {
      setError('Please enter a valid email address');
      return false;
    }
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      
      if (res.ok) {
        // Store email for verification page
        localStorage.setItem('verificationEmail', formData.email);
        
        // Show success toast
        toast.success(data.message || 'User registered successfully! Check email for OTP', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });
        
        // Navigate to verification page with email
        navigate('/verify-email', { state: { email: formData.email } });
      } else {
        setError(data.message || 'Signup failed. Please try again.');
        toast.error(data.message || 'Signup failed. Please try again.', {
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
        <h2>Sign Up</h2>
        {error && <div className="error-message">{error}</div>}
        <FormInput 
          label="Username" 
          type="text" 
          name="username" 
          value={formData.username} 
          onChange={handleChange}
          required 
        />
        <FormInput 
          label="Email" 
          type="email" 
          name="email" 
          value={formData.email} 
          onChange={handleChange}
          required 
        />
        <FormInput 
          label="Password" 
          type="password" 
          name="password" 
          value={formData.password} 
          onChange={handleChange}
          required 
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Signing up...' : 'Sign Up'}
        </button>
        <div className="auth-links">
          <p>Already have an account? <Link to="/login">Login</Link></p>
        </div>
      </form>
    </div>
  );
};

export default SignupPage;
