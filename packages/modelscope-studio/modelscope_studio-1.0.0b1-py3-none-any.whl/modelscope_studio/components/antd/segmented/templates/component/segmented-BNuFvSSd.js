import { g as $, w as E } from "./Index-iTHtB6wE.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Segmented;
var F = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(l, t, n) {
  var s, r = {}, e = null, o = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) le.call(t, s) && !se.hasOwnProperty(s) && (r[s] = t[s]);
  if (l && l.defaultProps) for (s in t = l.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ne,
    type: l,
    key: e,
    ref: o,
    props: r,
    _owner: oe.current
  };
}
S.Fragment = re;
S.jsx = M;
S.jsxs = M;
F.exports = S;
var g = F.exports;
const {
  SvelteComponent: ce,
  assign: O,
  binding_callbacks: k,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: j,
  compute_slots: de,
  create_slot: ue,
  detach: b,
  element: G,
  empty: P,
  exclude_internal_props: L,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: ge,
  transition_in: v,
  transition_out: R,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function T(l) {
  let t, n;
  const s = (
    /*#slots*/
    l[7].default
  ), r = ue(
    s,
    l,
    /*$$scope*/
    l[6],
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
      var o = W(t);
      r && r.l(o), o.forEach(b), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      y(e, t, o), r && r.m(t, null), l[9](t), n = !0;
    },
    p(e, o) {
      r && r.p && (!n || o & /*$$scope*/
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
          o,
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
      R(r, e), n = !1;
    },
    d(e) {
      e && b(t), r && r.d(e), l[9](null);
    }
  };
}
function Se(l) {
  let t, n, s, r, e = (
    /*$$slots*/
    l[4].default && T(l)
  );
  return {
    c() {
      t = G("react-portal-target"), n = ge(), e && e.c(), s = P(), this.h();
    },
    l(o) {
      t = z(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(b), n = ae(o), e && e.l(o), s = P(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      y(o, t, c), l[8](t), y(o, n, c), e && e.m(o, c), y(o, s, c), r = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = T(o), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (pe(), R(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(o) {
      r || (v(e), r = !0);
    },
    o(o) {
      R(e), r = !1;
    },
    d(o) {
      o && (b(t), b(n), b(s)), l[8](null), e && e.d(o);
    }
  };
}
function N(l) {
  const {
    svelteInit: t,
    ...n
  } = l;
  return n;
}
function xe(l, t, n) {
  let s, r, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(N(t)), u = E();
  j(l, u, (d) => n(0, s = d));
  const p = E();
  j(l, p, (d) => n(1, r = d));
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
    _.set(N(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function V(d) {
    k[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function J(d) {
    k[d ? "unshift" : "push"](() => {
      r = d, p.set(r);
    });
  }
  return l.$$set = (d) => {
    n(17, t = O(O({}, t), L(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, o = d.$$scope);
  }, t = L(t), [s, r, u, p, c, i, o, e, V, J];
}
class Ce extends ce {
  constructor(t) {
    super(), me(this, t, xe, Se, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, x = window.ms_globals.tree;
function Re(l) {
  function t(n) {
    const s = E(), r = new Ce({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, o], A({
            createPortal: C,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), A({
              createPortal: C,
              node: x
            });
          }), o;
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
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(l) {
  return l ? Object.keys(l).reduce((t, n) => {
    const s = l[n];
    return typeof s == "number" && !Ie.includes(n) ? t[n] = s + "px" : t[n] = s, t;
  }, {}) : {};
}
function I(l) {
  const t = [], n = l.cloneNode(!1);
  if (l._reactElement)
    return t.push(C(h.cloneElement(l._reactElement, {
      ...l._reactElement.props,
      children: h.Children.toArray(l._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = I(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: o,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(l.getEventListeners()).forEach((r) => {
    l.getEventListeners(r).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      n.addEventListener(c, o, i);
    });
  });
  const s = Array.from(l.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = I(e);
      t.push(...c), n.appendChild(o);
    } else e.nodeType === 3 && n.appendChild(e.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function ke(l, t) {
  l && (typeof l == "function" ? l(t) : l.current = t);
}
const D = Y(({
  slot: l,
  clone: t,
  className: n,
  style: s
}, r) => {
  const e = K(), [o, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !l)
      return;
    let i = l;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(r, a), n && a.classList.add(...n.split(" ")), s) {
        const f = Oe(s);
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
        } = I(l);
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
  }, [l, t, n, s, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function H(l, t) {
  return l.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return n;
    const s = {
      ...n.props
    };
    let r = s;
    Object.keys(n.slots).forEach((o) => {
      if (!n.slots[o] || !(n.slots[o] instanceof Element) && !n.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((a, f) => {
        r[a] || (r[a] = {}), f !== c.length - 1 && (r = s[a]);
      });
      const i = n.slots[o];
      let _, u, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, u = i.callback, p = i.clone || !1), r[c[c.length - 1]] = _ ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ g.jsx(D, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ g.jsx(D, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : r[c[c.length - 1]], r = s;
    });
    const e = "children";
    return n[e] && (s[e] = H(n[e], t)), s;
  });
}
const Pe = Re(({
  slotItems: l,
  options: t,
  onChange: n,
  onValueChange: s,
  children: r,
  ...e
}) => /* @__PURE__ */ g.jsxs(g.Fragment, {
  children: [/* @__PURE__ */ g.jsx("div", {
    style: {
      display: "none"
    },
    children: r
  }), /* @__PURE__ */ g.jsx(ee, {
    ...e,
    onChange: (o) => {
      n == null || n(o), s(o);
    },
    options: Z(() => t || H(l), [t, l])
  })]
}));
export {
  Pe as Segmented,
  Pe as default
};
