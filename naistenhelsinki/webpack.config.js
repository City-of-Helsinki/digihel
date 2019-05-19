const path = require('path');

module.exports = {
  entry: path.join(__dirname, '/static_src/js/naistenhelsinki/index.js'),
  output: {
    path: path.join(__dirname, '/static/js/'),
    filename: 'naistenhelsinki.js'
  },
  module: {
    loaders: [
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/ }
    ]
  }
};
