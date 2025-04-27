export default [
  {
    files: ['incident_reporting/static/js/**'],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
    },
    rules: {
      'no-console': 'warn',
      'eqeqeq': 'error',
      'curly': 'error',
    },
  },
];
