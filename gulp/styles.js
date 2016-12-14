var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var autoprefixer = require('gulp-autoprefixer');
var cleancss = require('gulp-clean-css');

gulp.task('styles', ['sprite'], function() {
    return gulp.src(['src/styles/*.scss', 'dist/css/sprite.css'])
        .pipe(sass())
        .pipe(autoprefixer('last 2 version'))
        .pipe(cleancss({advanced:false}))
        .pipe(concat('main.css'))
        .pipe(gulp.dest('staging/css'));
});
