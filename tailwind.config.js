/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./readverse/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  safelist: [
    {
      pattern: /bg-(info|success|warning|error)/,
    },
    {
      pattern: /text-(info|success|warning|error)-content/,
    },
  ],
};
