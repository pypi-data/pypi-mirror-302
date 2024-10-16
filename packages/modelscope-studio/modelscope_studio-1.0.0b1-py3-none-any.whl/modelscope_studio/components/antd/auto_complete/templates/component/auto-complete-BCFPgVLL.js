import { g as ee, w as C } from "./Index-BYFyNtph.js";
const g = window.ms_globals.React, z = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, P = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.internalContext.AutoCompleteContext, ne = window.ms_globals.antd.AutoComplete;
var G = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var re = g, le = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, e, r) {
  var o, l = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) se.call(e, o) && !ae.hasOwnProperty(o) && (l[o] = e[o]);
  if (n && n.defaultProps) for (o in e = n.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: le,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: ce.current
  };
}
x.Fragment = oe;
x.jsx = U;
x.jsxs = U;
G.exports = x;
var m = G.exports;
const {
  SvelteComponent: ie,
  assign: A,
  binding_callbacks: F,
  check_outros: ue,
  children: H,
  claim_element: q,
  claim_space: de,
  component_subscribe: L,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: B,
  empty: T,
  exclude_internal_props: N,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: he,
  init: we,
  insert_hydration: E,
  safe_not_equal: ge,
  set_custom_element_data: V,
  space: be,
  transition_in: v,
  transition_out: k,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ce,
  getContext: Ee,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function D(n) {
  let e, r;
  const o = (
    /*#slots*/
    n[7].default
  ), l = _e(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = B("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(e);
      l && l.l(s), s.forEach(b), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      E(t, e, s), l && l.m(e, null), n[9](e), r = !0;
    },
    p(t, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && ye(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? me(
          o,
          /*$$scope*/
          t[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (v(l, t), r = !0);
    },
    o(t) {
      k(l, t), r = !1;
    },
    d(t) {
      t && b(e), l && l.d(t), n[9](null);
    }
  };
}
function Re(n) {
  let e, r, o, l, t = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      e = B("react-portal-target"), r = be(), t && t.c(), o = T(), this.h();
    },
    l(s) {
      e = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(e).forEach(b), r = de(s), t && t.l(s), o = T(), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, e, c), n[8](e), E(s, r, c), t && t.m(s, c), E(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && v(t, 1)) : (t = D(s), t.c(), v(t, 1), t.m(o.parentNode, o)) : t && (he(), k(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(s) {
      l || (v(t), l = !0);
    },
    o(s) {
      k(t), l = !1;
    },
    d(s) {
      s && (b(e), b(r), b(o)), n[8](null), t && t.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Ie(n, e, r) {
  let o, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = fe(t);
  let {
    svelteInit: a
  } = e;
  const p = C(W(e)), d = C();
  L(n, d, (u) => r(0, o = u));
  const _ = C();
  L(n, _, (u) => r(1, l = u));
  const i = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: w,
    subSlotIndex: R
  } = ee() || {}, Y = a({
    parent: f,
    props: p,
    target: d,
    slot: _,
    slotKey: h,
    slotIndex: w,
    subSlotIndex: R,
    onDestroy(u) {
      i.push(u);
    }
  });
  xe("$$ms-gr-react-wrapper", Y), Ce(() => {
    p.set(W(e));
  }), ve(() => {
    i.forEach((u) => u());
  });
  function K(u) {
    F[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function Q(u) {
    F[u ? "unshift" : "push"](() => {
      l = u, _.set(l);
    });
  }
  return n.$$set = (u) => {
    r(17, e = A(A({}, e), N(u))), "svelteInit" in u && r(5, a = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, e = N(e), [o, l, d, _, c, a, s, t, K, Q];
}
class Se extends ie {
  constructor(e) {
    super(), we(this, e, Ie, Re, ge, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Oe(n) {
  function e(r) {
    const o = C(), l = new Se({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? I;
          return c.nodes = [...c.nodes, s], M({
            createPortal: O,
            node: I
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== o), M({
              createPortal: O,
              node: I
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const o = n[r];
    return typeof o == "number" && !ke.includes(r) ? e[r] = o + "px" : e[r] = o, e;
  }, {}) : {};
}
function j(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(O(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: a
    }) => {
      r.addEventListener(c, s, a);
    });
  });
  const o = Array.from(n.childNodes);
  for (let l = 0; l < o.length; l++) {
    const t = o[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(t);
      e.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Pe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const y = z(({
  slot: n,
  clone: e,
  className: r,
  style: o
}, l) => {
  const t = X(), [s, c] = Z([]);
  return $(() => {
    var _;
    if (!t.current || !n)
      return;
    let a = n;
    function p() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Pe(l, i), r && i.classList.add(...r.split(" ")), o) {
        const f = je(o);
        Object.keys(f).forEach((h) => {
          i.style[h] = f[h];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: f,
          clonedElement: h
        } = j(n);
        a = h, c(f), a.style.display = "contents", p(), (w = t.current) == null || w.appendChild(a);
      };
      i(), d = new window.MutationObserver(() => {
        var f, h;
        (f = t.current) != null && f.contains(a) && ((h = t.current) == null || h.removeChild(a)), i();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", p(), (_ = t.current) == null || _.appendChild(a);
    return () => {
      var i, f;
      a.style.display = "", (i = t.current) != null && i.contains(a) && ((f = t.current) == null || f.removeChild(a)), d == null || d.disconnect();
    };
  }, [n, e, r, o, l]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ae(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function S(n) {
  return P(() => Ae(n), [n]);
}
function J(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const o = {
      ...r.props
    };
    let l = o;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((i, f) => {
        l[i] || (l[i] = {}), f !== c.length - 1 && (l = o[i]);
      });
      const a = r.slots[s];
      let p, d, _ = !1;
      a instanceof Element ? p = a : (p = a.el, d = a.callback, _ = a.clone || !1), l[c[c.length - 1]] = p ? d ? (...i) => (d(c[c.length - 1], i), /* @__PURE__ */ m.jsx(y, {
        slot: p,
        clone: _ || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ m.jsx(y, {
        slot: p,
        clone: _ || (e == null ? void 0 : e.clone)
      }) : l[c[c.length - 1]], l = o;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (o[t] = J(r[t], e)), o;
  });
}
function Fe(n, e) {
  return n ? /* @__PURE__ */ m.jsx(y, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: e,
  slots: r
}, o) {
  return (...l) => (e(n, l), Fe(r[n], {
    clone: !0,
    ...o
  }));
}
const Te = z(({
  children: n,
  ...e
}, r) => /* @__PURE__ */ m.jsx(te.Provider, {
  value: P(() => ({
    ...e,
    elRef: r
  }), [e, r]),
  children: n
})), De = Oe(({
  slots: n,
  children: e,
  onValueChange: r,
  filterOption: o,
  onChange: l,
  options: t,
  optionItems: s,
  getPopupContainer: c,
  dropdownRender: a,
  elRef: p,
  setSlotParams: d,
  ..._
}) => {
  const i = S(c), f = S(o), h = S(a);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [n.children ? null : /* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ m.jsx(ne, {
      ..._,
      ref: p,
      allowClear: n["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(y, {
          slot: n["allowClear.clearIcon"]
        })
      } : _.allowClear,
      options: P(() => t || J(s, {
        children: "options"
      }), [s, t]),
      onChange: (w, ...R) => {
        l == null || l(w, ...R), r(w);
      },
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ m.jsx(y, {
        slot: n.notFoundContent
      }) : _.notFoundContent,
      filterOption: f || o,
      getPopupContainer: i,
      dropdownRender: n.dropdownRender ? Le({
        slots: n,
        setSlotParams: d,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : h,
      children: n.children ? /* @__PURE__ */ m.jsxs(Te, {
        children: [/* @__PURE__ */ m.jsx("div", {
          style: {
            display: "none"
          },
          children: e
        }), /* @__PURE__ */ m.jsx(y, {
          slot: n.children
        })]
      }) : null
    })]
  });
});
export {
  De as AutoComplete,
  De as default
};
