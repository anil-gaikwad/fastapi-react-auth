import React from 'react';

const FormInput = ({ label, type, name, value, onChange, required, placeholder }) => {
  return (
    <div className="form-group">
      <label htmlFor={name}>{label}</label>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        className="form-control"
        placeholder={placeholder}
      />
    </div>
  );
};

export default FormInput; 