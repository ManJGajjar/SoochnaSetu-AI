/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: '#0F1C2E',
        saffron: '#FF6B35',
        'green-india': '#138808',
        'orange-india': '#FF9933',
        'white-india': '#FFFFFF',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 3s ease-in-out infinite',
        'slideUp': 'slideUp 0.8s ease-out forwards',
        'fadeIn': 'fadeIn 1s ease-out forwards',
      },
    },
  },
  plugins: [],
}
