var gulp = require('gulp');
var concat = require('gulp-concat');
var jshint = require('gulp-jshint');
var uglify = require('gulp-uglify');

gulp.task('scripts', function() {
    return gulp.src([
    'node_modules/photoswipe/dist/photoswipe.js', 
    'node_modules/photoswipe/dist/photoswipe-ui-default.js',
    'node_modules/masonry-layout/dist/masonry.pkgd.js',
    'node_modules/imagesloaded/imagesloaded.pkgd.js',
    'src/scripts/*.js'])  //TODO Move to require file
        .pipe(concat('main.js'))
        .pipe(jshint())
        .pipe(jshint.reporter("default"))   
        .pipe(uglify())
        .pipe(gulp.dest('staging/js'));
});
