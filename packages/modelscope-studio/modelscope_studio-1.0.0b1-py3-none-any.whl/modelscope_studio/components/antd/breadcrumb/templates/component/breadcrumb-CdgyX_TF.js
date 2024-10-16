import { g as $, w as E } from "./Index-1nay8m4R.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Breadcrumb;
var B = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, r) {
  var o, l = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) le.call(t, o) && !se.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: s,
    props: l,
    _owner: oe.current
  };
}
C.Fragment = re;
C.jsx = F;
C.jsxs = F;
B.exports = C;
var h = B.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: j,
  check_outros: ae,
  children: M,
  claim_element: W,
  claim_space: ie,
  component_subscribe: P,
  compute_slots: ue,
  create_slot: de,
  detach: b,
  element: z,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: G,
  space: ge,
  transition_in: v,
  transition_out: I,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(n) {
  let t, r;
  const o = (
    /*#slots*/
    n[7].default
  ), l = de(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = z("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = M(t);
      l && l.l(s), s.forEach(b), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), l && l.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && be(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (v(l, e), r = !0);
    },
    o(e) {
      I(l, e), r = !1;
    },
    d(e) {
      e && b(t), l && l.d(e), n[9](null);
    }
  };
}
function Re(n) {
  let t, r, o, l, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = z("react-portal-target"), r = ge(), e && e.c(), o = L(), this.h();
    },
    l(s) {
      t = W(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(t).forEach(b), r = ie(s), e && e.l(s), o = L(), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), n[8](t), y(s, r, c), e && e.m(s, c), y(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(s), e.c(), v(e, 1), e.m(o.parentNode, o)) : e && (pe(), I(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(s) {
      l || (v(e), l = !0);
    },
    o(s) {
      I(e), l = !1;
    },
    d(s) {
      s && (b(t), b(r), b(o)), n[8](null), e && e.d(s);
    }
  };
}
function A(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ce(n, t, r) {
  let o, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ue(e);
  let {
    svelteInit: a
  } = t;
  const _ = E(A(t)), d = E();
  P(n, d, (u) => r(0, o = u));
  const p = E();
  P(n, p, (u) => r(1, l = u));
  const i = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: H
  } = $() || {}, q = a({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: H,
    onDestroy(u) {
      i.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", q), we(() => {
    _.set(A(t));
  }), ye(() => {
    i.forEach((u) => u());
  });
  function V(u) {
    j[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function J(u) {
    j[u ? "unshift" : "push"](() => {
      l = u, p.set(l);
    });
  }
  return n.$$set = (u) => {
    r(17, t = k(k({}, t), T(u))), "svelteInit" in u && r(5, a = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = T(t), [o, l, d, p, c, a, s, e, V, J];
}
class xe extends ce {
  constructor(t) {
    super(), me(this, t, Ce, Re, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, x = window.ms_globals.tree;
function Se(n) {
  function t(r) {
    const o = E(), l = new xe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, s], D({
            createPortal: S,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== o), D({
              createPortal: S,
              node: x
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
      r(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const o = n[r];
    return typeof o == "number" && !Ie.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function O(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(S(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
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
    const e = o[l];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = O(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const R = Y(({
  slot: n,
  clone: t,
  className: r,
  style: o
}, l) => {
  const e = K(), [s, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !n)
      return;
    let a = n;
    function _() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), ke(l, i), r && i.classList.add(...r.split(" ")), o) {
        const f = Oe(o);
        Object.keys(f).forEach((m) => {
          i.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = O(n);
        a = m, c(f), a.style.display = "contents", _(), (w = e.current) == null || w.appendChild(a);
      };
      i(), d = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(a) && ((m = e.current) == null || m.removeChild(a)), i();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", _(), (p = e.current) == null || p.appendChild(a);
    return () => {
      var i, f;
      a.style.display = "", (i = e.current) != null && i.contains(a) && ((f = e.current) == null || f.removeChild(a)), d == null || d.disconnect();
    };
  }, [n, t, r, o, l]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function U(n, t) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
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
      let _, d, p = !1;
      a instanceof Element ? _ = a : (_ = a.el, d = a.callback, p = a.clone || !1), l[c[c.length - 1]] = _ ? d ? (...i) => (d(c[c.length - 1], i), /* @__PURE__ */ h.jsx(R, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(R, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = o;
    });
    const e = "children";
    return r[e] && (o[e] = U(r[e], t)), o;
  });
}
function je(n, t) {
  return n ? /* @__PURE__ */ h.jsx(R, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Pe({
  key: n,
  setSlotParams: t,
  slots: r
}, o) {
  return (...l) => (t(n, l), je(r[n], {
    clone: !0,
    ...o
  }));
}
const Te = Se(({
  slots: n,
  items: t,
  slotItems: r,
  setSlotParams: o,
  children: l,
  ...e
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: l
  }), /* @__PURE__ */ h.jsx(ee, {
    ...e,
    itemRender: n.itemRender ? Pe({
      setSlotParams: o,
      slots: n,
      key: "itemRender"
    }, {
      clone: !0
    }) : e.itemRender,
    items: Z(() => t || U(r), [t, r]),
    separator: n.separator ? /* @__PURE__ */ h.jsx(R, {
      slot: n.separator,
      clone: !0
    }) : e.separator
  })]
}));
export {
  Te as Breadcrumb,
  Te as default
};
