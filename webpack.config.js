// vi: set et :
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const miniCssExtractPlugin = new MiniCssExtractPlugin({
  filename: '../css/[name].css',
});

module.exports = {
  mode: 'development',
  entry: {
    shared: ['bootstrap'],
    predhinata: {
      import: ['./js/index.js', './scss/index.scss'],
      dependOn: 'shared',
    },
  },
  output: {
    path: path.resolve(__dirname, 'static', 'js'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [
          path.resolve(__dirname, 'node_modules'),
        ],
      },
      {
        test: /\.(scss)$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
    ],
  },
  plugins: [miniCssExtractPlugin],
};
