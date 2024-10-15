"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[5430],{85430:(e,t,o)=>{o.d(t,{z:()=>s});var r=o(68866),a=o(69765),i=o(78156),n=o.n(i),l=o(4444);(0,r.W)().register((0,a.Vd)());const s=(0,i.forwardRef)(((e,t)=>{const o=(0,i.useRef)(null),{className:r,minimal:a,appearance:s,form:c,formaction:h,formenctype:p,formmethod:d,formtarget:u,type:b,autofocus:g,formnovalidate:y,defaultSlottedContent:f,disabled:v,required:m,...$}=e;return(0,l.h)(o,"autofocus",e.autofocus),(0,l.h)(o,"formnovalidate",e.formnovalidate),(0,l.h)(o,"defaultSlottedContent",e.defaultSlottedContent),(0,l.h)(o,"disabled",e.disabled),(0,l.h)(o,"required",e.required),(0,i.useImperativeHandle)(t,(()=>o.current),[o.current]),n().createElement("jp-button",{ref:o,...$,appearance:e.appearance,form:e.form,formaction:e.formaction,formenctype:e.formenctype,formmethod:e.formmethod,formtarget:e.formtarget,type:e.type,class:e.className,exportparts:e.exportparts,for:e.htmlFor,part:e.part,tabindex:e.tabIndex,minimal:e.minimal?"":void 0,style:{...e.style}},e.children)}))},69765:(e,t,o)=>{o.d(t,{Vd:()=>O});var r=o(82616),a=o(98332),i=o(95185),n=o(92221),l=o(14869),s=o(52865),c=o(89155),h=o(940),p=o(50755);class d extends p.I{}class u extends((0,h.Um)(d)){constructor(){super(...arguments),this.proxy=document.createElement("input")}}class b extends u{constructor(){super(...arguments),this.handleClick=e=>{var t;this.disabled&&(null===(t=this.defaultSlottedContent)||void 0===t?void 0:t.length)<=1&&e.stopPropagation()},this.handleSubmission=()=>{if(!this.form)return;const e=this.proxy.isConnected;e||this.attachProxy(),"function"==typeof this.form.requestSubmit?this.form.requestSubmit(this.proxy):this.proxy.click(),e||this.detachProxy()},this.handleFormReset=()=>{var e;null===(e=this.form)||void 0===e||e.reset()},this.handleUnsupportedDelegatesFocus=()=>{var e;window.ShadowRoot&&!window.ShadowRoot.prototype.hasOwnProperty("delegatesFocus")&&(null===(e=this.$fastController.definition.shadowOptions)||void 0===e?void 0:e.delegatesFocus)&&(this.focus=()=>{this.control.focus()})}}formactionChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.formAction=this.formaction)}formenctypeChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.formEnctype=this.formenctype)}formmethodChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.formMethod=this.formmethod)}formnovalidateChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.formNoValidate=this.formnovalidate)}formtargetChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.formTarget=this.formtarget)}typeChanged(e,t){this.proxy instanceof HTMLInputElement&&(this.proxy.type=this.type),"submit"===t&&this.addEventListener("click",this.handleSubmission),"submit"===e&&this.removeEventListener("click",this.handleSubmission),"reset"===t&&this.addEventListener("click",this.handleFormReset),"reset"===e&&this.removeEventListener("click",this.handleFormReset)}validate(){super.validate(this.control)}connectedCallback(){var e;super.connectedCallback(),this.proxy.setAttribute("type",this.type),this.handleUnsupportedDelegatesFocus();const t=Array.from(null===(e=this.control)||void 0===e?void 0:e.children);t&&t.forEach((e=>{e.addEventListener("click",this.handleClick)}))}disconnectedCallback(){var e;super.disconnectedCallback();const t=Array.from(null===(e=this.control)||void 0===e?void 0:e.children);t&&t.forEach((e=>{e.removeEventListener("click",this.handleClick)}))}}(0,i.gn)([(0,a.Lj)({mode:"boolean"})],b.prototype,"autofocus",void 0),(0,i.gn)([(0,a.Lj)({attribute:"form"})],b.prototype,"formId",void 0),(0,i.gn)([a.Lj],b.prototype,"formaction",void 0),(0,i.gn)([a.Lj],b.prototype,"formenctype",void 0),(0,i.gn)([a.Lj],b.prototype,"formmethod",void 0),(0,i.gn)([(0,a.Lj)({mode:"boolean"})],b.prototype,"formnovalidate",void 0),(0,i.gn)([a.Lj],b.prototype,"formtarget",void 0),(0,i.gn)([a.Lj],b.prototype,"type",void 0),(0,i.gn)([n.LO],b.prototype,"defaultSlottedContent",void 0);class g{}(0,i.gn)([(0,a.Lj)({attribute:"aria-expanded"})],g.prototype,"ariaExpanded",void 0),(0,i.gn)([(0,a.Lj)({attribute:"aria-pressed"})],g.prototype,"ariaPressed",void 0),(0,c.e)(g,l.v),(0,c.e)(b,s.hW,g);var y=o(25269),f=o(62564),v=o(17832),m=o(12634),$=o(61424),x=o(98242),H=o(30550),k=o(87206),L=o(21601),w=o(58201),T=o(13370);const C=m.i`
  ${(0,L.j)("inline-flex")} :host {
    font-family: ${k.SV};
    outline: none;
    font-size: ${k.cS};
    line-height: ${k.RU};
    height: calc(${T.i} * 1px);
    min-width: calc(${T.i} * 1px);
    background-color: ${k.wF};
    color: ${k.hY};
    border-radius: calc(${k.UW} * 1px);
    fill: currentcolor;
    cursor: pointer;
    margin: calc((${k.vx} + 2) * 1px);
  }

  .control {
    background: transparent;
    height: inherit;
    flex-grow: 1;
    box-sizing: border-box;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    padding: 0
      max(
        1px,
        calc((10 + (${k._5} * 2 * (${k.hV} + ${k.pR})))) * 1px
      );
    white-space: nowrap;
    outline: none;
    text-decoration: none;
    border: calc(${k.H} * 1px) solid transparent;
    color: inherit;
    border-radius: inherit;
    fill: inherit;
    cursor: inherit;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
  }

  :host(:hover) {
    background-color: ${k.Xi};
  }

  :host(:active) {
    background-color: ${k.Gy};
  }

  :host([aria-pressed='true']) {
    box-shadow: inset 0px 0px 2px 2px ${k.hP};
  }

  :host([minimal]),
  :host([scale='xsmall']) {
    --element-scale: -4;
  }

  :host([scale='small']) {
    --element-scale: -2;
  }

  :host([scale='medium']) {
    --element-scale: 0;
  }

  :host([scale='large']) {
    --element-scale: 2;
  }

  :host([scale='xlarge']) {
    --element-scale: 4;
  }

  /* prettier-ignore */
  .control:${w.b} {
      outline: calc(${k.vx} * 1px) solid ${k.Nz};
      outline-offset: 2px;
      -moz-outline-radius: 0px;
    }

  .control::-moz-focus-inner {
    border: 0;
  }

  .start,
  .end {
    display: flex;
  }

  .control.icon-only {
    padding: 0;
    line-height: 0;
  }

  ::slotted(svg) {
    ${""} width: 16px;
    height: 16px;
    pointer-events: none;
  }

  .start {
    margin-inline-end: 11px;
  }

  .end {
    margin-inline-start: 11px;
  }
`.withBehaviors((0,x.vF)(m.i`
    :host .control {
      background-color: ${H.H.ButtonFace};
      border-color: ${H.H.ButtonText};
      color: ${H.H.ButtonText};
      fill: currentColor;
    }

    :host(:hover) .control {
      forced-color-adjust: none;
      background-color: ${H.H.Highlight};
      color: ${H.H.HighlightText};
    }

    /* prettier-ignore */
    .control:${w.b} {
          forced-color-adjust: none;
          background-color: ${H.H.Highlight};
          outline-color: ${H.H.ButtonText};
          color: ${H.H.HighlightText};
        }

    .control:hover,
    :host([appearance='outline']) .control:hover {
      border-color: ${H.H.ButtonText};
    }

    :host([href]) .control {
      border-color: ${H.H.LinkText};
      color: ${H.H.LinkText};
    }

    :host([href]) .control:hover,
        :host([href]) .control:${w.b} {
      forced-color-adjust: none;
      background: ${H.H.ButtonFace};
      outline-color: ${H.H.LinkText};
      color: ${H.H.LinkText};
      fill: currentColor;
    }
  `)),j=m.i`
  :host([appearance='accent']) {
    background: ${k.Av};
    color: ${k.w4};
  }

  :host([appearance='accent']:hover) {
    background: ${k.OC};
    color: ${k.lJ};
  }

  :host([appearance='accent'][aria-pressed='true']) {
    box-shadow: inset 0px 0px 2px 2px ${k.VN};
  }

  :host([appearance='accent']:active) .control:active {
    background: ${k.UE};
    color: ${k.Pp};
  }

  :host([appearance="accent"]) .control:${w.b} {
    outline-color: ${k.D8};
  }
`.withBehaviors((0,x.vF)(m.i`
    :host([appearance='accent']) .control {
      forced-color-adjust: none;
      background: ${H.H.Highlight};
      color: ${H.H.HighlightText};
    }

    :host([appearance='accent']) .control:hover,
    :host([appearance='accent']:active) .control:active {
      background: ${H.H.HighlightText};
      border-color: ${H.H.Highlight};
      color: ${H.H.Highlight};
    }

    :host([appearance="accent"]) .control:${w.b} {
      outline-color: ${H.H.Highlight};
    }

    :host([appearance='accent'][href]) .control {
      background: ${H.H.LinkText};
      color: ${H.H.HighlightText};
    }

    :host([appearance='accent'][href]) .control:hover {
      background: ${H.H.ButtonFace};
      border-color: ${H.H.LinkText};
      box-shadow: none;
      color: ${H.H.LinkText};
      fill: currentColor;
    }

    :host([appearance="accent"][href]) .control:${w.b} {
      outline-color: ${H.H.HighlightText};
    }
  `)),E=m.i`
  :host([appearance='error']) {
    background: ${k.a6};
    color: ${k.w4};
  }

  :host([appearance='error']:hover) {
    background: ${k.ek};
    color: ${k.lJ};
  }

  :host([appearance='error'][aria-pressed='true']) {
    box-shadow: inset 0px 0px 2px 2px ${k.DV};
  }

  :host([appearance='error']:active) .control:active {
    background: ${k.GB};
    color: ${k.Pp};
  }

  :host([appearance="error"]) .control:${w.b} {
    outline-color: ${k.mH};
  }
`.withBehaviors((0,x.vF)(m.i`
    :host([appearance='error']) .control {
      forced-color-adjust: none;
      background: ${H.H.Highlight};
      color: ${H.H.HighlightText};
    }

    :host([appearance='error']) .control:hover,
    :host([appearance='error']:active) .control:active {
      background: ${H.H.HighlightText};
      border-color: ${H.H.Highlight};
      color: ${H.H.Highlight};
    }

    :host([appearance="error"]) .control:${w.b} {
      outline-color: ${H.H.Highlight};
    }

    :host([appearance='error'][href]) .control {
      background: ${H.H.LinkText};
      color: ${H.H.HighlightText};
    }

    :host([appearance='error'][href]) .control:hover {
      background: ${H.H.ButtonFace};
      border-color: ${H.H.LinkText};
      box-shadow: none;
      color: ${H.H.LinkText};
      fill: currentColor;
    }

    :host([appearance="error"][href]) .control:${w.b} {
      outline-color: ${H.H.HighlightText};
    }
  `)),V=(m.i`
  :host([appearance='hypertext']) {
    font-size: inherit;
    line-height: inherit;
    height: auto;
    min-width: 0;
    background: transparent;
  }

  :host([appearance='hypertext']) .control {
    display: inline;
    padding: 0;
    border: none;
    box-shadow: none;
    border-radius: 0;
    line-height: 1;
  }

  :host a.control:not(:link) {
    background-color: transparent;
    cursor: default;
  }
  :host([appearance='hypertext']) .control:link,
  :host([appearance='hypertext']) .control:visited {
    background: transparent;
    color: ${k.go};
    border-bottom: calc(${k.H} * 1px) solid ${k.go};
  }

  :host([appearance='hypertext']:hover),
  :host([appearance='hypertext']) .control:hover {
    background: transparent;
    border-bottom-color: ${k.D9};
  }

  :host([appearance='hypertext']:active),
  :host([appearance='hypertext']) .control:active {
    background: transparent;
    border-bottom-color: ${k.VN};
  }

  :host([appearance="hypertext"]) .control:${w.b} {
    outline-color: transparent;
    border-bottom: calc(${k.vx} * 1px) solid ${k.yG};
    margin-bottom: calc(calc(${k.H} - ${k.vx}) * 1px);
  }
`.withBehaviors((0,x.vF)(m.i`
    :host([appearance='hypertext']:hover) {
      background-color: ${H.H.ButtonFace};
      color: ${H.H.ButtonText};
    }
    :host([appearance="hypertext"][href]) .control:hover,
        :host([appearance="hypertext"][href]) .control:active,
        :host([appearance="hypertext"][href]) .control:${w.b} {
      color: ${H.H.LinkText};
      border-bottom-color: ${H.H.LinkText};
      box-shadow: none;
    }
  `)),m.i`
  :host([appearance='lightweight']) {
    background: transparent;
    color: ${k.go};
  }

  :host([appearance='lightweight']) .control {
    padding: 0;
    height: initial;
    border: none;
    box-shadow: none;
    border-radius: 0;
  }

  :host([appearance='lightweight']:hover) {
    background: transparent;
    color: ${k.D9};
  }

  :host([appearance='lightweight']:active) {
    background: transparent;
    color: ${k.VN};
  }

  :host([appearance='lightweight']) .content {
    position: relative;
  }

  :host([appearance='lightweight']) .content::before {
    content: '';
    display: block;
    height: calc(${k.H} * 1px);
    position: absolute;
    top: calc(1em + 4px);
    width: 100%;
  }

  :host([appearance='lightweight']:hover) .content::before {
    background: ${k.D9};
  }

  :host([appearance='lightweight']:active) .content::before {
    background: ${k.VN};
  }

  :host([appearance="lightweight"]) .control:${w.b} {
    outline-color: transparent;
  }

  :host([appearance="lightweight"]) .control:${w.b} .content::before {
    background: ${k.hY};
    height: calc(${k.vx} * 1px);
  }
`.withBehaviors((0,x.vF)(m.i`
    :host([appearance="lightweight"]) .control:hover,
        :host([appearance="lightweight"]) .control:${w.b} {
      forced-color-adjust: none;
      background: ${H.H.ButtonFace};
      color: ${H.H.Highlight};
    }
    :host([appearance="lightweight"]) .control:hover .content::before,
        :host([appearance="lightweight"]) .control:${w.b} .content::before {
      background: ${H.H.Highlight};
    }

    :host([appearance="lightweight"][href]) .control:hover,
        :host([appearance="lightweight"][href]) .control:${w.b} {
      background: ${H.H.ButtonFace};
      box-shadow: none;
      color: ${H.H.LinkText};
    }

    :host([appearance="lightweight"][href]) .control:hover .content::before,
        :host([appearance="lightweight"][href]) .control:${w.b} .content::before {
      background: ${H.H.LinkText};
    }
  `))),F=m.i`
  :host([appearance='outline']) {
    background: transparent;
    border-color: ${k.Av};
  }

  :host([appearance='outline']:hover) {
    border-color: ${k.OC};
  }

  :host([appearance='outline']:active) {
    border-color: ${k.UE};
  }

  :host([appearance='outline']) .control {
    border-color: inherit;
  }

  :host([appearance="outline"]) .control:${w.b} {
    outline-color: ${k.D8};
  }
`.withBehaviors((0,x.vF)(m.i`
    :host([appearance='outline']) .control {
      border-color: ${H.H.ButtonText};
    }
    :host([appearance="outline"]) .control:${w.b} {
      forced-color-adjust: none;
      background-color: ${H.H.Highlight};
      outline-color: ${H.H.ButtonText};
      color: ${H.H.HighlightText};
      fill: currentColor;
    }
    :host([appearance='outline'][href]) .control {
      background: ${H.H.ButtonFace};
      border-color: ${H.H.LinkText};
      color: ${H.H.LinkText};
      fill: currentColor;
    }
    :host([appearance="outline"][href]) .control:hover,
        :host([appearance="outline"][href]) .control:${w.b} {
      forced-color-adjust: none;
      outline-color: ${H.H.LinkText};
    }
  `)),B=m.i`
  :host([appearance='stealth']),
  :host([appearance='stealth'][disabled]:active),
  :host([appearance='stealth'][disabled]:hover) {
    background: transparent;
  }

  :host([appearance='stealth']:hover) {
    background: ${k.Qp};
  }

  :host([appearance='stealth']:active) {
    background: ${k.sG};
  }

  :host([appearance='stealth']) .control:${w.b} {
    outline-color: ${k.D8};
  }

  /* Make the focus outline displayed within the button if
     it is in a start or end slot; e.g. in a tree item
     This will make the focus outline bounded within the container.
   */
  :host([appearance='stealth'][slot="end"]) .control:${w.b},
  :host([appearance='stealth'][slot="start"]) .control:${w.b} {
    outline-offset: -2px;
  }
`.withBehaviors((0,x.vF)(m.i`
    :host([appearance='stealth']),
    :host([appearance='stealth']) .control {
      forced-color-adjust: none;
      background: ${H.H.ButtonFace};
      border-color: transparent;
      color: ${H.H.ButtonText};
      fill: currentColor;
    }

    :host([appearance='stealth']:hover) .control {
      background: ${H.H.Highlight};
      border-color: ${H.H.Highlight};
      color: ${H.H.HighlightText};
      fill: currentColor;
    }

    :host([appearance="stealth"]:${w.b}) .control {
      outline-color: ${H.H.Highlight};
      color: ${H.H.HighlightText};
      fill: currentColor;
    }

    :host([appearance='stealth'][href]) .control {
      color: ${H.H.LinkText};
    }

    :host([appearance="stealth"][href]:hover) .control,
        :host([appearance="stealth"][href]:${w.b}) .control {
      background: ${H.H.LinkText};
      border-color: ${H.H.LinkText};
      color: ${H.H.HighlightText};
      fill: currentColor;
    }

    :host([appearance="stealth"][href]:${w.b}) .control {
      forced-color-adjust: none;
      box-shadow: 0 0 0 1px ${H.H.LinkText};
    }
  `));class I{constructor(e,t,o){this.propertyName=e,this.value=t,this.styles=o}bind(e){n.y$.getNotifier(e).subscribe(this,this.propertyName),this.handleChange(e,this.propertyName)}unbind(e){n.y$.getNotifier(e).unsubscribe(this,this.propertyName),e.$fastController.removeStyles(this.styles)}handleChange(e,t){e[t]===this.value?e.$fastController.addStyles(this.styles):e.$fastController.removeStyles(this.styles)}}function S(e,t){return new I("appearance",e,t)}class R extends b{constructor(){super(...arguments),this.appearance="neutral"}defaultSlottedContentChanged(e,t){const o=this.defaultSlottedContent.filter((e=>e.nodeType===Node.ELEMENT_NODE));1===o.length&&(o[0]instanceof SVGElement||o[0].classList.contains("fa")||o[0].classList.contains("fas"))?this.control.classList.add("icon-only"):this.control.classList.remove("icon-only")}}(0,r.gn)([a.Lj],R.prototype,"appearance",void 0),(0,r.gn)([(0,a.Lj)({attribute:"minimal",mode:"boolean"})],R.prototype,"minimal",void 0),(0,r.gn)([a.Lj],R.prototype,"scale",void 0);const O=R.compose({baseName:"button",baseClass:b,template:(e,t)=>y.d`
    <button
        class="control"
        part="control"
        ?autofocus="${e=>e.autofocus}"
        ?disabled="${e=>e.disabled}"
        form="${e=>e.formId}"
        formaction="${e=>e.formaction}"
        formenctype="${e=>e.formenctype}"
        formmethod="${e=>e.formmethod}"
        formnovalidate="${e=>e.formnovalidate}"
        formtarget="${e=>e.formtarget}"
        name="${e=>e.name}"
        type="${e=>e.type}"
        value="${e=>e.value}"
        aria-atomic="${e=>e.ariaAtomic}"
        aria-busy="${e=>e.ariaBusy}"
        aria-controls="${e=>e.ariaControls}"
        aria-current="${e=>e.ariaCurrent}"
        aria-describedby="${e=>e.ariaDescribedby}"
        aria-details="${e=>e.ariaDetails}"
        aria-disabled="${e=>e.ariaDisabled}"
        aria-errormessage="${e=>e.ariaErrormessage}"
        aria-expanded="${e=>e.ariaExpanded}"
        aria-flowto="${e=>e.ariaFlowto}"
        aria-haspopup="${e=>e.ariaHaspopup}"
        aria-hidden="${e=>e.ariaHidden}"
        aria-invalid="${e=>e.ariaInvalid}"
        aria-keyshortcuts="${e=>e.ariaKeyshortcuts}"
        aria-label="${e=>e.ariaLabel}"
        aria-labelledby="${e=>e.ariaLabelledby}"
        aria-live="${e=>e.ariaLive}"
        aria-owns="${e=>e.ariaOwns}"
        aria-pressed="${e=>e.ariaPressed}"
        aria-relevant="${e=>e.ariaRelevant}"
        aria-roledescription="${e=>e.ariaRoledescription}"
        ${(0,f.i)("control")}
    >
        ${(0,s.m9)(e,t)}
        <span class="content" part="content">
            <slot ${(0,v.Q)("defaultSlottedContent")}></slot>
        </span>
        ${(0,s.LC)(e,t)}
    </button>
`,styles:(e,t)=>m.i`
    :host([disabled]),
    :host([disabled]:hover),
    :host([disabled]:active) {
      opacity: ${k.VF};
      background-color: ${k.wF};
      cursor: ${$.H};
    }

    ${C}
  `.withBehaviors((0,x.vF)(m.i`
      :host([disabled]),
      :host([disabled]) .control,
      :host([disabled]:hover),
      :host([disabled]:active) {
        forced-color-adjust: none;
        background-color: ${H.H.ButtonFace};
        outline-color: ${H.H.GrayText};
        color: ${H.H.GrayText};
        cursor: ${$.H};
        opacity: 1;
      }
    `),S("accent",m.i`
        :host([appearance='accent'][disabled]),
        :host([appearance='accent'][disabled]:hover),
        :host([appearance='accent'][disabled]:active) {
          background: ${k.Av};
        }

        ${j}
      `.withBehaviors((0,x.vF)(m.i`
          :host([appearance='accent'][disabled]) .control,
          :host([appearance='accent'][disabled]) .control:hover {
            background: ${H.H.ButtonFace};
            border-color: ${H.H.GrayText};
            color: ${H.H.GrayText};
          }
        `))),S("error",m.i`
        :host([appearance='error'][disabled]),
        :host([appearance='error'][disabled]:hover),
        :host([appearance='error'][disabled]:active) {
          background: ${k.a6};
        }

        ${E}
      `.withBehaviors((0,x.vF)(m.i`
          :host([appearance='error'][disabled]) .control,
          :host([appearance='error'][disabled]) .control:hover {
            background: ${H.H.ButtonFace};
            border-color: ${H.H.GrayText};
            color: ${H.H.GrayText};
          }
        `))),S("lightweight",m.i`
        :host([appearance='lightweight'][disabled]:hover),
        :host([appearance='lightweight'][disabled]:active) {
          background-color: transparent;
          color: ${k.go};
        }

        :host([appearance='lightweight'][disabled]) .content::before,
        :host([appearance='lightweight'][disabled]:hover) .content::before,
        :host([appearance='lightweight'][disabled]:active) .content::before {
          background: transparent;
        }

        ${V}
      `.withBehaviors((0,x.vF)(m.i`
          :host([appearance='lightweight'].disabled) .control {
            forced-color-adjust: none;
            color: ${H.H.GrayText};
          }

          :host([appearance='lightweight'].disabled)
            .control:hover
            .content::before {
            background: none;
          }
        `))),S("outline",m.i`
        :host([appearance='outline'][disabled]),
        :host([appearance='outline'][disabled]:hover),
        :host([appearance='outline'][disabled]:active) {
          background: transparent;
          border-color: ${k.Av};
        }

        ${F}
      `.withBehaviors((0,x.vF)(m.i`
          :host([appearance='outline'][disabled]) .control {
            border-color: ${H.H.GrayText};
          }
        `))),S("stealth",m.i`
        ${B}
      `.withBehaviors((0,x.vF)(m.i`
          :host([appearance='stealth'][disabled]) {
            background: ${H.H.ButtonFace};
          }

          :host([appearance='stealth'][disabled]) .control {
            background: ${H.H.ButtonFace};
            border-color: transparent;
            color: ${H.H.GrayText};
          }
        `)))),shadowOptions:{delegatesFocus:!0}})},940:(e,t,o)=>{o.d(t,{Um:()=>d});var r=o(40478),a=o(91211),i=o(98332),n=o(92221),l=o(27081);const s="form-associated-proxy",c="ElementInternals",h=c in window&&"setFormValue"in window[c].prototype,p=new WeakMap;function d(e){const t=class extends e{constructor(...e){super(...e),this.dirtyValue=!1,this.disabled=!1,this.proxyEventsToBlock=["change","click"],this.proxyInitialized=!1,this.required=!1,this.initialValue=this.initialValue||"",this.elementInternals||(this.formResetCallback=this.formResetCallback.bind(this))}static get formAssociated(){return h}get validity(){return this.elementInternals?this.elementInternals.validity:this.proxy.validity}get form(){return this.elementInternals?this.elementInternals.form:this.proxy.form}get validationMessage(){return this.elementInternals?this.elementInternals.validationMessage:this.proxy.validationMessage}get willValidate(){return this.elementInternals?this.elementInternals.willValidate:this.proxy.willValidate}get labels(){if(this.elementInternals)return Object.freeze(Array.from(this.elementInternals.labels));if(this.proxy instanceof HTMLElement&&this.proxy.ownerDocument&&this.id){const e=this.proxy.labels,t=Array.from(this.proxy.getRootNode().querySelectorAll(`[for='${this.id}']`)),o=e?t.concat(Array.from(e)):t;return Object.freeze(o)}return r.ow}valueChanged(e,t){this.dirtyValue=!0,this.proxy instanceof HTMLElement&&(this.proxy.value=this.value),this.currentValue=this.value,this.setFormValue(this.value),this.validate()}currentValueChanged(){this.value=this.currentValue}initialValueChanged(e,t){this.dirtyValue||(this.value=this.initialValue,this.dirtyValue=!1)}disabledChanged(e,t){this.proxy instanceof HTMLElement&&(this.proxy.disabled=this.disabled),a.SO.queueUpdate((()=>this.classList.toggle("disabled",this.disabled)))}nameChanged(e,t){this.proxy instanceof HTMLElement&&(this.proxy.name=this.name)}requiredChanged(e,t){this.proxy instanceof HTMLElement&&(this.proxy.required=this.required),a.SO.queueUpdate((()=>this.classList.toggle("required",this.required))),this.validate()}get elementInternals(){if(!h)return null;let e=p.get(this);return e||(e=this.attachInternals(),p.set(this,e)),e}connectedCallback(){super.connectedCallback(),this.addEventListener("keypress",this._keypressHandler),this.value||(this.value=this.initialValue,this.dirtyValue=!1),this.elementInternals||(this.attachProxy(),this.form&&this.form.addEventListener("reset",this.formResetCallback))}disconnectedCallback(){super.disconnectedCallback(),this.proxyEventsToBlock.forEach((e=>this.proxy.removeEventListener(e,this.stopPropagation))),!this.elementInternals&&this.form&&this.form.removeEventListener("reset",this.formResetCallback)}checkValidity(){return this.elementInternals?this.elementInternals.checkValidity():this.proxy.checkValidity()}reportValidity(){return this.elementInternals?this.elementInternals.reportValidity():this.proxy.reportValidity()}setValidity(e,t,o){this.elementInternals?this.elementInternals.setValidity(e,t,o):"string"==typeof t&&this.proxy.setCustomValidity(t)}formDisabledCallback(e){this.disabled=e}formResetCallback(){this.value=this.initialValue,this.dirtyValue=!1}attachProxy(){var e;this.proxyInitialized||(this.proxyInitialized=!0,this.proxy.style.display="none",this.proxyEventsToBlock.forEach((e=>this.proxy.addEventListener(e,this.stopPropagation))),this.proxy.disabled=this.disabled,this.proxy.required=this.required,"string"==typeof this.name&&(this.proxy.name=this.name),"string"==typeof this.value&&(this.proxy.value=this.value),this.proxy.setAttribute("slot",s),this.proxySlot=document.createElement("slot"),this.proxySlot.setAttribute("name",s)),null===(e=this.shadowRoot)||void 0===e||e.appendChild(this.proxySlot),this.appendChild(this.proxy)}detachProxy(){var e;this.removeChild(this.proxy),null===(e=this.shadowRoot)||void 0===e||e.removeChild(this.proxySlot)}validate(e){this.proxy instanceof HTMLElement&&this.setValidity(this.proxy.validity,this.proxy.validationMessage,e)}setFormValue(e,t){this.elementInternals&&this.elementInternals.setFormValue(e,t||e)}_keypressHandler(e){if(e.key===l.kL&&this.form instanceof HTMLFormElement){const e=this.form.querySelector("[type=submit]");null==e||e.click()}}stopPropagation(e){e.stopPropagation()}};return(0,i.Lj)({mode:"boolean"})(t.prototype,"disabled"),(0,i.Lj)({mode:"fromView",attribute:"value"})(t.prototype,"initialValue"),(0,i.Lj)({attribute:"current-value"})(t.prototype,"currentValue"),(0,i.Lj)(t.prototype,"name"),(0,i.Lj)({mode:"boolean"})(t.prototype,"required"),(0,n.LO)(t.prototype,"value"),t}},14869:(e,t,o)=>{o.d(t,{v:()=>i});var r=o(95185),a=o(98332);class i{}(0,r.gn)([(0,a.Lj)({attribute:"aria-atomic"})],i.prototype,"ariaAtomic",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-busy"})],i.prototype,"ariaBusy",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-controls"})],i.prototype,"ariaControls",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-current"})],i.prototype,"ariaCurrent",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-describedby"})],i.prototype,"ariaDescribedby",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-details"})],i.prototype,"ariaDetails",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-disabled"})],i.prototype,"ariaDisabled",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-errormessage"})],i.prototype,"ariaErrormessage",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-flowto"})],i.prototype,"ariaFlowto",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-haspopup"})],i.prototype,"ariaHaspopup",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-hidden"})],i.prototype,"ariaHidden",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-invalid"})],i.prototype,"ariaInvalid",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-keyshortcuts"})],i.prototype,"ariaKeyshortcuts",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-label"})],i.prototype,"ariaLabel",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-labelledby"})],i.prototype,"ariaLabelledby",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-live"})],i.prototype,"ariaLive",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-owns"})],i.prototype,"ariaOwns",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-relevant"})],i.prototype,"ariaRelevant",void 0),(0,r.gn)([(0,a.Lj)({attribute:"aria-roledescription"})],i.prototype,"ariaRoledescription",void 0)},82616:(e,t,o)=>{function r(e,t,o,r){var a,i=arguments.length,n=i<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,o):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,o,r);else for(var l=e.length-1;l>=0;l--)(a=e[l])&&(n=(i<3?a(n):i>3?a(t,o,n):a(t,o))||n);return i>3&&n&&Object.defineProperty(t,o,n),n}o.d(t,{gn:()=>r}),Object.create,Object.create,"function"==typeof SuppressedError&&SuppressedError}}]);