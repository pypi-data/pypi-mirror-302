"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[2424],{63956:(e,t,n)=>{n.d(t,{k:()=>j});var s=n(68866),o=n(80189),i=n(25269),a=n(58545),r=n(41681);const l=e=>"function"==typeof e,d=()=>null;function c(e){return void 0===e?d:l(e)?e:()=>e}function h(e,t,n){const s=l(e)?e:()=>e,o=c(t),i=c(n);return(e,t)=>s(e,t)?o(e,t):i(e,t)}var p=n(62564),g=n(17832),u=n(52865),m=n(12634),f=n(27002),b=n(21601),x=n(58201),v=n(61424),$=n(98242),y=n(30550),k=n(87206),C=n(13370);class w{constructor(e,t){this.cache=new WeakMap,this.ltr=e,this.rtl=t}bind(e){this.attach(e)}unbind(e){const t=this.cache.get(e);t&&k.o7.unsubscribe(t)}attach(e){const t=this.cache.get(e)||new F(this.ltr,this.rtl,e),n=k.o7.getValueFor(e);k.o7.subscribe(t),t.attach(n),this.cache.set(e,t)}}class F{constructor(e,t,n){this.ltr=e,this.rtl=t,this.source=n,this.attached=null}handleChange({target:e,token:t}){this.attach(t.getValueFor(e))}attach(e){this.attached!==this[e]&&(null!==this.attached&&this.source.$fastController.removeStyles(this.attached),this.attached=this[e],null!==this.attached&&this.source.$fastController.addStyles(this.attached))}}const I=m.j`(((${k.nf} + ${k.hV}) * 0.5 + 2) * ${k._5})`,T=m.i`
  .expand-collapse-glyph {
    transform: rotate(0deg);
  }
  :host(.nested) .expand-collapse-button {
    left: var(
      --expand-collapse-button-nested-width,
      calc(
        (
            ${I} +
              ((${k.nf} + ${k.hV}) * 1.25)
          ) * -1px
      )
    );
  }
  :host([selected])::after {
    left: calc(${k.vx} * 1px);
  }
  :host([expanded]) > .positioning-region .expand-collapse-glyph {
    transform: rotate(90deg);
  }
`,E=m.i`
  .expand-collapse-glyph {
    transform: rotate(180deg);
  }
  :host(.nested) .expand-collapse-button {
    right: var(
      --expand-collapse-button-nested-width,
      calc(
        (
            ${I} +
              ((${k.nf} + ${k.hV}) * 1.25)
          ) * -1px
      )
    );
  }
  :host([selected])::after {
    right: calc(${k.vx} * 1px);
  }
  :host([expanded]) > .positioning-region .expand-collapse-glyph {
    transform: rotate(90deg);
  }
`,L=f.DesignToken.create("tree-item-expand-collapse-hover").withDefault((e=>{const t=k.DF.getValueFor(e);return t.evaluate(e,t.evaluate(e).hover).hover})),O=f.DesignToken.create("tree-item-expand-collapse-selected-hover").withDefault((e=>{const t=k.At.getValueFor(e);return k.DF.getValueFor(e).evaluate(e,t.evaluate(e).rest).hover}));class S extends o.k{}const H=S.compose({baseName:"tree-item",baseClass:o.k,template:(e,t)=>i.d`
    <template
        role="treeitem"
        slot="${e=>e.isNestedItem()?"item":void 0}"
        tabindex="-1"
        class="${e=>e.expanded?"expanded":""} ${e=>e.selected?"selected":""} ${e=>e.nested?"nested":""}
            ${e=>e.disabled?"disabled":""}"
        aria-expanded="${e=>e.childItems&&e.childItemLength()>0?e.expanded:void 0}"
        aria-selected="${e=>e.selected}"
        aria-disabled="${e=>e.disabled}"
        @focusin="${(e,t)=>e.handleFocus(t.event)}"
        @focusout="${(e,t)=>e.handleBlur(t.event)}"
        ${(0,a.p)({property:"childItems",filter:(0,r.R)()})}
    >
        <div class="positioning-region" part="positioning-region">
            <div class="content-region" part="content-region">
                ${h((e=>e.childItems&&e.childItemLength()>0),i.d`
                        <div
                            aria-hidden="true"
                            class="expand-collapse-button"
                            part="expand-collapse-button"
                            @click="${(e,t)=>e.handleExpandCollapseButtonClick(t.event)}"
                            ${(0,p.i)("expandCollapseButton")}
                        >
                            <slot name="expand-collapse-glyph">
                                ${t.expandCollapseGlyph||""}
                            </slot>
                        </div>
                    `)}
                ${(0,u.m9)(e,t)}
                <slot></slot>
                ${(0,u.LC)(e,t)}
            </div>
        </div>
        ${h((e=>e.childItems&&e.childItemLength()>0&&(e.expanded||e.renderCollapsedChildren)),i.d`
                <div role="group" class="items" part="items">
                    <slot name="item" ${(0,g.Q)("items")}></slot>
                </div>
            `)}
    </template>
`,styles:(e,t)=>m.i`
    /**
     * This animation exists because when tree item children are conditionally loaded
     * there is a visual bug where the DOM exists but styles have not yet been applied (essentially FOUC).
     * This subtle animation provides a ever so slight timing adjustment for loading that solves the issue.
     */
    @keyframes treeItemLoading {
      0% {
        opacity: 0;
      }
      100% {
        opacity: 1;
      }
    }

    ${(0,b.j)("block")} :host {
      contain: content;
      position: relative;
      outline: none;
      color: ${k.hY};
      background: ${k.jq};
      cursor: pointer;
      font-family: ${k.SV};
      --tree-item-nested-width: 0;
    }

    :host(:focus) > .positioning-region {
      outline: none;
    }

    :host(:focus) .content-region {
      outline: none;
    }

    :host(:${x.b}) .positioning-region {
      border-color: ${k.D8};
      box-shadow: 0 0 0 calc((${k.vx} - ${k.H}) * 1px)
        ${k.D8} inset;
      color: ${k.hY};
    }

    .positioning-region {
      display: flex;
      position: relative;
      box-sizing: border-box;
      background: ${k.jq};
      border: transparent calc(${k.H} * 1px) solid;
      border-radius: calc(${k.UW} * 1px);
      height: calc((${C.i} + 1) * 1px);
    }

    .positioning-region::before {
      content: '';
      display: block;
      width: var(--tree-item-nested-width);
      flex-shrink: 0;
    }

    :host(:not([disabled])) .positioning-region:hover {
      background: ${k.Qp};
    }

    :host(:not([disabled])) .positioning-region:active {
      background: ${k.sG};
    }

    .content-region {
      display: inline-flex;
      align-items: center;
      white-space: nowrap;
      width: 100%;
      min-width: 0;
      height: calc(${C.i} * 1px);
      margin-inline-start: calc(${k._5} * 2px + 8px);
      font-size: ${k.cS};
      line-height: ${k.RU};
      font-weight: 400;
    }

    .items {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      font-size: calc(1em + (${k._5} + 16) * 1px);
    }

    .expand-collapse-button {
      background: none;
      border: none;
      outline: none;
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: calc(${I} * 1px);
      height: calc(${I} * 1px);
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      margin-left: 6px;
      margin-right: 6px;
    }

    .expand-collapse-glyph {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: calc((16 + ${k.hV}) * 1px);
      height: calc((16 + ${k.hV}) * 1px);
      transition: transform 0.1s linear;

      pointer-events: none;
      fill: currentcolor;
    }

    .start,
    .end {
      display: flex;
      fill: currentcolor;
    }

    ::slotted(svg) {
      /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
      width: 16px;
      height: 16px;

      /* Something like that would do if the typography is adaptive
      font-size: inherit;
      width: ${k.Pw};
      height: ${k.Pw};
      */
    }

    .start {
      /* TODO: horizontalSpacing https://github.com/microsoft/fast/issues/2766 */
      margin-inline-end: calc(${k._5} * 2px + 2px);
    }

    .end {
      /* TODO: horizontalSpacing https://github.com/microsoft/fast/issues/2766 */
      margin-inline-start: calc(${k._5} * 2px + 2px);
    }

    :host([expanded]) > .items {
      animation: treeItemLoading ease-in 10ms;
      animation-iteration-count: 1;
      animation-fill-mode: forwards;
    }

    :host([disabled]) .content-region {
      opacity: ${k.VF};
      cursor: ${v.H};
    }

    :host(.nested) .content-region {
      position: relative;
      /* Add left margin to collapse button size */
      margin-inline-start: calc(
        (
            ${I} +
              ((${k.nf} + ${k.hV}) * 1.25)
          ) * 1px
      );
    }

    :host(.nested) .expand-collapse-button {
      position: absolute;
    }

    :host(.nested:not([disabled])) .expand-collapse-button:hover {
      background: ${L};
    }

    :host([selected]) .positioning-region {
      background: ${k.wF};
    }

    :host([selected]:not([disabled])) .positioning-region:hover {
      background: ${k.Xi};
    }

    :host([selected]:not([disabled])) .positioning-region:active {
      background: ${k.Gy};
    }

    :host([selected]:not([disabled])) .expand-collapse-button:hover {
      background: ${O};
    }

    :host([selected])::after {
      /* The background needs to be calculated based on the selected background state
         for this control. We currently have no way of changing that, so setting to
         accent-foreground-rest for the time being */
      background: ${k.go};
      border-radius: calc(${k.UW} * 1px);
      content: '';
      display: block;
      position: absolute;
      top: calc((${C.i} / 4) * 1px);
      width: 3px;
      height: calc((${C.i} / 2) * 1px);
    }

    ::slotted(${e.tagFor(o.k)}) {
      --tree-item-nested-width: 1em;
      --expand-collapse-button-nested-width: calc(
        (
            ${I} +
              ((${k.nf} + ${k.hV}) * 1.25)
          ) * -1px
      );
    }
  `.withBehaviors(new w(T,E),(0,$.vF)(m.i`
      :host {
        forced-color-adjust: none;
        border-color: transparent;
        background: ${y.H.Field};
        color: ${y.H.FieldText};
      }
      :host .content-region .expand-collapse-glyph {
        fill: ${y.H.FieldText};
      }
      :host .positioning-region:hover,
      :host([selected]) .positioning-region {
        background: ${y.H.Highlight};
      }
      :host .positioning-region:hover .content-region,
      :host([selected]) .positioning-region .content-region {
        color: ${y.H.HighlightText};
      }
      :host .positioning-region:hover .content-region .expand-collapse-glyph,
      :host .positioning-region:hover .content-region .start,
      :host .positioning-region:hover .content-region .end,
      :host([selected]) .content-region .expand-collapse-glyph,
      :host([selected]) .content-region .start,
      :host([selected]) .content-region .end {
        fill: ${y.H.HighlightText};
      }
      :host([selected])::after {
        background: ${y.H.Field};
      }
      :host(:${x.b}) .positioning-region {
        border-color: ${y.H.FieldText};
        box-shadow: 0 0 0 2px inset ${y.H.Field};
        color: ${y.H.FieldText};
      }
      :host([disabled]) .content-region,
      :host([disabled]) .positioning-region:hover .content-region {
        opacity: 1;
        color: ${y.H.GrayText};
      }
      :host([disabled]) .content-region .expand-collapse-glyph,
      :host([disabled]) .content-region .start,
      :host([disabled]) .content-region .end,
      :host([disabled])
        .positioning-region:hover
        .content-region
        .expand-collapse-glyph,
      :host([disabled]) .positioning-region:hover .content-region .start,
      :host([disabled]) .positioning-region:hover .content-region .end {
        fill: ${y.H.GrayText};
      }
      :host([disabled]) .positioning-region:hover {
        background: ${y.H.Field};
      }
      .expand-collapse-glyph,
      .start,
      .end {
        fill: ${y.H.FieldText};
      }
      :host(.nested) .expand-collapse-button:hover {
        background: ${y.H.Field};
      }
      :host(.nested) .expand-collapse-button:hover .expand-collapse-glyph {
        fill: ${y.H.FieldText};
      }
    `)),expandCollapseGlyph:'\n        <svg\n            viewBox="0 0 16 16"\n            xmlns="http://www.w3.org/2000/svg"\n            class="expand-collapse-glyph"\n        >\n            <path\n                d="M5.00001 12.3263C5.00124 12.5147 5.05566 12.699 5.15699 12.8578C5.25831 13.0167 5.40243 13.1437 5.57273 13.2242C5.74304 13.3047 5.9326 13.3354 6.11959 13.3128C6.30659 13.2902 6.4834 13.2152 6.62967 13.0965L10.8988 8.83532C11.0739 8.69473 11.2153 8.51658 11.3124 8.31402C11.4096 8.11146 11.46 7.88966 11.46 7.66499C11.46 7.44033 11.4096 7.21853 11.3124 7.01597C11.2153 6.81341 11.0739 6.63526 10.8988 6.49467L6.62967 2.22347C6.48274 2.10422 6.30501 2.02912 6.11712 2.00691C5.92923 1.9847 5.73889 2.01628 5.56823 2.09799C5.39757 2.17969 5.25358 2.30817 5.153 2.46849C5.05241 2.62882 4.99936 2.8144 5.00001 3.00369V12.3263Z"\n            />\n        </svg>\n    '});var N=n(78156),V=n.n(N),D=n(4444);(0,s.W)().register(H());const j=(0,N.forwardRef)(((e,t)=>{const n=(0,N.useRef)(null),{className:s,expanded:o,selected:i,disabled:a,...r}=e;(0,D.O)(n,"expanded-change",e.onExpand),(0,D.O)(n,"selected-change",e.onSelect),(0,D.h)(n,"expanded",e.expanded),(0,D.h)(n,"selected",e.selected),(0,D.h)(n,"disabled",e.disabled),(0,N.useImperativeHandle)(t,(()=>n.current),[n.current]);let l=s??"";return n.current?.nested&&(l+=" nested"),V().createElement("jp-tree-item",{ref:n,...r,class:l.trim(),exportparts:e.exportparts,for:e.htmlFor,part:e.part,tabindex:e.tabIndex,style:{...e.style}},e.children)}))},55947:(e,t,n)=>{n.d(t,{L:()=>k});var s=n(68866),o=n(95185),i=n(91211),a=n(98332),r=n(92221),l=n(27081),d=n(99415),c=n(80189),h=n(50755);class p extends h.I{constructor(){super(...arguments),this.currentFocused=null,this.handleFocus=e=>{if(!(this.slottedTreeItems.length<1))return e.target===this?(null===this.currentFocused&&(this.currentFocused=this.getValidFocusableItem()),void(null!==this.currentFocused&&c.k.focusItem(this.currentFocused))):void(this.contains(e.target)&&(this.setAttribute("tabindex","-1"),this.currentFocused=e.target))},this.handleBlur=e=>{e.target instanceof HTMLElement&&(null===e.relatedTarget||!this.contains(e.relatedTarget))&&this.setAttribute("tabindex","0")},this.handleKeyDown=e=>{if(e.defaultPrevented)return;if(this.slottedTreeItems.length<1)return!0;const t=this.getVisibleNodes();switch(e.key){case l.tU:return void(t.length&&c.k.focusItem(t[0]));case l.Kh:return void(t.length&&c.k.focusItem(t[t.length-1]));case l.BE:if(e.target&&this.isFocusableElement(e.target)){const t=e.target;t instanceof c.k&&t.childItemLength()>0&&t.expanded?t.expanded=!1:t instanceof c.k&&t.parentElement instanceof c.k&&c.k.focusItem(t.parentElement)}return!1;case l.mr:if(e.target&&this.isFocusableElement(e.target)){const t=e.target;t instanceof c.k&&t.childItemLength()>0&&!t.expanded?t.expanded=!0:t instanceof c.k&&t.childItemLength()>0&&this.focusNextNode(1,e.target)}return;case l.iF:return void(e.target&&this.isFocusableElement(e.target)&&this.focusNextNode(1,e.target));case l.SB:return void(e.target&&this.isFocusableElement(e.target)&&this.focusNextNode(-1,e.target));case l.kL:return void this.handleClick(e)}return!0},this.handleSelectedChange=e=>{if(e.defaultPrevented)return;if(!(e.target instanceof Element&&(0,c.t)(e.target)))return!0;const t=e.target;t.selected?(this.currentSelected&&this.currentSelected!==t&&(this.currentSelected.selected=!1),this.currentSelected=t):t.selected||this.currentSelected!==t||(this.currentSelected=null)},this.setItems=()=>{const e=this.treeView.querySelector("[aria-selected='true']");this.currentSelected=e,null!==this.currentFocused&&this.contains(this.currentFocused)||(this.currentFocused=this.getValidFocusableItem()),this.nested=this.checkForNestedItems(),this.getVisibleNodes().forEach((e=>{(0,c.t)(e)&&(e.nested=this.nested)}))},this.isFocusableElement=e=>(0,c.t)(e),this.isSelectedElement=e=>e.selected}slottedTreeItemsChanged(){this.$fastController.isConnected&&this.setItems()}connectedCallback(){super.connectedCallback(),this.setAttribute("tabindex","0"),i.SO.queueUpdate((()=>{this.setItems()}))}handleClick(e){if(e.defaultPrevented)return;if(!(e.target instanceof Element&&(0,c.t)(e.target)))return!0;const t=e.target;t.disabled||(t.selected=!t.selected)}focusNextNode(e,t){const n=this.getVisibleNodes();if(!n)return;const s=n[n.indexOf(t)+e];(0,d.Re)(s)&&c.k.focusItem(s)}getValidFocusableItem(){const e=this.getVisibleNodes();let t=e.findIndex(this.isSelectedElement);return-1===t&&(t=e.findIndex(this.isFocusableElement)),-1!==t?e[t]:null}checkForNestedItems(){return this.slottedTreeItems.some((e=>(0,c.t)(e)&&e.querySelector("[role='treeitem']")))}getVisibleNodes(){return(0,d.UM)(this,"[role='treeitem']")||[]}}(0,o.gn)([(0,a.Lj)({attribute:"render-collapsed-nodes"})],p.prototype,"renderCollapsedNodes",void 0),(0,o.gn)([r.LO],p.prototype,"currentSelected",void 0),(0,o.gn)([r.LO],p.prototype,"slottedTreeItems",void 0);var g=n(25269),u=n(62564),m=n(17832),f=n(12634),b=n(21601);const x=class extends p{handleClick(e){if(e.defaultPrevented)return;if(!(e.target instanceof Element))return!0;let t=e.target;for(;t&&!(0,c.t)(t);)t=t.parentElement,t===this&&(t=null);t&&!t.disabled&&(t.selected=!0)}}.compose({baseName:"tree-view",baseClass:p,template:(e,t)=>g.d`
    <template
        role="tree"
        ${(0,u.i)("treeView")}
        @keydown="${(e,t)=>e.handleKeyDown(t.event)}"
        @focusin="${(e,t)=>e.handleFocus(t.event)}"
        @focusout="${(e,t)=>e.handleBlur(t.event)}"
        @click="${(e,t)=>e.handleClick(t.event)}"
        @selected-change="${(e,t)=>e.handleSelectedChange(t.event)}"
    >
        <slot ${(0,m.Q)("slottedTreeItems")}></slot>
    </template>
`,styles:(e,t)=>f.i`
  ${(0,b.j)("flex")} :host {
    flex-direction: column;
    align-items: stretch;
    min-width: fit-content;
    font-size: 0;
  }

  :host:focus-visible {
    outline: none;
  }
`});var v=n(78156),$=n.n(v),y=n(4444);(0,s.W)().register(x());const k=(0,v.forwardRef)(((e,t)=>{const n=(0,v.useRef)(null),{className:s,renderCollapsedNodes:o,currentSelected:i,...a}=e;return(0,v.useLayoutEffect)((()=>{n.current?.setItems()}),[n.current]),(0,y.h)(n,"currentSelected",e.currentSelected),(0,v.useImperativeHandle)(t,(()=>n.current),[n.current]),$().createElement("jp-tree-view",{ref:n,...a,class:e.className,exportparts:e.exportparts,for:e.htmlFor,part:e.part,tabindex:e.tabIndex,"render-collapsed-nodes":e.renderCollapsedNodes?"":void 0,style:{...e.style}},e.children)}))},80189:(e,t,n)=>{n.d(t,{k:()=>h,t:()=>c});var s=n(95185),o=n(98332),i=n(92221),a=n(99415),r=n(52865),l=n(89155),d=n(50755);function c(e){return(0,a.Re)(e)&&"treeitem"===e.getAttribute("role")}class h extends d.I{constructor(){super(...arguments),this.expanded=!1,this.focusable=!1,this.isNestedItem=()=>c(this.parentElement),this.handleExpandCollapseButtonClick=e=>{this.disabled||e.defaultPrevented||(this.expanded=!this.expanded)},this.handleFocus=e=>{this.setAttribute("tabindex","0")},this.handleBlur=e=>{this.setAttribute("tabindex","-1")}}expandedChanged(){this.$fastController.isConnected&&this.$emit("expanded-change",this)}selectedChanged(){this.$fastController.isConnected&&this.$emit("selected-change",this)}itemsChanged(e,t){this.$fastController.isConnected&&this.items.forEach((e=>{c(e)&&(e.nested=!0)}))}static focusItem(e){e.focusable=!0,e.focus()}childItemLength(){const e=this.childItems.filter((e=>c(e)));return e?e.length:0}}(0,s.gn)([(0,o.Lj)({mode:"boolean"})],h.prototype,"expanded",void 0),(0,s.gn)([(0,o.Lj)({mode:"boolean"})],h.prototype,"selected",void 0),(0,s.gn)([(0,o.Lj)({mode:"boolean"})],h.prototype,"disabled",void 0),(0,s.gn)([i.LO],h.prototype,"focusable",void 0),(0,s.gn)([i.LO],h.prototype,"childItems",void 0),(0,s.gn)([i.LO],h.prototype,"items",void 0),(0,s.gn)([i.LO],h.prototype,"nested",void 0),(0,s.gn)([i.LO],h.prototype,"renderCollapsedChildren",void 0),(0,l.e)(h,r.hW)}}]);