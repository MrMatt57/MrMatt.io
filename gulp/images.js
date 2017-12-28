var gulp = require('gulp');
var imagemin = require('gulp-imagemin');
var changed = require('gulp-changed');
var imageResize = require('gulp-image-resize');
var rename = require("gulp-rename");

gulp.task('images', ['images-optimize', 'images-thumb', 'images-fullthumb']);

gulp.task('images-optimize', function () {
  return gulp.src(['src/img/*.*', 'src/img/auto-thumb/*.*', 'src/img/auto-fullthumb/*.*'])
    .pipe(changed('staging/img'))
    .pipe(imagemin())
    .pipe(gulp.dest('staging/img'));
});

var createThumbs = function(folder, size){
  gulp.task('images-' + folder, function () {
    return gulp.src('src/img/auto-' + folder + '/*.*')
      .pipe(changed('staging/img'))
      .pipe(imageResize({
        imageMagick: true,
        width : size
      }))
      .pipe(rename(function (path) { path.basename += "-thumbnail"; }))
      .pipe(gulp.dest('staging/img'));
  });
}

createThumbs('fullthumb', 720);
createThumbs('thumb', 350);
