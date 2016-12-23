var gulp = require('gulp');
var spritesmith = require('gulp.spritesmith');

gulp.task('sprite', function (cb) {
  var tasksDone = 0;

  var finished = function(){
      tasksDone++;
      if (tasksDone === 2) {
          cb();
      }
  }

  // Generate our spritesheet
  var spriteData = gulp.src('src/sprite/*.png').pipe(spritesmith({
    imgName: 'sprite.png',
    cssName: 'sprite.css',
    imgPath: '/img/sprite.png'
  }));

  // Pipe image stream through image optimizer and onto disk
  var imgStream = spriteData.img
    // DEV: We must buffer our stream into a Buffer for `imagemin`
    .pipe(gulp.dest('staging/img/'))
    .on('end', finished);

  // Pipe CSS stream through CSS optimizer and onto disk
  var cssStream = spriteData.css
    .pipe(gulp.dest('dist/css/'))
    .on('end', finished);

});