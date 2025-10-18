/** @type {import('tailwindcss').Config} */
module.exports = {
  // NOTE: Update this to include the paths to all files that contain Nativewind classes.
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        'pink-50': '#fce7f3',
        'pink-300': '#f9a8d4',
        'pink-500': '#ec4899',
        'pink-600': '#db2777',
        'pink-700': '#be185d',
        'dark-pink': '#1a0a14',
      },
    },
  },
  plugins: [],
}