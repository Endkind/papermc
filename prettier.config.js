module.exports = {
  plugins: [require("prettier-plugin-sh")],
  overrides: [
    {
      files: "*.sh",
      options: {
        parser: "sh",
      },
    },
  ],
};
