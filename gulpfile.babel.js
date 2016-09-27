var gulp  = require('gulp')
var $     = require('gulp-load-plugins')()
var webpackstream = require('webpack-stream')

// will be true || false. Allow us to do "if (prod) {..}" when building
var prod = $.util.env.type == 'production';

var babelconfig = require('./webpack.config')

// html
gulp.task('html', () => {
    gulp.src(['./src/*.html'], { base: './src' })
    .pipe(gulp.dest('./static/'))
    .pipe($.connect.reload())
});

// stylus
gulp.task('css', () => {
    gulp.src(['src/css/*.styl'], { base: './src' })
    .pipe($.stylus({

      'include css': true,
      compress: true
    }))
    .pipe(gulp.dest('./static/'))
    .pipe($.connect.reload())
});

// js
gulp.task('js', () => {
     gulp.src(['src/js/**/*.js'], { base: 'src' })
    .pipe(webpackstream(babelconfig))
    .pipe(prod ? $.uglify() : $.util.noop())
    .pipe(gulp.dest('./static/js'))
    .pipe($.connect.reload())
})



// assets
gulp.task('assets', () => {
  return gulp.src(['src/assets/**/*.*'], { base: 'src' })
    .pipe($.cache($.imagemin({
      optimizationLevel: 3,
      progressive: true,
      interlaced: true
    })))
    .pipe(gulp.dest('static'))
    .pipe($.connect.reload())
});

// connect localserver
gulp.task('connect', () => {
  $.connect.server({
    root: 'static',
    port: 9000,
    livereload: true
  })
});

// watch
gulp.task('watch', ['connect'], () => {

  // watch html files
  gulp.watch('src/*.html', ['html']);

  // watch .styl files
  gulp.watch('src/css/*', ['css']);

  // watch .js files
  gulp.watch('src/js/**/*.js', ['js']);

  // watch image files
  gulp.watch('src/assets/**/*.*', ['assets']);

});


// for dev - just run 'gulp'
gulp.task('default', ['connect', 'watch'])

// for distribution. call with gulp build --type production
// but really, you should be doing $ npm run build
gulp.task('build', ['js', 'css', 'html', 'assets'])