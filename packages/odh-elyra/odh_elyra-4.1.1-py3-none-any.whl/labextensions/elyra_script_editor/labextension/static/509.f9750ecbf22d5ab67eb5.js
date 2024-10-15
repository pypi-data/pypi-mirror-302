"use strict";(self.webpackChunk_elyra_script_editor=self.webpackChunk_elyra_script_editor||[]).push([[509],{753:function(e,t,i){var n=this&&this.__createBinding||(Object.create?function(e,t,i,n){void 0===n&&(n=i);var o=Object.getOwnPropertyDescriptor(t,i);o&&!("get"in o?!t.__esModule:o.writable||o.configurable)||(o={enumerable:!0,get:function(){return t[i]}}),Object.defineProperty(e,n,o)}:function(e,t,i,n){void 0===n&&(n=i),e[n]=t[i]}),o=this&&this.__setModuleDefault||(Object.create?function(e,t){Object.defineProperty(e,"default",{enumerable:!0,value:t})}:function(e,t){e.default=t}),r=this&&this.__importStar||function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var i in e)"default"!==i&&Object.prototype.hasOwnProperty.call(e,i)&&n(t,e,i);return o(t,e),t};Object.defineProperty(t,"__esModule",{value:!0}),t.KernelDropdown=void 0;const s=i(200),l=i(460),a=r(i(345)),u=(0,a.forwardRef)((({specs:e,defaultKernel:t,callback:i},n)=>{const o=(0,a.useMemo)((()=>Object.assign({},e.kernelspecs)),[e]),[r,s]=(0,a.useState)(t||"");(0,a.useImperativeHandle)(n,(()=>({getSelection:()=>r})));const u=Object.keys(o).length?Object.entries(o).map((([e,t])=>{var i;return a.default.createElement("option",{key:e,value:e},null!==(i=null==t?void 0:t.display_name)&&void 0!==i?i:e)})):a.default.createElement("option",{key:"no-kernel",value:"no-kernel"},"No Kernel");return a.default.createElement(l.HTMLSelect,{onChange:e=>{const t=e.target.value;s(t),i(t)},value:r},u)}));class c extends s.ReactWidget{constructor(e,t,i,n){super(),this.specs=e,this.defaultKernel=t,this.ref=i,this.callback=n,this.defaultKernel=t}render(){return a.default.createElement(u,{ref:this.ref,specs:this.specs,defaultKernel:this.defaultKernel,callback:this.callback})}}t.KernelDropdown=c},703:function(e,t,i){var n=this&&this.__awaiter||function(e,t,i,n){return new(i||(i=Promise))((function(o,r){function s(e){try{a(n.next(e))}catch(e){r(e)}}function l(e){try{a(n.throw(e))}catch(e){r(e)}}function a(e){var t;e.done?o(e.value):(t=e.value,t instanceof i?t:new i((function(e){e(t)}))).then(s,l)}a((n=n.apply(e,t||[])).next())}))},o=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0}),t.ScriptEditor=void 0;const r=i(200),s=i(135),l=i(154),a=i(762),u=i(215),c=i(460),d=i(602),h=i(256),p=o(i(345)),v=i(753),g=i(367),f=i(528),y="elyra-ScriptEditor-OutputArea-error";class m extends s.DocumentWidget{constructor(e){super(e),this.debuggerAvailable=e=>n(this,void 0,void 0,(function*(){return yield this.controller.debuggerAvailable(e)})),this.initializeKernelSpecs=()=>n(this,void 0,void 0,(function*(){const e=this.getLanguage(),t=yield this.controller.getKernelSpecsByLanguage(e);this.defaultKernel=yield this.controller.getDefaultKernel(e),this.kernelName=this.defaultKernel,this.kernelSelectorRef=p.default.createRef(),null!==t&&this.toolbar.insertItem(4,"select",new v.KernelDropdown(t,this.defaultKernel,this.kernelSelectorRef,this.handleKernelSelectionUpdate)),this._kernelSelectionChanged.emit(this.kernelSelection)})),this.handleKernelSelectionUpdate=e=>n(this,void 0,void 0,(function*(){e!==this.kernelName&&(this.kernelName=e,this._kernelSelectionChanged.emit(e))})),this.createOutputAreaWidget=()=>{this.dockPanel=new c.DockPanelSvg({tabsMovable:!1}),h.Widget.attach(this.dockPanel,document.body),window.addEventListener("resize",(()=>{var e;null===(e=this.dockPanel)||void 0===e||e.fit()}));const e=new a.OutputAreaModel,t=new u.RenderMimeRegistry({initialFactories:u.standardRendererFactories});this.outputAreaWidget=new a.OutputArea({rendermime:t,model:e}),this.outputAreaWidget.addClass("elyra-ScriptEditor-OutputArea"),this.layout.addWidget(this.dockPanel)},this.runScript=()=>n(this,void 0,void 0,(function*(){this.runDisabled||(this.clearOutputArea(),this.displayOutputArea(),yield this.runner.runScript(this.kernelName,this.context.path,this.model.sharedModel.getSource(),this.handleKernelMsg))})),this.interruptRun=()=>n(this,void 0,void 0,(function*(){var e;yield this.runner.interruptKernel(),(null===(e=this.dockPanel)||void 0===e?void 0:e.isEmpty)||this.updatePromptText(" ")})),this.disableRunButton=e=>{this.runButton.enabled=!e,this.runDisabled=e},this.clearOutputArea=()=>{var e,t,i;null===(e=this.dockPanel)||void 0===e||e.hide(),null===(t=this.outputAreaWidget)||void 0===t||t.model.clear(),null===(i=this.outputAreaWidget)||void 0===i||i.removeClass(y)},this.handleKernelMsg=e=>n(this,void 0,void 0,(function*(){let t="";if(e.status)this.displayKernelStatus(e.status);else{if(e.error)return t="Error : "+e.error.type+" - "+e.error.output,this.displayOutput(t),void this.getOutputAreaChildWidget().addClass(y);e.output&&(t=e.output),this.displayOutput(t)}})),this.createScrollButtons=e=>{var t,i;const n=document.createElement("button"),o=document.createElement("button");n.className="elyra-ScriptEditor-scrollTop",o.className="elyra-ScriptEditor-scrollBottom",n.onclick=function(){e.node.scrollTop=0},o.onclick=function(){e.node.scrollTop=e.node.scrollHeight},c.caretUpEmptyThinIcon.element({container:n,elementPosition:"center",title:"Top"}),c.caretDownEmptyThinIcon.element({container:o,elementPosition:"center",title:"Bottom"}),null===(t=this.dockPanel)||void 0===t||t.node.appendChild(n),null===(i=this.dockPanel)||void 0===i||i.node.appendChild(o)},this.displayOutputArea=()=>{var e,t,i,n,o,r;if(void 0!==this.outputAreaWidget&&(null===(t=null===(e=this.kernelSelectorRef)||void 0===e?void 0:e.current)||void 0===t?void 0:t.getSelection())){if(null===(i=this.dockPanel)||void 0===i||i.show(),void 0!==this.dockPanel&&h.BoxLayout.setStretch(this.dockPanel,1),null===(n=this.dockPanel)||void 0===n?void 0:n.isEmpty){this.scrollingWidget=new l.ScrollingWidget({content:this.outputAreaWidget}),this.createScrollButtons(this.scrollingWidget),null===(o=this.dockPanel)||void 0===o||o.addWidget(this.scrollingWidget,{mode:"split-bottom"});const e=null===(r=this.dockPanel)||void 0===r?void 0:r.tabBars().next().value;void 0!==e&&(e.id="tab-ScriptEditor-output",null!==e.currentTitle&&(e.currentTitle.label="Console Output",e.currentTitle.closable=!0),e.disposed.connect((()=>{this.interruptRun(),this.clearOutputArea()}),this))}this.outputAreaWidget.model.add({name:"stdout",output_type:"stream",text:["Waiting for kernel to start..."]}),this.updatePromptText(" "),this.setOutputAreaClasses()}},this.displayKernelStatus=e=>{"busy"===e?(this.emptyOutput=!0,this.displayOutput(" "),this.updatePromptText("*")):"idle"===e&&this.updatePromptText(" ")},this.displayOutput=e=>{var t,i,n,o;if(e){const r={name:"stdout",output_type:"stream",text:[e]};this.emptyOutput?(null===(t=this.outputAreaWidget)||void 0===t||t.model.clear(!1),null===(i=this.outputAreaWidget)||void 0===i||i.model.add(r),this.emptyOutput=!1,null===(n=this.outputAreaWidget)||void 0===n||n.model.clear(!0)):null===(o=this.outputAreaWidget)||void 0===o||o.model.add(r),this.updatePromptText("*"),this.setOutputAreaClasses()}},this.setOutputAreaClasses=()=>{this.getOutputAreaChildWidget().addClass("elyra-ScriptEditor-OutputArea-child"),this.getOutputAreaOutputWidget().addClass("elyra-ScriptEditor-OutputArea-output"),this.getOutputAreaPromptWidget().addClass("elyra-ScriptEditor-OutputArea-prompt")},this.getOutputAreaChildWidget=()=>{var e;return(null===(e=this.outputAreaWidget)||void 0===e?void 0:e.layout).widgets[0]},this.getOutputAreaOutputWidget=()=>this.getOutputAreaChildWidget().layout.widgets[1],this.getOutputAreaPromptWidget=()=>this.getOutputAreaChildWidget().layout.widgets[0],this.updatePromptText=e=>{this.getOutputAreaPromptWidget().node.innerText="["+e+"]:"},this.saveFile=()=>n(this,void 0,void 0,(function*(){if(this.context.model.readOnly)return(0,r.showDialog)({title:"Cannot Save",body:"Document is read-only",buttons:[r.Dialog.okButton()]});this.context.save().then((()=>{if(!this.isDisposed)return this.context.createCheckpoint()}))})),this.addClass("elyra-ScriptEditor"),this.model=this.content.model,this.runner=new f.ScriptRunner(this.disableRunButton),this.kernelSelectorRef=null,this.emptyOutput=!0,this.controller=new g.ScriptEditorController,this.runDisabled=!1,this.defaultKernel=null,this.kernelName=null,this._kernelSelectionChanged=new d.Signal(this),this.title.icon=this.getIcon();const t=new r.ToolbarButton({icon:c.saveIcon,onClick:this.saveFile,tooltip:"Save file contents"}),i=new r.ToolbarButton({className:"elyra-ScriptEditor-Run",icon:c.runIcon,onClick:this.runScript,tooltip:"Run",enabled:!this.runDisabled}),o=new r.ToolbarButton({icon:c.stopIcon,onClick:this.interruptRun,tooltip:"Interrupt the kernel"}),s=this.toolbar;s.addItem("save",t),s.addItem("run",i),s.addItem("interrupt",o),this.toolbar.addClass("elyra-ScriptEditor-Toolbar"),this.runButton=i,this.createOutputAreaWidget(),this.context.ready.then((()=>this.initializeKernelSpecs()))}get kernelSelectionChanged(){return this._kernelSelectionChanged}get kernelSelection(){var e,t;return null!==(t=null!==(e=this.kernelName)&&void 0!==e?e:this.defaultKernel)&&void 0!==t?t:""}}t.ScriptEditor=m},367:function(e,t,i){var n=this&&this.__awaiter||function(e,t,i,n){return new(i||(i=Promise))((function(o,r){function s(e){try{a(n.next(e))}catch(e){r(e)}}function l(e){try{a(n.throw(e))}catch(e){r(e)}}function a(e){var t;e.done?o(e.value):(t=e.value,t instanceof i?t:new i((function(e){e(t)}))).then(s,l)}a((n=n.apply(e,t||[])).next())}))};Object.defineProperty(t,"__esModule",{value:!0}),t.ScriptEditorController=void 0;const o=i(354);t.ScriptEditorController=class{constructor(){this.getKernelSpecs=()=>n(this,void 0,void 0,(function*(){yield this.kernelSpecManager.ready;const e=this.kernelSpecManager.specs;return JSON.parse(JSON.stringify(e))})),this.getKernelSpecsByLanguage=e=>n(this,void 0,void 0,(function*(){var t;const i=yield this.getKernelSpecs();return Object.entries(null!==(t=null==i?void 0:i.kernelspecs)&&void 0!==t?t:[]).filter((t=>{var i;return!1===(null===(i=t[1])||void 0===i?void 0:i.language.includes(e))})).forEach((e=>null==i||delete i.kernelspecs[e[0]])),i})),this.getKernelSpecsByName=e=>n(this,void 0,void 0,(function*(){var t;const i=yield this.getKernelSpecs();return Object.entries(null!==(t=null==i?void 0:i.kernelspecs)&&void 0!==t?t:[]).filter((t=>{var i,n;return!1===(null===(n=null===(i=t[1])||void 0===i?void 0:i.name)||void 0===n?void 0:n.includes(e))})).forEach((e=>null==i||delete i.kernelspecs[e[0]])),i})),this.getDefaultKernel=e=>n(this,void 0,void 0,(function*(){var t;const i=yield this.getKernelSpecs();return i?(null===(t=i.default)||void 0===t?void 0:t.includes(e))?i.default:this.getFirstKernelName(e):""})),this.getFirstKernelName=e=>n(this,void 0,void 0,(function*(){var t;const i=yield this.getKernelSpecsByLanguage(e);if(i&&0!==Object.keys(i.kernelspecs).length){const[e,n]=Object.entries(i.kernelspecs)[0];return null!==(t=n.name)&&void 0!==t?t:e}return""})),this.debuggerAvailable=e=>n(this,void 0,void 0,(function*(){var t,i,n;const o=yield this.getKernelSpecsByName(e);return!(null===(n=null===(i=null===(t=null==o?void 0:o.kernelspecs[e])||void 0===t?void 0:t.metadata)||void 0===i?void 0:i.debugger)||void 0===n||!n)})),this.kernelSpecManager=new o.KernelSpecManager}}},709:(e,t,i)=>{Object.defineProperty(t,"__esModule",{value:!0}),t.ScriptEditorWidgetFactory=void 0;const n=i(135),o=i(710);class r extends n.ABCWidgetFactory{constructor(e){super(e.factoryOptions),this._services=e.editorServices,this.options=e}createNewWidget(e){const t=this._services.factoryService.newDocumentEditor,i=new o.FileEditor({factory:e=>t(e),context:e,mimeTypeService:this._services.mimeTypeService});return this.options.instanceCreator({content:i,context:e})}}t.ScriptEditorWidgetFactory=r},528:function(e,t,i){var n=this&&this.__awaiter||function(e,t,i,n){return new(i||(i=Promise))((function(o,r){function s(e){try{a(n.next(e))}catch(e){r(e)}}function l(e){try{a(n.throw(e))}catch(e){r(e)}}function a(e){var t;e.done?o(e.value):(t=e.value,t instanceof i?t:new i((function(e){e(t)}))).then(s,l)}a((n=n.apply(e,t||[])).next())}))};Object.defineProperty(t,"__esModule",{value:!0}),t.ScriptRunner=void 0;const o=i(200),r=i(354),s="Could not start session to execute script.";t.ScriptRunner=class{constructor(e){this.errorDialog=e=>(this.disableButton(!1),(0,o.showDialog)({title:"Error",body:e,buttons:[o.Dialog.okButton()]})),this.runScript=(e,t,i,o)=>n(this,void 0,void 0,(function*(){var n;if(!e)return this.disableButton(!0),this.errorDialog("Could not run script because no supporting kernel is defined.");this.disableButton(!0);try{yield this.startSession(e,t)}catch(e){return this.errorDialog(s)}if(!(null===(n=this.sessionConnection)||void 0===n?void 0:n.kernel))return this.errorDialog(s);const r=this.sessionConnection.kernel.requestExecute({code:i});r.onIOPub=e=>{const t=e.header.msg_type,i={};if("error"===t){const t=e;i.error={type:t.content.ename,output:t.content.evalue}}else if("execute_result"===t||"display_data"===t){const t=e;"text/plain"in t.content.data?i.output=t.content.data["text/plain"]:console.log("Ignoring received message "+JSON.stringify(e))}else if("stream"===t){const t=e;i.output=t.content.text}else if("status"===t){const t=e;i.status=t.content.execution_state}o(i)};try{yield r.done,this.disableButton(!1)}catch(e){console.log("Exception: done = "+JSON.stringify(e))}})),this.startSession=(e,t)=>n(this,void 0,void 0,(function*(){const i={kernel:{name:e},path:t,type:"file",name:t};if(!this.sessionConnection||!this.sessionConnection.kernel)try{this.sessionConnection=yield this.sessionManager.startNew(i),this.sessionConnection.setPath(t)}catch(e){console.log("Exception: kernel start = "+JSON.stringify(e))}})),this.shutdownSession=()=>n(this,void 0,void 0,(function*(){var e;if(this.sessionConnection){const t=null===(e=this.sessionConnection.kernel)||void 0===e?void 0:e.name;try{yield this.sessionConnection.shutdown(),this.sessionConnection=null,console.log(t+" kernel shut down")}catch(e){console.log("Exception: session shutdown = "+JSON.stringify(e))}}})),this.shutdownKernel=()=>n(this,void 0,void 0,(function*(){if(this.sessionConnection){const e=this.sessionConnection.kernel;try{e&&(yield r.KernelAPI.shutdownKernel(e.id)),console.log((null==e?void 0:e.name)+" kernel shutdown")}catch(e){console.log("Exception: kernel shutdown = "+JSON.stringify(e))}}})),this.interruptKernel=()=>n(this,void 0,void 0,(function*(){if(this.sessionConnection){const e=this.sessionConnection.kernel;try{e&&(yield r.KernelAPI.interruptKernel(e.id,e.serverSettings)),console.log((null==e?void 0:e.name)+" kernel interrupted."),this.disableButton(!1)}catch(e){console.log("Exception: kernel interrupt = "+JSON.stringify(e))}}})),this.disableButton=e,this.kernelSpecManager=new r.KernelSpecManager,this.kernelManager=new r.KernelManager,this.sessionManager=new r.SessionManager({kernelManager:this.kernelManager}),this.sessionConnection=null}}},509:function(e,t,i){var n=this&&this.__createBinding||(Object.create?function(e,t,i,n){void 0===n&&(n=i);var o=Object.getOwnPropertyDescriptor(t,i);o&&!("get"in o?!t.__esModule:o.writable||o.configurable)||(o={enumerable:!0,get:function(){return t[i]}}),Object.defineProperty(e,n,o)}:function(e,t,i,n){void 0===n&&(n=i),e[n]=t[i]}),o=this&&this.__exportStar||function(e,t){for(var i in e)"default"===i||Object.prototype.hasOwnProperty.call(t,i)||n(t,e,i)};Object.defineProperty(t,"__esModule",{value:!0}),o(i(753),t),o(i(703),t),o(i(367),t),o(i(528),t),o(i(709),t)}}]);