/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./readverse/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
