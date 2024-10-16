import { g as ne, w as v, d as re, a as y } from "./Index-CxziM5DK.js";
const h = window.ms_globals.React, R = window.ms_globals.React.useMemo, z = window.ms_globals.React.useState, G = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, O = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Dropdown;
var U = {
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
var se = h, le = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, r) {
  var l, s = {}, e = null, o = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) ie.call(t, l) && !ae.hasOwnProperty(l) && (s[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) s[l] === void 0 && (s[l] = t[l]);
  return {
    $$typeof: le,
    type: n,
    key: e,
    ref: o,
    props: s,
    _owner: ue.current
  };
}
C.Fragment = ce;
C.jsx = H;
C.jsxs = H;
U.exports = C;
var b = U.exports;
const {
  SvelteComponent: de,
  assign: P,
  binding_callbacks: T,
  check_outros: fe,
  children: V,
  claim_element: q,
  claim_space: pe,
  component_subscribe: L,
  compute_slots: _e,
  create_slot: me,
  detach: w,
  element: J,
  empty: A,
  exclude_internal_props: N,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: I,
  safe_not_equal: ye,
  set_custom_element_data: Y,
  space: Ee,
  transition_in: x,
  transition_out: k,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ie,
  getContext: xe,
  onDestroy: Re,
  setContext: Ce
} = window.__gradio__svelte__internal;
function D(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), s = me(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), s && s.c(), this.h();
    },
    l(e) {
      t = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = V(t);
      s && s.l(o), o.forEach(w), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      I(e, t, o), s && s.m(t, null), n[9](t), r = !0;
    },
    p(e, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && ve(
        s,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ge(
          l,
          /*$$scope*/
          e[6],
          o,
          null
        ) : he(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (x(s, e), r = !0);
    },
    o(e) {
      k(s, e), r = !1;
    },
    d(e) {
      e && w(t), s && s.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, r, l, s, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = J("react-portal-target"), r = Ee(), e && e.c(), l = A(), this.h();
    },
    l(o) {
      t = q(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), V(t).forEach(w), r = pe(o), e && e.l(o), l = A(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      I(o, t, c), n[8](t), I(o, r, c), e && e.m(o, c), I(o, l, c), s = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = D(o), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (we(), k(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(o) {
      s || (x(e), s = !0);
    },
    o(o) {
      k(e), s = !1;
    },
    d(o) {
      o && (w(t), w(r), w(l)), n[8](null), e && e.d(o);
    }
  };
}
function F(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Oe(n, t, r) {
  let l, s, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = _e(e);
  let {
    svelteInit: i
  } = t;
  const p = v(F(t)), f = v();
  L(n, f, (d) => r(0, l = d));
  const _ = v();
  L(n, _, (d) => r(1, s = d));
  const u = [], a = xe("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: Q
  } = ne() || {}, X = i({
    parent: a,
    props: p,
    target: f,
    slot: _,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: Q,
    onDestroy(d) {
      u.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", X), Ie(() => {
    p.set(F(t));
  }), Re(() => {
    u.forEach((d) => d());
  });
  function Z(d) {
    T[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  function $(d) {
    T[d ? "unshift" : "push"](() => {
      s = d, _.set(s);
    });
  }
  return n.$$set = (d) => {
    r(17, t = P(P({}, t), N(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, o = d.$$scope);
  }, t = N(t), [l, s, f, _, c, i, o, e, Z, $];
}
class ke extends de {
  constructor(t) {
    super(), be(this, t, Oe, Se, ye, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, S = window.ms_globals.tree;
function je(n) {
  function t(r) {
    const l = v(), s = new ke({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, o], B({
            createPortal: O,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), B({
              createPortal: O,
              node: S
            });
          }), o;
        },
        ...r.props
      }
    });
    return l.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function Pe(n) {
  const [t, r] = z(() => y(n));
  return G(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Te(n) {
  const t = R(() => re(n, (r) => r), [n]);
  return Pe(t);
}
const Le = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Le.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function j(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((s) => {
        if (h.isValidElement(s) && s.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = j(s.props.el);
          return h.cloneElement(s, {
            ...s.props,
            el: o,
            children: [...h.Children.toArray(s.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, o, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let s = 0; s < l.length; s++) {
    const e = l[s];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = j(e);
      t.push(...c), r.appendChild(o);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ne(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const E = ee(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, s) => {
  const e = te(), [o, c] = z([]);
  return G(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function p() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Ne(s, u), r && u.classList.add(...r.split(" ")), l) {
        const a = Ae(l);
        Object.keys(a).forEach((m) => {
          u.style[m] = a[m];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var g;
        const {
          portals: a,
          clonedElement: m
        } = j(n);
        i = m, c(a), i.style.display = "contents", p(), (g = e.current) == null || g.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var a, m;
        (a = e.current) != null && a.contains(i) && ((m = e.current) == null || m.removeChild(i)), u();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, a;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((a = e.current) == null || a.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, r, l, s]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function De(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function M(n) {
  return R(() => De(n), [n]);
}
function Fe(n, t) {
  const r = R(() => h.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, o) => {
    if (e.props.node.slotIndex && o.props.node.slotIndex) {
      const c = y(e.props.node.slotIndex) || 0, i = y(o.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && o.props.node.subSlotIndex ? (y(e.props.node.subSlotIndex) || 0) - (y(o.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Te(r);
}
function K(n, t) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let s = l;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((u, a) => {
        s[u] || (s[u] = {}), a !== c.length - 1 && (s = l[u]);
      });
      const i = r.slots[o];
      let p, f, _ = !1;
      i instanceof Element ? p = i : (p = i.el, f = i.callback, _ = i.clone || !1), s[c[c.length - 1]] = p ? f ? (...u) => (f(c[c.length - 1], u), /* @__PURE__ */ b.jsx(E, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ b.jsx(E, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = l;
    });
    const e = "children";
    return r[e] && (l[e] = K(r[e], t)), l;
  });
}
function Be(n, t) {
  return n ? /* @__PURE__ */ b.jsx(E, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function W({
  key: n,
  setSlotParams: t,
  slots: r
}, l) {
  return (...s) => (t(n, s), Be(r[n], {
    clone: !0,
    ...l
  }));
}
const We = je(({
  getPopupContainer: n,
  slots: t,
  menuItems: r,
  children: l,
  dropdownRender: s,
  setSlotParams: e,
  ...o
}) => {
  var f, _, u;
  const c = M(n), i = M(s), p = Fe(l, "buttonsRender");
  return /* @__PURE__ */ b.jsx(oe.Button, {
    ...o,
    buttonsRender: p.length ? (...a) => (e("buttonsRender", a), p.map((m, g) => /* @__PURE__ */ b.jsx(E, {
      slot: m
    }, g))) : o.buttonsRender,
    menu: {
      ...o.menu,
      items: R(() => {
        var a;
        return ((a = o.menu) == null ? void 0 : a.items) || K(r);
      }, [r, (f = o.menu) == null ? void 0 : f.items]),
      expandIcon: t["menu.expandIcon"] ? W({
        slots: t,
        setSlotParams: e,
        key: "menu.expandIcon"
      }, {
        clone: !0
      }) : (_ = o.menu) == null ? void 0 : _.expandIcon,
      overflowedIndicator: t["menu.overflowedIndicator"] ? /* @__PURE__ */ b.jsx(E, {
        slot: t["menu.overflowedIndicator"]
      }) : (u = o.menu) == null ? void 0 : u.overflowedIndicator
    },
    getPopupContainer: c,
    dropdownRender: t.dropdownRender ? W({
      slots: t,
      setSlotParams: e,
      key: "dropdownRender"
    }, {
      clone: !0
    }) : i
  });
});
export {
  We as DropdownButton,
  We as default
};
