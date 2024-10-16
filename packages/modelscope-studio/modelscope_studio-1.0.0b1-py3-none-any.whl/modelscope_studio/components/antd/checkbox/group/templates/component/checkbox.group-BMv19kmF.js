import { g as $, w as E } from "./Index-C3LKPJIG.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Checkbox;
var G = {
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
function F(l, t, r) {
  var s, n = {}, e = null, o = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) le.call(t, s) && !se.hasOwnProperty(s) && (n[s] = t[s]);
  if (l && l.defaultProps) for (s in t = l.defaultProps, t) n[s] === void 0 && (n[s] = t[s]);
  return {
    $$typeof: ne,
    type: l,
    key: e,
    ref: o,
    props: n,
    _owner: oe.current
  };
}
x.Fragment = re;
x.jsx = F;
x.jsxs = F;
G.exports = x;
var g = G.exports;
const {
  SvelteComponent: ce,
  assign: I,
  binding_callbacks: O,
  check_outros: ie,
  children: M,
  claim_element: W,
  claim_space: ae,
  component_subscribe: j,
  compute_slots: ue,
  create_slot: de,
  detach: b,
  element: z,
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
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function T(l) {
  let t, r;
  const s = (
    /*#slots*/
    l[7].default
  ), n = de(
    s,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = z("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = M(t);
      n && n.l(o), o.forEach(b), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      y(e, t, o), n && n.m(t, null), l[9](t), r = !0;
    },
    p(e, o) {
      n && n.p && (!r || o & /*$$scope*/
      64) && be(
        n,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
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
      r || (v(n, e), r = !0);
    },
    o(e) {
      k(n, e), r = !1;
    },
    d(e) {
      e && b(t), n && n.d(e), l[9](null);
    }
  };
}
function xe(l) {
  let t, r, s, n, e = (
    /*$$slots*/
    l[4].default && T(l)
  );
  return {
    c() {
      t = z("react-portal-target"), r = ge(), e && e.c(), s = P(), this.h();
    },
    l(o) {
      t = W(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(t).forEach(b), r = ae(o), e && e.l(o), s = P(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      y(o, t, c), l[8](t), y(o, r, c), e && e.m(o, c), y(o, s, c), n = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = T(o), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (pe(), k(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(o) {
      n || (v(e), n = !0);
    },
    o(o) {
      k(e), n = !1;
    },
    d(o) {
      o && (b(t), b(r), b(s)), l[8](null), e && e.d(o);
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
function Ce(l, t, r) {
  let s, n, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = ue(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(N(t)), d = E();
  j(l, d, (u) => r(0, s = u));
  const p = E();
  j(l, p, (u) => r(1, n = u));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q
  } = $() || {}, B = i({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", B), we(() => {
    _.set(N(t));
  }), ye(() => {
    a.forEach((u) => u());
  });
  function V(u) {
    O[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function J(u) {
    O[u ? "unshift" : "push"](() => {
      n = u, p.set(n);
    });
  }
  return l.$$set = (u) => {
    r(17, t = I(I({}, t), L(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, o = u.$$scope);
  }, t = L(t), [s, n, d, p, c, i, o, e, V, J];
}
class Re extends ce {
  constructor(t) {
    super(), me(this, t, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, C = window.ms_globals.tree;
function ke(l) {
  function t(r) {
    const s = E(), n = new Re({
      ...r,
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
          }, c = e.parent ?? C;
          return c.nodes = [...c.nodes, o], A({
            createPortal: R,
            node: C
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), A({
              createPortal: R,
              node: C
            });
          }), o;
        },
        ...r.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(l) {
  return l ? Object.keys(l).reduce((t, r) => {
    const s = l[r];
    return typeof s == "number" && !Se.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function S(l) {
  const t = [], r = l.cloneNode(!1);
  if (l._reactElement)
    return t.push(R(h.cloneElement(l._reactElement, {
      ...l._reactElement.props,
      children: h.Children.toArray(l._reactElement.props.children).map((n) => {
        if (h.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = S(n.props.el);
          return h.cloneElement(n, {
            ...n.props,
            el: o,
            children: [...h.Children.toArray(n.props.children), ...e]
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
      listener: o,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, o, i);
    });
  });
  const s = Array.from(l.childNodes);
  for (let n = 0; n < s.length; n++) {
    const e = s[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = S(e);
      t.push(...c), r.appendChild(o);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Oe(l, t) {
  l && (typeof l == "function" ? l(t) : l.current = t);
}
const D = Y(({
  slot: l,
  clone: t,
  className: r,
  style: s
}, n) => {
  const e = K(), [o, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !l)
      return;
    let i = l;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(n, a), r && a.classList.add(...r.split(" ")), s) {
        const f = Ie(s);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = S(l);
        i = m, c(f), i.style.display = "contents", _(), (w = e.current) == null || w.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), d.observe(l, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", _(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [l, t, r, s, n]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function H(l, t) {
  return l.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let n = s;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((a, f) => {
        n[a] || (n[a] = {}), f !== c.length - 1 && (n = s[a]);
      });
      const i = r.slots[o];
      let _, d, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, d = i.callback, p = i.clone || !1), n[c[c.length - 1]] = _ ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ g.jsx(D, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ g.jsx(D, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : n[c[c.length - 1]], n = s;
    });
    const e = "children";
    return r[e] && (s[e] = H(r[e], t)), s;
  });
}
const Pe = ke(({
  onValueChange: l,
  onChange: t,
  elRef: r,
  optionItems: s,
  options: n,
  children: e,
  ...o
}) => /* @__PURE__ */ g.jsxs(g.Fragment, {
  children: [/* @__PURE__ */ g.jsx("div", {
    style: {
      display: "none"
    },
    children: e
  }), /* @__PURE__ */ g.jsx(ee.Group, {
    ...o,
    ref: r,
    options: Z(() => n || H(s), [s, n]),
    onChange: (c) => {
      t == null || t(c), l(c);
    }
  })]
}));
export {
  Pe as CheckboxGroup,
  Pe as default
};
