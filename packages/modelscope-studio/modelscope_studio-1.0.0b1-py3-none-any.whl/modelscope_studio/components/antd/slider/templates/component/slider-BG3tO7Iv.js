import { g as $, w as y } from "./Index-YakRDC_1.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, M = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Slider;
var G = {
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(r, n, t) {
  var l, o = {}, e = null, s = null;
  t !== void 0 && (e = "" + t), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) oe.call(n, l) && !le.hasOwnProperty(l) && (o[l] = n[l]);
  if (r && r.defaultProps) for (l in n = r.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ne,
    type: r,
    key: e,
    ref: s,
    props: o,
    _owner: se.current
  };
}
S.Fragment = re;
S.jsx = W;
S.jsxs = W;
G.exports = S;
var g = G.exports;
const {
  SvelteComponent: ie,
  assign: k,
  binding_callbacks: P,
  check_outros: ce,
  children: z,
  claim_element: U,
  claim_space: ae,
  component_subscribe: L,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: H,
  empty: j,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: E,
  safe_not_equal: he,
  set_custom_element_data: K,
  space: ge,
  transition_in: C,
  transition_out: I,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: Ce
} = window.__gradio__svelte__internal;
function F(r) {
  let n, t;
  const l = (
    /*#slots*/
    r[7].default
  ), o = de(
    l,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      n = H("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, n, s), o && o.m(n, null), r[9](n), t = !0;
    },
    p(e, s) {
      o && o.p && (!t || s & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        t ? pe(
          l,
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
      t || (C(o, e), t = !0);
    },
    o(e) {
      I(o, e), t = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), r[9](null);
    }
  };
}
function Se(r) {
  let n, t, l, o, e = (
    /*$$slots*/
    r[4].default && F(r)
  );
  return {
    c() {
      n = H("react-portal-target"), t = ge(), e && e.c(), l = j(), this.h();
    },
    l(s) {
      n = U(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(w), t = ae(s), e && e.l(s), l = j(), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, n, c), r[8](n), E(s, t, c), e && e.m(s, c), E(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = F(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (_e(), I(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      I(e), o = !1;
    },
    d(s) {
      s && (w(n), w(t), w(l)), r[8](null), e && e.d(s);
    }
  };
}
function N(r) {
  const {
    svelteInit: n,
    ...t
  } = r;
  return t;
}
function xe(r, n, t) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const m = y(N(n)), d = y();
  L(r, d, (a) => t(0, l = a));
  const p = y();
  L(r, p, (a) => t(1, o = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: q
  } = $() || {}, V = i({
    parent: f,
    props: m,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: q,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ce("$$ms-gr-react-wrapper", V), be(() => {
    m.set(N(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function B(a) {
    P[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function J(a) {
    P[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return r.$$set = (a) => {
    t(17, n = k(k({}, n), T(a))), "svelteInit" in a && t(5, i = a.svelteInit), "$$scope" in a && t(6, s = a.$$scope);
  }, n = T(n), [l, o, d, p, c, i, s, e, B, J];
}
class Re extends ie {
  constructor(n) {
    super(), me(this, n, xe, Se, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ie(r) {
  function n(t) {
    const l = y(), o = new Re({
      ...t,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, s], A({
            createPortal: R,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: x
            });
          }), s;
        },
        ...t.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((t) => {
    window.ms_globals.initializePromise.then(() => {
      t(n);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(r) {
  return r ? Object.keys(r).reduce((n, t) => {
    const l = r[t];
    return typeof l == "number" && !Oe.includes(t) ? n[t] = l + "px" : n[t] = l, n;
  }, {}) : {};
}
function O(r) {
  const n = [], t = r.cloneNode(!1);
  if (r._reactElement)
    return n.push(R(h.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: h.Children.toArray(r._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), t)), {
      clonedElement: t,
      portals: n
    };
  Object.keys(r.getEventListeners()).forEach((o) => {
    r.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      t.addEventListener(c, s, i);
    });
  });
  const l = Array.from(r.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = O(e);
      n.push(...c), t.appendChild(s);
    } else e.nodeType === 3 && t.appendChild(e.cloneNode());
  }
  return {
    clonedElement: t,
    portals: n
  };
}
function Pe(r, n) {
  r && (typeof r == "function" ? r(n) : r.current = n);
}
const v = Y(({
  slot: r,
  clone: n,
  className: t,
  style: l
}, o) => {
  const e = Q(), [s, c] = X([]);
  return Z(() => {
    var p;
    if (!e.current || !r)
      return;
    let i = r;
    function m() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Pe(o, u), t && u.classList.add(...t.split(" ")), l) {
        const f = ke(l);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var b;
        const {
          portals: f,
          clonedElement: _
        } = O(r);
        i = _, c(f), i.style.display = "contents", m(), (b = e.current) == null || b.appendChild(i);
      };
      u(), d = new window.MutationObserver(() => {
        var f, _;
        (f = e.current) != null && f.contains(i) && ((_ = e.current) == null || _.removeChild(i)), u();
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [r, n, t, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(r) {
  try {
    return typeof r == "string" ? new Function(`return (...args) => (${r})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function D(r) {
  return M(() => Le(r), [r]);
}
const je = (r) => r.reduce((n, t) => {
  const l = t == null ? void 0 : t.props.number;
  return l !== void 0 && (n[l] = (t == null ? void 0 : t.slots.label) instanceof Element ? {
    ...t.props,
    label: /* @__PURE__ */ g.jsx(v, {
      slot: t == null ? void 0 : t.slots.label
    })
  } : (t == null ? void 0 : t.slots.children) instanceof Element ? /* @__PURE__ */ g.jsx(v, {
    slot: t == null ? void 0 : t.slots.children
  }) : {
    ...t == null ? void 0 : t.props
  }), n;
}, {}), Fe = Ie(({
  marks: r,
  markItems: n,
  children: t,
  onValueChange: l,
  onChange: o,
  elRef: e,
  tooltip: s,
  ...c
}) => {
  const i = (p) => {
    o == null || o(p), l(p);
  }, m = D(s == null ? void 0 : s.getPopupContainer), d = D(s == null ? void 0 : s.formatter);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(ee, {
      ...c,
      tooltip: {
        ...s,
        getPopupContainer: m,
        formatter: d
      },
      marks: M(() => r || je(n), [n, r]),
      ref: e,
      onChange: i
    })]
  });
});
export {
  Fe as Slider,
  Fe as default
};
