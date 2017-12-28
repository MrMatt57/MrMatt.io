function TableOfContents() {
    if(document.querySelectorAll('#toc').length == 0){
        return;
    }
    var toc = "";
    var level = 2;
    var container = document.querySelector('#articlebody');
    var output = '#toc-content';
    container.innerHTML = container.innerHTML.replace(
        /<h([\d])(.*)>([^<]+)<\/h([\d])>/gi,
        function(str, openLevel, id, titleText, closeLevel) {
            if (openLevel != closeLevel) {
                return str;
            }
            if (openLevel > level) {
                toc += (new Array(openLevel - level + 1)).join('<ul>');
            } else if (openLevel < level) {
                toc += (new Array(level - openLevel + 1)).join('</li></ul>');
            } else {
                toc += (new Array(level + 1)).join('</li>');
            } 
            level = parseInt(openLevel);
            var anchor = titleText.replace(/ /g, "_");
            toc += '<li><a href="#' + anchor + '">' + titleText +
                '</a>';
            return '<h' + openLevel + '><a href="#' + anchor + '" id="' + anchor + '">' +
                titleText + '</a></h' + closeLevel + '>';
        }
    );
    if (level) {
        toc += (new Array(level + 1)).join('</ul>');
    }
    document.querySelector(output).innerHTML += toc;
};