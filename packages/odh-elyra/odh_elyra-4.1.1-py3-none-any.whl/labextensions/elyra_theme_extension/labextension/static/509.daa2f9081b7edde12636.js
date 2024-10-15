"use strict";(self.webpackChunk_elyra_theme_extension=self.webpackChunk_elyra_theme_extension||[]).push([[509,453,55],{21411:(e,t,n)=>{n.d(t,{A:()=>c});var r=n(36758),a=n.n(r),o=n(40935),i=n.n(o)()(a());i.push([e.id,'/*\n * Copyright 2018-2023 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n.jp-LabShell {\n  background: var(--jp-layout-color3);\n}\n',""]);const c=i},40935:e=>{e.exports=function(e){var t=[];return t.toString=function(){return this.map((function(t){var n="",r=void 0!==t[5];return t[4]&&(n+="@supports (".concat(t[4],") {")),t[2]&&(n+="@media ".concat(t[2]," {")),r&&(n+="@layer".concat(t[5].length>0?" ".concat(t[5]):""," {")),n+=e(t),r&&(n+="}"),t[2]&&(n+="}"),t[4]&&(n+="}"),n})).join("")},t.i=function(e,n,r,a,o){"string"==typeof e&&(e=[[null,e,void 0]]);var i={};if(r)for(var c=0;c<this.length;c++){var s=this[c][0];null!=s&&(i[s]=!0)}for(var l=0;l<e.length;l++){var d=[].concat(e[l]);r&&i[d[0]]||(void 0!==o&&(void 0===d[5]||(d[1]="@layer".concat(d[5].length>0?" ".concat(d[5]):""," {").concat(d[1],"}")),d[5]=o),n&&(d[2]?(d[1]="@media ".concat(d[2]," {").concat(d[1],"}"),d[2]=n):d[2]=n),a&&(d[4]?(d[1]="@supports (".concat(d[4],") {").concat(d[1],"}"),d[4]=a):d[4]="".concat(a)),t.push(d))}},t}},36758:e=>{e.exports=function(e){return e[1]}},13453:(e,t,n)=>{n.r(t),n.d(t,{default:()=>y});var r=n(72591),a=n.n(r),o=n(1740),i=n.n(o),c=n(88128),s=n.n(c),l=n(30855),d=n.n(l),u=n(93051),p=n.n(u),h=n(73656),f=n.n(h),m=n(21411),v={};v.styleTagTransform=f(),v.setAttributes=d(),v.insert=s().bind(null,"head"),v.domAPI=i(),v.insertStyleElement=p(),a()(m.A,v);const y=m.A&&m.A.locals?m.A.locals:void 0},72591:e=>{var t=[];function n(e){for(var n=-1,r=0;r<t.length;r++)if(t[r].identifier===e){n=r;break}return n}function r(e,r){for(var o={},i=[],c=0;c<e.length;c++){var s=e[c],l=r.base?s[0]+r.base:s[0],d=o[l]||0,u="".concat(l," ").concat(d);o[l]=d+1;var p=n(u),h={css:s[1],media:s[2],sourceMap:s[3],supports:s[4],layer:s[5]};if(-1!==p)t[p].references++,t[p].updater(h);else{var f=a(h,r);r.byIndex=c,t.splice(c,0,{identifier:u,updater:f,references:1})}i.push(u)}return i}function a(e,t){var n=t.domAPI(t);return n.update(e),function(t){if(t){if(t.css===e.css&&t.media===e.media&&t.sourceMap===e.sourceMap&&t.supports===e.supports&&t.layer===e.layer)return;n.update(e=t)}else n.remove()}}e.exports=function(e,a){var o=r(e=e||[],a=a||{});return function(e){e=e||[];for(var i=0;i<o.length;i++){var c=n(o[i]);t[c].references--}for(var s=r(e,a),l=0;l<o.length;l++){var d=n(o[l]);0===t[d].references&&(t[d].updater(),t.splice(d,1))}o=s}}},88128:e=>{var t={};e.exports=function(e,n){var r=function(e){if(void 0===t[e]){var n=document.querySelector(e);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(e){n=null}t[e]=n}return t[e]}(e);if(!r)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");r.appendChild(n)}},93051:e=>{e.exports=function(e){var t=document.createElement("style");return e.setAttributes(t,e.attributes),e.insert(t,e.options),t}},30855:(e,t,n)=>{e.exports=function(e){var t=n.nc;t&&e.setAttribute("nonce",t)}},1740:e=>{e.exports=function(e){if("undefined"==typeof document)return{update:function(){},remove:function(){}};var t=e.insertStyleElement(e);return{update:function(n){!function(e,t,n){var r="";n.supports&&(r+="@supports (".concat(n.supports,") {")),n.media&&(r+="@media ".concat(n.media," {"));var a=void 0!==n.layer;a&&(r+="@layer".concat(n.layer.length>0?" ".concat(n.layer):""," {")),r+=n.css,a&&(r+="}"),n.media&&(r+="}"),n.supports&&(r+="}");var o=n.sourceMap;o&&"undefined"!=typeof btoa&&(r+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(o))))," */")),t.styleTagTransform(r,e,t.options)}(t,e,n)},remove:function(){!function(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e)}(t)}}}},73656:e=>{e.exports=function(e,t){if(t.styleSheet)t.styleSheet.cssText=e;else{for(;t.firstChild;)t.removeChild(t.firstChild);t.appendChild(document.createTextNode(e))}}},8509:(e,t,n)=>{Object.defineProperty(t,"__esModule",{value:!0});const r=n(70103),a=n(87909),o=n(12200),i=n(56887),c=n(86241),s=n(2678),l=n(87460),d=n(64053),u=n(79501);n(13453);const p="launcher:create",h="elyra:open-help",f="elyra:releases",m={id:"elyra-theme-extension",autoStart:!0,requires:[s.ITranslator,a.ILabShell,c.IMainMenu],optional:[o.ICommandPalette],provides:i.ILauncher,activate:(e,t,n,a,i)=>{console.log("Elyra - theme extension is activated!");const{commands:c,shell:s}=e,m=t.load("jupyterlab"),y=new u.LauncherModel;return c.addCommand(p,{label:m.__("New Launcher"),execute:e=>{const r=e.cwd?String(e.cwd):"",a="launcher-"+v.id++,i=new u.Launcher({model:y,cwd:r,callback:e=>{n.add(e,"main",{ref:a})},commands:c,translator:t});i.model=y,i.title.icon=l.launcherIcon,i.title.label=m.__("Launcher");const p=new o.MainAreaWidget({content:i});return p.title.closable=!!(0,d.toArray)(n.widgets("main")).length,p.id=a,s.add(p,"main",{activate:e.activate,ref:e.ref}),n.layoutModified.connect((()=>{p.title.closable=(0,d.toArray)(n.widgets("main")).length>1}),p),p}}),i&&i.addItem({command:p,category:m.__("Launcher")}),n&&(n.addButtonEnabled=!0,n.addRequested.connect(((e,t)=>{var n;const r=(null===(n=t.currentTitle)||void 0===n?void 0:n.owner.id)||t.titles[t.titles.length-1].owner.id;return c.hasCommand("filebrowser:create-main-launcher")?c.execute("filebrowser:create-main-launcher",{ref:r}):c.execute(p,{ref:r})}))),c.addCommand(h,{label:"Documentation",icon:r.helpIcon,execute:e=>{window.open("https://elyra.readthedocs.io/en/latest/","_blank")}}),c.addCommand(f,{label:"What's new in latest",caption:"What's new in this release",icon:r.whatsNewIcon,execute:e=>{window.open("https://github.com/elyra-ai/elyra/releases/latest/","_blank")}}),y.add({command:h,category:"Elyra",rank:10}),y.add({command:f,category:"Elyra",rank:11}),y}};var v;!function(e){e.id=0}(v||(v={})),t.default=m},79501:function(e,t,n){var r=this&&this.__createBinding||(Object.create?function(e,t,n,r){void 0===r&&(r=n);var a=Object.getOwnPropertyDescriptor(t,n);a&&!("get"in a?!t.__esModule:a.writable||a.configurable)||(a={enumerable:!0,get:function(){return t[n]}}),Object.defineProperty(e,r,a)}:function(e,t,n,r){void 0===r&&(r=n),e[r]=t[n]}),a=this&&this.__setModuleDefault||(Object.create?function(e,t){Object.defineProperty(e,"default",{enumerable:!0,value:t})}:function(e,t){e.default=t}),o=this&&this.__importStar||function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var n in e)"default"!==n&&Object.prototype.hasOwnProperty.call(e,n)&&r(t,e,n);return a(t,e),t};Object.defineProperty(t,"__esModule",{value:!0}),t.Launcher=t.LauncherModel=void 0;const i=n(70103),c=n(56887),s=n(64053),l=o(n(93345)),d="Elyra";class u extends c.LauncherModel{*items(){const e=[];let t=!1,n=!1;this.itemsList.forEach((e=>{"script-editor:create-new-python-editor"===e.command?t=!0:"script-editor:create-new-r-editor"===e.command&&(n=!0)})),t||n||(yield*this.itemsList),this.itemsList.forEach((r=>{var a,o;"fileeditor:create-new"===r.command&&(t&&"py"===(null===(a=r.args)||void 0===a?void 0:a.fileExt)||n&&"r"===(null===(o=r.args)||void 0===o?void 0:o.fileExt))||e.push(r)})),yield*e}}t.LauncherModel=u;class p extends c.Launcher{constructor(e){super(e),this._translator=this.translator.load("jupyterlab")}replaceCategoryIcon(e,t){const n=l.Children.map(e.props.children,(e=>{if("jp-Launcher-sectionHeader"===e.props.className){const n=l.Children.map(e.props.children,(e=>"jp-Launcher-sectionTitle"!==e.props.className?l.createElement(t.react,{stylesheet:"launcherSection"}):e));return l.cloneElement(e,e.props,n)}return e}));return l.cloneElement(e,e.props,n)}render(){if(!this.model)return null;const e=super.render(),t=(null==e?void 0:e.props.children).props.children,n=[],r=[this._translator.__("Notebook"),this._translator.__("Console"),d,this._translator.__("Other")];return(0,s.each)(r,((e,r)=>{l.Children.forEach(t,(t=>{t.key===e&&(t.key===d&&(t=this.replaceCategoryIcon(t,i.elyraIcon)),n.push(t))}))})),l.createElement("div",{className:"jp-Launcher-body"},l.createElement("div",{className:"jp-Launcher-content"},l.createElement("div",{className:"jp-Launcher-cwd"},l.createElement("h3",null,this.cwd)),n))}}t.Launcher=p}}]);