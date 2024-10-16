import { g as $, w as E } from "./Index-DaOGUbSx.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Descriptions;
var F = {
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
function M(l, t, r) {
  var o, n = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) le.call(t, o) && !se.hasOwnProperty(o) && (n[o] = t[o]);
  if (l && l.defaultProps) for (o in t = l.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: ne,
    type: l,
    key: e,
    ref: s,
    props: n,
    _owner: oe.current
  };
}
C.Fragment = re;
C.jsx = M;
C.jsxs = M;
F.exports = C;
var h = F.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: j,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ae,
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
  transition_out: I,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(l) {
  let t, r;
  const o = (
    /*#slots*/
    l[7].default
  ), n = ue(
    o,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(t);
      n && n.l(s), s.forEach(b), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), n && n.m(t, null), l[9](t), r = !0;
    },
    p(e, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && be(
        n,
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
      r || (v(n, e), r = !0);
    },
    o(e) {
      I(n, e), r = !1;
    },
    d(e) {
      e && b(t), n && n.d(e), l[9](null);
    }
  };
}
function xe(l) {
  let t, r, o, n, e = (
    /*$$slots*/
    l[4].default && N(l)
  );
  return {
    c() {
      t = G("react-portal-target"), r = ge(), e && e.c(), o = L(), this.h();
    },
    l(s) {
      t = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(b), r = ae(s), e && e.l(s), o = L(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), l[8](t), y(s, r, c), e && e.m(s, c), y(s, o, c), n = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(s), e.c(), v(e, 1), e.m(o.parentNode, o)) : e && (pe(), I(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      n || (v(e), n = !0);
    },
    o(s) {
      I(e), n = !1;
    },
    d(s) {
      s && (b(t), b(r), b(o)), l[8](null), e && e.d(s);
    }
  };
}
function A(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function Ce(l, t, r) {
  let o, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(A(t)), u = E();
  P(l, u, (d) => r(0, o = d));
  const p = E();
  P(l, p, (d) => r(1, n = d));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q
  } = $() || {}, B = i({
    parent: f,
    props: _,
    target: u,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", B), we(() => {
    _.set(A(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function V(d) {
    j[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function J(d) {
    j[d ? "unshift" : "push"](() => {
      n = d, p.set(n);
    });
  }
  return l.$$set = (d) => {
    r(17, t = k(k({}, t), T(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = T(t), [o, n, u, p, c, i, s, e, V, J];
}
class Re extends ce {
  constructor(t) {
    super(), me(this, t, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, R = window.ms_globals.tree;
function Se(l) {
  function t(r) {
    const o = E(), n = new Re({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, s], D({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), D({
              createPortal: S,
              node: R
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(l) {
  return l ? Object.keys(l).reduce((t, r) => {
    const o = l[r];
    return typeof o == "number" && !Ie.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function O(l) {
  const t = [], r = l.cloneNode(!1);
  if (l._reactElement)
    return t.push(S(g.cloneElement(l._reactElement, {
      ...l._reactElement.props,
      children: g.Children.toArray(l._reactElement.props.children).map((n) => {
        if (g.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(n.props.el);
          return g.cloneElement(n, {
            ...n.props,
            el: s,
            children: [...g.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(l.getEventListeners()).forEach((n) => {
    l.getEventListeners(n).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const o = Array.from(l.childNodes);
  for (let n = 0; n < o.length; n++) {
    const e = o[n];
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
function ke(l, t) {
  l && (typeof l == "function" ? l(t) : l.current = t);
}
const x = Y(({
  slot: l,
  clone: t,
  className: r,
  style: o
}, n) => {
  const e = K(), [s, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !l)
      return;
    let i = l;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(n, a), r && a.classList.add(...r.split(" ")), o) {
        const f = Oe(o);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = O(l);
        i = m, c(f), i.style.display = "contents", _(), (w = e.current) == null || w.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), u.observe(l, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", _(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [l, t, r, o, n]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function H(l, t) {
  return l.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const o = {
      ...r.props
    };
    let n = o;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        n[a] || (n[a] = {}), f !== c.length - 1 && (n = o[a]);
      });
      const i = r.slots[s];
      let _, u, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, u = i.callback, p = i.clone || !1), n[c[c.length - 1]] = _ ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ h.jsx(x, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(x, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : n[c[c.length - 1]], n = o;
    });
    const e = "children";
    return r[e] && (o[e] = H(r[e], t)), o;
  });
}
const Pe = Se(({
  slots: l,
  items: t,
  slotItems: r,
  children: o,
  ...n
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: o
  }), /* @__PURE__ */ h.jsx(ee, {
    ...n,
    extra: l.extra ? /* @__PURE__ */ h.jsx(x, {
      slot: l.extra
    }) : n.extra,
    title: l.title ? /* @__PURE__ */ h.jsx(x, {
      slot: l.title
    }) : n.title,
    items: Z(() => t || H(r), [t, r])
  })]
}));
export {
  Pe as Descriptions,
  Pe as default
};
