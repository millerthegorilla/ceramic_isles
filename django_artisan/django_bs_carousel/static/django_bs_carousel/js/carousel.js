/*! modernizr 3.6.0 (Custom Build) | MIT *
 * https://modernizr.com/download/?-webp-setclasses !*/
! function(e, n, A) {
    function o(e, n) {
        return typeof e === n
    }

    function t() {
        var e, n, A, t, a, i, l;
        for (var f in r)
            if (r.hasOwnProperty(f)) {
                if (e = [], n = r[f], n.name && (e.push(n.name.toLowerCase()), n.options && n.options.aliases && n.options.aliases.length))
                    for (A = 0; A < n.options.aliases.length; A++) e.push(n.options.aliases[A].toLowerCase());
                for (t = o(n.fn, "function") ? n.fn() : n.fn, a = 0; a < e.length; a++) i = e[a], l = i.split("."), 1 === l.length ? Modernizr[l[0]] = t : (!Modernizr[l[0]] || Modernizr[l[0]] instanceof Boolean || (Modernizr[l[0]] = new Boolean(Modernizr[l[0]])), Modernizr[l[0]][l[1]] = t), s.push((t ? "" : "no-") + l.join("-"))
            }
    }

    function a(e) {
        var n = u.className,
            A = Modernizr._config.classPrefix || "";
        if (c && (n = n.baseVal), Modernizr._config.enableJSClass) {
            var o = new RegExp("(^|\\s)" + A + "no-js(\\s|$)");
            n = n.replace(o, "$1" + A + "js$2")
        }
        Modernizr._config.enableClasses && (n += " " + A + e.join(" " + A), c ? u.className.baseVal = n : u.className = n)
    }

    function i(e, n) {
        if ("object" == typeof e)
            for (var A in e) f(e, A) && i(A, e[A]);
        else {
            e = e.toLowerCase();
            var o = e.split("."),
                t = Modernizr[o[0]];
            if (2 == o.length && (t = t[o[1]]), "undefined" != typeof t) return Modernizr;
            n = "function" == typeof n ? n() : n, 1 == o.length ? Modernizr[o[0]] = n : (!Modernizr[o[0]] || Modernizr[o[0]] instanceof Boolean || (Modernizr[o[0]] = new Boolean(Modernizr[o[0]])), Modernizr[o[0]][o[1]] = n), a([(n && 0 != n ? "" : "no-") + o.join("-")]), Modernizr._trigger(e, n)
        }
        return Modernizr
    }
    var s = [],
        r = [],
        l = {
            _version: "3.6.0",
            _config: {
                classPrefix: "",
                enableClasses: !0,
                enableJSClass: !0,
                usePrefixes: !0
            },
            _q: [],
            on: function(e, n) {
                var A = this;
                setTimeout(function() {
                    n(A[e])
                }, 0)
            },
            addTest: function(e, n, A) {
                r.push({
                    name: e,
                    fn: n,
                    options: A
                })
            },
            addAsyncTest: function(e) {
                r.push({
                    name: null,
                    fn: e
                })
            }
        },
        Modernizr = function() {};
    Modernizr.prototype = l, Modernizr = new Modernizr;
    var f, u = n.documentElement,
        c = "svg" === u.nodeName.toLowerCase();
    ! function() {
        var e = {}.hasOwnProperty;
        f = o(e, "undefined") || o(e.call, "undefined") ? function(e, n) {
            return n in e && o(e.constructor.prototype[n], "undefined")
        } : function(n, A) {
            return e.call(n, A)
        }
    }(), l._l = {}, l.on = function(e, n) {
        this._l[e] || (this._l[e] = []), this._l[e].push(n), Modernizr.hasOwnProperty(e) && setTimeout(function() {
            Modernizr._trigger(e, Modernizr[e])
        }, 0)
    }, l._trigger = function(e, n) {
        if (this._l[e]) {
            var A = this._l[e];
            setTimeout(function() {
                var e, o;
                for (e = 0; e < A.length; e++)(o = A[e])(n)
            }, 0), delete this._l[e]
        }
    }, Modernizr._q.push(function() {
        l.addTest = i
    }), Modernizr.addAsyncTest(function() {
        function e(e, n, A) {
            function o(n) {
                var o = n && "load" === n.type ? 1 == t.width : !1,
                    a = "webp" === e;
                i(e, a && o ? new Boolean(o) : o), A && A(n)
            }
            var t = new Image;
            t.onerror = o, t.onload = o, t.src = n
        }
        var n = [{
                uri: "data:image/webp;base64,UklGRiQAAABXRUJQVlA4IBgAAAAwAQCdASoBAAEAAwA0JaQAA3AA/vuUAAA=",
                name: "webp"
            }, {
                uri: "data:image/webp;base64,UklGRkoAAABXRUJQVlA4WAoAAAAQAAAAAAAAAAAAQUxQSAwAAAABBxAR/Q9ERP8DAABWUDggGAAAADABAJ0BKgEAAQADADQlpAADcAD++/1QAA==",
                name: "webp.alpha"
            }, {
                uri: "data:image/webp;base64,UklGRlIAAABXRUJQVlA4WAoAAAASAAAAAAAAAAAAQU5JTQYAAAD/////AABBTk1GJgAAAAAAAAAAAAAAAAAAAGQAAABWUDhMDQAAAC8AAAAQBxAREYiI/gcA",
                name: "webp.animation"
            }, {
                uri: "data:image/webp;base64,UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=",
                name: "webp.lossless"
            }],
            A = n.shift();
        e(A.name, A.uri, function(A) {
            if (A && "load" === A.type)
                for (var o = 0; o < n.length; o++) e(n[o].name, n[o].uri)
        })
    }), t(), a(s), delete l.addTest, delete l.addAsyncTest;
    for (var p = 0; p < Modernizr._q.length; p++) Modernizr._q[p]();
    e.Modernizr = Modernizr
}(window, document);

// https://stackoverflow.com/questions/1977871/check-if-an-image-is-loaded-no-errors-with-jquery
function IsImageOk(img, loadingImage) {
    if (img.src == loadingImage)
    {
        return false;
    }
    // During the onload event, IE correctly identifies any images that
    // weren’t downloaded as not complete. Others should too. Gecko-based
    // browsers act like NS4 in that they report this incorrectly.
    if (!img.complete) {
        return false;
    }
    else
    {
        return true;
    }

    // However, they do have two very useful properties: naturalWidth and
    // naturalHeight. These give the true size of the image. If it failed
    // to load, either of these should be zero.
    if (img.naturalWidth === 0) {
        return false;
    }

    // No other way of checking: assume it’s not ok.
    return false;
}

function fisherYatesShuffle(arr){
    for(var i =arr.length-1 ; i>0 ;i--){
        var j = Math.floor( Math.random() * (i + 1) ); //random index
        [arr[i],arr[j]]=[arr[j],arr[i]]; // swap
    }
}

var Singleton = (function(){
    function Singleton(rand, ieLength) {
        this._eli = [];
        if(ieLength)
        {
            for (var i=0;i<ieLength;++i) this._eli[i]=i;
            if(rand)    
            {
                fisherYatesShuffle(this._eli); 
            }
        }
    }
    Singleton.prototype.getEli = function()
    {
        return this._eli;
    }
    Singleton.prototype._eli = [];
    Singleton.prototype.currentImageIndex = 0;
    Singleton.prototype._nextELIndex = function* () 
    { 
        this.currentImageIndex = 0; 
        while (this.currentImageIndex < this._eli.length)
        {
            yield this._eli[this.currentImageIndex];
            this.currentImageIndex++;
        }
    }
    // Singleton.prototype.nextImageIndex = (that, eln, elp) => { 
    //     that.currentImageIndex = that.currentImageIndex++ % that._eli.length; return that._eli[that._eli.findIndex((el) => el==that.currentImageIndex)]; 
    // }
    // Singleton.prototype.prevImageIndex = (that, eln, elp) => { 
    //     that.currentImageIndex = that.currentImageIndex-- < 0 ? that._eli.length - 1 : that.currentImageIndex; return that._eli[that._eli.findIndex((el) => el==that.currentImageIndex)]; 
    // }
    var instance;
    return {
        getInstance: function(rand, ieLength){
            if (null == instance) {
                instance = new Singleton(rand, ieLength);               
                instance.constructor = null; // Note how the constructor is hidden to prevent instantiation
            }
            return instance; //return the singleton instance
        }
   };
})();

$(window).on('load', function() {

    //$(document).off('bs.carousel.data-api');
    
    // function nexti () { 
    //     console.log('next');
    //     //clearTimeout(tohandle); tohandle=undefined; carousel.to(elInds.nextImageIndex(elInds)); carousel.cycle(); carousel.pause(); 
    // };
    // function previ(e) {
    //     return e.preventDefault();
    //     //clearTimeout(tohandle); tohandle=undefined; carousel.to(elInds.prevImageIndex(elInds)); carousel.cycle(); carousel.pause(); 
    // };
    // const prevBtn = document.querySelector('.carousel-control-prev');

    // prevBtn.addEventListener('click', previ);
    const imgElements = document.querySelectorAll('.carousel-image');
    const ieLength = imgElements.length;
    if(ieLength)
    {
        const nextIndicator = document.querySelector('.carousel-control-next');
        nextIndicator.setAttribute('data-bs-slide', "");
        const prevIndicator = document.querySelector('.carousel-control-prev');
        prevIndicator.setAttribute('data-bs-slide', "");
        const dataEl = document.getElementById('hidden-data');
        const imgPause = parseInt(dataEl.dataset.imgPause);
        const loadingImage = location.protocol + "//" + location.host + dataEl.dataset.loadingImage;
        var myCarouselEl = document.querySelector('#carousel-large-background');
        let carousel = bootstrap.Carousel.getInstance(myCarouselEl);
        var elInds = Singleton.getInstance();
        var elIter = elInds._nextELIndex(); 
        var firstImgInd = elIter.next();
        var firstActiveImg = {}
        var tohandle = 0;

        function slide(i) {
            clearTimeout(tohandle);
            tohandle=undefined;
            carousel.to(i);
            carousel.pause();
            nextIndicator.setAttribute('data-bs-slide-to', elInds._eli[elInds.currentImageIndex + 1])
            prevIndicator.setAttribute('data-bs-slide-to', elInds._eli[elInds.currentImageIndex - 1])
        }

        const callback = function(changes, observer)
        {
            changes.forEach(change => {
                carousel.pause()
                if (change.attributeName == 'src') {
                    observer.disconnect();
                    if(change.target.src == loadingImage)
                    {
                        observer.observe(change.target, {
                            attributes: true
                        }); 
                    }
                    else
                    {
                        var nextImgInd = elIter.next();
                        if(nextImgInd.done)
                        {
                            elIter = elInds._nextELIndex();
                            nextImgInd = elIter.next();
                        }
                        tohandle = setTimeout(slide, imgPause, nextImgInd.value);
                    }
                }
            });
        };
        const observer = new MutationObserver(callback)

        function slidListener(e) {
            carousel.pause();
            var nextImgInd = elIter.next()
            console.log('269',nextImgInd.value);
            if(nextImgInd.done)
            {
                elIter = elInds._nextELIndex();
                nextImgInd = elIter.next()
            }
            var nextImg = imgElements[nextImgInd.value]
            if (nextImg.src == loadingImage)
            {
                config = { attributes: true }
                observer.disconnect()
                observer.observe(nextImg, config );
            }
            else
            {
                if(tohandle)
                {
                   clearTimeout(tohandle);
                   tohandle = setTimeout(slide, imgPause, elInds._eli[elInds.currentImage]);
                }
                else
                {
                    tohandle = setTimeout(slide, imgPause, nextImgInd.value);
                }
            }
        };

        myCarouselEl.addEventListener('slid.bs.carousel', slidListener);

        try
        {
            firstActiveImg = imgElements[firstImgInd.value];
            firstActiveImg.parentElement.classList.add('active');
            carousel.pause();
        }
        catch (err)
        {
            myCarouselEl.removeEventListener('slid.bs.carousel', slidListener);
            return;
        }

        if (IsImageOk(firstActiveImg, loadingImage))
        {
            //doesn't get here for the moment
            var nextImgInd = elIter.next();
            tohandle = setTimeout(slide, imgPause, nextImgInd.value);
        }
        else
        {   
            config = { attributes: true };
            observer.observe(firstActiveImg, config );
        }
    }
});

$(document).ready(function () {
    const imgElements = document.querySelectorAll('.carousel-image');
    const ieLength = imgElements.length;
    if(ieLength)
    {
        const dataEl = document.getElementById('hidden-data');
        const useCache = dataEl.dataset.useCache == 'False' ? false : true;
        const randomizeImages = dataEl.dataset.randomizeImages == 'False' ? false : true;
        const elInds = Singleton.getInstance(randomizeImages, ieLength, imgElements);
        const imagesPerRequest = parseInt(dataEl.dataset.imagesPerRequest);
        const imageSizeLarge = dataEl.dataset.imageSizeLarge;
        const imageSizeSmall = dataEl.dataset.imageSizeSmall;
        const screenSize = window.innerWidth < 500 ? imageSizeSmall : imageSizeLarge;
        const siteUrl = location.protocol + "//" + location.host + "/imgurl/";
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const ImageLoaderWorker = new Worker('/static/django_bs_carousel/js/il_min.js', {'type': 'classic', 'credentials': 'same-origin'});
        var iteration = 0;
        const webpSupport = Modernizr.webp;
        let closing = false;
        function closingCode(){
            closing == true;
            ImageLoaderWorker.terminate();
            return null;
        }
        window.onbeforeunload = closingCode;
        
        function pm() {
            if (!closing && ieLength > 0)
            {
                let start = iteration * imagesPerRequest;
                let finish = iteration * imagesPerRequest + imagesPerRequest;
                if(useCache)
                {
                    pks = [];
                    elis = elInds.getEli().slice(start, finish);
                    for(i of elis)
                    {
                        pks.push(parseInt(imgElements[i].id));
                    }
                    ImageLoaderWorker.postMessage({
                        'pks': pks,
                        'iteration': iteration,
                        'indexes': elis,
                        'useCache': useCache,
                        'webpSupport': webpSupport,
                        'screenSize': screenSize,
                        'requestUrl': siteUrl,
                        'token': csrftoken,
                        'randomizeImages': randomizeImages,
                    });
                }
                else
                {
                    let urls = [];
                    for (i of elInds.getEli().slice(start, finish))
                    {
                        urls.push({'id': i, 'url': imgElements[i].dataset.imageSrc});
                    }
                    ImageLoaderWorker.postMessage({
                       'urls': urls,
                       'useCache': useCache,
                       'webpSupport': webpSupport,
                       'screenSize': screenSize,
                       'requestUrl': siteUrl,
                       'token': csrftoken,
                   }); 
                }
            }
        }

        let hid = false;
        ImageLoaderWorker.addEventListener('message', event => {
            const imageData = event.data;
            const ids = imageData.ids;
            const abs = imageData.abs;
            ids.forEach((id,idx) =>{
                var mimestring = useCache && webpSupport ? "image/webp" : "image/jpeg";
                var blob = new Blob([abs[idx]], { type: mimestring });
                
                var imageElement = imgElements[id];
                var objectURL = URL.createObjectURL(blob);

                // Once the image is loaded, we'll want to do some extra cleanup
                if (imageElement)
                {
                  imageElement.onload = () => {
                    URL.revokeObjectURL(objectURL);
                  }
                  imageElement.removeAttribute('data-image-src');
                  imageElement.setAttribute('size', screenSize);
                  imageElement.setAttribute('src', objectURL);
                }
            }) 
            if(iteration < imgElements.length / imagesPerRequest)
            { 
                if(!document.hidden && window.location.pathname == '/')
                {
                    pm();
                    iteration++;
                }
                else
                {
                    hid = true;
                }
            }
        })

        pm();
        iteration++;

        document.addEventListener('visibilitychange', function (event) {
            if (!document.hidden) {
                if (window.location.pathname == '/' && hid)
                {
                    hid = false;
                    pm();
                    iteration++;
                }
            }
        });
    }
});