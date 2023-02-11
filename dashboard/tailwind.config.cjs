/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    fontFamily: {
      'open': ['Open Sans', 'sans-serif'],
      'nunito': ['Nunito', 'sans-serif'],
      'mono': ["Roboto Mono",Menlo,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New,monospace]
    },
    extend: {}
  },
  plugins: [],
  darkMode: 'class'
};