// LanguageSelect.js
import React from 'react';

const LanguageSelect = ({ label, value, onChange, languages }) => {
  return (
    <div>
      <label htmlFor={label}>{label}:</label>
      <select id={label} onChange={onChange} value={value}>
        {languages.map(language => (
          <option key={language.code} value={language.code}>
            {language.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelect;
