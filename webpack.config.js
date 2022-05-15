const path = require('path');
const autoprefixer = require('autoprefixer');

function tryResolve_(url, sourceFilename) {
  // Put require.resolve in a try/catch to avoid node-sass failing with cryptic libsass errors
  // when the importer throws
  try {
    return require.resolve(url, {paths: [path.dirname(sourceFilename)]});
  } catch (e) {
    return '';
  }
}

function tryResolveScss(url, sourceFilename) {
  // Support omission of .scss and leading _
  const normalizedUrl = url.endsWith('.scss') ? url : `${url}.scss`;
  return tryResolve_(normalizedUrl, sourceFilename) ||
    tryResolve_(path.join(path.dirname(normalizedUrl), `_${path.basename(normalizedUrl)}`),
      sourceFilename);
}

function materialImporter(url, prev) {
  if (url.startsWith('@material')) {
    const resolved = tryResolveScss(url, prev);
    return {file: resolved || url};
  }
  return {file: url};
}

var config = {
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: 'css/[name].css',
            },
          },
          {loader: 'extract-loader'},
          {loader: 'css-loader'},
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  autoprefixer()
                ]
              }
            } 
          },
          {
             loader: 'sass-loader',
             options: {   
               // Prefer Dart Sass
               implementation: require('sass'),

               // See https://github.com/webpack-contrib/sass-loader/issues/804
               webpackImporter: false,
               sassOptions: {
                 importer: materialImporter,
                 includePaths: ['./node_modules'],
               },
             },
           }
        ],
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env'],
        },
      }
    ],
  },
};

var baseConfig = Object.assign({}, config, {
    name: "base",
    entry: ["./catering_service/static/catering_service/css/base.scss", "./catering_service/static/catering_service/js/base.js"],
    output: {
       filename: "js/base.js",
       path: path.resolve(__dirname, './assets/catering_service'),
    },    
});

var layout1Config = Object.assign({}, config, {
    name: "layout_1",
    entry: ["./catering_service/static/catering_service/css/layout_1.scss", "./catering_service/static/catering_service/js/layout_1.js"],
    output: {
       filename: "js/layout_1.js",
       path: path.resolve(__dirname, './assets/catering_service'),
    },
});

var layout2Config = Object.assign({}, config, {
    name: "layout_2",
    entry: ["./catering_service/static/catering_service/css/layout_2.scss", "./catering_service/static/catering_service/js/layout_2.js"],
    output: {
       filename: "js/layout_2.js",
       path: path.resolve(__dirname, './assets/catering_service'),
    },
});


var authAppConfig = Object.assign({}, config, {
    name: "auth_app",
    entry: ["./auth_app/static/auth_app/css/auth_app.css", "./auth_app/static/auth_app/js/auth_app.js"],
    output: {
       filename: "js/auth_app.js",
       path: path.resolve(__dirname, './assets/auth_app'),
    },
});

var menuConfig = Object.assign({}, config, {
    name: "menu",
    entry: [
              "./src/static/src/css/menu.css", 
              "./src/static/src/js/menu.js", 
          ],
    output: {
       filename: "js/menu.js",
       path: path.resolve(__dirname, './assets/src'),
    },
});


module.exports = [
  baseConfig, layout1Config, layout2Config, authAppConfig, menuConfig,  
];