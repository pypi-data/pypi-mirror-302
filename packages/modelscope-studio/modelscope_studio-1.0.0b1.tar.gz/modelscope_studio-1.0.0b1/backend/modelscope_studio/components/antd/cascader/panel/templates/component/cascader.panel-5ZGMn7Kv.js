import { g as $, w as E } from "./Index-BazWaFx1.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Cascader;
var D = {
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(o, t, n) {
  var s, r = {}, e = null, l = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) oe.call(t, s) && !se.hasOwnProperty(s) && (r[s] = t[s]);
  if (o && o.defaultProps) for (s in t = o.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ne,
    type: o,
    key: e,
    ref: l,
    props: r,
    _owner: le.current
  };
}
x.Fragment = re;
x.jsx = M;
x.jsxs = M;
D.exports = x;
var h = D.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: j,
  check_outros: ae,
  children: W,
  claim_element: z,
  claim_space: ie,
  component_subscribe: P,
  compute_slots: de,
  create_slot: ue,
  detach: b,
  element: G,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: ge,
  transition_in: v,
  transition_out: S,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(o) {
  let t, n;
  const s = (
    /*#slots*/
    o[7].default
  ), r = ue(
    s,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = W(t);
      r && r.l(l), l.forEach(b), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, t, l), r && r.m(t, null), o[9](t), n = !0;
    },
    p(e, l) {
      r && r.p && (!n || l & /*$$scope*/
      64) && be(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        n ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (v(r, e), n = !0);
    },
    o(e) {
      S(r, e), n = !1;
    },
    d(e) {
      e && b(t), r && r.d(e), o[9](null);
    }
  };
}
function Ce(o) {
  let t, n, s, r, e = (
    /*$$slots*/
    o[4].default && N(o)
  );
  return {
    c() {
      t = G("react-portal-target"), n = ge(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      t = z(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(b), n = ie(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      y(l, t, c), o[8](t), y(l, n, c), e && e.m(l, c), y(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (pe(), S(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      r || (v(e), r = !0);
    },
    o(l) {
      S(e), r = !1;
    },
    d(l) {
      l && (b(t), b(n), b(s)), o[8](null), e && e.d(l);
    }
  };
}
function A(o) {
  const {
    svelteInit: t,
    ...n
  } = o;
  return n;
}
function xe(o, t, n) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = de(e);
  let {
    svelteInit: a
  } = t;
  const _ = E(A(t)), u = E();
  P(o, u, (d) => n(0, s = d));
  const p = E();
  P(o, p, (d) => n(1, r = d));
  const i = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q
  } = $() || {}, B = a({
    parent: f,
    props: _,
    target: u,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q,
    onDestroy(d) {
      i.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", B), we(() => {
    _.set(A(t));
  }), ye(() => {
    i.forEach((d) => d());
  });
  function V(d) {
    j[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function J(d) {
    j[d ? "unshift" : "push"](() => {
      r = d, p.set(r);
    });
  }
  return o.$$set = (d) => {
    n(17, t = k(k({}, t), T(d))), "svelteInit" in d && n(5, a = d.svelteInit), "$$scope" in d && n(6, l = d.$$scope);
  }, t = T(t), [s, r, u, p, c, a, l, e, V, J];
}
class Ie extends ce {
  constructor(t) {
    super(), me(this, t, xe, Ce, he, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(o) {
  function t(n) {
    const s = E(), r = new Ie({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, l], F({
            createPortal: R,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== s), F({
              createPortal: R,
              node: I
            });
          }), l;
        },
        ...n.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(o) {
  return o ? Object.keys(o).reduce((t, n) => {
    const s = o[n];
    return typeof s == "number" && !Se.includes(n) ? t[n] = s + "px" : t[n] = s, t;
  }, {}) : {};
}
function O(o) {
  const t = [], n = o.cloneNode(!1);
  if (o._reactElement)
    return t.push(R(g.cloneElement(o._reactElement, {
      ...o._reactElement.props,
      children: g.Children.toArray(o._reactElement.props.children).map((r) => {
        if (g.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(r.props.el);
          return g.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...g.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(o.getEventListeners()).forEach((r) => {
    o.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: a
    }) => {
      n.addEventListener(c, l, a);
    });
  });
  const s = Array.from(o.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(e);
      t.push(...c), n.appendChild(l);
    } else e.nodeType === 3 && n.appendChild(e.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function ke(o, t) {
  o && (typeof o == "function" ? o(t) : o.current = t);
}
const C = Y(({
  slot: o,
  clone: t,
  className: n,
  style: s
}, r) => {
  const e = K(), [l, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !o)
      return;
    let a = o;
    function _() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), ke(r, i), n && i.classList.add(...n.split(" ")), s) {
        const f = Oe(s);
        Object.keys(f).forEach((m) => {
          i.style[m] = f[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = O(o);
        a = m, c(f), a.style.display = "contents", _(), (w = e.current) == null || w.appendChild(a);
      };
      i(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(a) && ((m = e.current) == null || m.removeChild(a)), i();
      }), u.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", _(), (p = e.current) == null || p.appendChild(a);
    return () => {
      var i, f;
      a.style.display = "", (i = e.current) != null && i.contains(a) && ((f = e.current) == null || f.removeChild(a)), u == null || u.disconnect();
    };
  }, [o, t, n, s, r]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function H(o, t) {
  return o.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return n;
    const s = {
      ...n.props
    };
    let r = s;
    Object.keys(n.slots).forEach((l) => {
      if (!n.slots[l] || !(n.slots[l] instanceof Element) && !n.slots[l].el)
        return;
      const c = l.split(".");
      c.forEach((i, f) => {
        r[i] || (r[i] = {}), f !== c.length - 1 && (r = s[i]);
      });
      const a = n.slots[l];
      let _, u, p = !1;
      a instanceof Element ? _ = a : (_ = a.el, u = a.callback, p = a.clone || !1), r[c[c.length - 1]] = _ ? u ? (...i) => (u(c[c.length - 1], i), /* @__PURE__ */ h.jsx(C, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(C, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : r[c[c.length - 1]], r = s;
    });
    const e = "children";
    return n[e] && (s[e] = H(n[e], t)), s;
  });
}
const Pe = Re(({
  slots: o,
  children: t,
  onValueChange: n,
  onChange: s,
  onLoadData: r,
  optionItems: e,
  options: l,
  ...c
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ h.jsx(ee.Panel, {
    ...c,
    options: Z(() => l || H(e), [l, e]),
    loadData: r,
    onChange: (a, ..._) => {
      s == null || s(a, ..._), n(a);
    },
    expandIcon: o.expandIcon ? /* @__PURE__ */ h.jsx(C, {
      slot: o.expandIcon
    }) : c.expandIcon,
    notFoundContent: o.notFoundContent ? /* @__PURE__ */ h.jsx(C, {
      slot: o.notFoundContent
    }) : c.notFoundContent
  })]
}));
export {
  Pe as CascaderPanel,
  Pe as default
};
