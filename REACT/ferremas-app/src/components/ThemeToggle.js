import React, { useState, useEffect } from 'react';

export default function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    // Load the initial theme from localStorage or default to 'light'
    return localStorage.getItem('theme') || 'light';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  return (
    <fieldset>
      <label>
        <input
          name="terms"
          type="checkbox"
          role="switch"
          onChange={toggleTheme}
          checked={theme === 'dark'}
        />
        {theme === 'light' ? 'Modo claro' : 'Modo oscuro'}
      </label>
    </fieldset>
  );
}
  