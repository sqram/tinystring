import webpack from 'webpack'


module.exports = {
  entry: './src/js/index.js',
  output: {

    filename: "bundle.js"
  },

  plugins: ([
    //new webpack.optimize.CommonsChunkPlugin("common", "common.bundle.js"),
    new webpack.optimize.DedupePlugin(),
    //new webpack.optimize.UglifyJsPlugin({sourceMap: false, mangle: true})
  ]),

  module: {
    loaders: [
      {
        test: /\.js?$/,
        exclude: /vendor|node_modules/,
        loader: 'babel'
      }
    ]
  }

}