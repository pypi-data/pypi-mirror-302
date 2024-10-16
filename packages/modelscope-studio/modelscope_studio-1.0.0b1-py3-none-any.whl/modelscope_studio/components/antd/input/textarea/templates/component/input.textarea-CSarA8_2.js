import { g as $, w as E } from "./Index-DCDYVGns.js";
const h = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Input;
var D = {
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
var te = h, re = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(t, r, n) {
  var l, o = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), r.key !== void 0 && (e = "" + r.key), r.ref !== void 0 && (s = r.ref);
  for (l in r) oe.call(r, l) && !se.hasOwnProperty(l) && (o[l] = r[l]);
  if (t && t.defaultProps) for (l in r = t.defaultProps, r) o[l] === void 0 && (o[l] = r[l]);
  return {
    $$typeof: re,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: le.current
  };
}
C.Fragment = ne;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var w = D.exports;
const {
  SvelteComponent: ie,
  assign: k,
  binding_callbacks: P,
  check_outros: ae,
  children: W,
  claim_element: z,
  claim_space: ce,
  component_subscribe: F,
  compute_slots: de,
  create_slot: ue,
  detach: g,
  element: G,
  empty: j,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: v,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: we,
  transition_in: x,
  transition_out: R,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: be,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function L(t) {
  let r, n;
  const l = (
    /*#slots*/
    t[7].default
  ), o = ue(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      r = G("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      r = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(r);
      o && o.l(s), s.forEach(g), this.h();
    },
    h() {
      U(r, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, r, s), o && o.m(r, null), t[9](r), n = !0;
    },
    p(e, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && ge(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        n ? _e(
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
      n || (x(o, e), n = !0);
    },
    o(e) {
      R(o, e), n = !1;
    },
    d(e) {
      e && g(r), o && o.d(e), t[9](null);
    }
  };
}
function xe(t) {
  let r, n, l, o, e = (
    /*$$slots*/
    t[4].default && L(t)
  );
  return {
    c() {
      r = G("react-portal-target"), n = we(), e && e.c(), l = j(), this.h();
    },
    l(s) {
      r = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(r).forEach(g), n = ce(s), e && e.l(s), l = j(), this.h();
    },
    h() {
      U(r, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      v(s, r, a), t[8](r), v(s, n, a), e && e.m(s, a), v(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && x(e, 1)) : (e = L(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (pe(), R(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(s) {
      o || (x(e), o = !0);
    },
    o(s) {
      R(e), o = !1;
    },
    d(s) {
      s && (g(r), g(n), g(l)), t[8](null), e && e.d(s);
    }
  };
}
function A(t) {
  const {
    svelteInit: r,
    ...n
  } = t;
  return n;
}
function Ce(t, r, n) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = r;
  const a = de(e);
  let {
    svelteInit: i
  } = r;
  const m = E(A(r)), f = E();
  F(t, f, (d) => n(0, l = d));
  const _ = E();
  F(t, _, (d) => n(1, o = d));
  const c = [], u = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: K
  } = $() || {}, q = i({
    parent: u,
    props: m,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: K,
    onDestroy(d) {
      c.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", q), ye(() => {
    m.set(A(r));
  }), Ee(() => {
    c.forEach((d) => d());
  });
  function V(d) {
    P[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  function B(d) {
    P[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return t.$$set = (d) => {
    n(17, r = k(k({}, r), T(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, r = T(r), [l, o, f, _, a, i, s, e, V, B];
}
class Ie extends ie {
  constructor(r) {
    super(), me(this, r, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(t) {
  function r(n) {
    const l = E(), o = new Ie({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? I;
          return a.nodes = [...a.nodes, s], N({
            createPortal: S,
            node: I
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), N({
              createPortal: S,
              node: I
            });
          }), s;
        },
        ...n.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(t) {
  return t ? Object.keys(t).reduce((r, n) => {
    const l = t[n];
    return typeof l == "number" && !Re.includes(n) ? r[n] = l + "px" : r[n] = l, r;
  }, {}) : {};
}
function O(t) {
  const r = [], n = t.cloneNode(!1);
  if (t._reactElement)
    return r.push(S(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((o) => {
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
    }), n)), {
      clonedElement: n,
      portals: r
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      n.addEventListener(a, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = O(e);
      r.push(...a), n.appendChild(s);
    } else e.nodeType === 3 && n.appendChild(e.cloneNode());
  }
  return {
    clonedElement: n,
    portals: r
  };
}
function ke(t, r) {
  t && (typeof t == "function" ? t(r) : t.current = r);
}
const H = J(({
  slot: t,
  clone: r,
  className: n,
  style: l
}, o) => {
  const e = Y(), [s, a] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function m() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ke(o, c), n && c.classList.add(...n.split(" ")), l) {
        const u = Oe(l);
        Object.keys(u).forEach((p) => {
          c.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (r && window.MutationObserver) {
      let c = function() {
        var y;
        const {
          portals: u,
          clonedElement: p
        } = O(t);
        i = p, a(u), i.style.display = "contents", m(), (y = e.current) == null || y.appendChild(i);
      };
      c(), f = new window.MutationObserver(() => {
        var u, p;
        (u = e.current) != null && u.contains(i) && ((p = e.current) == null || p.removeChild(i)), c();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var c, u;
      i.style.display = "", (c = e.current) != null && c.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, r, n, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Pe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function b(t) {
  return Z(() => Pe(t), [t]);
}
function Fe(t, r) {
  return t ? /* @__PURE__ */ w.jsx(H, {
    slot: t,
    clone: r == null ? void 0 : r.clone
  }) : null;
}
function je({
  key: t,
  setSlotParams: r,
  slots: n
}, l) {
  return (...o) => (r(t, o), Fe(n[t], {
    clone: !0,
    ...l
  }));
}
const Le = Se(({
  slots: t,
  children: r,
  count: n,
  showCount: l,
  onValueChange: o,
  onChange: e,
  elRef: s,
  setSlotParams: a,
  ...i
}) => {
  const m = b(n == null ? void 0 : n.strategy), f = b(n == null ? void 0 : n.exceedFormatter), _ = b(n == null ? void 0 : n.show), c = b(typeof l == "object" ? l.formatter : void 0);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ w.jsx(ee.TextArea, {
      ...i,
      ref: s,
      onChange: (u) => {
        e == null || e(u), o(u.target.value);
      },
      showCount: t["showCount.formatter"] ? {
        formatter: je({
          slots: t,
          setSlotParams: a,
          key: "showCount.formatter"
        })
      } : typeof l == "object" && c ? {
        formatter: c
      } : l,
      count: {
        ...n,
        exceedFormatter: f,
        strategy: m,
        show: _ || (n == null ? void 0 : n.show)
      },
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ w.jsx(H, {
          slot: t["allowClear.clearIcon"]
        })
      } : i.allowClear
    })]
  });
});
export {
  Le as InputTextarea,
  Le as default
};
