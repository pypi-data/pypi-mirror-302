"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7001],{281788:(e,t,a)=>{a.d(t,{B8:()=>d,TZ:()=>r,mf:()=>l,u7:()=>o});var n=a(431069),s=a(68492);const i=(e,t,a)=>{let n=`api/v1/dashboard/${e}/filter_state`;return t&&(n=n.concat(`/${t}`)),a&&(n=n.concat(`?tab_id=${a}`)),n},r=(e,t,a,r)=>n.Z.put({endpoint:i(e,a,r),jsonPayload:{value:t}}).then((e=>e.json.message)).catch((e=>(s.Z.error(e),null))),o=(e,t,a)=>n.Z.post({endpoint:i(e,void 0,a),jsonPayload:{value:t}}).then((e=>e.json.key)).catch((e=>(s.Z.error(e),null))),d=(e,t)=>n.Z.get({endpoint:i(e,t)}).then((({json:e})=>JSON.parse(e.value))).catch((e=>(s.Z.error(e),null))),l=e=>n.Z.get({endpoint:`/api/v1/dashboard/permalink/${e}`}).then((({json:e})=>e)).catch((e=>(s.Z.error(e),null)))},257001:(e,t,a)=>{a.r(t),a.d(t,{DashboardPage:()=>re,DashboardPageIdContext:()=>ne,default:()=>oe});var n=a(667294),s=a(211965),i=a(616550),r=a(751995),o=a(61988),d=a(828216),l=a(414114),c=a(838703),u=a(708743),p=a(904305),h=a(550810),f=a(514505),v=a(961337),g=a(427600),b=a(23525),m=a(909467),y=a(281788),w=a(14890),x=a(45697),E=a.n(x),_=a(593185),S=a(514278),C=a(920292),D=a(81255);function j(e){return Object.values(e).reduce(((e,t)=>(t&&t.type===D.dW&&t.meta&&t.meta.chartId&&e.push(t.meta.chartId),e)),[])}var I=a(602275),$=a(203741),O=a(599543),U=a(156967);const T=[D.dW,D.xh,D.t];function R(e){return!Object.values(e).some((({type:e})=>e&&T.includes(e)))}var k=a(11794),F=a(135944);const Z={actions:E().shape({addSliceToDashboard:E().func.isRequired,removeSliceFromDashboard:E().func.isRequired,triggerQuery:E().func.isRequired,logEvent:E().func.isRequired,clearDataMaskState:E().func.isRequired}).isRequired,dashboardInfo:I.$X.isRequired,dashboardState:I.DZ.isRequired,slices:E().objectOf(I.Rw).isRequired,activeFilters:E().object.isRequired,chartConfiguration:E().object,datasources:E().object.isRequired,ownDataCharts:E().object.isRequired,layout:E().object.isRequired,impressionId:E().string.isRequired,timeout:E().number,userId:E().string};class q extends n.PureComponent{static onBeforeUnload(e){e?window.addEventListener("beforeunload",q.unload):window.removeEventListener("beforeunload",q.unload)}static unload(){const e=(0,o.t)("You have unsaved changes.");return window.event.returnValue=e,e}constructor(e){var t,a;super(e),this.appliedFilters=null!=(t=e.activeFilters)?t:{},this.appliedOwnDataCharts=null!=(a=e.ownDataCharts)?a:{},this.onVisibilityChange=this.onVisibilityChange.bind(this)}componentDidMount(){const e=(0,C.Z)(),{dashboardState:t,layout:a}=this.props,n={is_soft_navigation:$.Yd.timeOriginOffset>0,is_edit_mode:t.editMode,mount_duration:$.Yd.getTimestamp(),is_empty:R(a),is_published:t.isPublished,bootstrap_data_length:e.length},s=(0,U.Z)();s&&(n.target_id=s),this.props.actions.logEvent($.Wl,n),"hidden"===document.visibilityState&&(this.visibilityEventData={start_offset:$.Yd.getTimestamp(),ts:(new Date).getTime()}),window.addEventListener("visibilitychange",this.onVisibilityChange),this.applyCharts()}componentDidUpdate(){this.applyCharts()}UNSAFE_componentWillReceiveProps(e){const t=j(this.props.layout),a=j(e.layout);this.props.dashboardInfo.id===e.dashboardInfo.id&&(t.length<a.length?a.filter((e=>-1===t.indexOf(e))).forEach((t=>{return this.props.actions.addSliceToDashboard(t,(a=e.layout,n=t,Object.values(a).find((e=>e&&e.type===D.dW&&e.meta&&e.meta.chartId===n))));var a,n})):t.length>a.length&&t.filter((e=>-1===a.indexOf(e))).forEach((e=>this.props.actions.removeSliceFromDashboard(e))))}applyCharts(){const{hasUnsavedChanges:e,editMode:t}=this.props.dashboardState,{appliedFilters:a,appliedOwnDataCharts:n}=this,{activeFilters:s,ownDataCharts:i,chartConfiguration:r}=this.props;(0,_.cr)(_.TT.DashboardCrossFilters)&&!r||(t||(0,O.JB)(n,i,{ignoreUndefined:!0})&&(0,O.JB)(a,s,{ignoreUndefined:!0})||this.applyFilters(),e?q.onBeforeUnload(!0):q.onBeforeUnload(!1))}componentWillUnmount(){window.removeEventListener("visibilitychange",this.onVisibilityChange),this.props.actions.clearDataMaskState()}onVisibilityChange(){if("hidden"===document.visibilityState)this.visibilityEventData={start_offset:$.Yd.getTimestamp(),ts:(new Date).getTime()};else if("visible"===document.visibilityState){const e=this.visibilityEventData.start_offset;this.props.actions.logEvent($.Ev,{...this.visibilityEventData,duration:$.Yd.getTimestamp()-e})}}applyFilters(){const{appliedFilters:e}=this,{activeFilters:t,ownDataCharts:a,datasources:n,slices:s}=this.props,i=Object.keys(t),r=Object.keys(e),o=new Set(i.concat(r)),d=((e,t)=>{const a=Object.keys(e),n=Object.keys(t),s=(i=a,r=n,[...i.filter((e=>!r.includes(e))),...r.filter((e=>!i.includes(e)))]).filter((a=>e[a]||t[a]));var i,r;return new Set([...a,...n]).forEach((a=>{(0,O.JB)(e[a],t[a])||s.push(a)})),[...new Set(s)]})(a,this.appliedOwnDataCharts);[...o].forEach((a=>{if(!i.includes(a)&&r.includes(a))d.push(...(0,k.H)(e,t,s,n)[a]);else if(r.includes(a)){if((0,O.JB)(e[a].values,t[a].values,{ignoreUndefined:!0})||d.push(...(0,k.H)(t,e,s,n)[a]),!(0,O.JB)(e[a].scope,t[a].scope)){const n=(t[a].scope||[]).concat(e[a].scope||[]);d.push(...n)}}else d.push(...(0,k.H)(t,e,s,n)[a])})),this.refreshCharts([...new Set(d)]),this.appliedFilters=t,this.appliedOwnDataCharts=a}refreshCharts(e){e.forEach((e=>{this.props.actions.triggerQuery(!0,e)}))}render(){return this.context.loading?(0,F.tZ)(c.Z,{}):this.props.children}}q.contextType=S.Zn,q.propTypes=Z,q.defaultProps={timeout:60,userId:""};const L=q;var M=a(452256),P=a(797381),B=a(643399),J=a(987915),Q=a(174599);const Y=(0,d.$j)((function(e){var t,a,n,s;const{datasources:i,sliceEntities:r,dataMask:o,dashboardInfo:d,dashboardState:l,dashboardLayout:c,impressionId:u,nativeFilters:p}=e;return{timeout:null==(t=d.common)||null==(a=t.conf)?void 0:a.SUPERSET_WEBSERVER_TIMEOUT,userId:d.userId,dashboardInfo:d,dashboardState:l,datasources:i,activeFilters:{...(0,B.De)(),...(0,J.g)({chartConfiguration:null==(n=d.metadata)?void 0:n.chart_configuration,nativeFilters:p.filters,dataMask:o,allSliceIds:l.sliceIds})},chartConfiguration:null==(s=d.metadata)?void 0:s.chart_configuration,ownDataCharts:(0,J.U)(o,"ownState"),slices:r.slices,layout:c.present,impressionId:u}}),(function(e){return{actions:(0,w.DE)({setDatasources:h.Fy,clearDataMaskState:Q.sh,addSliceToDashboard:m.Pi,removeSliceFromDashboard:m.rL,triggerQuery:M.triggerQuery,logEvent:P.logEvent},e)}}))(L);var N=a(964296);const z=e=>s.iv`
  body {
    h1 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xxl}px;
      letter-spacing: -0.2px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${3*e.gridUnit}px;
    }

    h2 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xl}px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    h3,
    h4,
    h5,
    h6 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.l}px;
      letter-spacing: 0.2px;
      margin-top: ${2*e.gridUnit}px;
      margin-bottom: ${e.gridUnit}px;
    }
  }
`,V=e=>s.iv`
  .header-title a {
    margin: ${e.gridUnit/2}px;
    padding: ${e.gridUnit/2}px;
  }
  .header-controls {
    &,
    &:hover {
      margin-top: ${e.gridUnit}px;
    }
  }
`,A=e=>s.iv`
  .filter-card-popover {
    width: 240px;
    padding: 0;
    border-radius: 4px;

    &.ant-popover-placement-bottom {
      padding-top: ${e.gridUnit}px;
    }

    &.ant-popover-placement-left {
      padding-right: ${3*e.gridUnit}px;
    }

    .ant-popover-inner {
      box-shadow: 0 0 8px rgb(0 0 0 / 10%);
    }

    .ant-popover-inner-content {
      padding: ${4*e.gridUnit}px;
    }

    .ant-popover-arrow {
      display: none;
    }
  }

  .filter-card-tooltip {
    &.ant-tooltip-placement-bottom {
      padding-top: 0;
      & .ant-tooltip-arrow {
        top: -13px;
      }
    }
  }
`,W=e=>s.iv`
  .ant-dropdown-menu.chart-context-menu {
    min-width: ${43*e.gridUnit}px;
  }
  .ant-dropdown-menu-submenu.chart-context-submenu {
    max-width: ${60*e.gridUnit}px;
    min-width: ${40*e.gridUnit}px;
  }
`,H=e=>s.iv`
  a,
  .ant-tabs-tabpane,
  .ant-tabs-tab-btn,
  .superset-button,
  .superset-button.ant-dropdown-trigger,
  .header-controls span {
    &:focus-visible {
      box-shadow: 0 0 0 2px ${e.colors.primary.dark1};
      border-radius: ${e.gridUnit/2}px;
      outline: none;
      text-decoration: none;
    }
    &:not(
        .superset-button,
        .ant-menu-item,
        a,
        .fave-unfave-icon,
        .ant-tabs-tabpane,
        .header-controls span
      ) {
      &:focus-visible {
        padding: ${e.gridUnit/2}px;
      }
    }
  }
`;var K=a(478718),X=a.n(K);const G={},ee=()=>{const e=(0,v.rV)(v.dR.DashboardExploreContext,{});return Object.fromEntries(Object.entries(e).filter((([,e])=>!e.isRedundant)))},te=(e,t)=>{const a=ee();(0,v.LS)(v.dR.DashboardExploreContext,{...a,[e]:t})},ae=({dashboardPageId:e})=>{const t=(0,d.v9)((({dashboardInfo:t,dashboardState:a,nativeFilters:n,dataMask:s})=>{var i,r,o;return{labelsColor:(null==(i=t.metadata)?void 0:i.label_colors)||G,labelsColorMap:(null==(r=t.metadata)?void 0:r.shared_label_colors)||G,colorScheme:null==a?void 0:a.colorScheme,chartConfiguration:(null==(o=t.metadata)?void 0:o.chart_configuration)||G,nativeFilters:Object.entries(n.filters).reduce(((e,[t,a])=>({...e,[t]:X()(a,["chartsInScope"])})),{}),dataMask:s,dashboardId:t.id,filterBoxFilters:(0,B.De)(),dashboardPageId:e}}),d.wU);return(0,n.useEffect)((()=>(te(e,t),()=>{te(e,{...t,isRedundant:!0})})),[t,e]),null},ne=(0,n.createContext)(""),se=(0,n.lazy)((()=>Promise.all([a.e(1216),a.e(6658),a.e(1323),a.e(7802),a.e(8573),a.e(876),a.e(981),a.e(9484),a.e(8109),a.e(1108),a.e(9820),a.e(3197),a.e(7317),a.e(8003),a.e(1090),a.e(9818),a.e(868),a.e(1006),a.e(4717),a.e(452)]).then(a.bind(a,578307)))),ie=document.title,re=({idOrSlug:e})=>{const t=(0,r.Fg)(),a=(0,d.I0)(),w=(0,i.k6)(),x=(0,n.useMemo)((()=>(0,N.x0)()),[]),E=(0,d.v9)((({dashboardInfo:e})=>e&&Object.keys(e).length>0)),{addDangerToast:_}=(0,l.e1)(),{result:S,error:C}=(0,u.QU)(e),{result:D,error:j}=(0,u.Es)(e),{result:I,error:$,status:O}=(0,u.JL)(e),U=(0,n.useRef)(!1),T=C||j,R=Boolean(S&&D),{dashboard_title:k,css:Z,id:q=0}=S||{};if((0,n.useEffect)((()=>{const e=()=>{const e=ee();(0,v.LS)(v.dR.DashboardExploreContext,{...e,[x]:{...e[x],isRedundant:!0}})};return window.addEventListener("beforeunload",e),()=>{window.removeEventListener("beforeunload",e)}}),[x]),(0,n.useEffect)((()=>{a((0,m.sL)(O))}),[a,O]),(0,n.useEffect)((()=>{q&&async function(){const e=(0,b.eY)(g.KD.permalinkKey),t=(0,b.eY)(g.KD.nativeFiltersKey),n=(0,b.eY)(g.KD.nativeFilters);let s,i=t||{};if(e){const t=await(0,y.mf)(e);t&&({dataMask:i,activeTabs:s}=t.state)}else t&&(i=await(0,y.B8)(q,t));n&&(i=n),R&&(U.current||(U.current=!0),a((0,p.Y)({history:w,dashboard:S,charts:D,activeTabs:s,dataMask:i})))}()}),[R]),(0,n.useEffect)((()=>(k&&(document.title=k),()=>{document.title=ie})),[k]),(0,n.useEffect)((()=>"string"==typeof Z?(0,f.Z)(Z):()=>{}),[Z]),(0,n.useEffect)((()=>{$?_((0,o.t)("Error loading chart datasources. Filters may not work correctly.")):a((0,h.Fy)(I))}),[_,I,$,a]),T)throw T;return R&&E?(0,F.BX)(F.HY,{children:[(0,F.tZ)(s.xB,{styles:[A(t),z(t),W(t),H(t),V(t),"",""]}),(0,F.tZ)(ae,{dashboardPageId:x}),(0,F.tZ)(ne.Provider,{value:x,children:(0,F.tZ)(Y,{children:(0,F.tZ)(se,{})})})]}):(0,F.tZ)(c.Z,{})},oe=re},987915:(e,t,a)=>{a.d(t,{U:()=>n,g:()=>s});const n=(e,t)=>Object.values(e).filter((e=>e[t])).reduce(((e,a)=>({...e,[a.id]:t?a[t]:a})),{}),s=({chartConfiguration:e,nativeFilters:t,dataMask:a,allSliceIds:n})=>{const s={};return Object.values(a).forEach((({id:a,extraFormData:i})=>{var r,o,d,l,c,u,p,h,f;const v=null!=(r=null!=(o=null!=(d=null==t||null==(l=t[a])?void 0:l.chartsInScope)?d:null==e||null==(c=e[a])||null==(u=c.crossFilters)?void 0:u.chartsInScope)?o:n)?r:[],g=null==t||null==(p=t[a])?void 0:p.filterType,b=null!=(h=null==t||null==(f=t[a])?void 0:f.targets)?h:v;s[a]={scope:v,filterType:g,targets:b,values:i}})),s}},11794:(e,t,a)=>{a.d(t,{H:()=>d});var n=a(355786),s=a(10916);function i(e){var t,a;const s=null!=(t=(0,n.Z)(null==e?void 0:e.groupby))?t:[],i=null!=(a=(0,n.Z)(null==e?void 0:e.all_columns))?a:[];return s.concat(i).some((e=>"string"!=typeof e&&void 0!==e.expressionType))}function r(e,t,a,n){return Object.values(t).filter((t=>{var s,r,o;const{datasource:d,slice_id:l}=t;if(!a.includes(l))return!1;const c=d?n[d]:Object.values(n).find((e=>e.id===t.datasource_id)),{column:u,datasetId:p}=null!=(s=null==(r=e.targets)?void 0:r[0])?s:{},h=null!=(o=null==c?void 0:c.column_names)?o:[];return(null==c?void 0:c.id)===p||(!!i(t.form_data)||h.some((e=>e===(null==u?void 0:u.name)||e===(null==u?void 0:u.displayName))))})).map((e=>e.slice_id))}function o(e,t,a,n,s){var r,o;const d=a[e],l=null!=(r=null==t||null==(o=t.values)?void 0:o.filters)?r:[];if(!d)return[];const c=d.datasource?s[d.datasource]:Object.values(s).find((e=>e.id===d.datasource_id));return Object.values(a).filter((t=>{var a;if(t.slice_id===Number(e))return!1;if(!n.includes(t.slice_id))return!1;const r=t.datasource?s[t.datasource]:Object.values(s).find((e=>e.id===t.datasource_id));if(r===c)return!0;const o=null!=(a=null==r?void 0:r.column_names)?a:[];if(i(t.form_data))return!0;for(const e of l){if("string"!=typeof e.col&&void 0!==e.col.expressionType)return!0;if(o.includes(e.col))return!0}return!1})).map((e=>e.slice_id))}function d(e,t,a,n){return Object.entries(e).reduce(((e,[i,d])=>{var l;const c=Object.keys(a).includes(i)&&(0,s.w0)(d),u=Array.isArray(d.scope)?d.scope:null!=(l=d.chartsInScope)?l:[];if(c){var p,h,f,v;const s=null==t?void 0:t[i],r=d,l=(d.values&&void 0===d.values.filters||0===(null==(p=d.values)||null==(h=p.filters)?void 0:h.length))&&null!=s&&null!=(f=s.values)&&null!=(v=f.filters)&&v.length?s:r;return{...e,[i]:o(i,l,a,u,n)}}const g=d;return(0,s.A8)(g)||(0,s.kI)(g)?{...e,[i]:r(g,a,u,n)}:{...e,[i]:u}}),{})}},514505:(e,t,a)=>{function n(e){const t="CssEditor-css",a=document.head||document.getElementsByTagName("head")[0],n=document.querySelector(`.${t}`)||function(e){const t=document.createElement("style");return t.className=e,t.type="text/css",t}(t);return"styleSheet"in n?n.styleSheet.cssText=e:n.innerHTML=e,a.appendChild(n),function(){n.remove()}}a.d(t,{Z:()=>n})},708743:(e,t,a)=>{a.d(t,{schemaEndpoints:()=>_.Kt,CN:()=>n.CN,tableEndpoints:()=>E.QD,$O:()=>f,hb:()=>m,QU:()=>y,Es:()=>w,JL:()=>x,L8:()=>C,Xx:()=>_.Xx,SJ:()=>E.SJ,uY:()=>E.uY,zA:()=>E.zA});var n=a(845673),s=a(242190),i=a(667294),r=a(938325),o=a(610362);const d=o.h.injectEndpoints({endpoints:e=>({catalogs:e.query({providesTags:[{type:"Catalogs",id:"LIST"}],query:({dbId:e,forceRefresh:t})=>({endpoint:`/api/v1/database/${e}/catalogs/`,urlParams:{force:t},transformResponse:({json:e})=>e.result.sort().map((e=>({value:e,label:e,title:e})))}),serializeQueryArgs:({queryArgs:{dbId:e}})=>({dbId:e})})})}),{useLazyCatalogsQuery:l,useCatalogsQuery:c,endpoints:u,util:p}=d,h=[];function f(e){const{dbId:t,onSuccess:a,onError:n}=e||{},[s]=l(),o=c({dbId:t,forceRefresh:!1},{skip:!t}),d=(0,r.Z)(((e,t=!1)=>{!e||o.currentData&&!t||s({dbId:e,forceRefresh:t}).then((({isSuccess:e,isError:s,data:i})=>{e&&(null==a||a(i||h,t)),s&&(null==n||n())}))})),u=(0,i.useCallback)((()=>{d(t,!0)}),[t,d]);return(0,i.useEffect)((()=>{d(t,!1)}),[t,d]),{...o,refetch:u}}var v=a(115926);function g({owners:e}){return e?e.map((e=>`${e.first_name} ${e.last_name}`)):null}const b=a.n(v)().encode({columns:["owners.first_name","owners.last_name"],keys:["none"]});function m(e){return(0,s.l6)((0,s.s_)(`/api/v1/chart/${e}?q=${b}`),g)}const y=e=>(0,s.l6)((0,s.s_)(`/api/v1/dashboard/${e}`),(e=>({...e,metadata:e.json_metadata&&JSON.parse(e.json_metadata)||{},position_data:e.position_json&&JSON.parse(e.position_json),owners:e.owners||[]}))),w=e=>(0,s.s_)(`/api/v1/dashboard/${e}/charts`),x=e=>(0,s.s_)(`/api/v1/dashboard/${e}/datasets`);var E=a(123936),_=a(469279);const S=o.h.injectEndpoints({endpoints:e=>({queryValidations:e.query({providesTags:["QueryValidations"],query:({dbId:e,catalog:t,schema:a,sql:n,templateParams:s})=>{let i=s;try{i=JSON.parse(s||"")}catch(e){i=void 0}const r={catalog:t,schema:a,sql:n,...i&&{template_params:i}};return{method:"post",endpoint:`/api/v1/database/${e}/validate_sql/`,headers:{"Content-Type":"application/json"},body:JSON.stringify(r),transformResponse:({json:e})=>e.result}}})})}),{useQueryValidationsQuery:C}=S}}]);
//# sourceMappingURL=58943c540e77f48002bf.chunk.js.map