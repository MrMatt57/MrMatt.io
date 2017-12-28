var images = document.querySelectorAll('.galleryimage');
if (images.length > 0) {
    initPhotoSwipeFromDOM('.gallery');
    var elem = document.querySelector('.gallery');
    imagesLoaded(images, function() {
        var colwidth = Number(elem.dataset.colwidth);
        var msnry = new Masonry(elem, {
            // options
            itemSelector: '.grid-item',
            columnWidth: colwidth
        });
    });
}
TableOfContents();