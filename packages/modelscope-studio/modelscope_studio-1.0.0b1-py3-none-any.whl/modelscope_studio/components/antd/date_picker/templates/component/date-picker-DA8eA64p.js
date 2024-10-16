import { g as be, w as k } from "./Index-Co_qfH4X.js";
const y = window.ms_globals.React, pe = window.ms_globals.React.forwardRef, me = window.ms_globals.React.useRef, he = window.ms_globals.React.useState, ve = window.ms_globals.React.useEffect, v = window.ms_globals.React.useMemo, T = window.ms_globals.ReactDOM.createPortal, ge = window.ms_globals.antd.DatePicker, W = window.ms_globals.dayjs;
var Q = {
  exports: {}
}, P = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ye = y, we = Symbol.for("react.element"), xe = Symbol.for("react.fragment"), Ee = Object.prototype.hasOwnProperty, Ie = ye.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function X(e, t, r) {
  var s, o = {}, n = null, l = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) Ee.call(t, s) && !Re.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: we,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: Ie.current
  };
}
P.Fragment = xe;
P.jsx = X;
P.jsxs = X;
Q.exports = P;
var m = Q.exports;
const {
  SvelteComponent: Ce,
  assign: z,
  binding_callbacks: G,
  check_outros: je,
  children: Z,
  claim_element: $,
  claim_space: ke,
  component_subscribe: U,
  compute_slots: Oe,
  create_slot: Se,
  detach: E,
  element: ee,
  empty: H,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Pe,
  get_slot_changes: De,
  group_outros: Fe,
  init: Ne,
  insert_hydration: O,
  safe_not_equal: Ae,
  set_custom_element_data: te,
  space: Le,
  transition_in: S,
  transition_out: M,
  update_slot_base: Te
} = window.__gradio__svelte__internal, {
  beforeUpdate: Me,
  getContext: Ve,
  onDestroy: We,
  setContext: ze
} = window.__gradio__svelte__internal;
function B(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = Se(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ee("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = $(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = Z(t);
      o && o.l(l), l.forEach(E), this.h();
    },
    h() {
      te(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      O(n, t, l), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && Te(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? De(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : Pe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (S(o, n), r = !0);
    },
    o(n) {
      M(o, n), r = !1;
    },
    d(n) {
      n && E(t), o && o.d(n), e[9](null);
    }
  };
}
function Ge(e) {
  let t, r, s, o, n = (
    /*$$slots*/
    e[4].default && B(e)
  );
  return {
    c() {
      t = ee("react-portal-target"), r = Le(), n && n.c(), s = H(), this.h();
    },
    l(l) {
      t = $(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(t).forEach(E), r = ke(l), n && n.l(l), s = H(), this.h();
    },
    h() {
      te(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      O(l, t, c), e[8](t), O(l, r, c), n && n.m(l, c), O(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && S(n, 1)) : (n = B(l), n.c(), S(n, 1), n.m(s.parentNode, s)) : n && (Fe(), M(n, 1, 1, () => {
        n = null;
      }), je());
    },
    i(l) {
      o || (S(n), o = !0);
    },
    o(l) {
      M(n), o = !1;
    },
    d(l) {
      l && (E(t), E(r), E(s)), e[8](null), n && n.d(l);
    }
  };
}
function J(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ue(e, t, r) {
  let s, o, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const c = Oe(n);
  let {
    svelteInit: i
  } = t;
  const _ = k(J(t)), d = k();
  U(e, d, (a) => r(0, s = a));
  const p = k();
  U(e, p, (a) => r(1, o = a));
  const u = [], f = Ve("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: w,
    subSlotIndex: I
  } = be() || {}, D = i({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: h,
    slotIndex: w,
    subSlotIndex: I,
    onDestroy(a) {
      u.push(a);
    }
  });
  ze("$$ms-gr-react-wrapper", D), Me(() => {
    _.set(J(t));
  }), We(() => {
    u.forEach((a) => a());
  });
  function R(a) {
    G[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function F(a) {
    G[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return e.$$set = (a) => {
    r(17, t = z(z({}, t), q(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = q(t), [s, o, d, p, c, i, l, n, R, F];
}
class He extends Ce {
  constructor(t) {
    super(), Ne(this, t, Ue, Ge, Ae, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, A = window.ms_globals.tree;
function qe(e) {
  function t(r) {
    const s = k(), o = new He({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? A;
          return c.nodes = [...c.nodes, l], Y({
            createPortal: T,
            node: A
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), Y({
              createPortal: T,
              node: A
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Be = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Je(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return typeof s == "number" && !Be.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function V(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(T(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: y.Children.toArray(e._reactElement.props.children).map((o) => {
        if (y.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = V(o.props.el);
          return y.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...y.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = V(n);
      t.push(...c), r.appendChild(l);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ye(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const g = pe(({
  slot: e,
  clone: t,
  className: r,
  style: s
}, o) => {
  const n = me(), [l, c] = he([]);
  return ve(() => {
    var p;
    if (!n.current || !e)
      return;
    let i = e;
    function _() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Ye(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = Je(s);
        Object.keys(f).forEach((h) => {
          u.style[h] = f[h];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w;
        const {
          portals: f,
          clonedElement: h
        } = V(e);
        i = h, c(f), i.style.display = "contents", _(), (w = n.current) == null || w.appendChild(i);
      };
      u(), d = new window.MutationObserver(() => {
        var f, h;
        (f = n.current) != null && f.contains(i) && ((h = n.current) == null || h.removeChild(i)), u();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", _(), (p = n.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = n.current) != null && u.contains(i) && ((f = n.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, t, r, s, o]), y.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ke(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function j(e) {
  return v(() => Ke(e), [e]);
}
function ne(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let o = s;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const c = l.split(".");
      c.forEach((u, f) => {
        o[u] || (o[u] = {}), f !== c.length - 1 && (o = s[u]);
      });
      const i = r.slots[l];
      let _, d, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, d = i.callback, p = i.clone || !1), o[c[c.length - 1]] = _ ? d ? (...u) => (d(c[c.length - 1], u), /* @__PURE__ */ m.jsx(g, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(g, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : o[c[c.length - 1]], o = s;
    });
    const n = "children";
    return r[n] && (s[n] = ne(r[n], t)), s;
  });
}
function Qe(e, t) {
  return e ? /* @__PURE__ */ m.jsx(g, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function L({
  key: e,
  setSlotParams: t,
  slots: r
}, s) {
  return (...o) => (t(e, o), Qe(r[e], {
    clone: !0,
    ...s
  }));
}
function b(e) {
  return Array.isArray(e) ? e.map((t) => b(t)) : W(typeof e == "number" ? e * 1e3 : e);
}
function K(e) {
  return Array.isArray(e) ? e.map((t) => t ? t.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const Ze = qe(({
  slots: e,
  disabledDate: t,
  value: r,
  defaultValue: s,
  defaultPickerValue: o,
  pickerValue: n,
  showTime: l,
  presets: c,
  presetItems: i,
  onChange: _,
  minDate: d,
  maxDate: p,
  cellRender: u,
  panelRender: f,
  getPopupContainer: h,
  onValueChange: w,
  onPanelChange: I,
  children: D,
  setSlotParams: R,
  elRef: F,
  ...a
}) => {
  const re = j(t), oe = j(h), le = j(u), se = j(f), ce = v(() => typeof l == "object" ? {
    ...l,
    defaultValue: l.defaultValue ? b(l.defaultValue) : void 0
  } : l, [l]), ie = v(() => r ? b(r) : void 0, [r]), ae = v(() => s ? b(s) : void 0, [s]), ue = v(() => o ? b(o) : void 0, [o]), de = v(() => n ? b(n) : void 0, [n]), fe = v(() => d ? b(d) : void 0, [d]), _e = v(() => p ? b(p) : void 0, [p]);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: D
    }), /* @__PURE__ */ m.jsx(ge, {
      ...a,
      ref: F,
      value: ie,
      defaultValue: ae,
      defaultPickerValue: ue,
      pickerValue: de,
      minDate: fe,
      maxDate: _e,
      showTime: ce,
      disabledDate: re,
      getPopupContainer: oe,
      cellRender: e.cellRender ? L({
        slots: e,
        setSlotParams: R,
        key: "cellRender"
      }) : le,
      panelRender: e.panelRender ? L({
        slots: e,
        setSlotParams: R,
        key: "panelRender"
      }) : se,
      presets: v(() => (c || ne(i)).map((x) => ({
        ...x,
        value: b(x.value)
      })), [c, i]),
      onPanelChange: (x, ...N) => {
        const C = K(x);
        I == null || I(C, ...N);
      },
      onChange: (x, ...N) => {
        const C = K(x);
        _ == null || _(C, ...N), w(C);
      },
      renderExtraFooter: e.renderExtraFooter ? L({
        slots: e,
        setSlotParams: R,
        key: "renderExtraFooter"
      }) : a.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.prevIcon
      }) : a.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.nextIcon
      }) : a.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.suffixIcon
      }) : a.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.superNextIcon
      }) : a.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.superPrevIcon
      }) : a.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(g, {
          slot: e["allowClear.clearIcon"]
        })
      } : a.allowClear
    })]
  });
});
export {
  Ze as DatePicker,
  Ze as default
};
