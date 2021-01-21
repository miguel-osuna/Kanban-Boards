var { merge } = require("webpack-merge");
var webpack = require("webpack");
var CopyWebpackPlugin = require("copy-webpack-plugin");
var MiniCssExtractPlugin = require("mini-css-extract-plugin");
var OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
var TerserPlugin = require("terser-webpack-plugin");

var common = {
  watchOptions: {
    poll: (process.env.WEBPACK_WATCHER_POLL || "true") === "true",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [/node_modules/],
        loader: "babel-loader", // Transpiles ES6 Javascript
      },
      {
        test: [/\.scss$/, /\.css$/],
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "postcss-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        exclude: /fonts/,
        loader: "file-loader?name=/images/[name].[ext]",
      },
      {
        test: /\.(ttf|eot|svg|woff2?)$/,
        exclude: /images/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "fonts/",
              publicPath: "../fonts",
            },
          },
        ],
      },
    ],
  },
  optimization: {
    minimizer: [
      // This overwrites the default webpack minimizer configuration
      new TerserPlugin({ cache: true, parallel: true, sourceMap: false }), // Minifies and Uglifies Javascript
      new OptimizeCSSAssetsPlugin({}), // Minifies and Uglyfies CSS
    ],
  },
};

module.exports = [
  merge(common, {
    entry: [
      // Where to start bundling
      __dirname + "/app/app.scss",
      __dirname + "/app/app.js",
    ],
    output: {
      // Where to output
      path: __dirname + "/../public",
      filename: "js/app.js",
    },
    resolve: {
      modules: [
        // What directories should be searched when resolving modules
        "/node_modules",
        __dirname + "/app",
      ],
    },
    plugins: [
      // What extra processing to perform
      new CopyWebpackPlugin({ patterns: [{ from: __dirname + "/static" }] }),
      new MiniCssExtractPlugin({ filename: "css/app.css" }),
      new webpack.ProvidePlugin({ $: "jquery", jQuery: "jquery" }),
    ],
  }),
];
