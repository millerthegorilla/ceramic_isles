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
    Singleton.prototype.prevIndex = function () {
        if(this.currentImageIndex == 0)
        {
            return this._eli[this._eli.length - 1];
        }
        else
        {
            return this._eli[this.currentImageIndex - 1];
        }
    }
    Singleton.prototype.nextIndex = function () {
        if(this.currentImageIndex == this._eli.length - 1)
        {
            return this._eli[0];
        }
        else
        {
            return this._eli[this.currentImageIndex + 1];
        }
    }
    Singleton.prototype.currIndex = function() {
        return this._eli[this.currentImageIndex];
    }
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
    const imgElements = document.querySelectorAll('.carousel-image');
    const ieLength = imgElements.length;
    if(ieLength)
    {
        const nextIndicator = document.querySelector('.carousel-control-next');
        const prevIndicator = document.querySelector('.carousel-control-prev');
        const dataEl = document.getElementById('hidden-data');
        const imgPause = parseInt(dataEl.dataset.imgPause);
        const offset = dataEl.dataset.offset == 'False' ? false : true;
        const randomizeImages = dataEl.dataset.randomizeImages == 'False' ? false : true;
        const loadingImage = location.protocol + "//" + location.host + dataEl.dataset.loadingImage;
        var carouselEl = document.querySelector('#carousel-large-background');
        let carousel = bootstrap.Carousel.getInstance(carouselEl);
        var elIndexes = Singleton.getInstance(randomizeImages, ieLength, imgElements);
        var elIter = elIndexes._nextELIndex(); 
        var firstImgInd = elIter.next();
        var firstActiveImg;
        var tohandle = 0;

        function slide(i) {
            clearTimeout(tohandle);
            tohandle=undefined;
            carousel.to(i);
            carousel.pause();
        }

        // handles first image.
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
                            elIter = elIndexes._nextELIndex();
                            nextImgInd = elIter.next();
                        }
                        tohandle = setTimeout(slide, imgPause, nextImgInd.value);
                    }
                }
            });
        };
        const observer = new MutationObserver(callback)

        // const callback2 = function(changes, observer)
        // { 
        //     changes.forEach(change => { 
        //         if(change.attributeName == 'class')
        //         {
        //             if(manualMove)
        //             {
        //                 if(change.target.classList.contains('active'))
        //                 {
        //                     if(change.target.classList.contains('carousel-item-next') || change.target.classList.contains('carousel-item-prev') || imgElements[elIndexes.curr()].parentElement != change.target)
        //                     {
        //                         clearTimeout(tohandle);
        //                         change.target.classList.remove('active');
        //                         imgElements[elIndexes.curr()].parentElement.classList.add('active');
        //                         setIndicators();
        //                     }
        //                 }
        //                 manualMove = false;
        //             }
        //         }
        //     });
        // };
        // const observer2 = new MutationObserver(callback2);
        // const root = document.querySelector('.carousel-inner');
        // observer2.observe(root, {
        //     subtree: true,
        //     attributes: true
        // }); 
        function setIndicators()
        {
            nextIndicator.setAttribute('data-bs-slide-to', elIndexes.nextIndex());
            var cn = document.querySelector('.carousel-item-next');
            if (cn)
            {
                cn.classList.remove('carousel-item-next');
            }
            imgElements[elIndexes.nextIndex()].parentElement.classList.add('carousel-item-next');
            prevIndicator.setAttribute('data-bs-slide-to', elIndexes.prevIndex());
            var cp = document.querySelector('.carousel-item-prev');
            if(cp)
            {
                cp.classList.remove('carousel-item-prev');
            }
            imgElements[elIndexes.prevIndex()].parentElement.classList.add('carousel-item-prev');
        }

        function manualMove(e) 
        { 
            console.log(tohandle);
            clearTimeout(tohandle);
            tohandle = undefined;
            e.preventDefault();
            e.stopPropagation();
            // have to move twice to take care of the unremoveable bootstrap click handler
            if(event.target.classList[0].includes('prev'))
            {
                slide(elIndexes.getEli()[elIndexes.currentImageIndex - 2]);
            }
            else
            {
                slide(elIndexes.getEli()[elIndexes.currentImageIndex]);
            }
            setIndicators();
        }

        
        document.querySelector('span.carousel-control-prev-icon').addEventListener('click', manualMove, true)
        document.querySelector('span.carousel-control-next-icon').addEventListener('click', manualMove, true)

        function slidListener(e) {
            setIndicators();
            carousel.pause();
            var nextImgInd = elIter.next()
            if(nextImgInd.done)
            {
                elIter = elIndexes._nextELIndex();
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
                   tohandle = setTimeout(slide, imgPause, elIndexes._eli[elIndexes.currentImageIndex]);
                }
                else
                {
                    tohandle = setTimeout(slide, imgPause, nextImgInd.value);
                }
            }
        };

        carouselEl.addEventListener('slid.bs.carousel', slidListener);
  
        firstActiveImg = imgElements[firstImgInd.value];
        if(firstActiveImg)
        {
            firstActiveImg.parentElement.classList.add('active');
        }
        else
        {
            firstActiveImg = imgElements[elIndexes.currIndex()];
            firstActiveImg.parentElement.classList.add('active');
        }
        if(offset)
        {
            firstActiveImg.src = firstActiveImg.dataset.imageSrc;
        }
        carousel.pause();
        
        setIndicators();

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
        // if randomizeImages - turn off touch swiping.
        const elIndexes = Singleton.getInstance(randomizeImages, ieLength, imgElements);
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
                    elis = elIndexes.getEli().slice(start, finish);
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
                    for (i of elIndexes.getEli().slice(start, finish))
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