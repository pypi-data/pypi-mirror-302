import { g as $, w as E } from "./Index-BziHDSZY.js";
const g = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Input;
var D = {
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
var te = g, re = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(e, r, n) {
  var l, o = {}, t = null, s = null;
  n !== void 0 && (t = "" + n), r.key !== void 0 && (t = "" + r.key), r.ref !== void 0 && (s = r.ref);
  for (l in r) oe.call(r, l) && !se.hasOwnProperty(l) && (o[l] = r[l]);
  if (e && e.defaultProps) for (l in r = e.defaultProps, r) o[l] === void 0 && (o[l] = r[l]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: le.current
  };
}
S.Fragment = ne;
S.jsx = M;
S.jsxs = M;
D.exports = S;
var _ = D.exports;
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
  detach: y,
  element: G,
  empty: A,
  exclude_internal_props: L,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: pe,
  insert_hydration: v,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: we,
  transition_in: C,
  transition_out: O,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: be,
  onDestroy: xe,
  setContext: Ee
} = window.__gradio__svelte__internal;
function T(e) {
  let r, n;
  const l = (
    /*#slots*/
    e[7].default
  ), o = ue(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      r = G("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      r = z(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(r);
      o && o.l(s), s.forEach(y), this.h();
    },
    h() {
      U(r, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      v(t, r, s), o && o.m(r, null), e[9](r), n = !0;
    },
    p(t, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && ge(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        n ? _e(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      n || (C(o, t), n = !0);
    },
    o(t) {
      O(o, t), n = !1;
    },
    d(t) {
      t && y(r), o && o.d(t), e[9](null);
    }
  };
}
function ve(e) {
  let r, n, l, o, t = (
    /*$$slots*/
    e[4].default && T(e)
  );
  return {
    c() {
      r = G("react-portal-target"), n = we(), t && t.c(), l = A(), this.h();
    },
    l(s) {
      r = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(r).forEach(y), n = ce(s), t && t.l(s), l = A(), this.h();
    },
    h() {
      U(r, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      v(s, r, a), e[8](r), v(s, n, a), t && t.m(s, a), v(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, a), a & /*$$slots*/
      16 && C(t, 1)) : (t = T(s), t.c(), C(t, 1), t.m(l.parentNode, l)) : t && (me(), O(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      o || (C(t), o = !0);
    },
    o(s) {
      O(t), o = !1;
    },
    d(s) {
      s && (y(r), y(n), y(l)), e[8](null), t && t.d(s);
    }
  };
}
function N(e) {
  const {
    svelteInit: r,
    ...n
  } = e;
  return n;
}
function Ce(e, r, n) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = r;
  const a = de(t);
  let {
    svelteInit: i
  } = r;
  const h = E(N(r)), f = E();
  F(e, f, (d) => n(0, l = d));
  const m = E();
  F(e, m, (d) => n(1, o = d));
  const c = [], u = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: H
  } = $() || {}, K = i({
    parent: u,
    props: h,
    target: f,
    slot: m,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: H,
    onDestroy(d) {
      c.push(d);
    }
  });
  Ee("$$ms-gr-react-wrapper", K), ye(() => {
    h.set(N(r));
  }), xe(() => {
    c.forEach((d) => d());
  });
  function q(d) {
    P[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  function V(d) {
    P[d ? "unshift" : "push"](() => {
      o = d, m.set(o);
    });
  }
  return e.$$set = (d) => {
    n(17, r = k(k({}, r), L(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, r = L(r), [l, o, f, m, a, i, s, t, q, V];
}
class Se extends ie {
  constructor(r) {
    super(), pe(this, r, Ce, ve, he, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ie(e) {
  function r(n) {
    const l = E(), o = new Se({
      ...n,
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
          }, a = t.parent ?? I;
          return a.nodes = [...a.nodes, s], B({
            createPortal: R,
            node: I
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), B({
              createPortal: R,
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
function Oe(e) {
  return e ? Object.keys(e).reduce((r, n) => {
    const l = e[n];
    return typeof l == "number" && !Re.includes(n) ? r[n] = l + "px" : r[n] = l, r;
  }, {}) : {};
}
function j(e) {
  const r = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return r.push(R(g.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: g.Children.toArray(e._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...g.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: r
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      n.addEventListener(a, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = j(t);
      r.push(...a), n.appendChild(s);
    } else t.nodeType === 3 && n.appendChild(t.cloneNode());
  }
  return {
    clonedElement: n,
    portals: r
  };
}
function je(e, r) {
  e && (typeof e == "function" ? e(r) : e.current = r);
}
const w = J(({
  slot: e,
  clone: r,
  className: n,
  style: l
}, o) => {
  const t = Y(), [s, a] = Q([]);
  return X(() => {
    var m;
    if (!t.current || !e)
      return;
    let i = e;
    function h() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), je(o, c), n && c.classList.add(...n.split(" ")), l) {
        const u = Oe(l);
        Object.keys(u).forEach((p) => {
          c.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (r && window.MutationObserver) {
      let c = function() {
        var b;
        const {
          portals: u,
          clonedElement: p
        } = j(e);
        i = p, a(u), i.style.display = "contents", h(), (b = t.current) == null || b.appendChild(i);
      };
      c(), f = new window.MutationObserver(() => {
        var u, p;
        (u = t.current) != null && u.contains(i) && ((p = t.current) == null || p.removeChild(i)), c();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (m = t.current) == null || m.appendChild(i);
    return () => {
      var c, u;
      i.style.display = "", (c = t.current) != null && c.contains(i) && ((u = t.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, r, n, l, o]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function x(e) {
  return Z(() => ke(e), [e]);
}
function Pe(e, r) {
  return e ? /* @__PURE__ */ _.jsx(w, {
    slot: e,
    clone: r == null ? void 0 : r.clone
  }) : null;
}
function Fe({
  key: e,
  setSlotParams: r,
  slots: n
}, l) {
  return (...o) => (r(e, o), Pe(n[e], {
    clone: !0,
    ...l
  }));
}
const Le = Ie(({
  slots: e,
  children: r,
  count: n,
  showCount: l,
  onValueChange: o,
  onChange: t,
  elRef: s,
  setSlotParams: a,
  ...i
}) => {
  const h = x(n == null ? void 0 : n.strategy), f = x(n == null ? void 0 : n.exceedFormatter), m = x(n == null ? void 0 : n.show), c = x(typeof l == "object" ? l.formatter : void 0);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ _.jsx(ee.Search, {
      ...i,
      ref: s,
      onChange: (u) => {
        t == null || t(u), o(u.target.value);
      },
      showCount: e["showCount.formatter"] ? {
        formatter: Fe({
          slots: e,
          setSlotParams: a,
          key: "showCount.formatter"
        })
      } : typeof l == "object" && c ? {
        formatter: c
      } : l,
      count: {
        ...n,
        exceedFormatter: f,
        strategy: h,
        show: m || (n == null ? void 0 : n.show)
      },
      enterButton: e.enterButton ? /* @__PURE__ */ _.jsx(w, {
        slot: e.enterButton
      }) : i.enterButton,
      addonAfter: e.addonAfter ? /* @__PURE__ */ _.jsx(w, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ _.jsx(w, {
        slot: e.addonBefore
      }) : i.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(w, {
          slot: e["allowClear.clearIcon"]
        })
      } : i.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(w, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ _.jsx(w, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  Le as InputSearch,
  Le as default
};
