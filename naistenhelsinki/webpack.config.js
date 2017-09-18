const path = require('path');

module.exports = {
  entry: path.resolve(__dirname + '/static_src/js/Naistenhelsinki/index.js'),
  output: {
    path: path.resolve(__dirname + '/static/js/'),
    filename: 'naistenhelsinki.js'
  },
  module: {
    loaders: [
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/ }
    ]
  }
};
