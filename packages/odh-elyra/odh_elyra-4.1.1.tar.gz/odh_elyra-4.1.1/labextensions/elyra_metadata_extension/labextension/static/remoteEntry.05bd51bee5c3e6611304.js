var _JUPYTERLAB;(()=>{"use strict";var e,r,t,a,n,o,i,l,u,d,s,f,c,p,h,v,m,b,y,g,w,j,S,P={41859:(e,r,t)=>{var a={"./index":()=>Promise.all([t.e(635),t.e(482),t.e(509)]).then((()=>()=>t(8509))),"./extension":()=>Promise.all([t.e(635),t.e(482),t.e(509)]).then((()=>()=>t(8509))),"./style":()=>t.e(453).then((()=>()=>t(13453)))},n=(e,r)=>(t.R=r,r=t.o(a,e)?a[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),o=(e,r)=>{if(t.S){var a="default",n=t.S[a];if(n&&n!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[a]=e,t.I(a,r)}};t.d(r,{get:()=>n,init:()=>o})}},x={};function E(e){var r=x[e];if(void 0!==r)return r.exports;var t=x[e]={id:e,loaded:!1,exports:{}};return P[e].call(t.exports,t,t.exports,E),t.loaded=!0,t.exports}E.m=P,E.c=x,E.n=e=>{var r=e&&e.__esModule?()=>e.default:()=>e;return E.d(r,{a:r}),r},E.d=(e,r)=>{for(var t in r)E.o(r,t)&&!E.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},E.f={},E.e=e=>Promise.all(Object.keys(E.f).reduce(((r,t)=>(E.f[t](e,r),r)),[])),E.u=e=>e+"."+{294:"8b5bc473d012718241b6",346:"abed61396622ab3ab68c",453:"4ca6ad4503379ab4deb0",482:"f44e6c8c9a6f4974fdf4",509:"fecaed033a9b0dd98d24",635:"bacc903f797e485c4c88",707:"812ee83dce6e95961754",913:"ef2a24b46c541c8c4975"}[e]+".js?v="+{294:"8b5bc473d012718241b6",346:"abed61396622ab3ab68c",453:"4ca6ad4503379ab4deb0",482:"f44e6c8c9a6f4974fdf4",509:"fecaed033a9b0dd98d24",635:"bacc903f797e485c4c88",707:"812ee83dce6e95961754",913:"ef2a24b46c541c8c4975"}[e],E.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),E.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="@elyra/metadata-extension:",E.l=(t,a,n,o)=>{if(e[t])e[t].push(a);else{var i,l;if(void 0!==n)for(var u=document.getElementsByTagName("script"),d=0;d<u.length;d++){var s=u[d];if(s.getAttribute("src")==t||s.getAttribute("data-webpack")==r+n){i=s;break}}i||(l=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,E.nc&&i.setAttribute("nonce",E.nc),i.setAttribute("data-webpack",r+n),i.src=t),e[t]=[a];var f=(r,a)=>{i.onerror=i.onload=null,clearTimeout(c);var n=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),n&&n.forEach((e=>e(a))),r)return r(a)},c=setTimeout(f.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=f.bind(null,i.onerror),i.onload=f.bind(null,i.onload),l&&document.head.appendChild(i)}},E.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},E.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),(()=>{E.S={};var e={},r={};E.I=(t,a)=>{a||(a=[]);var n=r[t];if(n||(n=r[t]={}),!(a.indexOf(n)>=0)){if(a.push(n),e[t])return e[t];E.o(E.S,t)||(E.S[t]={});var o=E.S[t],i="@elyra/metadata-extension",l=(e,r,t,a)=>{var n=o[e]=o[e]||{},l=n[r];(!l||!l.loaded&&(!a!=!l.eager?a:i>l.from))&&(n[r]={get:t,from:i,eager:!!a})},u=[];return"default"===t&&(l("@elyra/metadata-common","4.1.1",(()=>Promise.all([E.e(635),E.e(482),E.e(707)]).then((()=>()=>E(71707))))),l("@elyra/metadata-extension","4.1.1",(()=>Promise.all([E.e(635),E.e(482),E.e(509)]).then((()=>()=>E(8509))))),l("@elyra/services","4.1.1",(()=>Promise.all([E.e(346),E.e(294)]).then((()=>()=>E(92294)))))),e[t]=u.length?Promise.all(u).then((()=>e[t]=1)):1}}})(),(()=>{var e;E.g.importScripts&&(e=E.g.location+"");var r=E.g.document;if(!e&&r&&(r.currentScript&&"SCRIPT"===r.currentScript.tagName.toUpperCase()&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");if(t.length)for(var a=t.length-1;a>-1&&(!e||!/^http(s?):/.test(e));)e=t[a--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),E.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),a=t[1]?r(t[1]):[];return t[2]&&(a.length++,a.push.apply(a,r(t[2]))),t[3]&&(a.push([]),a.push.apply(a,r(t[3]))),a},a=(e,r)=>{e=t(e),r=t(r);for(var a=0;;){if(a>=e.length)return a<r.length&&"u"!=(typeof r[a])[0];var n=e[a],o=(typeof n)[0];if(a>=r.length)return"u"==o;var i=r[a],l=(typeof i)[0];if(o!=l)return"o"==o&&"n"==l||"s"==l||"u"==o;if("o"!=o&&"u"!=o&&n!=i)return n<i;a++}},n=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var a=1,o=1;o<e.length;o++)a--,t+="u"==(typeof(l=e[o]))[0]?"-":(a>0?".":"")+(a=2,l);return t}var i=[];for(o=1;o<e.length;o++){var l=e[o];i.push(0===l?"not("+u()+")":1===l?"("+u()+" || "+u()+")":2===l?i.pop()+" "+i.pop():n(l))}return u();function u(){return i.pop().replace(/^\((.+)\)$/,"$1")}},o=(e,r)=>{if(0 in e){r=t(r);var a=e[0],n=a<0;n&&(a=-a-1);for(var i=0,l=1,u=!0;;l++,i++){var d,s,f=l<e.length?(typeof e[l])[0]:"";if(i>=r.length||"o"==(s=(typeof(d=r[i]))[0]))return!u||("u"==f?l>a&&!n:""==f!=n);if("u"==s){if(!u||"u"!=f)return!1}else if(u)if(f==s)if(l<=a){if(d!=e[l])return!1}else{if(n?d>e[l]:d<e[l])return!1;d!=e[l]&&(u=!1)}else if("s"!=f&&"n"!=f){if(n||l<=a)return!1;u=!1,l--}else{if(l<=a||s<f!=n)return!1;u=!1}else"s"!=f&&"n"!=f&&(u=!1,l--)}}var c=[],p=c.pop.bind(c);for(i=1;i<e.length;i++){var h=e[i];c.push(1==h?p()|p():2==h?p()&p():h?o(h,r):!p())}return!!p()},i=(e,r)=>e&&E.o(e,r),l=e=>(e.loaded=1,e.get()),u=e=>Object.keys(e).reduce(((r,t)=>(e[t].eager&&(r[t]=e[t]),r)),{}),d=(e,r,t,n)=>{var i=n?u(e[r]):e[r];return(r=Object.keys(i).reduce(((e,r)=>!o(t,r)||e&&!a(e,r)?e:r),0))&&i[r]},s=(e,r,t)=>{var n=t?u(e[r]):e[r];return Object.keys(n).reduce(((e,r)=>!e||!n[e].loaded&&a(e,r)?r:e),0)},f=(e,r,t,a)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+n(a)+")",c=(e,r,t,a,o)=>{var i=e[t];return"No satisfying version ("+n(a)+")"+(o?" for eager consumption":"")+" of shared module "+t+" found in shared scope "+r+".\nAvailable versions: "+Object.keys(i).map((e=>e+" from "+i[e].from)).join(", ")},p=e=>{throw new Error(e)},h=e=>{"undefined"!=typeof console&&console.warn&&console.warn(e)},m=(e,r,t)=>t?t():((e,r)=>p("Shared module "+r+" doesn't exist in shared scope "+e))(e,r),b=(v=e=>function(r,t,a,n,o){var i=E.I(r);return i&&i.then&&!a?i.then(e.bind(e,r,E.S[r],t,!1,n,o)):e(r,E.S[r],t,a,n,o)})(((e,r,t,a,n,o)=>{if(!i(r,t))return m(e,t,o);var u=d(r,t,n,a);return u?l(u):o?o():void p(c(r,e,t,n,a))})),y=v(((e,r,t,a,n,u)=>{if(!i(r,t))return m(e,t,u);var d=s(r,t,a);return o(n,d)||h(f(r,t,d,n)),l(r[t][d])})),g={},w={12200:()=>y("default","@jupyterlab/apputils",!1,[1,4,3,5]),16797:()=>b("default","@elyra/services",!1,[4,4,1,1],(()=>E.e(913).then((()=>()=>E(92294))))),35256:()=>y("default","@lumino/widgets",!1,[1,2,3,1,,"alpha",0]),40131:()=>y("default","@jupyterlab/codeeditor",!1,[1,4,2,5]),64053:()=>y("default","@lumino/algorithm",!1,[1,2,0,0]),77313:()=>y("default","@jupyterlab/filebrowser",!1,[1,4,2,5]),87460:()=>y("default","@jupyterlab/ui-components",!1,[1,4,2,5]),93345:()=>y("default","react",!1,[1,18,2,0]),2678:()=>y("default","@jupyterlab/translation",!1,[1,4,2,5]),84199:()=>b("default","@elyra/metadata-common",!1,[4,4,1,1],(()=>E.e(707).then((()=>()=>E(71707))))),87909:()=>y("default","@jupyterlab/application",!1,[1,4,2,5]),74602:()=>y("default","@lumino/signaling",!1,[1,2,0,0]),57354:()=>y("default","@jupyterlab/services",!1,[1,7,2,5]),81473:()=>y("default","@jupyterlab/coreutils",!1,[1,6,2,5])},j={346:[57354,81473],482:[12200,16797,35256,40131,64053,77313,87460,93345],509:[2678,84199,87909],707:[74602],913:[57354,81473]},S={},E.f.consumes=(e,r)=>{E.o(j,e)&&j[e].forEach((e=>{if(E.o(g,e))return r.push(g[e]);if(!S[e]){var t=r=>{g[e]=0,E.m[e]=t=>{delete E.c[e],t.exports=r()}};S[e]=!0;var a=r=>{delete g[e],E.m[e]=t=>{throw delete E.c[e],r}};try{var n=w[e]();n.then?r.push(g[e]=n.then(t).catch(a)):t(n)}catch(e){a(e)}}}))},(()=>{E.b=document.baseURI||self.location.href;var e={468:0};E.f.j=(r,t)=>{var a=E.o(e,r)?e[r]:void 0;if(0!==a)if(a)t.push(a[2]);else if(346!=r){var n=new Promise(((t,n)=>a=e[r]=[t,n]));t.push(a[2]=n);var o=E.p+E.u(r),i=new Error;E.l(o,(t=>{if(E.o(e,r)&&(0!==(a=e[r])&&(e[r]=void 0),a)){var n=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+n+": "+o+")",i.name="ChunkLoadError",i.type=n,i.request=o,a[1](i)}}),"chunk-"+r,r)}else e[r]=0};var r=(r,t)=>{var a,n,[o,i,l]=t,u=0;if(o.some((r=>0!==e[r]))){for(a in i)E.o(i,a)&&(E.m[a]=i[a]);l&&l(E)}for(r&&r(t);u<o.length;u++)n=o[u],E.o(e,n)&&e[n]&&e[n][0](),e[n]=0},t=self.webpackChunk_elyra_metadata_extension=self.webpackChunk_elyra_metadata_extension||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})(),E.nc=void 0;var k=E(41859);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB)["@elyra/metadata-extension"]=k})();