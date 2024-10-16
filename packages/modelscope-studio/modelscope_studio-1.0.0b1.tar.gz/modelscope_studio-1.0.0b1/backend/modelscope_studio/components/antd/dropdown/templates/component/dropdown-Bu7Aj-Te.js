import { g as te, w as y } from "./Index-C3Pv2D9v.js";
const w = window.ms_globals.React, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, $ = window.ms_globals.React.useState, ee = window.ms_globals.React.useEffect, W = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Dropdown;
var z = {
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
var re = w, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ie.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: ce.current
  };
}
C.Fragment = le;
C.jsx = G;
C.jsxs = G;
z.exports = C;
var h = z.exports;
const {
  SvelteComponent: ae,
  assign: O,
  binding_callbacks: j,
  check_outros: de,
  children: U,
  claim_element: H,
  claim_space: ue,
  component_subscribe: P,
  compute_slots: fe,
  create_slot: _e,
  detach: g,
  element: q,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: he,
  init: we,
  insert_hydration: E,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: be,
  transition_in: v,
  transition_out: S,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = _e(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      r && r.l(s), s.forEach(g), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && ye(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? me(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (v(r, e), o = !0);
    },
    o(e) {
      S(r, e), o = !1;
    },
    d(e) {
      e && g(t), r && r.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = q("react-portal-target"), o = be(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(g), o = ue(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, t, c), n[8](t), E(s, o, c), e && e.m(s, c), E(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (he(), S(e, 1, 1, () => {
        e = null;
      }), de());
    },
    i(s) {
      r || (v(e), r = !0);
    },
    o(s) {
      S(e), r = !1;
    },
    d(s) {
      s && (g(t), g(o), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function F(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Re(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = fe(e);
  let {
    svelteInit: i
  } = t;
  const p = y(F(t)), u = y();
  P(n, u, (d) => o(0, l = d));
  const _ = y();
  P(n, _, (d) => o(1, r = d));
  const a = [], f = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: J
  } = te() || {}, Y = i({
    parent: f,
    props: p,
    target: u,
    slot: _,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: J,
    onDestroy(d) {
      a.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", Y), Ee(() => {
    p.set(F(t));
  }), xe(() => {
    a.forEach((d) => d());
  });
  function K(d) {
    j[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function Q(d) {
    j[d ? "unshift" : "push"](() => {
      r = d, _.set(r);
    });
  }
  return n.$$set = (d) => {
    o(17, t = O(O({}, t), T(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, t = T(t), [l, r, u, _, c, i, s, e, K, Q];
}
class Se extends ae {
  constructor(t) {
    super(), we(this, t, Re, Ie, ge, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, I = window.ms_globals.tree;
function ke(n) {
  function t(o) {
    const l = y(), r = new Se({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, s], A({
            createPortal: R,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: I
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Oe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function k(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...w.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(e);
      t.push(...c), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Pe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const x = X(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = Z(), [s, c] = $([]);
  return ee(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(r, a), o && a.classList.add(...o.split(" ")), l) {
        const f = je(l);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: f,
          clonedElement: m
        } = k(n);
        i = m, c(f), i.style.display = "contents", p(), (b = e.current) == null || b.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, l, r]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function D(n) {
  return W(() => Le(n), [n]);
}
function V(n, t) {
  return n.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const l = {
      ...o.props
    };
    let r = l;
    Object.keys(o.slots).forEach((s) => {
      if (!o.slots[s] || !(o.slots[s] instanceof Element) && !o.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        r[a] || (r[a] = {}), f !== c.length - 1 && (r = l[a]);
      });
      const i = o.slots[s];
      let p, u, _ = !1;
      i instanceof Element ? p = i : (p = i.el, u = i.callback, _ = i.clone || !1), r[c[c.length - 1]] = p ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ h.jsx(x, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(x, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      }) : r[c[c.length - 1]], r = l;
    });
    const e = "children";
    return o[e] && (l[e] = V(o[e], t)), l;
  });
}
function Te(n, t) {
  return n ? /* @__PURE__ */ h.jsx(x, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function M({
  key: n,
  setSlotParams: t,
  slots: o
}, l) {
  return (...r) => (t(n, r), Te(o[n], {
    clone: !0,
    ...l
  }));
}
const Fe = ke(({
  getPopupContainer: n,
  innerStyle: t,
  children: o,
  slots: l,
  menuItems: r,
  dropdownRender: e,
  setSlotParams: s,
  ...c
}) => {
  var u, _, a;
  const i = D(n), p = D(e);
  return /* @__PURE__ */ h.jsx(h.Fragment, {
    children: /* @__PURE__ */ h.jsx(ne, {
      ...c,
      menu: {
        ...c.menu,
        items: W(() => {
          var f;
          return ((f = c.menu) == null ? void 0 : f.items) || V(r);
        }, [r, (u = c.menu) == null ? void 0 : u.items]),
        expandIcon: l["menu.expandIcon"] ? M({
          slots: l,
          setSlotParams: s,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : (_ = c.menu) == null ? void 0 : _.expandIcon,
        overflowedIndicator: l["menu.overflowedIndicator"] ? /* @__PURE__ */ h.jsx(x, {
          slot: l["menu.overflowedIndicator"]
        }) : (a = c.menu) == null ? void 0 : a.overflowedIndicator
      },
      getPopupContainer: i,
      dropdownRender: l.dropdownRender ? M({
        slots: l,
        setSlotParams: s,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : p,
      children: /* @__PURE__ */ h.jsx("div", {
        className: "ms-gr-antd-dropdown-content",
        style: {
          display: "inline-block",
          ...t
        },
        children: o
      })
    })
  });
});
export {
  Fe as Dropdown,
  Fe as default
};
