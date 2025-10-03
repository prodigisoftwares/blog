module.exports = {
  content: [
    "../blog/apps/**/templates/**/*.{html,py,js}",
    "../blog/**/templates/**/*.{html,py,js}",
    "../blog/static/**/*.js",
  ],
  media: false,
  plugins: [require("@tailwindcss/typography")],
};
