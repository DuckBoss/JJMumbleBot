(this["webpackJsonpjjmumblebot-web"]=this["webpackJsonpjjmumblebot-web"]||[]).push([[0],{131:function(t,e,n){},152:function(t,e,n){},160:function(t,e,n){"use strict";n.r(e);var c=n(2),a=n(0),r=n.n(a),o=n(14),s=n.n(o),i=(n(131),n(50)),u=n(8),l=n(7);function h(){var t=Object(u.a)(["\n  body {\n    background: ",";\n    color: ",";\n    font-family: Tahoma, Helvetica, Arial, Roboto, sans-serif;\n    transition: all 0.25s ease;\n  }\n  "]);return h=function(){return t},t}var d=Object(l.b)(h(),(function(t){return t.theme.body}),(function(t){return t.theme.text})),j={body:"#FFF",text:"#363537",accent_primary:"#00c9bc",accent_secondary:"#c9005e",contrast:"#fff",contrast2:"#9F9F9F",toggleForeground:"#fff",toggleBackground:"#363537",black:"#000",white:"#fff"},b={body:"#363537",text:"#FAFAFA",accent_primary:"#00c9bc",accent_secondary:"#c9005e",contrast:"#202021",contrast2:"#000",toggleForeground:"#fff",toggleBackground:"#363537",black:"#000",white:"#fff"},p=n(15),m=n(16),f=n(18),O=n(17),x=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(){var t;Object(p.a)(this,n);for(var c=arguments.length,a=new Array(c),r=0;r<c;r++)a[r]=arguments[r];return(t=e.call.apply(e,[this].concat(a))).getBotName=function(){fetch("/api/general/name",{headers:{Accept:"application/json","Content-Type":"application/json"}}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){return document.title="".concat(t.data.name," Dashboard")})).catch((function(t){console.trace(t),document.title="JJMumbleBot Dashboard"}))},t}return Object(m.a)(n,[{key:"componentDidMount",value:function(){this.getBotName()}},{key:"render",value:function(){return Object(c.jsx)("div",{})}}]),n}(r.a.Component),k=n(197),g=n(200),v=n(233),y=function(t){var e=t.theme,n=(t.themeText,t.toggleTheme);return Object(c.jsx)(k.a,{children:Object(c.jsx)(g.a,{control:Object(c.jsx)(v.a,{checked:"dark"===e,onChange:n,name:"darkModeChecked"}),label:"Dark Mode"})})},_=n(60),C=n(205),T=n(76),S=n.n(T),D=n(228),w=n(201),A=n(115),P=n(206);function N(){var t=Object(u.a)(["\n    display: 'block';\n    padding: 0.2em;\n    background-color: ",";\n"]);return N=function(){return t},t}function B(){var t=Object(u.a)(["\n    color: ",";\n    &:hover {\n        color: ",";\n    }\n"]);return B=function(){return t},t}function M(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n    &:hover {\n        background-color: ",";\n        color: ",";\n    }\n"]);return M=function(){return t},t}function I(){var t=Object(u.a)(["\n    & label {\n        color: ",";\n    }\n    & input {\n        color: ",";\n        width: 100%;\n    }\n"]);return I=function(){return t},t}var F=Object(l.c)(D.a)(I(),(function(t){return t.theme.text}),(function(t){return t.theme.text})),H=Object(l.c)(C.a)(M(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text}),(function(t){return t.theme.accent_secondary}),(function(t){return t.theme.white})),W=Object(l.c)(w.a)(B(),(function(t){return t.theme.text}),(function(t){return t.theme.text})),J=Object(l.c)(A.a)(N(),(function(t){return t.theme.body})),L=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).refreshBotDetails=function(){fetch("/api/general",{headers:{Accept:"application/json","Content-Type":"application/json"}}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){c.setState({botName:t.data.name}),c.setState({botCommandToken:t.data.command_token})})).catch((function(t){console.log(t),c.setState({botName:"N/A"}),c.setState({botCommandToken:"!"})}))},c.updateCommandText=function(t){c.setState({commandText:t.target.value}),c.cmdIsValid()?c.setState({cmdIsValid:!0}):c.setState({cmdIsValid:!1})},c.sendCommand=function(t){t.preventDefault(),c.cmdIsValid()?(c.setState({sentCmd:c.state.commandText}),fetch("/api/command",{method:"POST",body:JSON.stringify({text:c.state.commandText})}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)})),c.setState({commandText:""})):c.setState({commandText:""}),c.setState({cmdIsValid:!1})},c.cmdIsValid=function(){return c.state.commandText.length>0&&c.state.commandText.charAt(0)===c.state.botCommandToken},c.state={botName:"",botCommandToken:"",commandText:"",cmdInvalid:!0,invalidCmdText:"",sentCmd:""},c.updateCommandText=c.updateCommandText.bind(Object(_.a)(c)),c.sendCommand=c.sendCommand.bind(Object(_.a)(c)),c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){this.refreshBotDetails(this.props.url)}},{key:"render",value:function(){return Object(c.jsx)(P.a,{item:!0,xs:12,children:Object(c.jsx)(J,{elevation:3,children:Object(c.jsx)("form",{onSubmit:this.sendCommand,autoComplete:"off",children:Object(c.jsx)(F,{InputLabelProps:{className:"label-field"},variant:"outlined",value:this.state.commandText,type:"text",fullWidth:!0,onChange:this.updateCommandText,placeholder:"".concat(this.state.botCommandToken,"command ..."),label:!this.cmdIsValid()&&this.state.commandText.length>0?"Invalid command! Format: ".concat(this.state.botCommandToken,"command ..."):"Send commands to ".concat(this.state.botName," from here..."),error:this.state.commandText.charAt(0)!==this.state.botCommandToken&&this.state.commandText.length>0,InputProps:{endAdornment:"compact"===this.props.type?Object(c.jsx)(W,{component:"span",type:"submit",disabled:!this.cmdIsValid,onClick:this.sendCommand,children:Object(c.jsx)(S.a,{})}):Object(c.jsx)(H,{component:"span",endIcon:Object(c.jsx)(S.a,{}),type:"submit",variant:"contained",style:{width:"150px",height:"40px"},disabled:!this.cmdIsValid,onClick:this.sendCommand,children:"Send"})}})})})})}}]),n}(r.a.Component),E=n(207),U=n(208),V=n(162),R=n(209),q=n(210),z=n(211),Q=n(57),G=n(212),K=n(48),X=n.n(K),Y=n(231);function Z(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n"]);return Z=function(){return t},t}function $(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";   \n"]);return $=function(){return t},t}function tt(){var t=Object(u.a)(["\n    .tableHead {\n        background: ",";\n    }\n"]);return tt=function(){return t},t}function et(){var t=Object(u.a)(["\n    background-color: rgb(0,0,0,0);\n    color: ",";\n    &:hover {\n        background-color: ",";\n        color: ",";\n    }\n"]);return et=function(){return t},t}var nt=Object(l.c)(w.a)(et(),(function(t){return t.theme.text}),(function(t){return t.theme.accent_secondary}),(function(t){return t.theme.white})),ct=Object(l.c)(E.a)(tt(),(function(t){return t.theme.contrast2})),at=Object(l.c)(U.a)($(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),rt=Object(l.c)(Y.a)(Z(),(function(t){return t.theme.body}),(function(t){return t.theme.text})),ot=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).getCommandHistory=function(t){fetch("/api/cmdhistory",{headers:{Accept:"application/json","Content-Type":"application/json"}}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(e){c.setState({cmd_history:e.data.cmd_history}),t&&c.setState({showAlert:!0,alertMsg:"Successfully refreshed the command history list!",alertSeverity:"success"})})).catch((function(t){console.log(t),c.setState({cmd_history:[]}),c.setState({showAlert:!0,alertMsg:"Error retrieving the command history list!",alertSeverity:"error"})}))},c.closeAlert=function(){c.setState({showAlert:!1,alertMsg:"",alertSeverity:""})},c.state={showAlert:!1,alertMsg:"",alertSeverity:"",cmd_history:[]},c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){this.getCommandHistory(!1)}},{key:"componentDidUpdate",value:function(t,e){t.socketData.last_cmd_output!==this.props.socketData.last_cmd_output&&this.getCommandHistory(!1)}},{key:"render",value:function(){var t=this,e=this.state.showAlert?Object(c.jsx)(rt,{onClose:this.closeAlert,severity:this.state.alertSeverity,children:this.state.alertMsg}):"";return Object(c.jsxs)(P.a,{item:!0,xs:12,sm:4,children:[Object(c.jsx)(V.a,{in:this.state.showAlert,children:e}),Object(c.jsx)(R.a,{component:"span",children:Object(c.jsx)(A.a,{elevation:3,children:Object(c.jsxs)(ct,{className:"cmdTable",children:[Object(c.jsx)(q.a,{children:Object(c.jsx)(z.a,{children:Object(c.jsx)(at,{className:"tableHead",children:Object(c.jsxs)(Q.a,{variant:"body2",children:[Object(c.jsx)("b",{children:"Command History"}),Object(c.jsx)(nt,{id:"refreshCmdHistoryButton",onClick:function(){return t.getCommandHistory(!0)},size:"small",children:Object(c.jsx)(X.a,{})})]})})})}),Object(c.jsx)(G.a,{className:"tableBody",children:this.state.cmd_history.map((function(t,e){return Object(c.jsx)(z.a,{children:Object(c.jsx)(at,{component:"td",scope:"row",className:"cmdHistoryCmdCell",children:t})},t+e)}))})]})})})]})}}]),n}(r.a.Component),st=n(97),it=n.n(st);function ut(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";   \n"]);return ut=function(){return t},t}function lt(){var t=Object(u.a)(["\n    .tableHead {\n        background: ",";\n    }\n    .outTableBody {\n        height: 100px;\n        overflow: hide;\n    }\n"]);return lt=function(){return t},t}var ht=Object(l.c)(E.a)(lt(),(function(t){return t.theme.contrast2})),dt=Object(l.c)(U.a)(ut(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),jt=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).state={last_cmd_type:"",last_cmd:""},c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){0!==Object.keys(this.props.socketData).length&&this.setState({last_cmd:this.props.socketData.last_cmd_output,last_cmd_type:this.props.socketData.last_cmd_type})}},{key:"componentDidUpdate",value:function(t,e){t.socketData.last_cmd_output!==this.props.socketData.last_cmd_output&&this.setState({last_cmd:this.props.socketData.last_cmd_output,last_cmd_type:this.props.socketData.last_cmd_type})}},{key:"render",value:function(){return Object(c.jsx)(P.a,{item:!0,xs:12,sm:4,children:Object(c.jsx)(R.a,{component:"span",children:Object(c.jsx)(A.a,{elevation:3,children:Object(c.jsxs)(ht,{className:"cmdTable",children:[Object(c.jsx)(q.a,{children:Object(c.jsx)(z.a,{children:Object(c.jsx)(dt,{className:"tableHead",children:Object(c.jsx)(Q.a,{variant:"body2",children:Object(c.jsxs)("b",{children:["Latest Command Output ",this.state.last_cmd_type]})})})})}),Object(c.jsx)(G.a,{className:"tableBody",children:Object(c.jsx)(z.a,{children:Object(c.jsx)(dt,{className:"recentCmdCell",children:it()(this.state.last_cmd)})})})]})})})})}}]),n}(r.a.Component),bt=n(100),pt=n.n(bt),mt=n(215),ft=n(77),Ot=n.n(ft),xt=n(78),kt=n.n(xt),gt=n(213),vt=n(99),yt=n.n(vt),_t=n(98),Ct=n.n(_t),Tt=n(79),St=n.n(Tt);function Dt(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n    user-select: none;\n"]);return Dt=function(){return t},t}var wt=Object(l.c)(gt.a)(Dt(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),At=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(){return Object(p.a)(this,n),e.apply(this,arguments)}return Object(m.a)(n,[{key:"render",value:function(){var t=this,e=Object(c.jsx)(Ot.a,{}),a=Object(c.jsx)(kt.a,{});return this.props.users&&this.props.items&&(a=this.props.users.length>0||this.props.items.length>0?Object(c.jsx)(kt.a,{}):Object(c.jsx)(St.a,{}),e=this.props.users.length>0||this.props.items.length>0?Object(c.jsx)(Ot.a,{}):Object(c.jsx)(St.a,{})),Object(c.jsxs)(wt,{nodeId:this.props.node_id+"",label:this.props.item_label,expandIcon:a,collapseIcon:e,children:[this.props.users?this.props.users.map((function(e,n){return Object(c.jsx)(wt,{nodeId:t.props.node_id+n+"",label:Object(c.jsx)(Q.a,{variant:"subtitle2",gutterBottom:!0,noWrap:!0,children:e}),icon:t.props.bot_name===e?Object(c.jsx)(Ct.a,{}):Object(c.jsx)(yt.a,{})},"".concat(t.props.node_id+n,"-key"))})):"",this.props.items.map((function(e,a){return Object(c.jsx)(n,{node_id:a+t.props.node_id+1+"",items:e.subchannels,users:e.users,bot_name:t.props.bot_name,item_label:Object(c.jsx)(Q.a,{variant:"body2",gutterBottom:!0,noWrap:!0,children:e.channel_name})},"".concat(a+t.props.node_id+1,"-key"))}))]},"".concat(this.props.node_id,"-key"))}}]),n}(r.a.Component),Pt=n(214);function Nt(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";   \n"]);return Nt=function(){return t},t}function Bt(){var t=Object(u.a)(["\n    background: ",";\n    padding: 5em;\n    .tableHead {\n        background: ",";\n    }\n"]);return Bt=function(){return t},t}var Mt=Object(l.c)(E.a)(Bt(),(function(t){return t.theme.contrast}),(function(t){return t.theme.contrast2})),It=Object(l.c)(U.a)(Nt(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),Ft=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).useStyles=function(){return Object(Pt.a)({root:{height:500,flexGrow:1,maxWidth:400}})},c.refreshBotName=function(){fetch("/api/general/name",{headers:{Accept:"application/json","Content-Type":"application/json"}}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){c.setState({botName:t.data.name})})).catch((function(t){console.log(t),c.setState({botName:"N/A"})}))},c.max_expand=Array.from({length:256},(function(t,e){return e+1+""})),c.state={botName:"",list_hash:"",list_items:[]},c.classes=c.useStyles(),c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){Object.keys(this.props.socketData).length>0&&this.setState({list_items:this.props.socketData.server_hierarchy.hierarchy,list_hash:this.props.socketData.server_hierarchy.hash}),this.refreshBotName()}},{key:"componentDidUpdate",value:function(t,e){Object.keys(this.props.socketData).length>0&&t.socketData.server_hierarchy&&this.state.list_hash!==this.props.socketData.server_hierarchy.hash&&this.setState({list_items:this.props.socketData.server_hierarchy.hierarchy,list_hash:this.props.socketData.server_hierarchy.hash})}},{key:"render",value:function(){return Object(c.jsx)(P.a,{item:!0,xs:12,sm:4,children:Object(c.jsx)(R.a,{component:"span",children:Object(c.jsx)(A.a,{elevation:3,children:Object(c.jsxs)(Mt,{className:"cmdTable",children:[Object(c.jsx)(q.a,{children:Object(c.jsx)(z.a,{children:Object(c.jsx)(It,{className:"tableHead",children:Object(c.jsxs)(Q.a,{variant:"body2",children:[Object(c.jsx)("b",{children:"Channels"})," ",Object(c.jsx)(pt.a,{})]})})})}),Object(c.jsx)(G.a,{className:"tableBody",children:Object(c.jsx)(mt.a,{defaultExpanded:this.max_expand,children:Object(c.jsx)(At,{bot_name:this.state.botName,items:this.state.list_items,item_label:Object(c.jsx)(Q.a,{variant:"body2",gutterBottom:!0,noWrap:!0,children:"All Channels"}),node_id:1},"online-users-hierarchy-key")})})]})})})})}}]),n}(r.a.Component),Ht=n(101),Wt=n.n(Ht);function Jt(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n"]);return Jt=function(){return t},t}function Lt(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n    th {\n        background: ",";\n    }\n"]);return Lt=function(){return t},t}function Et(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n"]);return Et=function(){return t},t}function Ut(){var t=Object(u.a)(["\n    background-color: rgb(0,0,0,0);\n    color: ",";\n    &:hover {\n        background-color: ",";\n        color: ",";\n    }\n"]);return Ut=function(){return t},t}var Vt=Object(l.c)(w.a)(Ut(),(function(t){return t.theme.text}),(function(t){return t.theme.accent_secondary}),(function(t){return t.theme.white})),Rt=Object(l.c)(Y.a)(Et(),(function(t){return t.theme.body}),(function(t){return t.theme.text})),qt=Object(l.c)(E.a)(Lt(),(function(t){return t.theme.body}),(function(t){return t.theme.text}),(function(t){return t.theme.contrast2})),zt=Object(l.c)(U.a)(Jt(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),Qt=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).refreshPlugins=function(t,e){fetch(t,{headers:{Accept:"application/json","Content-Type":"application/json"}}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){c.setState({items:t.data.plugins}),e&&c.setState({showAlert:!0,alertMsg:"Successfully refreshed the plugins list!",alertSeverity:"success"})})).catch((function(t){console.log(t),c.setState({showAlert:!0,alertMsg:"Error retrieving the plugins list!",alertSeverity:"error"})}))},c.closeAlert=function(){c.setState({showAlert:!1,alertMsg:"",alertSeverity:""})},c.state={showAlert:!1,alertMsg:"",alertSeverity:"",items:[]},c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){this.refreshPlugins("/api/plugins",!1)}},{key:"render",value:function(){var t=this,e=this.state.showAlert?Object(c.jsx)(Rt,{onClose:this.closeAlert,severity:this.state.alertSeverity,children:this.state.alertMsg}):"";return Object(c.jsxs)(P.a,{item:!0,xs:12,children:[Object(c.jsx)(V.a,{in:this.state.showAlert,children:e}),Object(c.jsx)(R.a,{component:A.a,children:Object(c.jsxs)(qt,{children:[Object(c.jsx)(q.a,{children:Object(c.jsx)(z.a,{children:Object(c.jsxs)(zt,{component:"th",children:[Object(c.jsx)("b",{children:"Active Plugins:"}),Object(c.jsx)(Vt,{id:"refreshButton",onClick:function(){return t.refreshPlugins("/api/plugins",!0)},size:"small",children:Object(c.jsx)(X.a,{})})]})})}),Object(c.jsx)(G.a,{children:this.state.items.map((function(t){return Object(c.jsx)(z.a,{children:Object(c.jsx)(zt,{component:"td",scope:"row",children:t})},t)}))})]})})]})}}]),n}(r.a.Component),Gt=n(204),Kt=n(216),Xt=n(217),Yt=n(218),Zt=n(219),$t=n(223),te=n(104),ee=n.n(te),ne=n(102),ce=n.n(ne),ae=n(103),re=n.n(ae),oe=n(234);function se(){var t=Object(u.a)(["\n    color: ",";\n"]);return se=function(){return t},t}function ie(){var t=Object(u.a)(["\n    color: ",";\n"]);return ie=function(){return t},t}function ue(){var t=Object(u.a)(["\n    color: ",";\n"]);return ue=function(){return t},t}function le(){var t=Object(u.a)(["\n    color: ",";\n"]);return le=function(){return t},t}var he=Object(l.c)(ce.a)(le(),(function(t){return t.theme.accent_secondary})),de=Object(l.c)(re.a)(ue(),(function(t){return t.theme.text})),je=Object(l.c)(ee.a)(ie(),(function(t){return t.theme.text})),be=Object(l.c)(Q.a)(se(),(function(t){return t.theme.text})),pe=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(){var t;Object(p.a)(this,n);for(var c=arguments.length,a=new Array(c),r=0;r<c;r++)a[r]=arguments[r];return(t=e.call.apply(e,[this].concat(a))).removeTrack=function(){fetch("/api/removetrack",{method:"POST",body:JSON.stringify({text:"".concat(t.props.indexText)})}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},t.skipToTrack=function(){fetch("/api/skipto",{method:"POST",body:JSON.stringify({text:"".concat(t.props.indexText)})}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},t}return Object(m.a)(n,[{key:"render",value:function(){return Object(c.jsxs)(Kt.a,{children:[this.props.useIcon?Object(c.jsxs)(Xt.a,{children:[Object(c.jsx)(je,{}),this.props.indexText?Object(c.jsx)(be,{noWrap:!0,children:Object(c.jsx)("b",{children:this.props.indexText})}):""]}):"",Object(c.jsx)(Yt.a,{primary:this.props.primaryText?Object(c.jsx)(be,{variant:"body1",noWrap:!0,children:this.props.primaryText}):"N/A",secondary:this.props.secondaryText?Object(c.jsx)(be,{variant:"caption",noWrap:!0,children:Object(c.jsx)("a",{href:"".concat(this.props.secondaryText),target:"_blank",rel:"noopener noreferrer",children:this.props.secondaryText})}):null}),this.props.useButtons?Object(c.jsxs)(Zt.a,{children:[Object(c.jsx)(oe.a,{title:"Remove Track","aria-label":"delete-track-tooltip",children:Object(c.jsx)(w.a,{edge:"end","aria-label":"delete-track",onClick:this.removeTrack,children:Object(c.jsx)(he,{})})}),Object(c.jsx)(oe.a,{title:"Skip To Track","aria-label":"skip-track-tooltip",children:Object(c.jsx)(w.a,{edge:"end","aria-label":"skip-track",onClick:this.skipToTrack,children:Object(c.jsx)(de,{})})})]}):""]})}}]),n}(r.a.Component),me=n(220),fe=n(222),Oe=n(221),xe=n(106),ke=n.n(xe),ge=n(107),ve=n.n(ge),ye=n(108),_e=n.n(ye),Ce=n(109),Te=n.n(Ce),Se=n(110),De=n.n(Se);function we(){var t=Object(u.a)(["\n    color: ",";\n"]);return we=function(){return t},t}function Ae(){var t=Object(u.a)(["\n    color: ",";\n"]);return Ae=function(){return t},t}function Pe(){var t=Object(u.a)(["\n    flex: 1 0 auto;\n"]);return Pe=function(){return t},t}function Ne(){var t=Object(u.a)(["\n    \n"]);return Ne=function(){return t},t}function Be(){var t=Object(u.a)(["\n    display: flex;\n    justify-content: center;\n    paddingLeft: 1em;\n    paddingBottom: 1em;\n"]);return Be=function(){return t},t}function Me(){var t=Object(u.a)(["\n    display: block;\n    text-align: center;\n"]);return Me=function(){return t},t}function Ie(){var t=Object(u.a)(["\n    color: ",";\n"]);return Ie=function(){return t},t}function Fe(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n    display: block;\n    width: 500px;\n"]);return Fe=function(){return t},t}var He=Object(l.c)(me.a)(Fe(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),We=Object(l.c)(w.a)(Ie(),(function(t){return t.theme.text})),Je=l.c.div(Me()),Le=l.c.div(Be()),Ee=Object(l.c)(Oe.a)(Ne()),Ue=Object(l.c)(fe.a)(Pe()),Ve=Object(l.c)(X.a)(Ae(),(function(t){return t.theme.accent_secondary})),Re=Object(l.c)(X.a)(we(),(function(t){return t.theme.text})),qe=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).stopTrack=function(){fetch("/api/stop",{method:"POST"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},c.nextTrack=function(){fetch("/api/nexttrack",{method:"POST"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},c.togglePause=function(){"Paused"===c.state.status?fetch("/api/resume",{method:"POST"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)})):"Playing"===c.state.status&&fetch("/api/pause",{method:"POST"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},c.toggleLoop=function(){fetch("/api/loop",{method:"POST"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},c.shuffleQueue=function(){fetch("/api/shuffle",{method:"POST"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},c.state={audio_track:{},img_src:"",track_hash:"",status:"",looping:!1},c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){Object.keys(this.props.socketData).length>0&&this.props.socketData.audio_data&&this.setState({audio_track:this.props.socketData.audio_data.track,status:this.props.socketData.audio_data.status,looping:this.props.socketData.audio_data.loop,img_src:this.props.socketData.audio_data.img_uri_formatted,track_hash:this.props.socketData.audio_data.hash})}},{key:"componentDidUpdate",value:function(t,e){Object.keys(this.props.socketData).length>0&&t.socketData.audio_data.track&&this.state.track_hash!==this.props.socketData.audio_data.hash&&this.setState({audio_track:this.props.socketData.audio_data.track,status:this.props.socketData.audio_data.status,looping:this.props.socketData.audio_data.loop,img_src:this.props.socketData.audio_data.img_uri_formatted,track_hash:this.props.socketData.audio_data.hash})}},{key:"render",value:function(){return Object(c.jsxs)(He,{children:[Object(c.jsxs)(Je,{children:[Object(c.jsxs)(Ue,{children:[Object(c.jsx)(Q.a,{component:"h5",variant:"h5",noWrap:!0,children:this.state.audio_track.name||"No Track Available"}),Object(c.jsx)(Q.a,{component:"h5",variant:"subtitle1",noWrap:!0,children:"Paused"===this.state.status?"[PAUSED]":""})]}),Object(c.jsxs)(Le,{children:[Object(c.jsx)(oe.a,{title:"Stop and Clear Queue","aria-label":"stop-tooltip",children:Object(c.jsx)(We,{"aria-label":"stop",onClick:this.stopTrack,children:Object(c.jsx)(ke.a,{})})}),Object(c.jsx)(oe.a,{title:"".concat("Paused"===this.state.status?"Play":"Pause"),"aria-label":"play-tooltip",children:Object(c.jsx)(We,{"aria-label":"play/pause",onClick:this.togglePause,children:"Paused"===this.state.status?Object(c.jsx)(ve.a,{}):Object(c.jsx)(_e.a,{})})}),Object(c.jsx)(oe.a,{title:"Next Track","aria-label":"next-tooltip",children:Object(c.jsx)(We,{"aria-label":"next",onClick:this.nextTrack,children:Object(c.jsx)(Te.a,{})})}),Object(c.jsx)(oe.a,{title:"".concat(this.state.looping?"Disable":"Enable"," Looping"),"arial-label":"loop-tooltip",children:Object(c.jsx)(We,{"aria-label":"loop",onClick:this.toggleLoop,children:this.state.looping?Object(c.jsx)(Ve,{}):Object(c.jsx)(Re,{})})}),Object(c.jsx)(oe.a,{title:"Shuffle Queue","aria-label":"shuffle-tooltip",children:Object(c.jsx)(We,{"aria-label":"shuffle",onClick:this.shuffleQueue,children:Object(c.jsx)(De.a,{})})})]})]}),Object(c.jsx)(Ee,{style:{height:0,paddingTop:"56%"},image:this.state.img_src||"..."})]})}}]),n}(r.a.Component);function ze(){var t=Object(u.a)(["\n    color: ",";\n"]);return ze=function(){return t},t}function Qe(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n"]);return Qe=function(){return t},t}var Ge=Object(l.c)(Gt.a)(Qe(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),Ke=Object(l.c)(Q.a)(ze(),(function(t){return t.theme.text})),Xe=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).state={list_hash:"",track_list:[]},c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){Object.keys(this.props.socketData).length>0&&this.props.socketData.audio_data.queue&&this.setState({track_list:this.props.socketData.audio_data.queue,list_hash:this.props.socketData.audio_data.hash})}},{key:"componentDidUpdate",value:function(t,e){Object.keys(this.props.socketData).length>0&&t.socketData.audio_data&&this.state.list_hash!==this.props.socketData.audio_data.hash&&this.setState({track_list:this.props.socketData.audio_data.queue,list_hash:this.props.socketData.audio_data.hash})}},{key:"render",value:function(){var t=this;return Object(c.jsx)(P.a,{item:!0,xs:12,children:Object(c.jsxs)(Ge,{component:A.a,children:[Object(c.jsx)(Kt.a,{style:{display:"flex",justifyContent:"center"},children:Object(c.jsx)(qe,{socketData:this.props.socketData})}),Object(c.jsxs)(Kt.a,{children:[Object(c.jsx)(Xt.a,{children:Object(c.jsx)(Ke,{noWrap:!0,children:Object(c.jsx)("b",{children:"#"})})}),Object(c.jsx)(Yt.a,{primary:Object(c.jsx)(Ke,{variant:"body1",children:Object(c.jsx)("b",{children:"Track Name"})}),secondary:Object(c.jsx)(Ke,{variant:"caption",children:Object(c.jsx)("b",{children:"Track URL"})})}),Object(c.jsx)(Zt.a,{children:Object(c.jsx)(Ke,{children:Object(c.jsx)("b",{children:"Actions"})})})]}),Object(c.jsx)($t.a,{}),this.state.track_list.map((function(e,n){return Object(c.jsxs)(a.Fragment,{children:[Object(c.jsx)(pe,{indexText:n+"",primaryText:e.name,secondaryText:e.alt_uri,useButtons:!0,useIcon:!0}),t.props.useDividers?Object(c.jsx)($t.a,{}):""]})}))]})})}}]),n}(r.a.Component),Ye=n(224);function Ze(){var t=Object(u.a)(["\n    height: 100%;\n    width: 100%;\n"]);return Ze=function(){return t},t}function $e(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n    display: inline-block;\n    text-align: center;\n    width: 200px;\n    height: 50px;\n"]);return $e=function(){return t},t}var tn=Object(l.c)(me.a)($e(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),en=Object(l.c)(Ye.a)(Ze()),nn=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(){var t;Object(p.a)(this,n);for(var c=arguments.length,a=new Array(c),r=0;r<c;r++)a[r]=arguments[r];return(t=e.call.apply(e,[this].concat(a))).playClip=function(){fetch("/api/soundboard-play",{method:"POST",body:JSON.stringify({text:"".concat(t.props.clipName)})}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},t}return Object(m.a)(n,[{key:"render",value:function(){return Object(c.jsx)(tn,{component:A.a,children:Object(c.jsx)(oe.a,{title:this.props.clipName,children:Object(c.jsx)(en,{onClick:this.playClip,children:Object(c.jsx)(Q.a,{variant:"body1",noWrap:!0,children:this.props.clipName})})})})}}]),n}(r.a.Component);function cn(){var t=Object(u.a)(["\n    height: 100%;\n    width: 100%;\n"]);return cn=function(){return t},t}function an(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n    display: inline-block;\n    text-align: center;\n    width: 200px;\n    height: 50px;\n"]);return an=function(){return t},t}function rn(){var t=Object(u.a)(["\n    color: ",";\n"]);return rn=function(){return t},t}var on=Object(l.c)(Q.a)(rn(),(function(t){return t.theme.text})),sn=Object(l.c)(me.a)(an(),(function(t){return t.theme.contrast}),(function(t){return t.theme.text})),un=Object(l.c)(Ye.a)(cn()),ln=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).getSBClips=function(){fetch("/api/soundboardclips",{method:"GET"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){c.setState({clips:t.data.clips})})).catch((function(t){return console.log(t)}))},c.playRandomClip=function(){fetch("/api/soundboard-random",{method:"POST"}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){console.log(t.status)})).catch((function(t){return console.log(t)}))},c.state={clips:[]},c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){this.getSBClips()}},{key:"render",value:function(){var t="Misc";return Object(c.jsx)("div",{children:Object(c.jsxs)(a.Fragment,{children:[Object(c.jsx)(sn,{component:A.a,children:Object(c.jsx)(oe.a,{title:"Play Random Clip",children:Object(c.jsx)(un,{onClick:this.playRandomClip,children:Object(c.jsx)(Q.a,{variant:"body1",noWrap:!0,children:"Random Clip"})})})}),this.state.clips.map((function(e,n){return Object(c.jsxs)(a.Fragment,{children:[e.charAt(0).toLowerCase()!==t.charAt(0).toLowerCase()?Object(c.jsxs)("div",{children:[Object(c.jsx)("br",{}),Object(c.jsx)(on,{variant:"h5",children:t=e.charAt(0).toLowerCase()!==e.charAt(0).toUpperCase()?e.charAt(0).toUpperCase():"Misc"}),Object(c.jsx)("hr",{})]}):"",Object(c.jsx)(nn,{clipName:e},"".concat(e,"-").concat(n))]},"frag-".concat(e,"-").concat(n))}))]})})}}]),n}(r.a.Component),hn=n(70),dn=n(113),jn=n(230),bn=n(225),pn=n(229),mn=n(226),fn=n(227);function On(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n    display: flex;\n    justify-content: space-between;\n    *:focus {\n        outline: 0 !important;\n    }\n"]);return On=function(){return t},t}function xn(){var t=Object(u.a)(["\n    background-color: ",";\n    color: ",";\n"]);return xn=function(){return t},t}var kn=Object(l.c)(jn.a)(xn(),(function(t){return t.theme.body}),(function(t){return t.theme.text})),gn=Object(l.c)(bn.a)(On(),(function(t){return t.theme.body}),(function(t){return t.theme.text})),vn=function(t){var e=t.children,n=t.value,a=t.index,r=Object(dn.a)(t,["children","value","index"]);return Object(c.jsx)("div",Object(hn.a)(Object(hn.a)({role:"tabpanel",hidden:n!==a,id:"simple-tabpanel-".concat(a),"aria-labelledby":"simple-tab-".concat(a)},r),{},{children:n===a&&Object(c.jsx)(pn.a,{p:3,children:Object(c.jsx)(Q.a,{component:"span",children:e})})}))},yn=function(t){Object(f.a)(n,t);var e=Object(O.a)(n);function n(t){var c;return Object(p.a)(this,n),(c=e.call(this,t)).getBotName=function(){fetch("/api/general/name",{headers:{Accept:"application/json","Content-Type":"application/json"}}).then((function(t){return t.ok?t:Promise.reject(t)})).then((function(t){return t.json()})).then((function(t){return c.setState({title:"".concat(t.data.name," Dashboard")})})).catch((function(t){console.trace(t),c.setState({title:"JJMumbleBot Dashboard"})}))},c.state={value:0,title:"JJMumbleBot Dashboard"},c}return Object(m.a)(n,[{key:"componentDidMount",value:function(){this.getBotName()}},{key:"handleChange",value:function(t,e){this.setState({value:e})}},{key:"render",value:function(){var t=this;return Object(c.jsxs)("div",{className:"top-nav-bar",children:[Object(c.jsx)(mn.a,{position:"static",children:Object(c.jsxs)(gn,{children:[Object(c.jsx)(Q.a,{variant:"h6",children:this.state.title},"app-bar-text-key"),Object(c.jsx)(kn,{value:this.state.value,onChange:this.handleChange.bind(this),children:this.props.tabs.map((function(t,e){return Object(c.jsx)(fn.a,Object(hn.a)({label:"".concat(t.name)},function(t){return{id:"simple-tab-".concat(t),"aria-controls":"simple-tabpanel-".concat(t)}}(e)),"tab-".concat(t.name,"-").concat(e))}))},"app-bar-tabs-key"),this.props.themeToggle]},"tool-bar-key")},"app-bar-key"),this.props.tabs.map((function(e,n){return Object(c.jsx)(vn,{value:t.state.value,index:n,hidden:t.state.value!==n,children:Object(c.jsx)(P.a,{container:!0,spacing:3,direction:"row",alignItems:"flex-start",children:e.items.map((function(t){return t}))},"".concat(n,"-grid"))},"".concat(n,"-panel"))}))]},"top-nav-bar-key")}}]),n}(r.a.Component),_n=n(232),Cn=n(112),Tn=n.n(Cn),Sn=(n(152),n(111)),Dn=n.n(Sn);function wn(){var t=Object(u.a)(["\n  color: ",";\n"]);return wn=function(){return t},t}function An(){var t=Object(u.a)(["\n  background-color: ",";\n  color: ",";\n"]);return An=function(){return t},t}function Pn(){var t=Object(u.a)(["\n  background-color: ",";\n  color: ",";\n"]);return Pn=function(){return t},t}var Nn=Object(l.c)(Wt.a)(Pn(),(function(t){return t.theme.body}),(function(t){return t.theme.text})),Bn=Object(l.c)(Y.a)(An(),(function(t){return t.theme.black}),(function(t){return t.theme.white})),Mn=Object(l.c)(w.a)(wn(),(function(t){return t.theme.white}));var In=function(){var t=Object(a.useRef)(null),e=Object(a.useState)(!1),n=Object(i.a)(e,2),r=n[0],o=n[1],s=Object(a.useState)(""),u=Object(i.a)(s,2),h=u[0],p=u[1],m=Object(a.useState)({}),f=Object(i.a)(m,2),O=f[0],k=f[1],g=function(){var t=Object(a.useState)("light"),e=Object(i.a)(t,2),n=e[0],c=e[1],r=function(t){window.localStorage.setItem("theme",t),c(t)};return Object(a.useEffect)((function(){var t=window.localStorage.getItem("theme");t&&c(t)}),[]),[n,function(){r("light"===n?"dark":"light")}]}(),v=Object(i.a)(g,2),_=v[0],C=v[1],T="light"===_?j:b,S="light"===_?"Light Mode":"Dark Mode",D=Object(c.jsx)(y,{theme:_,themeText:S,toggleTheme:C});return Object(a.useEffect)((function(){t.current=new WebSocket(Dn.a.format({protocol:"https:"===window.location.protocol?"wss":"ws",hostname:window.location.hostname,port:window.location.port||7e3,pathname:"/ws",slashes:!0})),t.current.onerror=function(){o(!0),p("There was an error connecting to the web socket endpoint!")}}),[]),Object(a.useEffect)((function(){t.current.onmessage=function(t){k(JSON.parse(t.data))}}),[O]),Object(c.jsxs)(l.a,{theme:T,children:[Object(c.jsx)(x,{}),Object(c.jsx)(d,{}),Object(c.jsx)(_n.a,{anchorOrigin:{vertical:"top",horizontal:"center"},open:r,children:Object(c.jsx)(Bn,{severity:"error",action:Object(c.jsx)(Mn,{component:"span",size:"small",onClick:function(){window.location.reload(!1)},children:Object(c.jsx)(Tn.a,{})}),children:h})}),Object(c.jsx)(yn,{themeToggle:D,tabs:[{name:"Commands",items:[Object(c.jsx)(L,{},"main-cmd-form-key"),Object(c.jsx)(jt,{socketData:O},"latest-cmd-key"),Object(c.jsx)(ot,{socketData:O},"cmd-history-key"),Object(c.jsx)(Ft,{socketData:O},"online-users-key"),Object(c.jsx)(Qt,{},"plugins-list-key")]},{name:"Audio",items:[Object(c.jsx)(Xe,{socketData:O,useDividers:!0},"audio-track-list-key")]},{name:"Sound Board",items:[Object(c.jsx)(ln,{},"sound-board-list-key")]},{name:"Debug",items:[Object(c.jsx)(Nn,{src:O,iconStyle:"square",collapsed:2,displayDataTypes:!1,theme:"light"===_?{base00:"rgba(0, 0, 0, 0)",base01:"rgb(245, 245, 245)",base02:"#2e2e2e",base03:"#93a1a1",base04:"rgba(0, 0, 0, 0.3)",base05:"#586e75",base06:"#073642",base07:"#002b36",base08:"#d33682",base09:"#cb4b16",base0A:"#dc322f",base0B:"#859900",base0C:"#6c71c4",base0D:"#586e75",base0E:"#2aa198",base0F:"#268bd2"}:{base00:"rgba (0, 0, 0, 0)",base01:"#202020",base02:"#c2c2c2",base03:"#505050",base04:"#b0b0b0",base05:"#d0d0d0",base06:"#e0e0e0",base07:"#ffffff",base08:"#eb008a",base09:"#f29333",base0A:"#f8ca12",base0B:"#37b349",base0C:"#00aabb",base0D:"#0e5a94",base0E:"#b31e8d",base0F:"#7a2d00"}},"json-viewer")]}]})]})},Fn=function(t){t&&t instanceof Function&&n.e(3).then(n.bind(null,236)).then((function(e){var n=e.getCLS,c=e.getFID,a=e.getFCP,r=e.getLCP,o=e.getTTFB;n(t),c(t),a(t),r(t),o(t)}))};n(159);s.a.render(Object(c.jsx)(r.a.StrictMode,{children:Object(c.jsx)(In,{})}),document.getElementById("root")),Fn()}},[[160,1,2]]]);
//# sourceMappingURL=main.760ce4c4.chunk.js.map