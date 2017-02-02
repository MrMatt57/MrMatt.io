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
    'node_modules/prismjs/prism.js',
    'node_modules/prismjs/components/prism-bash.js',
    'node_modules/prismjs/components/prism-json.js',
    'node_modules/prismjs/components/prism-html.js',
    'node_modules/prismjs/components/prism-js.js',
    'node_modules/prismjs/components/prism-groovy.js',
    'src/scripts/*.js',
    'src/scripts/init/*.js'
    ])  //TODO Move to require file
        .pipe(concat('main.js'))
        .pipe(jshint.reporter("default"))   
        .pipe(uglify())
        .pipe(gulp.dest('staging/js'));
});
