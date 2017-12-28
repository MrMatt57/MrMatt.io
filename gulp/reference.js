var gulp = require("gulp");
var replace = require("gulp-rev-replace");
var size = require('gulp-size');

gulp.task('reference:content', ['hugo:draft'], function() {
    var manifest = gulp.src('public/rev-manifest.json');

    return gulp.src(['public/**/*.html', 'public/**/*.xml', 'public/**/*.css'])
        .pipe(replace({manifest: manifest}))
        .pipe(size())
        .pipe(gulp.dest('public'));
});

var referenceTask = function(taskName, hugoTask){
    gulp.task(taskName, [hugoTask], function() {
        var manifest = gulp.src('public/rev-manifest.json');
    
        return gulp.src(['public/**/*.html', 'public/**/*.xml', 'public/**/*.css'])
            .pipe(replace({manifest: manifest, replaceInExtensions: ['.html', '.xml', '.css']}))
            .pipe(size())
            .pipe(gulp.dest('public'));
    });
}

referenceTask('reference:all', 'hugo:all');
referenceTask('reference:publish', 'hugo:live');