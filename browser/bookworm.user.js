// ==UserScript==
// @name        Bookworm
// @namespace   http://bookworm.oreilly.com/
// @description Pretiffies bookworm for my reading tastes
// @include     http://bookworm.oreilly.com/view/*
// ==/UserScript==

var remove = function() {
    for(var i = 0; i < arguments.length; i++) {
        var elem = document.getElementById(arguments[i]);
        elem.parentNode.removeChild(elem);
    }
};
remove('bw-header', 'bw-subheader', 'bw-upload-box', 'bw-shell-left');

var table = document.getElementById('bw-shell-table');
var content = document.getElementById('bw-shell-table-content');
var data = document.getElementById('bw-book-content');
var header = document.getElementsByTagName('h2')[0];
var ps = document.getElementsByTagName('p', content);
content.style.backgroundColor =
    table.style.backgroundColor =
    document.body.style.backgroundColor = '#343A3F';
header.style.color =
    content.style.color =
    table.style.color =
    document.body.style.color = '#D6DBDF';
header.fontSize = '36px';
header.fontWeight = 'bold';
header.style.fontFamily = "minion-pro-1, minion-pro-2, Palatino, Georgia, 'Times New Roman', serif";
data.style.fontSize = '22px';
data.style.lineHeight = '34px';
data.style.width = '900px';
data.style.margin = '0 auto';
for(var i = 0; i < ps.length; i++) {
    ps[i].style.fontFamily = "minion-pro-1, minion-pro-2, Palatino, Georgia, 'Times New Roman', serif";
}
