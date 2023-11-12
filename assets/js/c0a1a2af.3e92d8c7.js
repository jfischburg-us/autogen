"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[6473],{3905:(e,t,n)=>{n.d(t,{Zo:()=>u,kt:()=>d});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function s(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function o(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var c=r.createContext({}),l=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):s(s({},t),e)),n},u=function(e){var t=l(e.components);return r.createElement(c.Provider,{value:t},e.children)},g={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},p=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,i=e.originalType,c=e.parentName,u=o(e,["components","mdxType","originalType","parentName"]),p=l(n),d=a,f=p["".concat(c,".").concat(d)]||p[d]||g[d]||i;return n?r.createElement(f,s(s({ref:t},u),{},{components:n})):r.createElement(f,s({ref:t},u))}));function d(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var i=n.length,s=new Array(i);s[0]=p;var o={};for(var c in t)hasOwnProperty.call(t,c)&&(o[c]=t[c]);o.originalType=e,o.mdxType="string"==typeof e?e:a,s[1]=o;for(var l=2;l<i;l++)s[l]=n[l];return r.createElement.apply(null,s)}return r.createElement.apply(null,n)}p.displayName="MDXCreateElement"},3037:(e,t,n)=>{n.r(t),n.d(t,{contentTitle:()=>s,default:()=>u,frontMatter:()=>i,metadata:()=>o,toc:()=>c});var r=n(7462),a=(n(7294),n(3905));const i={sidebar_label:"retrieve_assistant_agent",title:"agentchat.contrib.retrieve_assistant_agent"},s=void 0,o={unversionedId:"reference/agentchat/contrib/retrieve_assistant_agent",id:"reference/agentchat/contrib/retrieve_assistant_agent",isDocsHomePage:!1,title:"agentchat.contrib.retrieve_assistant_agent",description:"RetrieveAssistantAgent Objects",source:"@site/docs/reference/agentchat/contrib/retrieve_assistant_agent.md",sourceDirName:"reference/agentchat/contrib",slug:"/reference/agentchat/contrib/retrieve_assistant_agent",permalink:"/autogen/docs/reference/agentchat/contrib/retrieve_assistant_agent",editUrl:"https://github.com/microsoft/autogen/edit/main/website/docs/reference/agentchat/contrib/retrieve_assistant_agent.md",tags:[],version:"current",frontMatter:{sidebar_label:"retrieve_assistant_agent",title:"agentchat.contrib.retrieve_assistant_agent"},sidebar:"referenceSideBar",previous:{title:"math_user_proxy_agent",permalink:"/autogen/docs/reference/agentchat/contrib/math_user_proxy_agent"},next:{title:"retrieve_user_proxy_agent",permalink:"/autogen/docs/reference/agentchat/contrib/retrieve_user_proxy_agent"}},c=[{value:"RetrieveAssistantAgent Objects",id:"retrieveassistantagent-objects",children:[],level:2}],l={toc:c};function u(e){let{components:t,...n}=e;return(0,a.kt)("wrapper",(0,r.Z)({},l,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h2",{id:"retrieveassistantagent-objects"},"RetrieveAssistantAgent Objects"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"class RetrieveAssistantAgent(AssistantAgent)\n")),(0,a.kt)("p",null,"(Experimental) Retrieve Assistant agent, designed to solve a task with LLM."),(0,a.kt)("p",null,"RetrieveAssistantAgent is a subclass of AssistantAgent configured with a default system message.\nThe default system message is designed to solve a task with LLM,\nincluding suggesting python code blocks and debugging.\n",(0,a.kt)("inlineCode",{parentName:"p"},"human_input_mode"),' is default to "NEVER"\nand ',(0,a.kt)("inlineCode",{parentName:"p"},"code_execution_config")," is default to False.\nThis agent doesn't execute code by default, and expects the user to execute the code."))}u.isMDXComponent=!0}}]);