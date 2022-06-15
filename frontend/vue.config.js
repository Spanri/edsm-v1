const path = require("path");

module.exports = {
  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src")
      }
    },
    module: {
      rules: [
        {
          test: /\.md$/,
          loader: "raw-loader" // npm install -D raw-loader
        }
      ]
    }
  }
};

