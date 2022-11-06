/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
module.exports = {
  content: ['./views/*.ejs','./views/*/*.ejs'],
  theme: {
    colors: {
      'primeA':'#16213E',
      'primeB':'#0F3460',
      'cyan':colors.cyan,
      'white':colors.white,
      'rose':colors.rose,
      'teal':colors.teal,
      'accent':'#00607A'
    },
    extend: {},
  },
  plugins: [],
}
