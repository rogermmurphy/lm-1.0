/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/lib/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        lmPink: "#f6c6d0",
        lmCream: "#fff7f2",
        lmPurple: "#b89bff",
        lmGray: "#444"
      },
      fontFamily: {
        lm: ["Poppins", "sans-serif"]
      }
    }
  },
  plugins: [],
};
