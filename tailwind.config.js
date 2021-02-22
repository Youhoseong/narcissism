module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      spacing: {
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",

      },

      minHeight: {
        "50vh": "50vh",
        "75vh": "75vh",
      },

      width: {
        "31/64": "48.4375%",
      }
    },
  },
  variants: {
    textColor: ['current'],
    rotate: ['expanded']
  },
  plugins: [
    require('@alexcarpenter/tailwindcss-aria'),
  ],
}
