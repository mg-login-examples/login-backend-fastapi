if(!self.define){let e,s={};const r=(r,o)=>(r=new URL(r+".js",o).href,s[r]||new Promise((s=>{if("document"in self){const e=document.createElement("script");e.src=r,e.onload=s,document.head.appendChild(e)}else e=r,importScripts(r),s()})).then((()=>{let e=s[r];if(!e)throw new Error(`Module ${r} didn’t register its module`);return e})));self.define=(o,t)=>{const i=e||("document"in self?document.currentScript.src:"")||location.href;if(s[i])return;let n={};const c=e=>r(e,i),l={module:{uri:i},exports:n,require:c};s[i]=Promise.all(o.map((e=>l[e]||c(e)))).then((e=>(t(...e),n)))}}define(["./workbox-79ffe3e0"],(function(e){"use strict";e.setCacheNameDetails({prefix:"password-reset"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/password-reset/css/app.3c3e42ab.css",revision:null},{url:"/password-reset/index.html",revision:"6f5c2f51682c81b3c7019ac18a04216b"},{url:"/password-reset/js/app.61d0a8a2.js",revision:null},{url:"/password-reset/js/chunk-vendors.169872e6.js",revision:null},{url:"/password-reset/manifest.json",revision:"43295ea5f0cf7dc0c3e81c7befc868ef"},{url:"/password-reset/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{})}));
//# sourceMappingURL=service-worker.js.map
