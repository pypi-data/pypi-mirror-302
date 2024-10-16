import { g as $, w as E } from "./Index-ByKJ1bKo.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Timeline;
var F = {
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
x.Fragment = re;
x.jsx = M;
x.jsxs = M;
F.exports = x;
var h = F.exports;
const {
  SvelteComponent: ie,
  assign: k,
  binding_callbacks: j,
  check_outros: ce,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: P,
  compute_slots: de,
  create_slot: ue,
  detach: b,
  element: G,
  empty: T,
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
  transition_out: I,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(l) {
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
function Ce(l) {
  let t, r, o, n, e = (
    /*$$slots*/
    l[4].default && D(l)
  );
  return {
    c() {
      t = G("react-portal-target"), r = ge(), e && e.c(), o = T(), this.h();
    },
    l(s) {
      t = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(b), r = ae(s), e && e.l(s), o = T(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      y(s, t, i), l[8](t), y(s, r, i), e && e.m(s, i), y(s, o, i), n = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && v(e, 1)) : (e = D(s), e.c(), v(e, 1), e.m(o.parentNode, o)) : e && (pe(), I(e, 1, 1, () => {
        e = null;
      }), ce());
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
function N(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function xe(l, t, r) {
  let o, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = de(e);
  let {
    svelteInit: c
  } = t;
  const _ = E(N(t)), u = E();
  P(l, u, (d) => r(0, o = d));
  const p = E();
  P(l, p, (d) => r(1, n = d));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q
  } = $() || {}, B = c({
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
    r(17, t = k(k({}, t), L(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = L(t), [o, n, u, p, i, c, s, e, V, J];
}
class Re extends ie {
  constructor(t) {
    super(), me(this, t, xe, Ce, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, R = window.ms_globals.tree;
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
          }, i = e.parent ?? R;
          return i.nodes = [...i.nodes, s], A({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== o), A({
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
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const o = Array.from(l.childNodes);
  for (let n = 0; n < o.length; n++) {
    const e = o[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = O(e);
      t.push(...i), r.appendChild(s);
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
const C = Y(({
  slot: l,
  clone: t,
  className: r,
  style: o
}, n) => {
  const e = K(), [s, i] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !l)
      return;
    let c = l;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(n, a), r && a.classList.add(...r.split(" ")), o) {
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
        c = m, i(f), c.style.display = "contents", _(), (w = e.current) == null || w.appendChild(c);
      };
      a(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(c) && ((m = e.current) == null || m.removeChild(c)), a();
      }), u.observe(l, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (p = e.current) == null || p.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((f = e.current) == null || f.removeChild(c)), u == null || u.disconnect();
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
      const i = s.split(".");
      i.forEach((a, f) => {
        n[a] || (n[a] = {}), f !== i.length - 1 && (n = o[a]);
      });
      const c = r.slots[s];
      let _, u, p = !1;
      c instanceof Element ? _ = c : (_ = c.el, u = c.callback, p = c.clone || !1), n[i[i.length - 1]] = _ ? u ? (...a) => (u(i[i.length - 1], a), /* @__PURE__ */ h.jsx(C, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(C, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : n[i[i.length - 1]], n = o;
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
    items: Z(() => t || H(r), [t, r]),
    pending: l.pending ? /* @__PURE__ */ h.jsx(C, {
      slot: l.pending
    }) : n.pending,
    pendingDot: l.pendingDot ? /* @__PURE__ */ h.jsx(C, {
      slot: l.pendingDot
    }) : n.pendingDot
  })]
}));
export {
  Pe as Timeline,
  Pe as default
};
