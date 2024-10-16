import { g as ee, w as v } from "./Index-BLU1Lo22.js";
const g = window.ms_globals.React, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, K = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tabs;
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
var ne = g, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(e, t, r) {
  var s, l = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) le.call(t, s) && !ae.hasOwnProperty(s) && (l[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
  return {
    $$typeof: re,
    type: e,
    key: n,
    ref: o,
    props: l,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var h = D.exports;
const {
  SvelteComponent: ce,
  assign: P,
  binding_callbacks: k,
  check_outros: ie,
  children: U,
  claim_element: W,
  claim_space: ue,
  component_subscribe: T,
  compute_slots: de,
  create_slot: fe,
  detach: E,
  element: G,
  empty: B,
  exclude_internal_props: L,
  get_all_dirty_from_scope: _e,
  get_slot_changes: pe,
  group_outros: he,
  init: be,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: H,
  space: ge,
  transition_in: y,
  transition_out: O,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ve,
  onDestroy: xe,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), l = fe(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = W(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = U(t);
      l && l.l(o), o.forEach(E), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      x(n, t, o), l && l.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      l && l.p && (!r || o & /*$$scope*/
      64) && Ee(
        l,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? pe(
          s,
          /*$$scope*/
          n[6],
          o,
          null
        ) : _e(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (y(l, n), r = !0);
    },
    o(n) {
      O(l, n), r = !1;
    },
    d(n) {
      n && E(t), l && l.d(n), e[9](null);
    }
  };
}
function Ce(e) {
  let t, r, s, l, n = (
    /*$$slots*/
    e[4].default && F(e)
  );
  return {
    c() {
      t = G("react-portal-target"), r = ge(), n && n.c(), s = B(), this.h();
    },
    l(o) {
      t = W(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(E), r = ue(o), n && n.l(o), s = B(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(o, a) {
      x(o, t, a), e[8](t), x(o, r, a), n && n.m(o, a), x(o, s, a), l = !0;
    },
    p(o, [a]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, a), a & /*$$slots*/
      16 && y(n, 1)) : (n = F(o), n.c(), y(n, 1), n.m(s.parentNode, s)) : n && (he(), O(n, 1, 1, () => {
        n = null;
      }), ie());
    },
    i(o) {
      l || (y(n), l = !0);
    },
    o(o) {
      O(n), l = !1;
    },
    d(o) {
      o && (E(t), E(r), E(s)), e[8](null), n && n.d(o);
    }
  };
}
function N(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ie(e, t, r) {
  let s, l, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const a = de(n);
  let {
    svelteInit: c
  } = t;
  const p = v(N(t)), u = v();
  T(e, u, (d) => r(0, s = d));
  const _ = v();
  T(e, _, (d) => r(1, l = d));
  const i = [], f = ve("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: w,
    subSlotIndex: V
  } = ee() || {}, J = c({
    parent: f,
    props: p,
    target: u,
    slot: _,
    slotKey: b,
    slotIndex: w,
    subSlotIndex: V,
    onDestroy(d) {
      i.push(d);
    }
  });
  ye("$$ms-gr-react-wrapper", J), we(() => {
    p.set(N(t));
  }), xe(() => {
    i.forEach((d) => d());
  });
  function Y(d) {
    k[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function Q(d) {
    k[d ? "unshift" : "push"](() => {
      l = d, _.set(l);
    });
  }
  return e.$$set = (d) => {
    r(17, t = P(P({}, t), L(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, o = d.$$scope);
  }, t = L(t), [s, l, u, _, a, c, o, n, Y, Q];
}
class Se extends ce {
  constructor(t) {
    super(), be(this, t, Ie, Ce, me, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(e) {
  function t(r) {
    const s = v(), l = new Se({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, a = n.parent ?? I;
          return a.nodes = [...a.nodes, o], A({
            createPortal: R,
            node: I
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== s), A({
              createPortal: R,
              node: I
            });
          }), o;
        },
        ...r.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return typeof s == "number" && !Oe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function j(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(R(g.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: g.Children.toArray(e._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: o
          } = j(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: o,
            children: [...g.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: o,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, o, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let l = 0; l < s.length; l++) {
    const n = s[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: a
      } = j(n);
      t.push(...a), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Pe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const m = X(({
  slot: e,
  clone: t,
  className: r,
  style: s
}, l) => {
  const n = Z(), [o, a] = K([]);
  return $(() => {
    var _;
    if (!n.current || !e)
      return;
    let c = e;
    function p() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Pe(l, i), r && i.classList.add(...r.split(" ")), s) {
        const f = je(s);
        Object.keys(f).forEach((b) => {
          i.style[b] = f[b];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: f,
          clonedElement: b
        } = j(e);
        c = b, a(f), c.style.display = "contents", p(), (w = n.current) == null || w.appendChild(c);
      };
      i(), u = new window.MutationObserver(() => {
        var f, b;
        (f = n.current) != null && f.contains(c) && ((b = n.current) == null || b.removeChild(c)), i();
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", p(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var i, f;
      c.style.display = "", (i = n.current) != null && i.contains(c) && ((f = n.current) == null || f.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, t, r, s, l]), g.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...o);
});
function ke(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function S(e) {
  return z(() => ke(e), [e]);
}
function Te(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function q(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let l = s;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const a = o.split(".");
      a.forEach((i, f) => {
        l[i] || (l[i] = {}), f !== a.length - 1 && (l = s[i]);
      });
      const c = r.slots[o];
      let p, u, _ = !1;
      c instanceof Element ? p = c : (p = c.el, u = c.callback, _ = c.clone || !1), l[a[a.length - 1]] = p ? u ? (...i) => (u(a[a.length - 1], i), /* @__PURE__ */ h.jsx(m, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(m, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      }) : l[a[a.length - 1]], l = s;
    });
    const n = "children";
    return r[n] && (s[n] = q(r[n], t)), s;
  });
}
function Be(e, t) {
  return e ? /* @__PURE__ */ h.jsx(m, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Le({
  key: e,
  setSlotParams: t,
  slots: r
}, s) {
  return (...l) => (t(e, l), Be(r[e], {
    clone: !0,
    ...s
  }));
}
const Ne = Re(({
  slots: e,
  indicator: t,
  items: r,
  onChange: s,
  onValueChange: l,
  slotItems: n,
  more: o,
  children: a,
  renderTabBar: c,
  setSlotParams: p,
  ...u
}) => {
  const _ = S(t == null ? void 0 : t.size), i = S(o == null ? void 0 : o.getPopupContainer), f = S(c);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: a
    }), /* @__PURE__ */ h.jsx(te, {
      ...u,
      indicator: _ ? {
        ...t,
        size: _
      } : t,
      renderTabBar: e.renderTabBar ? Le({
        slots: e,
        setSlotParams: p,
        key: "renderTabBar"
      }) : f,
      items: z(() => r || q(n), [r, n]),
      more: Te({
        ...o || {},
        getPopupContainer: i || (o == null ? void 0 : o.getPopupContainer),
        icon: e["more.icon"] ? /* @__PURE__ */ h.jsx(m, {
          slot: e["more.icon"]
        }) : o == null ? void 0 : o.icon
      }),
      tabBarExtraContent: e.tabBarExtraContent ? /* @__PURE__ */ h.jsx(m, {
        slot: e.tabBarExtraContent
      }) : e["tabBarExtraContent.left"] || e["tabBarExtraContent.right"] ? {
        left: e["tabBarExtraContent.left"] ? /* @__PURE__ */ h.jsx(m, {
          slot: e["tabBarExtraContent.left"]
        }) : void 0,
        right: e["tabBarExtraContent.right"] ? /* @__PURE__ */ h.jsx(m, {
          slot: e["tabBarExtraContent.right"]
        }) : void 0
      } : u.tabBarExtraContent,
      addIcon: e.addIcon ? /* @__PURE__ */ h.jsx(m, {
        slot: e.addIcon
      }) : u.addIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ h.jsx(m, {
        slot: e.removeIcon
      }) : u.removeIcon,
      onChange: (b) => {
        s == null || s(b), l(b);
      }
    })]
  });
});
export {
  Ne as Tabs,
  Ne as default
};
