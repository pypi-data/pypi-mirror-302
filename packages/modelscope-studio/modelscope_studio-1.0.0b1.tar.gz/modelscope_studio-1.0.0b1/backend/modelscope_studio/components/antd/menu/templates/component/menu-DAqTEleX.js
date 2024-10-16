import { g as $, w as E } from "./Index-Cup8gtx4.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, V = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Menu;
var M = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = h, re = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, l) {
  var o, r = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) le.call(t, o) && !oe.hasOwnProperty(o) && (r[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: se.current
  };
}
I.Fragment = ne;
I.jsx = F;
I.jsxs = F;
M.exports = I;
var w = M.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: P,
  check_outros: ie,
  children: U,
  claim_element: W,
  claim_space: de,
  component_subscribe: L,
  compute_slots: ae,
  create_slot: ue,
  detach: b,
  element: z,
  empty: C,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: pe,
  insert_hydration: g,
  safe_not_equal: he,
  set_custom_element_data: G,
  space: we,
  transition_in: v,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ge,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(n) {
  let t, l;
  const o = (
    /*#slots*/
    n[7].default
  ), r = ue(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = z("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      r && r.l(s), s.forEach(b), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      g(e, t, s), r && r.m(t, null), n[9](t), l = !0;
    },
    p(e, s) {
      r && r.p && (!l || s & /*$$scope*/
      64) && be(
        r,
        o,
        e,
        /*$$scope*/
        e[6],
        l ? _e(
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
      l || (v(r, e), l = !0);
    },
    o(e) {
      O(r, e), l = !1;
    },
    d(e) {
      e && b(t), r && r.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, l, o, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = z("react-portal-target"), l = we(), e && e.c(), o = C(), this.h();
    },
    l(s) {
      t = W(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(b), l = de(s), e && e.l(s), o = C(), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      g(s, t, c), n[8](t), g(s, l, c), e && e.m(s, c), g(s, o, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(s), e.c(), v(e, 1), e.m(o.parentNode, o)) : e && (me(), O(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      r || (v(e), r = !0);
    },
    o(s) {
      O(e), r = !1;
    },
    d(s) {
      s && (b(t), b(l), b(o)), n[8](null), e && e.d(s);
    }
  };
}
function A(n) {
  const {
    svelteInit: t,
    ...l
  } = n;
  return l;
}
function Ie(n, t, l) {
  let o, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const f = E(A(t)), d = E();
  L(n, d, (u) => l(0, o = u));
  const m = E();
  L(n, m, (u) => l(1, r = u));
  const a = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: H
  } = $() || {}, q = i({
    parent: _,
    props: f,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: H,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", q), ye(() => {
    f.set(A(t));
  }), ge(() => {
    a.forEach((u) => u());
  });
  function B(u) {
    P[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function J(u) {
    P[u ? "unshift" : "push"](() => {
      r = u, m.set(r);
    });
  }
  return n.$$set = (u) => {
    l(17, t = j(j({}, t), T(u))), "svelteInit" in u && l(5, i = u.svelteInit), "$$scope" in u && l(6, s = u.$$scope);
  }, t = T(t), [o, r, d, m, c, i, s, e, B, J];
}
class Re extends ce {
  constructor(t) {
    super(), pe(this, t, Ie, xe, he, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, R = window.ms_globals.tree;
function Se(n) {
  function t(l) {
    const o = E(), r = new Re({
      ...l,
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
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, s], K({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), K({
              createPortal: S,
              node: R
            });
          }), s;
        },
        ...l.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, l) => {
    const o = n[l];
    return typeof o == "number" && !Oe.includes(l) ? t[l] = o + "px" : t[l] = o, t;
  }, {}) : {};
}
function k(n) {
  const t = [], l = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(S(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      l.addEventListener(c, s, i);
    });
  });
  const o = Array.from(n.childNodes);
  for (let r = 0; r < o.length; r++) {
    const e = o[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(e);
      t.push(...c), l.appendChild(s);
    } else e.nodeType === 3 && l.appendChild(e.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function je(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const x = Y(({
  slot: n,
  clone: t,
  className: l,
  style: o
}, r) => {
  const e = Q(), [s, c] = X([]);
  return Z(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function f() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), je(r, a), l && a.classList.add(...l.split(" ")), o) {
        const _ = ke(o);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var y;
        const {
          portals: _,
          clonedElement: p
        } = k(n);
        i = p, c(_), i.style.display = "contents", f(), (y = e.current) == null || y.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var _, p;
        (_ = e.current) != null && _.contains(i) && ((p = e.current) == null || p.removeChild(i)), a();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", f(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, l, o, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Pe(n) {
  return Object.keys(n).reduce((t, l) => (n[l] !== void 0 && (t[l] = n[l]), t), {});
}
function D(n, t) {
  return n.filter(Boolean).map((l) => {
    if (typeof l != "object")
      return l;
    const o = {
      ...l.props
    };
    let r = o;
    Object.keys(l.slots).forEach((s) => {
      if (!l.slots[s] || !(l.slots[s] instanceof Element) && !l.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, _) => {
        r[a] || (r[a] = {}), _ !== c.length - 1 && (r = o[a]);
      });
      const i = l.slots[s];
      let f, d, m = !1;
      i instanceof Element ? f = i : (f = i.el, d = i.callback, m = i.clone || !1), r[c[c.length - 1]] = f ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ w.jsx(x, {
        slot: f,
        clone: m || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ w.jsx(x, {
        slot: f,
        clone: m || (t == null ? void 0 : t.clone)
      }) : r[c[c.length - 1]], r = o;
    });
    const e = "children";
    return l[e] && (o[e] = D(l[e], t)), o;
  });
}
function Le(n, t) {
  return n ? /* @__PURE__ */ w.jsx(x, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Ce({
  key: n,
  setSlotParams: t,
  slots: l
}, o) {
  return (...r) => (t(n, r), Le(l[n], {
    clone: !0,
    ...o
  }));
}
const Ne = Se(({
  slots: n,
  items: t,
  slotItems: l,
  children: o,
  onValueChange: r,
  onOpenChange: e,
  onSelect: s,
  onDeselect: c,
  setSlotParams: i,
  ...f
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [o, /* @__PURE__ */ w.jsx(ee, {
    ...Pe(f),
    onOpenChange: (d) => {
      e == null || e(d), r == null || r({
        openKeys: d,
        selectedKeys: f.selectedKeys || []
      });
    },
    onSelect: (d) => {
      s == null || s(d), r == null || r({
        openKeys: f.openKeys || [],
        selectedKeys: d.selectedKeys
      });
    },
    onDeselect: (d) => {
      c == null || c(d), r == null || r({
        openKeys: f.openKeys || [],
        selectedKeys: d.selectedKeys
      });
    },
    items: V(() => t || D(l), [t, l]),
    expandIcon: n.expandIcon ? Ce({
      key: "expandIcon",
      slots: n,
      setSlotParams: i
    }, {
      clone: !0
    }) : f.expandIcon,
    overflowedIndicator: n.overflowedIndicator ? /* @__PURE__ */ w.jsx(x, {
      slot: n.overflowedIndicator
    }) : f.overflowedIndicator
  })]
}));
export {
  Ne as Menu,
  Ne as default
};
