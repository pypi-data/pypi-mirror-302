import { g as $, w as E } from "./Index-6HXryL0a.js";
const h = window.ms_globals.React, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, V = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Collapse;
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(r, t, l) {
  var o, n = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) le.call(t, o) && !se.hasOwnProperty(o) && (n[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: ne,
    type: r,
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
var b = F.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: P,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: j,
  compute_slots: de,
  create_slot: ue,
  detach: g,
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
  transition_out: S,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(r) {
  let t, l;
  const o = (
    /*#slots*/
    r[7].default
  ), n = ue(
    o,
    r,
    /*$$scope*/
    r[6],
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
      n && n.l(s), s.forEach(g), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), n && n.m(t, null), r[9](t), l = !0;
    },
    p(e, s) {
      n && n.p && (!l || s & /*$$scope*/
      64) && be(
        n,
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
      l || (v(n, e), l = !0);
    },
    o(e) {
      S(n, e), l = !1;
    },
    d(e) {
      e && g(t), n && n.d(e), r[9](null);
    }
  };
}
function xe(r) {
  let t, l, o, n, e = (
    /*$$slots*/
    r[4].default && N(r)
  );
  return {
    c() {
      t = G("react-portal-target"), l = ge(), e && e.c(), o = L(), this.h();
    },
    l(s) {
      t = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(g), l = ae(s), e && e.l(s), o = L(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), r[8](t), y(s, l, c), e && e.m(s, c), y(s, o, c), n = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(s), e.c(), v(e, 1), e.m(o.parentNode, o)) : e && (pe(), S(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      n || (v(e), n = !0);
    },
    o(s) {
      S(e), n = !1;
    },
    d(s) {
      s && (g(t), g(l), g(o)), r[8](null), e && e.d(s);
    }
  };
}
function A(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function Ie(r, t, l) {
  let o, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(A(t)), u = E();
  j(r, u, (d) => l(0, o = d));
  const p = E();
  j(r, p, (d) => l(1, n = d));
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
  function J(d) {
    P[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function Y(d) {
    P[d ? "unshift" : "push"](() => {
      n = d, p.set(n);
    });
  }
  return r.$$set = (d) => {
    l(17, t = k(k({}, t), T(d))), "svelteInit" in d && l(5, i = d.svelteInit), "$$scope" in d && l(6, s = d.$$scope);
  }, t = T(t), [o, n, u, p, c, i, s, e, J, Y];
}
class Re extends ce {
  constructor(t) {
    super(), me(this, t, Ie, xe, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(r) {
  function t(l) {
    const o = E(), n = new Re({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, s], D({
            createPortal: R,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), D({
              createPortal: R,
              node: I
            });
          }), s;
        },
        ...l.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(r) {
  return r ? Object.keys(r).reduce((t, l) => {
    const o = r[l];
    return typeof o == "number" && !Ce.includes(l) ? t[l] = o + "px" : t[l] = o, t;
  }, {}) : {};
}
function C(r) {
  const t = [], l = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(R(h.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: h.Children.toArray(r._reactElement.props.children).map((n) => {
        if (h.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = C(n.props.el);
          return h.cloneElement(n, {
            ...n.props,
            el: s,
            children: [...h.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((n) => {
    r.getEventListeners(n).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      l.addEventListener(c, s, i);
    });
  });
  const o = Array.from(r.childNodes);
  for (let n = 0; n < o.length; n++) {
    const e = o[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = C(e);
      t.push(...c), l.appendChild(s);
    } else e.nodeType === 3 && l.appendChild(e.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function ke(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const O = K(({
  slot: r,
  clone: t,
  className: l,
  style: o
}, n) => {
  const e = Q(), [s, c] = X([]);
  return Z(() => {
    var p;
    if (!e.current || !r)
      return;
    let i = r;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(n, a), l && a.classList.add(...l.split(" ")), o) {
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
        } = C(r);
        i = m, c(f), i.style.display = "contents", _(), (w = e.current) == null || w.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), u.observe(r, {
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
  }, [r, t, l, o, n]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function H(r, t) {
  return r.filter(Boolean).map((l) => {
    if (typeof l != "object")
      return l;
    const o = {
      ...l.props
    };
    let n = o;
    Object.keys(l.slots).forEach((s) => {
      if (!l.slots[s] || !(l.slots[s] instanceof Element) && !l.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        n[a] || (n[a] = {}), f !== c.length - 1 && (n = o[a]);
      });
      const i = l.slots[s];
      let _, u, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, u = i.callback, p = i.clone || !1), n[c[c.length - 1]] = _ ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ b.jsx(O, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ b.jsx(O, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : n[c[c.length - 1]], n = o;
    });
    const e = "children";
    return l[e] && (o[e] = H(l[e], t)), o;
  });
}
function Pe(r, t) {
  return r ? /* @__PURE__ */ b.jsx(O, {
    slot: r,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function je({
  key: r,
  setSlotParams: t,
  slots: l
}, o) {
  return (...n) => (t(r, n), Pe(l[r], {
    clone: !0,
    ...o
  }));
}
const Te = Se(({
  slots: r,
  items: t,
  slotItems: l,
  children: o,
  onChange: n,
  onValueChange: e,
  setSlotParams: s,
  ...c
}) => /* @__PURE__ */ b.jsxs(b.Fragment, {
  children: [o, /* @__PURE__ */ b.jsx(ee, {
    ...c,
    onChange: (i) => {
      e == null || e(i), n == null || n(i);
    },
    expandIcon: r.expandIcon ? je({
      slots: r,
      setSlotParams: s,
      key: "expandIcon"
    }) : c.expandIcon,
    items: V(() => t || H(l), [t, l])
  })]
}));
export {
  Te as Collapse,
  Te as default
};
