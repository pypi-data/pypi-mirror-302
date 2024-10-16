import { g as ve, w as D } from "./Index-Rkglti8t.js";
const E = window.ms_globals.React, me = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, be = window.ms_globals.React.useState, ge = window.ms_globals.React.useEffect, y = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.DatePicker, U = window.ms_globals.dayjs;
var Z = {
  exports: {}
}, A = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ye = E, xe = Symbol.for("react.element"), Ee = Symbol.for("react.fragment"), Ie = Object.prototype.hasOwnProperty, Re = ye.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, n, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) Ie.call(n, l) && !je.hasOwnProperty(l) && (r[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: xe,
    type: e,
    key: t,
    ref: s,
    props: r,
    _owner: Re.current
  };
}
A.Fragment = Ee;
A.jsx = V;
A.jsxs = V;
Z.exports = A;
var h = Z.exports;
const {
  SvelteComponent: Se,
  assign: H,
  binding_callbacks: q,
  check_outros: Oe,
  children: $,
  claim_element: ee,
  claim_space: ke,
  component_subscribe: B,
  compute_slots: Ce,
  create_slot: Pe,
  detach: j,
  element: te,
  empty: J,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: De,
  get_slot_changes: Fe,
  group_outros: Ne,
  init: Ae,
  insert_hydration: F,
  safe_not_equal: Le,
  set_custom_element_data: ne,
  space: Te,
  transition_in: N,
  transition_out: z,
  update_slot_base: Me
} = window.__gradio__svelte__internal, {
  beforeUpdate: We,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function K(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = Pe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = te("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = ee(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = $(n);
      r && r.l(s), s.forEach(j), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      F(t, n, s), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Me(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? Fe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : De(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (N(r, t), o = !0);
    },
    o(t) {
      z(r, t), o = !1;
    },
    d(t) {
      t && j(n), r && r.d(t), e[9](null);
    }
  };
}
function He(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      n = te("react-portal-target"), o = Te(), t && t.c(), l = J(), this.h();
    },
    l(s) {
      n = ee(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(j), o = ke(s), t && t.l(s), l = J(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      F(s, n, i), e[8](n), F(s, o, i), t && t.m(s, i), F(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && N(t, 1)) : (t = K(s), t.c(), N(t, 1), t.m(l.parentNode, l)) : t && (Ne(), z(t, 1, 1, () => {
        t = null;
      }), Oe());
    },
    i(s) {
      r || (N(t), r = !0);
    },
    o(s) {
      z(t), r = !1;
    },
    d(s) {
      s && (j(n), j(o), j(l)), e[8](null), t && t.d(s);
    }
  };
}
function Q(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function qe(e, n, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = Ce(t);
  let {
    svelteInit: c
  } = n;
  const _ = D(Q(n)), f = D();
  B(e, f, (u) => o(0, l = u));
  const m = D();
  B(e, m, (u) => o(1, r = u));
  const a = [], p = ze("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: I,
    subSlotIndex: S
  } = ve() || {}, O = c({
    parent: p,
    props: _,
    target: f,
    slot: m,
    slotKey: b,
    slotIndex: I,
    subSlotIndex: S,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ue("$$ms-gr-react-wrapper", O), We(() => {
    _.set(Q(n));
  }), Ge(() => {
    a.forEach((u) => u());
  });
  function L(u) {
    q[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function k(u) {
    q[u ? "unshift" : "push"](() => {
      r = u, m.set(r);
    });
  }
  return e.$$set = (u) => {
    o(17, n = H(H({}, n), Y(u))), "svelteInit" in u && o(5, c = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, n = Y(n), [l, r, f, m, i, c, s, t, L, k];
}
class Be extends Se {
  constructor(n) {
    super(), Ae(this, n, qe, He, Le, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, T = window.ms_globals.tree;
function Je(e) {
  function n(o) {
    const l = D(), r = new Be({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? T;
          return i.nodes = [...i.nodes, s], X({
            createPortal: W,
            node: T
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), X({
              createPortal: W,
              node: T
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !Ye.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function G(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(W(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((r) => {
        if (E.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = G(r.props.el);
          return E.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...E.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, s, c);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = G(t);
      n.push(...i), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const g = me(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, r) => {
  const t = he(), [s, i] = be([]);
  return ge(() => {
    var m;
    if (!t.current || !e)
      return;
    let c = e;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Qe(r, a), o && a.classList.add(...o.split(" ")), l) {
        const p = Ke(l);
        Object.keys(p).forEach((b) => {
          a.style[b] = p[b];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var I;
        const {
          portals: p,
          clonedElement: b
        } = G(e);
        c = b, i(p), c.style.display = "contents", _(), (I = t.current) == null || I.appendChild(c);
      };
      a(), f = new window.MutationObserver(() => {
        var p, b;
        (p = t.current) != null && p.contains(c) && ((b = t.current) == null || b.removeChild(c)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (m = t.current) == null || m.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((p = t.current) == null || p.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, n, o, l, r]), E.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Xe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function C(e) {
  return y(() => Xe(e), [e]);
}
function re(e, n) {
  return e.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const l = {
      ...o.props
    };
    let r = l;
    Object.keys(o.slots).forEach((s) => {
      if (!o.slots[s] || !(o.slots[s] instanceof Element) && !o.slots[s].el)
        return;
      const i = s.split(".");
      i.forEach((a, p) => {
        r[a] || (r[a] = {}), p !== i.length - 1 && (r = l[a]);
      });
      const c = o.slots[s];
      let _, f, m = !1;
      c instanceof Element ? _ = c : (_ = c.el, f = c.callback, m = c.clone || !1), r[i[i.length - 1]] = _ ? f ? (...a) => (f(i[i.length - 1], a), /* @__PURE__ */ h.jsx(g, {
        slot: _,
        clone: m || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ h.jsx(g, {
        slot: _,
        clone: m || (n == null ? void 0 : n.clone)
      }) : r[i[i.length - 1]], r = l;
    });
    const t = "children";
    return o[t] && (l[t] = re(o[t], n)), l;
  });
}
function Ze(e, n) {
  return e ? /* @__PURE__ */ h.jsx(g, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function M({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return (...r) => (n(e, r), Ze(o[e], {
    clone: !0,
    ...l
  }));
}
function w(e) {
  return U(typeof e == "number" ? e * 1e3 : e);
}
function P(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const $e = Je(({
  slots: e,
  disabledDate: n,
  value: o,
  defaultValue: l,
  defaultPickerValue: r,
  pickerValue: t,
  presets: s,
  presetItems: i,
  showTime: c,
  onChange: _,
  minDate: f,
  maxDate: m,
  cellRender: a,
  panelRender: p,
  getPopupContainer: b,
  onValueChange: I,
  onPanelChange: S,
  onCalendarChange: O,
  children: L,
  setSlotParams: k,
  elRef: u,
  ...v
}) => {
  const oe = C(n), le = C(b), se = C(a), ce = C(p), ie = y(() => {
    var d;
    return typeof c == "object" ? {
      ...c,
      defaultValue: (d = c.defaultValue) == null ? void 0 : d.map((x) => w(x))
    } : c;
  }, [c]), ae = y(() => o == null ? void 0 : o.map((d) => w(d)), [o]), ue = y(() => l == null ? void 0 : l.map((d) => w(d)), [l]), de = y(() => Array.isArray(r) ? r.map((d) => w(d)) : r ? w(r) : void 0, [r]), fe = y(() => Array.isArray(t) ? t.map((d) => w(d)) : t ? w(t) : void 0, [t]), pe = y(() => f ? w(f) : void 0, [f]), _e = y(() => m ? w(m) : void 0, [m]);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: L
    }), /* @__PURE__ */ h.jsx(we.RangePicker, {
      ...v,
      ref: u,
      value: ae,
      defaultValue: ue,
      defaultPickerValue: de,
      pickerValue: fe,
      minDate: pe,
      maxDate: _e,
      showTime: ie,
      disabledDate: oe,
      getPopupContainer: le,
      cellRender: e.cellRender ? M({
        slots: e,
        setSlotParams: k,
        key: "cellRender"
      }) : se,
      panelRender: e.panelRender ? M({
        slots: e,
        setSlotParams: k,
        key: "panelRender"
      }) : ce,
      presets: y(() => (s || re(i)).map((d) => ({
        ...d,
        value: P(d.value)
      })), [s, i]),
      onPanelChange: (d, ...x) => {
        const R = P(d);
        S == null || S(R, ...x);
      },
      onChange: (d, ...x) => {
        const R = P(d);
        _ == null || _(R, ...x), I(R);
      },
      onCalendarChange: (d, ...x) => {
        const R = P(d);
        O == null || O(R, ...x);
      },
      renderExtraFooter: e.renderExtraFooter ? M({
        slots: e,
        setSlotParams: k,
        key: "renderExtraFooter"
      }) : v.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ h.jsx(g, {
        slot: e.prevIcon
      }) : v.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ h.jsx(g, {
        slot: e.nextIcon
      }) : v.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ h.jsx(g, {
        slot: e.suffixIcon
      }) : v.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ h.jsx(g, {
        slot: e.superNextIcon
      }) : v.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ h.jsx(g, {
        slot: e.superPrevIcon
      }) : v.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(g, {
          slot: e["allowClear.clearIcon"]
        })
      } : v.allowClear,
      separator: e.separator ? /* @__PURE__ */ h.jsx(g, {
        slot: e.separator,
        clone: !0
      }) : v.separator
    })]
  });
});
export {
  $e as DateRangePicker,
  $e as default
};
