var gulp = require('gulp');
var connect = require('gulp-connect');
var riot = require('gulp-riot');

gulp.task('webserver', function() {
  connect.server({
    root: 'src'
  });
});

gulp.task('default', ['webserver']);
