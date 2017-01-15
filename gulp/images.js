var gulp = require('gulp');
var imagemin = require('gulp-imagemin');
var changed = require('gulp-changed');
var imageResize = require('gulp-image-resize');
var rename = require("gulp-rename");


gulp.task('images', ['images-optimize', 'images-thumbs', 'images-fullthumbs']);

gulp.task('images-optimize', function () {
  return gulp.src(['src/img/*.*', 'src/img/auto-thumb/*.*', 'src/img/auto-fullthumb/*.*'])
    .pipe(changed('staging/img'))
    .pipe(imagemin())
    .pipe(gulp.dest('staging/img'));
});

gulp.task('images-thumbs', function () {
  return gulp.src('src/img/auto-thumb/*.*')
    .pipe(changed('staging/img'))
    .pipe(imageResize({
      imageMagick: true,
      width : 350
    }))
    .pipe(rename(function (path) { path.basename += "-thumbnail"; }))
    .pipe(gulp.dest('staging/img'));
});


gulp.task('images-fullthumbs', function () {
  return gulp.src('src/img/auto-fullthumb/*.*')
    .pipe(changed('staging/img'))
    .pipe(imageResize({
      imageMagick: true,
      width : 720
    }))
    .pipe(rename(function (path) { path.basename += "-thumbnail"; }))
    .pipe(gulp.dest('staging/img'));
});

