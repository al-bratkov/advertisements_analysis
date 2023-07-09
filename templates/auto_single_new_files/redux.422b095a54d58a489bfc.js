/*! For license information please see redux.422b095a54d58a489bfc.js.LICENSE.txt */
"use strict";(self["webpackChunkavito_desktop_site"]=self["webpackChunkavito_desktop_site"]||[]).push([[49685],{14890:function(r,t,n){n.r(t),n.d(t,{__DO_NOT_USE__ActionTypes:function(){return f},applyMiddleware:function(){return v},bindActionCreators:function(){return h},combineReducers:function(){return s},compose:function(){return l},createStore:function(){return a},legacy_createStore:function(){return p}});var e=n(1413);function o(r){return"Minified Redux error #"+r+"; visit https://redux.js.org/Errors?code="+r+" for the full message or "+"use the non-minified dev environment for full errors. "}var i="function"==typeof Symbol&&Symbol.observable||"@@observable",u=function(){return Math.random().toString(36).substring(7).split("").join(".")},f={INIT:"@@redux/INIT"+u(),REPLACE:"@@redux/REPLACE"+u(),PROBE_UNKNOWN_ACTION:function(){return"@@redux/PROBE_UNKNOWN_ACTION"+u()}};function c(r){if("object"!=typeof r||null===r)return!1;for(var t=r;null!==Object.getPrototypeOf(t);)t=Object.getPrototypeOf(t);return Object.getPrototypeOf(r)===t}function a(r,t,n){var e;if("function"==typeof t&&"function"==typeof n||"function"==typeof n&&"function"==typeof arguments[3])throw new Error(1?o(0):0);if("function"==typeof t&&void 0===n&&(n=t,t=void 0),void 0!==n){if("function"!=typeof n)throw new Error(1?o(1):0);return n(a)(r,t)}if("function"!=typeof r)throw new Error(1?o(2):0);var u=r,p=t,s=[],y=s,h=!1;function l(){y===s&&(y=s.slice())}function v(){if(h)throw new Error(1?o(3):0);return p}function w(r){if("function"!=typeof r)throw new Error(1?o(4):0);if(h)throw new Error(1?o(5):0);var t=!0;return l(),y.push(r),function(){if(t){if(h)throw new Error(1?o(6):0);t=!1,l();var n=y.indexOf(r);y.splice(n,1),s=null}}}function d(r){if(!c(r))throw new Error(1?o(7):0);if(void 0===r.type)throw new Error(1?o(8):0);if(h)throw new Error(1?o(9):0);try{h=!0,p=u(p,r)}finally{h=!1}for(var t=s=y,n=0;n<t.length;n++){(0,t[n])()}return r}function E(r){if("function"!=typeof r)throw new Error(1?o(10):0);u=r,d({type:f.REPLACE})}function b(){var r,t=w;return(r={subscribe:function(r){if("object"!=typeof r||null===r)throw new Error(1?o(11):0);function n(){r.next&&r.next(v())}return n(),{unsubscribe:t(n)}}})[i]=function(){return this},r}return d({type:f.INIT}),(e={dispatch:d,subscribe:w,getState:v,replaceReducer:E})[i]=b,e}var p=a;function s(r){for(var t=Object.keys(r),n={},e=0;e<t.length;e++){var i=t[e];"function"==typeof r[i]&&(n[i]=r[i])}var u,c=Object.keys(n);try{!function(r){Object.keys(r).forEach((function(t){var n=r[t];if(void 0===n(void 0,{type:f.INIT}))throw new Error(1?o(12):0);if(void 0===n(void 0,{type:f.PROBE_UNKNOWN_ACTION()}))throw new Error(1?o(13):0)}))}(n)}catch(a){u=a}return function(r,t){if(void 0===r&&(r={}),u)throw u;if(0);for(var e=!1,i={},f=0;f<c.length;f++){var a=c[f],p=n[a],s=r[a],y=p(s,t);if(void 0===y){t&&t.type;throw new Error(1?o(14):0)}i[a]=y,e=e||y!==s}return(e=e||c.length!==Object.keys(r).length)?i:r}}function y(r,t){return function(){return t(r.apply(this,arguments))}}function h(r,t){if("function"==typeof r)return y(r,t);if("object"!=typeof r||null===r)throw new Error(1?o(16):0);var n={};for(var e in r){var i=r[e];"function"==typeof i&&(n[e]=y(i,t))}return n}function l(){for(var r=arguments.length,t=new Array(r),n=0;n<r;n++)t[n]=arguments[n];return 0===t.length?function(r){return r}:1===t.length?t[0]:t.reduce((function(r,t){return function(){return r(t.apply(void 0,arguments))}}))}function v(){for(var r=arguments.length,t=new Array(r),n=0;n<r;n++)t[n]=arguments[n];return function(r){return function(){var n=r.apply(void 0,arguments),i=function(){throw new Error(1?o(15):0)},u={getState:n.getState,dispatch:function(){return i.apply(void 0,arguments)}},f=t.map((function(r){return r(u)}));return i=l.apply(void 0,f)(n.dispatch),(0,e.Z)((0,e.Z)({},n),{},{dispatch:i})}}}}}]);