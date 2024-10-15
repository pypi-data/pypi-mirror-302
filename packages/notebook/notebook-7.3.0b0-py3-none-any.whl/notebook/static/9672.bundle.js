"use strict";(self.webpackChunk_JUPYTERLAB_CORE_OUTPUT=self.webpackChunk_JUPYTERLAB_CORE_OUTPUT||[]).push([[9672],{99672:(e,t,o)=>{o.d(t,{o:()=>S});var a=o(68866),r=o(82616),l=o(98332),n=o(95185),i=o(91211),s=o(92221),d=o(14869),c=o(52865),h=o(89155),p=o(940),u=o(50755);class b extends u.I{}class g extends((0,p.Um)(b)){constructor(){super(...arguments),this.proxy=document.createElement("input")}}class $ extends g{readOnlyChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.readOnly=this.readOnly,this.validate())}autofocusChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.autofocus=this.autofocus,this.validate())}placeholderChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.placeholder=this.placeholder)}listChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.setAttribute("list",this.list),this.validate())}maxlengthChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.maxLength=this.maxlength,this.validate())}minlengthChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.minLength=this.minlength,this.validate())}patternChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.pattern=this.pattern,this.validate())}sizeChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.size=this.size)}spellcheckChanged(){this.proxy instanceof HTMLInputElement&&(this.proxy.spellcheck=this.spellcheck)}connectedCallback(){super.connectedCallback(),this.validate(),this.autofocus&&i.SO.queueUpdate((()=>{this.focus()}))}validate(){super.validate(this.control)}handleTextInput(){this.value=this.control.value}handleClearInput(){this.value="",this.control.focus(),this.handleChange()}handleChange(){this.$emit("change")}}(0,n.gn)([(0,l.Lj)({attribute:"readonly",mode:"boolean"})],$.prototype,"readOnly",void 0),(0,n.gn)([(0,l.Lj)({mode:"boolean"})],$.prototype,"autofocus",void 0),(0,n.gn)([l.Lj],$.prototype,"placeholder",void 0),(0,n.gn)([l.Lj],$.prototype,"list",void 0),(0,n.gn)([(0,l.Lj)({converter:l.Id})],$.prototype,"maxlength",void 0),(0,n.gn)([(0,l.Lj)({converter:l.Id})],$.prototype,"minlength",void 0),(0,n.gn)([l.Lj],$.prototype,"pattern",void 0),(0,n.gn)([(0,l.Lj)({converter:l.Id})],$.prototype,"size",void 0),(0,n.gn)([(0,l.Lj)({mode:"boolean"})],$.prototype,"spellcheck",void 0),(0,n.gn)([s.LO],$.prototype,"defaultSlottedNodes",void 0);class v{}(0,h.e)(v,d.v),(0,h.e)($,c.hW,v);var y=o(25269),x=o(17832),m=o(62564);function f(e,t,o){return e.nodeType!==Node.TEXT_NODE||"string"==typeof e.nodeValue&&!!e.nodeValue.trim().length}var k=o(12634),w=o(27002),L=o(58201),C=o(87206),H=o(21601),O=o(61424),T=o(98242),_=o(30550),I=o(13370);const E=k.i`
  ${(0,H.j)("inline-block")} :host {
    font-family: ${C.SV};
    outline: none;
    user-select: none;
    /* Ensure to display focus highlight */
    margin: calc((${C.vx} - ${C.H}) * 1px);
  }

  .root {
    box-sizing: border-box;
    position: relative;
    display: flex;
    flex-direction: row;
    color: ${C.hY};
    background: ${C._B};
    border-radius: calc(${C.UW} * 1px);
    border: calc(${C.H} * 1px) solid ${C.P0};
    height: calc(${I.i} * 1px);
  }

  :host([aria-invalid='true']) .root {
    border-color: ${C.a6};
  }

  .control {
    -webkit-appearance: none;
    font: inherit;
    background: transparent;
    border: 0;
    color: inherit;
    height: calc(100% - 4px);
    width: 100%;
    margin-top: auto;
    margin-bottom: auto;
    border: none;
    padding: 0 calc(${C._5} * 2px + 1px);
    font-size: ${C.cS};
    line-height: ${C.RU};
  }

  .control:placeholder-shown {
    text-overflow: ellipsis;
  }

  .control:hover,
  .control:${L.b},
  .control:disabled,
  .control:active {
    outline: none;
  }

  .label {
    display: block;
    color: ${C.hY};
    cursor: pointer;
    font-size: ${C.cS};
    line-height: ${C.RU};
    margin-bottom: 4px;
  }

  .label__hidden {
    display: none;
    visibility: hidden;
  }

  .start,
  .end {
    margin: auto;
    fill: currentcolor;
  }

  ::slotted(svg) {
    /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
    width: 16px;
    height: 16px;
  }

  .start {
    margin-inline-start: 11px;
  }

  .end {
    margin-inline-end: 11px;
  }

  :host(:hover:not([disabled])) .root {
    background: ${C.Tm};
    border-color: ${C.Dg};
  }

  :host([aria-invalid='true']:hover:not([disabled])) .root {
    border-color: ${C.ek};
  }

  :host(:active:not([disabled])) .root {
    background: ${C.Tm};
    border-color: ${C.hP};
  }

  :host([aria-invalid='true']:active:not([disabled])) .root {
    border-color: ${C.GB};
  }

  :host(:focus-within:not([disabled])) .root {
    border-color: ${C.D8};
    box-shadow: 0 0 0 calc((${C.vx} - ${C.H}) * 1px)
      ${C.D8};
  }

  :host([aria-invalid='true']:focus-within:not([disabled])) .root {
    border-color: ${C.mH};
    box-shadow: 0 0 0 calc((${C.vx} - ${C.H}) * 1px)
      ${C.mH};
  }

  :host([appearance='filled']) .root {
    background: ${C.wF};
  }

  :host([appearance='filled']:hover:not([disabled])) .root {
    background: ${C.Xi};
  }

  :host([disabled]) .label,
  :host([readonly]) .label,
  :host([readonly]) .control,
  :host([disabled]) .control {
    cursor: ${O.H};
  }

  :host([disabled]) {
    opacity: ${C.VF};
  }

  :host([disabled]) .control {
    border-color: ${C.ak};
  }
`.withBehaviors((0,T.vF)(k.i`
    .root,
    :host([appearance='filled']) .root {
      forced-color-adjust: none;
      background: ${_.H.Field};
      border-color: ${_.H.FieldText};
    }
    :host([aria-invalid='true']) .root {
      border-style: dashed;
    }
    :host(:hover:not([disabled])) .root,
    :host([appearance='filled']:hover:not([disabled])) .root,
    :host([appearance='filled']:hover) .root {
      background: ${_.H.Field};
      border-color: ${_.H.Highlight};
    }
    .start,
    .end {
      fill: currentcolor;
    }
    :host([disabled]) {
      opacity: 1;
    }
    :host([disabled]) .root,
    :host([appearance='filled']:hover[disabled]) .root {
      border-color: ${_.H.GrayText};
      background: ${_.H.Field};
    }
    :host(:focus-within:enabled) .root {
      border-color: ${_.H.Highlight};
      box-shadow: 0 0 0 calc((${C.vx} - ${C.H}) * 1px)
        ${_.H.Highlight};
    }
    input::placeholder {
      color: ${_.H.GrayText};
    }
  `)),F=w.DesignToken.create("clear-button-hover").withDefault((e=>{const t=C.DF.getValueFor(e),o=C.At.getValueFor(e);return t.evaluate(e,o.evaluate(e).hover).hover})),D=w.DesignToken.create("clear-button-active").withDefault((e=>{const t=C.DF.getValueFor(e),o=C.At.getValueFor(e);return t.evaluate(e,o.evaluate(e).hover).active}));class j extends ${constructor(){super(...arguments),this.appearance="outline"}}(0,r.gn)([l.Lj],j.prototype,"appearance",void 0);const z=j.compose({baseName:"search",baseClass:$,template:(e,t)=>y.d`
    <template
        class="
            ${e=>e.readOnly?"readonly":""}
        "
    >
        <label
            part="label"
            for="control"
            class="${e=>e.defaultSlottedNodes&&e.defaultSlottedNodes.length?"label":"label label__hidden"}"
        >
            <slot
                ${(0,x.Q)({property:"defaultSlottedNodes",filter:f})}
            ></slot>
        </label>
        <div class="root" part="root" ${(0,m.i)("root")}>
            ${(0,c.m9)(e,t)}
            <div class="input-wrapper" part="input-wrapper">
                <input
                    class="control"
                    part="control"
                    id="control"
                    @input="${e=>e.handleTextInput()}"
                    @change="${e=>e.handleChange()}"
                    ?autofocus="${e=>e.autofocus}"
                    ?disabled="${e=>e.disabled}"
                    list="${e=>e.list}"
                    maxlength="${e=>e.maxlength}"
                    minlength="${e=>e.minlength}"
                    pattern="${e=>e.pattern}"
                    placeholder="${e=>e.placeholder}"
                    ?readonly="${e=>e.readOnly}"
                    ?required="${e=>e.required}"
                    size="${e=>e.size}"
                    ?spellcheck="${e=>e.spellcheck}"
                    :value="${e=>e.value}"
                    type="search"
                    aria-atomic="${e=>e.ariaAtomic}"
                    aria-busy="${e=>e.ariaBusy}"
                    aria-controls="${e=>e.ariaControls}"
                    aria-current="${e=>e.ariaCurrent}"
                    aria-describedby="${e=>e.ariaDescribedby}"
                    aria-details="${e=>e.ariaDetails}"
                    aria-disabled="${e=>e.ariaDisabled}"
                    aria-errormessage="${e=>e.ariaErrormessage}"
                    aria-flowto="${e=>e.ariaFlowto}"
                    aria-haspopup="${e=>e.ariaHaspopup}"
                    aria-hidden="${e=>e.ariaHidden}"
                    aria-invalid="${e=>e.ariaInvalid}"
                    aria-keyshortcuts="${e=>e.ariaKeyshortcuts}"
                    aria-label="${e=>e.ariaLabel}"
                    aria-labelledby="${e=>e.ariaLabelledby}"
                    aria-live="${e=>e.ariaLive}"
                    aria-owns="${e=>e.ariaOwns}"
                    aria-relevant="${e=>e.ariaRelevant}"
                    aria-roledescription="${e=>e.ariaRoledescription}"
                    ${(0,m.i)("control")}
                />
                <slot name="close-button">
                    <button
                        class="clear-button ${e=>e.value?"":"clear-button__hidden"}"
                        part="clear-button"
                        tabindex="-1"
                        @click=${e=>e.handleClearInput()}
                    >
                        <slot name="close-glyph">
                            <svg
                                width="9"
                                height="9"
                                viewBox="0 0 9 9"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    d="M0.146447 0.146447C0.338683 -0.0478972 0.645911 -0.0270359 0.853553 0.146447L4.5 3.793L8.14645 0.146447C8.34171 -0.0488155 8.65829 -0.0488155 8.85355 0.146447C9.04882 0.341709 9.04882 0.658291 8.85355 0.853553L5.207 4.5L8.85355 8.14645C9.05934 8.35223 9.03129 8.67582 8.85355 8.85355C8.67582 9.03129 8.35409 9.02703 8.14645 8.85355L4.5 5.207L0.853553 8.85355C0.658291 9.04882 0.341709 9.04882 0.146447 8.85355C-0.0488155 8.65829 -0.0488155 8.34171 0.146447 8.14645L3.793 4.5L0.146447 0.853553C-0.0268697 0.680237 -0.0457894 0.34079 0.146447 0.146447Z"
                                />
                            </svg>
                        </slot>
                    </button>
                </slot>
            </div>
            ${(0,c.LC)(e,t)}
        </div>
    </template>
`,styles:(e,t)=>k.i`
  ${E}

  .control::-webkit-search-cancel-button {
    -webkit-appearance: none;
  }

  .control:hover,
    .control:${L.b},
    .control:disabled,
    .control:active {
    outline: none;
  }

  .clear-button {
    height: calc(100% - 2px);
    opacity: 0;
    margin: 1px;
    background: transparent;
    color: ${C.hY};
    fill: currentcolor;
    border: none;
    border-radius: calc(${C.UW} * 1px);
    min-width: calc(${I.i} * 1px);
    font-size: ${C.cS};
    line-height: ${C.RU};
    outline: none;
    font-family: ${C.SV};
    padding: 0 calc((10 + (${C._5} * 2 * ${C.hV})) * 1px);
  }

  .clear-button:hover {
    background: ${C.Qp};
  }

  .clear-button:active {
    background: ${C.sG};
  }

  :host([appearance='filled']) .clear-button:hover {
    background: ${F};
  }

  :host([appearance='filled']) .clear-button:active {
    background: ${D};
  }

  .input-wrapper {
    display: flex;
    position: relative;
    width: 100%;
  }

  .start,
  .end {
    display: flex;
    margin: 1px;
    fill: currentcolor;
  }

  ::slotted([slot='end']) {
    height: 100%;
  }

  .end {
    margin-inline-end: 1px;
    height: calc(100% - 2px);
  }

  ::slotted(svg) {
    /* TODO: adaptive typography https://github.com/microsoft/fast/issues/2432 */
    width: 16px;
    height: 16px;
    margin-inline-end: 11px;
    margin-inline-start: 11px;
    margin-top: auto;
    margin-bottom: auto;
  }

  .clear-button__hidden {
    opacity: 0;
  }

  :host(:hover:not([disabled], [readOnly])) .clear-button,
  :host(:active:not([disabled], [readOnly])) .clear-button,
  :host(:focus-within:not([disabled], [readOnly])) .clear-button {
    opacity: 1;
  }

  :host(:hover:not([disabled], [readOnly])) .clear-button__hidden,
  :host(:active:not([disabled], [readOnly])) .clear-button__hidden,
  :host(:focus-within:not([disabled], [readOnly])) .clear-button__hidden {
    opacity: 0;
  }
`,shadowOptions:{delegatesFocus:!0}});var U=o(78156),R=o.n(U),M=o(4444);(0,a.W)().register(z());const S=(0,U.forwardRef)(((e,t)=>{const o=(0,U.useRef)(null),{className:a,readonly:r,appearance:l,placeholder:n,list:i,pattern:s,readOnly:d,autofocus:c,maxlength:h,minlength:p,size:u,spellcheck:b,disabled:g,required:$,...v}=e;return(0,M.O)(o,"input",e.onInput),(0,M.O)(o,"change",e.onChange),(0,M.h)(o,"readOnly",e.readOnly),(0,M.h)(o,"autofocus",e.autofocus),(0,M.h)(o,"maxlength",e.maxlength),(0,M.h)(o,"minlength",e.minlength),(0,M.h)(o,"size",e.size),(0,M.h)(o,"spellcheck",e.spellcheck),(0,M.h)(o,"disabled",e.disabled),(0,M.h)(o,"required",e.required),(0,U.useImperativeHandle)(t,(()=>o.current),[o.current]),R().createElement("jp-search",{ref:o,...v,appearance:e.appearance,placeholder:e.placeholder,list:e.list,pattern:e.pattern,class:e.className,exportparts:e.exportparts,for:e.htmlFor,part:e.part,tabindex:e.tabIndex,readonly:e.readonly?"":void 0,style:{...e.style}},e.children)}))}}]);