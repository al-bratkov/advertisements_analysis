(()=>{var e,t,r,n,i={7349:e=>{e.exports={prefix:"uxs",windowClass:"UXS",windowSettings:"_uxsSettings",sessionId:"uxs_uid",event:"UXS_event",shownCampaignsEvents:"uxs_campaigns",iframeMessageType:"uxfb",auxiliaryComment:"UX Feedback Widget Script",sessionValue:"UXS_session_value",updatedTime:"UXS_updated_time",sessionCampaigns:"UXS_session_campaigns",eventCounts:"UXS_event_counts",pageCounts:"UXS_page_counts",brandName:"UX Feedback"}},4426:(e,t,r)=>{"use strict";r.d(t,{Z:()=>o});var n=r(7349),i=r.n(n);const o={LOCALIZATION:"ru",API_URL:"https://widget-api.uxfeedback.ru/v1",IMAGES_URL:"https://cdn3.uxfeedback.ru/i",PREFIX:i().prefix,WINDOW_CLASS:i().windowClass,WINDOW_SETTINGS:i().windowSettings,SESSION_ID:i().sessionId,EVENT:i().event,SHOWN_CAMPAIGNS_LS:i().shownCampaignsEvents,IFRAME_MESSAGE_TYPE:i().iframeMessageType,SESSION_VALUE:i().sessionValue,UPDATED_TIME:i().updatedTime,SESSION_CAMPAIGNS:i().sessionCampaigns,EVENT_COUNTS:i().eventCounts,PAGE_COUNTS:i().pageCounts,BRAND_NAME:i().brandName}}},o={};function s(e){var t=o[e];if(void 0!==t)return t.exports;var r=o[e]={exports:{}};return i[e](r,r.exports,s),r.exports}s.m=i,s.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return s.d(t,{a:t}),t},s.d=(e,t)=>{for(var r in t)s.o(t,r)&&!s.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},s.f={},s.e=e=>Promise.all(Object.keys(s.f).reduce(((t,r)=>(s.f[r](e,t),t)),[])),s.u=e=>"assets-3.1.0/"+e+"."+{249:"2064848b8ec3045d87d2",362:"ba2d084cd68b2aa98d77",444:"b63b3cd2d0ad8500deca",666:"7f20601f6a3553b35bb7"}[e]+".js",s.miniCssF=e=>"assets-3.1.0/"+e+"5f418f0c06fc725ec6af.css",s.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),s.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="widget:",s.l=(r,n,i,o)=>{if(e[r])e[r].push(n);else{var a,u;if(void 0!==i)for(var d=document.getElementsByTagName("script"),c=0;c<d.length;c++){var l=d[c];if(l.getAttribute("src")==r||l.getAttribute("data-webpack")==t+i){a=l;break}}a||(u=!0,(a=document.createElement("script")).charset="utf-8",a.timeout=120,s.nc&&a.setAttribute("nonce",s.nc),a.setAttribute("data-webpack",t+i),a.src=r,0!==a.src.indexOf(window.location.origin+"/")&&(a.crossOrigin="anonymous"),a.integrity=s.sriHashes[o],a.crossOrigin="anonymous"),e[r]=[n];var p=(t,n)=>{a.onerror=a.onload=null,clearTimeout(g);var i=e[r];if(delete e[r],a.parentNode&&a.parentNode.removeChild(a),i&&i.forEach((e=>e(n))),t)return t(n)},g=setTimeout(p.bind(null,void 0,{type:"timeout",target:a}),12e4);a.onerror=p.bind(null,a.onerror),a.onload=p.bind(null,a.onload),u&&document.head.appendChild(a)}},s.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e;s.g.importScripts&&(e=s.g.location+"");var t=s.g.document;if(!e&&t&&(t.currentScript&&(e=t.currentScript.src),!e)){var r=t.getElementsByTagName("script");r.length&&(e=r[r.length-1].src)}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),s.p=e})(),s.sriHashes={249:"sha384-eZDmxZ2jNE6RhB7hzpuRhUDCYR8yOnou2ldPrFsDQjPPDZWzNOpcUGmaC9DnBc14",362:"sha384-T0If/+HKNTGJhlLtu8ue4CRi/xLm+tu+Qooo4+s7eXxWkMffQGvmveNCwSh3lis9",444:"sha384-n4/uHlBHF4ZCNscDqMKIBwOoLjCKfHBt+441+0Ew3UFZGKp/t2/+L24mAhd1rt8b",666:"sha384-QtDynSimOaedibYXEBhHGMYQwZqdIC3hG8FRCnmNjqJY5Ei7lmizFRHJE1HeMkZl"},r=e=>new Promise(((t,r)=>{var n=s.miniCssF(e),i=s.p+n;if(((e,t)=>{for(var r=document.getElementsByTagName("link"),n=0;n<r.length;n++){var i=(s=r[n]).getAttribute("data-href")||s.getAttribute("href");if("stylesheet"===s.rel&&(i===e||i===t))return s}var o=document.getElementsByTagName("style");for(n=0;n<o.length;n++){var s;if((i=(s=o[n]).getAttribute("data-href"))===e||i===t)return s}})(n,i))return t();((e,t,r,n)=>{var i=document.createElement("link");i.rel="stylesheet",i.type="text/css",i.onerror=i.onload=o=>{if(i.onerror=i.onload=null,"load"===o.type)r();else{var s=o&&("load"===o.type?"missing":o.type),a=o&&o.target&&o.target.href||t,u=new Error("Loading CSS chunk "+e+" failed.\n("+a+")");u.code="CSS_CHUNK_LOAD_FAILED",u.type=s,u.request=a,i.parentNode.removeChild(i),n(u)}},i.href=t,0!==i.href.indexOf(window.location.origin+"/")&&(i.crossOrigin="anonymous"),document.head.appendChild(i)})(e,i,t,r)})),n={263:0},s.f.miniCss=(e,t)=>{n[e]?t.push(n[e]):0!==n[e]&&{362:1}[e]&&t.push(n[e]=r(e).then((()=>{n[e]=0}),(t=>{throw delete n[e],t})))},(()=>{var e={263:0};s.f.j=(t,r)=>{var n=s.o(e,t)?e[t]:void 0;if(0!==n)if(n)r.push(n[2]);else{var i=new Promise(((r,i)=>n=e[t]=[r,i]));r.push(n[2]=i);var o=s.p+s.u(t),a=new Error;s.l(o,(r=>{if(s.o(e,t)&&(0!==(n=e[t])&&(e[t]=void 0),n)){var i=r&&("load"===r.type?"missing":r.type),o=r&&r.target&&r.target.src;a.message="Loading chunk "+t+" failed.\n("+i+": "+o+")",a.name="ChunkLoadError",a.type=i,a.request=o,n[1](a)}}),"chunk-"+t,t)}};var t=(t,r)=>{var n,i,[o,a,u]=r,d=0;if(o.some((t=>0!==e[t]))){for(n in a)s.o(a,n)&&(s.m[n]=a[n]);u&&u(s)}for(t&&t(r);d<o.length;d++)i=o[d],s.o(e,i)&&e[i]&&e[i][0](),e[o[d]]=0},r=self.webpackChunkwidget=self.webpackChunkwidget||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})();var a={};(()=>{"use strict";s.r(a);var e=s(4426);!function(){const t=/Trident|MSIE/.test(navigator.userAgent),r=void 0!==window[e.Z.WINDOW_CLASS];t||r||function(t){t[e.Z.WINDOW_SETTINGS]||(t[e.Z.WINDOW_SETTINGS]={}),t[e.Z.WINDOW_CLASS]=new function(){const r=e.Z.WINDOW_SETTINGS,n=[];return{sendEvent:e=>{n.push(e)},getSentEvents:()=>n,addProperties:e=>{Object.hasOwnProperty.call(t[r],"properties")||(t[r].properties={}),t[r].properties={...t[r].properties,...e}},getProperties:()=>t[r].properties||{}}},Promise.all([s.e(249),s.e(444)]).then(s.bind(s,3444))}(window)}()})(),window.widget=a})();