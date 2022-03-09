(function(){/*! modernizr 3.6.0 (Custom Build) | MIT *
 * https://modernizr.com/download/?-webp-setclasses !*/
!function(e,n,A){function o(e,n){return typeof e===n}
function t(){var e,n,A,t,a,i,l;for(var f in r)
if(r.hasOwnProperty(f)){if(e=[],n=r[f],n.name&&(e.push(n.name.toLowerCase()),n.options&&n.options.aliases&&n.options.aliases.length))
for(A=0;A<n.options.aliases.length;A++)e.push(n.options.aliases[A].toLowerCase());for(t=o(n.fn,"function")?n.fn():n.fn,a=0;a<e.length;a++)i=e[a],l=i.split("."),1===l.length?Modernizr[l[0]]=t:(!Modernizr[l[0]]||Modernizr[l[0]]instanceof Boolean||(Modernizr[l[0]]=new Boolean(Modernizr[l[0]])),Modernizr[l[0]][l[1]]=t),s.push((t?"":"no-")+l.join("-"))}}
function a(e){var n=u.className,A=Modernizr._config.classPrefix||"";if(c&&(n=n.baseVal),Modernizr._config.enableJSClass){var o=new RegExp("(^|\\s)"+A+"no-js(\\s|$)");n=n.replace(o,"$1"+A+"js$2")}
Modernizr._config.enableClasses&&(n+=" "+A+e.join(" "+A),c?u.className.baseVal=n:u.className=n)}
function i(e,n){if("object"==typeof e)
for(var A in e)f(e,A)&&i(A,e[A]);else{e=e.toLowerCase();var o=e.split("."),t=Modernizr[o[0]];if(2==o.length&&(t=t[o[1]]),"undefined"!=typeof t)return Modernizr;n="function"==typeof n?n():n,1==o.length?Modernizr[o[0]]=n:(!Modernizr[o[0]]||Modernizr[o[0]]instanceof Boolean||(Modernizr[o[0]]=new Boolean(Modernizr[o[0]])),Modernizr[o[0]][o[1]]=n),a([(n&&0!=n?"":"no-")+o.join("-")]),Modernizr._trigger(e,n)}
return Modernizr}
var s=[],r=[],l={_version:"3.6.0",_config:{classPrefix:"",enableClasses:!0,enableJSClass:!0,usePrefixes:!0},_q:[],on:function(e,n){var A=this;setTimeout(function(){n(A[e])},0)},addTest:function(e,n,A){r.push({name:e,fn:n,options:A})},addAsyncTest:function(e){r.push({name:null,fn:e})}},Modernizr=function(){};Modernizr.prototype=l,Modernizr=new Modernizr;var f,u=n.documentElement,c="svg"===u.nodeName.toLowerCase();!function(){var e={}.hasOwnProperty;f=o(e,"undefined")||o(e.call,"undefined")?function(e,n){return n in e&&o(e.constructor.prototype[n],"undefined")}:function(n,A){return e.call(n,A)}}(),l._l={},l.on=function(e,n){this._l[e]||(this._l[e]=[]),this._l[e].push(n),Modernizr.hasOwnProperty(e)&&setTimeout(function(){Modernizr._trigger(e,Modernizr[e])},0)},l._trigger=function(e,n){if(this._l[e]){var A=this._l[e];setTimeout(function(){var e,o;for(e=0;e<A.length;e++)(o=A[e])(n)},0),delete this._l[e]}},Modernizr._q.push(function(){l.addTest=i}),Modernizr.addAsyncTest(function(){function e(e,n,A){function o(n){var o=n&&"load"===n.type?1==t.width:!1,a="webp"===e;i(e,a&&o?new Boolean(o):o),A&&A(n)}
var t=new Image;t.onerror=o,t.onload=o,t.src=n}
var n=[{uri:"data:image/webp;base64,UklGRiQAAABXRUJQVlA4IBgAAAAwAQCdASoBAAEAAwA0JaQAA3AA/vuUAAA=",name:"webp"},{uri:"data:image/webp;base64,UklGRkoAAABXRUJQVlA4WAoAAAAQAAAAAAAAAAAAQUxQSAwAAAABBxAR/Q9ERP8DAABWUDggGAAAADABAJ0BKgEAAQADADQlpAADcAD++/1QAA==",name:"webp.alpha"},{uri:"data:image/webp;base64,UklGRlIAAABXRUJQVlA4WAoAAAASAAAAAAAAAAAAQU5JTQYAAAD/////AABBTk1GJgAAAAAAAAAAAAAAAAAAAGQAAABWUDhMDQAAAC8AAAAQBxAREYiI/gcA",name:"webp.animation"},{uri:"data:image/webp;base64,UklGRh4AAABXRUJQVlA4TBEAAAAvAAAAAAfQ//73v/+BiOh/AAA=",name:"webp.lossless"}],A=n.shift();e(A.name,A.uri,function(A){if(A&&"load"===A.type)
for(var o=0;o<n.length;o++)e(n[o].name,n[o].uri)})}),t(),a(s),delete l.addTest,delete l.addAsyncTest;for(var p=0;p<Modernizr._q.length;p++)Modernizr._q[p]();e.Modernizr=Modernizr}(window,document);function IsImageOk(img,loadingImage){if(img.src==loadingImage)
{return false;}
if(!img.complete){return false;}
else
{return true;}
if(img.naturalWidth===0){return false;}
return false;}
var Singleton=(function(){function Singleton(rand){var list=document.querySelector('.carousel-inner'),i;if(rand)
{if(list.children.length)
{for(i=list.children.length;i>=0;i--){list.appendChild(list.children[Math.random()*i|0]);}}}
this.nodeList=list.children;}
Singleton.prototype.nodeList={};var instance;return{getInstance:function(rand){if(null==instance){instance=new Singleton(rand);instance.constructor=null;}
return instance;}};})();$(window).on('load',function(){const imgElements=document.querySelectorAll('.carousel-image');const ieLength=imgElements.length;if(ieLength)
{const nextIndicator=document.querySelector('.carousel-control-next');const prevIndicator=document.querySelector('.carousel-control-prev');const dataEl=document.getElementById('hidden-data');const offset=dataEl.dataset.offset=='False'?false:true;const randomizeImages=dataEl.dataset.randomizeImages=='True'?true:false;const loadingImage=location.protocol+"//"+location.host+dataEl.dataset.loadingImage;var carouselEl=document.querySelector('#carousel-large-background');let carousel=bootstrap.Carousel.getInstance(carouselEl);var nodes=Singleton.getInstance(randomizeImages).nodeList;const callback=function(changes,observer)
{changes.forEach(change=>{carousel.pause()
if(change.attributeName=='src'){observer.disconnect();if(change.target.src==loadingImage)
{observer.observe(change.target,{attributes:true});}
else
{carousel.cycle();}}});};const observer=new MutationObserver(callback)
carousel._items=nodes;firstActiveImg=carousel._items[0].children[0];if(firstActiveImg)
{firstActiveImg.parentElement.classList.add('active');}
if(offset)
{firstActiveImg.src=firstActiveImg.dataset.imageSrc;}
carousel.pause();if(IsImageOk(firstActiveImg,loadingImage))
{carousel.cycle();}
else
{config={attributes:true};observer.observe(firstActiveImg,config);}}});$(document).ready(function(){const dataEl=document.getElementById('hidden-data');const randomizeImages=dataEl.dataset.randomizeImages=='True'?true:false;const nodes=Singleton.getInstance(randomizeImages).nodeList;if(nodes.length)
{const useCache=dataEl.dataset.useCache=='True'?true:false;const imagesPerRequest=parseInt(dataEl.dataset.imagesPerRequest);const imageSizeLarge=dataEl.dataset.imageSizeLarge;const imageSizeSmall=dataEl.dataset.imageSizeSmall;const screenSize=window.innerWidth<500?imageSizeSmall:imageSizeLarge;const siteUrl=location.protocol+"//"+location.host+"/imgurl/";const csrftoken=document.querySelector('[name=csrfmiddlewaretoken]').value;const ImageLoaderWorker=new Worker('/static/django_bs_carousel/js/il_min.js',{'type':'classic','credentials':'same-origin'});var iteration=0;const webpSupport=Modernizr.webp;let closing=false;function closingCode(){closing==true;ImageLoaderWorker.terminate();return null;}
window.onbeforeunload=closingCode;function pm(){if(!closing)
{let start=iteration*imagesPerRequest;let finish=iteration*imagesPerRequest+imagesPerRequest;if(useCache)
{pks=[];indexes=[];idx=0;for(i of Array.prototype.slice.call(nodes,start,finish))
{indexes.push(start+idx)
pks.push(parseInt(i.children[0].id));idx++;}
ImageLoaderWorker.postMessage({'pks':pks,'iteration':iteration,'indexes':indexes,'useCache':useCache,'webpSupport':webpSupport,'screenSize':screenSize,'requestUrl':siteUrl,'token':csrftoken,'randomizeImages':randomizeImages,});}
else
{let urls=[];var index=start;for(i of Array.prototype.slice.call(nodes,start,finish))
{urls.push({'id':index,'url':i.children[0].dataset.imageSrc});index++;}
ImageLoaderWorker.postMessage({'urls':urls,'useCache':useCache,'webpSupport':webpSupport,'screenSize':screenSize,'requestUrl':siteUrl,'token':csrftoken,});}}}
let hid=false;ImageLoaderWorker.addEventListener('message',event=>{const imageData=event.data;const ids=imageData.ids;const abs=imageData.abs;ids.forEach((id,idx)=>{var mimestring=useCache&&webpSupport?"image/webp":"image/jpeg";var blob=new Blob([abs[idx]],{type:mimestring});var imageElement=nodes[id].children[0];var objectURL=URL.createObjectURL(blob);if(imageElement)
{imageElement.onload=()=>{URL.revokeObjectURL(objectURL);}
imageElement.removeAttribute('data-image-src');imageElement.setAttribute('size',screenSize);imageElement.setAttribute('src',objectURL);}})
if(iteration<nodes.length/imagesPerRequest)
{if(!document.hidden&&window.location.pathname=='/')
{pm();iteration++;}
else
{hid=true;}}})
pm();iteration++;document.addEventListener('visibilitychange',function(event){if(!document.hidden){if(window.location.pathname=='/'&&hid)
{hid=false;pm();iteration++;}}});}});}).call(this);