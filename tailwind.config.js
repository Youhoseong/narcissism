module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    textColor: ['current'],
    rotate: ['expanded']
  },
  plugins: [
    require('@alexcarpenter/tailwindcss-aria'),
  ],
}
