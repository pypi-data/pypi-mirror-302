var _JUPYTERLAB;(()=>{"use strict";var e,r,t,n,a,o,i,l,u,s,f,d,p,c,h,v,b,m,y,g,w,j,S,P={13599:(e,r,t)=>{var n={"./index":()=>Promise.all([t.e(817),t.e(509)]).then((()=>()=>t(8509))),"./extension":()=>Promise.all([t.e(817),t.e(509)]).then((()=>()=>t(8509))),"./style":()=>t.e(453).then((()=>()=>t(13453)))},a=(e,r)=>(t.R=r,r=t.o(n,e)?n[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var n="default",a=t.S[n];if(a&&a!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[n]=e,t.I(n,r)}};t.d(r,{get:()=>a,init:()=>o})}},x={};function E(e){var r=x[e];if(void 0!==r)return r.exports;var t=x[e]={id:e,loaded:!1,exports:{}};return P[e].call(t.exports,t,t.exports,E),t.loaded=!0,t.exports}E.m=P,E.c=x,E.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return E.d(r,{a:r}),r},E.d=(e,r)=>{for(var t in r)E.o(r,t)&&!E.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},E.f={},E.e=e=>Promise.all(Object.keys(E.f).reduce(((r,t)=>(E.f[t](e,r),r)),[])),E.u=e=>e+"."+{21:"80e825aa14b99d697404",55:"035b008338325d248d04",276:"ac8a466837d94e99c546",453:"f9800155d31a74a4f9d0",509:"daa2f9081b7edde12636",817:"2a61db930a6d6fe919d8"}[e]+".js?v="+{21:"80e825aa14b99d697404",55:"035b008338325d248d04",276:"ac8a466837d94e99c546",453:"f9800155d31a74a4f9d0",509:"daa2f9081b7edde12636",817:"2a61db930a6d6fe919d8"}[e],E.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),E.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@elyra/theme-extension:",E.l=(t,n,a,o)=>{if(e[t])e[t].push(n);else{var i,l;if(void 0!==a)for(var u=document.getElementsByTagName("script"),s=0;s<u.length;s++){var f=u[s];if(f.getAttribute("src")==t||f.getAttribute("data-webpack")==r+a){i=f;break}}i||(l=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,E.nc&&i.setAttribute("nonce",E.nc),i.setAttribute("data-webpack",r+a),i.src=t),e[t]=[n];var d=(r,n)=>{i.onerror=i.onload=null,clearTimeout(p);var a=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),a&&a.forEach((e=>e(n))),r)return r(n)},p=setTimeout(d.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=d.bind(null,i.onerror),i.onload=d.bind(null,i.onload),l&&document.head.appendChild(i)}},E.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},E.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),(()=>{E.S={};var e={},r={};E.I=(t,n)=>{n||(n=[]);var a=r[t];if(a||(a=r[t]={}),!(n.indexOf(a)>=0)){if(n.push(a),e[t])return e[t];E.o(E.S,t)||(E.S[t]={});var o=E.S[t],i="@elyra/theme-extension",l=(e,r,t,n)=>{var a=o[e]=o[e]||{},l=a[r];(!l||!l.loaded&&(!n!=!l.eager?n:i>l.from))&&(a[r]={get:t,from:i,eager:!!n})},u=[];return"default"===t&&(l("@elyra/theme-extension","4.1.1",(()=>Promise.all([E.e(817),E.e(509)]).then((()=>()=>E(8509))))),l("@elyra/ui-components","4.1.1",(()=>Promise.all([E.e(21),E.e(276),E.e(817),E.e(55)]).then((()=>()=>E(86427)))))),e[t]=u.length?Promise.all(u).then((()=>e[t]=1)):1}}})(),(()=>{var e;E.g.importScripts&&(e=E.g.location+"");var r=E.g.document;if(!e&&r&&(r.currentScript&&"SCRIPT"===r.currentScript.tagName.toUpperCase()&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");if(t.length)for(var n=t.length-1;n>-1&&(!e||!/^http(s?):/.test(e));)e=t[n--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),E.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),n=t[1]?r(t[1]):[];return t[2]&&(n.length++,n.push.apply(n,r(t[2]))),t[3]&&(n.push([]),n.push.apply(n,r(t[3]))),n},n=(e,r)=>{e=t(e),r=t(r);for(var n=0;;){if(n>=e.length)return n<r.length&&"u"!=(typeof r[n])[0];var a=e[n],o=(typeof a)[0];if(n>=r.length)return"u"==o;var i=r[n],l=(typeof i)[0];if(o!=l)return"o"==o&&"n"==l||"s"==l||"u"==o;if("o"!=o&&"u"!=o&&a!=i)return a<i;n++}},a=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var n=1,o=1;o<e.length;o++)n--,t+="u"==(typeof(l=e[o]))[0]?"-":(n>0?".":"")+(n=2,l);return t}var i=[];for(o=1;o<e.length;o++){var l=e[o];i.push(0===l?"not("+u()+")":1===l?"("+u()+" || "+u()+")":2===l?i.pop()+" "+i.pop():a(l))}return u();function u(){return i.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var n=e[0],a=n<0;a&&(n=-n-1);for(var i=0,l=1,u=!0;;l++,i++){var s,f,d=l<e.length?(typeof e[l])[0]:"";if(i>=r.length||"o"==(f=(typeof(s=r[i]))[0]))return!u||("u"==d?l>n&&!a:""==d!=a);if("u"==f){if(!u||"u"!=d)return!1}else if(u)if(d==f)if(l<=n){if(s!=e[l])return!1}else{if(a?s>e[l]:s<e[l])return!1;s!=e[l]&&(u=!1)}else if("s"!=d&&"n"!=d){if(a||l<=n)return!1;u=!1,l--}else{if(l<=n||f<d!=a)return!1;u=!1}else"s"!=d&&"n"!=d&&(u=!1,l--)}}var p=[],c=p.pop.bind(p);for(i=1;i<e.length;i++){var h=e[i];p.push(1==h?c()|c():2==h?c()&c():h?o(h,r):!c())}return!!c()},i=(e,r)=>e&&E.o(e,r),l=e=>(e.loaded=1,e.get()),u=e=>Object.keys(e).reduce(((r,t)=>(e[t].eager&&(r[t]=e[t]),r)),{}),s=(e,r,t,a)=>{var i=a?u(e[r]):e[r];return(r=Object.keys(i).reduce(((e,r)=>!o(t,r)||e&&!n(e,r)?e:r),0))&&i[r]},f=(e,r,t)=>{var a=t?u(e[r]):e[r];return Object.keys(a).reduce(((e,r)=>!e||!a[e].loaded&&n(e,r)?r:e),0)},d=(e,r,t,n)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+a(n)+")",p=(e,r,t,n,o)=>{var i=e[t];return"No satisfying version ("+a(n)+")"+(o?" for eager consumption":"")+" of shared module "+t+" found in shared scope "+r+".\nAvailable versions: "+Object.keys(i).map((e=>e+" from "+i[e].from)).join(", ")},c=e=>{throw new Error(e)},h=e=>{"undefined"!=typeof console&&console.warn&&console.warn(e)},b=(e,r,t)=>t?t():((e,r)=>c("Shared module "+r+" doesn't exist in shared scope "+e))(e,r),m=(v=e=>function(r,t,n,a,o){var i=E.I(r);return i&&i.then&&!n?i.then(e.bind(e,r,E.S[r],t,!1,a,o)):e(r,E.S[r],t,n,a,o)})(((e,r,t,n,a,o)=>{if(!i(r,t))return b(e,t,o);var u=s(r,t,a,n);return u?l(u):o?o():void c(p(r,e,t,a,n))})),y=v(((e,r,t,n,a,u)=>{if(!i(r,t))return b(e,t,u);var s=f(r,t,n);return o(a,s)||h(d(r,t,s,a)),l(r[t][s])})),g={},w={12200:()=>y("default","@jupyterlab/apputils",!1,[1,4,3,5]),87460:()=>y("default","@jupyterlab/ui-components",!1,[1,4,2,5]),93345:()=>y("default","react",!1,[1,18,2,0]),2678:()=>y("default","@jupyterlab/translation",!1,[1,4,2,5]),56887:()=>y("default","@jupyterlab/launcher",!1,[1,4,2,5]),64053:()=>y("default","@lumino/algorithm",!1,[1,2,0,0]),70103:()=>m("default","@elyra/ui-components",!1,[4,4,1,1],(()=>Promise.all([E.e(21),E.e(276)]).then((()=>()=>E(86427))))),86241:()=>y("default","@jupyterlab/mainmenu",!1,[1,4,2,5]),87909:()=>y("default","@jupyterlab/application",!1,[1,4,2,5]),35256:()=>y("default","@lumino/widgets",!1,[1,2,3,1,,"alpha",0]),40131:()=>y("default","@jupyterlab/codeeditor",!1,[1,4,2,5]),77313:()=>y("default","@jupyterlab/filebrowser",!1,[1,4,2,5])},j={276:[35256,40131,77313],509:[2678,56887,64053,70103,86241,87909],817:[12200,87460,93345]},S={},E.f.consumes=(e,r)=>{E.o(j,e)&&j[e].forEach((e=>{if(E.o(g,e))return r.push(g[e]);if(!S[e]){var t=r=>{g[e]=0,E.m[e]=t=>{delete E.c[e],t.exports=r()}};S[e]=!0;var n=r=>{delete g[e],E.m[e]=t=>{throw delete E.c[e],r}};try{var a=w[e]();a.then?r.push(g[e]=a.then(t).catch(n)):t(a)}catch(e){n(e)}}}))},(()=>{E.b=document.baseURI||self.location.href;var e={650:0};E.f.j=(r,t)=>{var n=E.o(e,r)?e[r]:void 0;if(0!==n)if(n)t.push(n[2]);else if(817!=r){var a=new Promise(((t,a)=>n=e[r]=[t,a]));t.push(n[2]=a);var o=E.p+E.u(r),i=new Error;E.l(o,(t=>{if(E.o(e,r)&&(0!==(n=e[r])&&(e[r]=void 0),n)){var a=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+a+": "+o+")",i.name="ChunkLoadError",i.type=a,i.request=o,n[1](i)}}),"chunk-"+r,r)}else e[r]=0};var r=(r,t)=>{var n,a,[o,i,l]=t,u=0;if(o.some((r=>0!==e[r]))){for(n in i)E.o(i,n)&&(E.m[n]=i[n]);l&&l(E)}for(r&&r(t);u<o.length;u++)a=o[u],E.o(e,a)&&e[a]&&e[a][0](),e[a]=0},t=self.webpackChunk_elyra_theme_extension=self.webpackChunk_elyra_theme_extension||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})(),E.nc=void 0;var k=E(13599);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@elyra/theme-extension"]=k})();