(function (){
    if(!window.bookmarklet){
        bookmarlet_js = document.body.appendChild(document.createElement("script"));
        bookmarlet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*999999999);
        window.bookmarklet=true;
    }else {
        bookmarkletLaunch();
    }
})()