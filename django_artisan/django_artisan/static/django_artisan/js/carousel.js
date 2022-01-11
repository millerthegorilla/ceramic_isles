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

$(document).ready(function() {
    const myCarouselEl = document.querySelector('#carousel-large-background')
    var carousel = new bootstrap.Carousel(myCarouselEl, {
        interval: false
    })
    offset = document.getElementById('lazyload_offset').getAttribute('data-offset')
    var img = document.querySelectorAll(".active")[0].parentElement.children[offset].children[0]
        //$($(".active").siblings()[offset]).children('img').get(0)
    observer = new MutationObserver((changes) => {
        changes.forEach(change => {
            if (change.attributeName.includes('src')) {
                var carousel = new bootstrap.Carousel(myCarouselEl, {
                    interval: 4200
                })
            }
        });
    });
    observer.observe(img, {
        attributes: true
    });
    // display image captions on rollover
    $(".carousel-item").hover(function() {
            $(".carousel-caption").hide();
            $(".carousel-caption").css('visibility', 'visible');
            $(".carousel-caption").stop().fadeIn(1000);
        },
        function() {
            $(".carousel-caption").stop().fadeOut(800, function() {
                $(".carousel-caption").css('visibility', 'hidden');
            });
        });

    const imgElements = document.querySelectorAll('.carousel-load');
    const ieLength = imgElements.length;
    const images_per_request = document.getElementById('images_per_request').getAttribute('data-images');
    const screen_size = window.innerWidth < 500 ? "400x500" : "1024x768";
    const siteurl = location.protocol + "//" + location.host + location.pathname + "imgurl/";
    console.log('siteurl = ' + siteurl)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const ImageLoaderWorker = new Worker('./static/django_artisan/js/image_loader_min.js');
    var iteration = 0;

    function pm() {
        ImageLoaderWorker.postMessage({
            'iteration': iteration,
            'images_per_request': images_per_request,
            'len_im_els': imgElements.length,
            'webp_support': Modernizr.webp,
            'screen_size': screen_size,
            'request_url': siteurl,
            'token': csrftoken,
        });
    }
    ImageLoaderWorker.addEventListener('message', event => {
        const imageData = event.data;
        // console.log(event.data.id)
        //console.log('#image-' + imageData.id);
        //console.log(`#image-${imageData.id}`)
        var imageElement = document.querySelectorAll("#image-" + String(imageData.id))[0];

        var objectURL = URL.createObjectURL(imageData.blob);

        // Once the image is loaded, we'll want to do some extra cleanup
        if (imageElement)
        {
          imageElement.onload = () => {
            URL.revokeObjectURL(objectURL);
          }
          imageElement.setAttribute('size', screen_size);
          imageElement.setAttribute('src', objectURL);
        }
        if (iteration < (ieLength/images_per_request))
        {
          pm();
          iteration++;
        }
    })

    pm();
    iteration++;
});