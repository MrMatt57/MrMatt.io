var gulp = require('gulp');

// PhotoSwipe Assets
gulp.task('photoswipe', function () {
  return gulp.src(['node_modules/photoswipe/src/css/default-skin/*.svg', 
  'node_modules/photoswipe/src/css/default-skin/*.png', 
  'node_modules/photoswipe/src/css/default-skin/*.gif']) // TODO move to config
    .pipe(gulp.dest('hugo/static/photoswipe'));
});
