const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');

module.exports = {
  entry: path.resolve(__dirname, 'static/js/src/index.js'),
  devtool: 'source-map',
  devServer: {
    contentBase: path.resolve(__dirname, 'static/js/dist'),
    compress: true,
    hot: true
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        include: path.resolve(__dirname, 'static/js/src'),
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['env', 'react']
          }
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.json', '.jsx']
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Lol Kek Cheburek',
      hash: true,
      template: path.resolve(__dirname, 'static/js/src/index.html')
    }),
    new webpack.HotModuleReplacementPlugin()
  ],
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'static/js/dist')
  }
};