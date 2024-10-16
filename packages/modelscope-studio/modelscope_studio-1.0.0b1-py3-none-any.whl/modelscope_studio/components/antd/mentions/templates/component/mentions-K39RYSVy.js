import { g as ee, w as E } from "./Index-CTj5uGMF.js";
const h = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, D = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Mentions;
var W = {
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
var ne = h, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) le.call(t, s) && !ce.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = z;
C.jsxs = z;
W.exports = C;
var g = W.exports;
const {
  SvelteComponent: ie,
  assign: P,
  binding_callbacks: j,
  check_outros: ae,
  children: G,
  claim_element: U,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: b,
  element: H,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: _e,
  get_slot_changes: pe,
  group_outros: me,
  init: he,
  insert_hydration: y,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: we,
  transition_in: v,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = fe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = H("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(t);
      r && r.l(l), l.forEach(b), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && be(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : _e(
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
      O(r, e), o = !1;
    },
    d(e) {
      e && b(t), r && r.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = H("react-portal-target"), o = we(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      t = U(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(t).forEach(b), o = ue(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      y(l, t, c), n[8](t), y(l, o, c), e && e.m(l, c), y(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (me(), O(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      r || (v(e), r = !0);
    },
    o(l) {
      O(e), r = !1;
    },
    d(l) {
      l && (b(t), b(o), b(s)), n[8](null), e && e.d(l);
    }
  };
}
function A(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Re(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(A(t)), d = E();
  F(n, d, (u) => o(0, s = u));
  const p = E();
  F(n, p, (u) => o(1, r = u));
  const a = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: V
  } = ee() || {}, J = i({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: V,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", J), Ee(() => {
    _.set(A(t));
  }), ve(() => {
    a.forEach((u) => u());
  });
  function Y(u) {
    j[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function K(u) {
    j[u ? "unshift" : "push"](() => {
      r = u, p.set(r);
    });
  }
  return n.$$set = (u) => {
    o(17, t = P(P({}, t), T(u))), "svelteInit" in u && o(5, i = u.svelteInit), "$$scope" in u && o(6, l = u.$$scope);
  }, t = T(t), [s, r, d, p, c, i, l, e, Y, K];
}
class Se extends ie {
  constructor(t) {
    super(), he(this, t, Re, xe, ge, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, x = window.ms_globals.tree;
function Oe(n) {
  function t(o) {
    const s = E(), r = new Se({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, l], M({
            createPortal: S,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), M({
              createPortal: S,
              node: x
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Ie.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function I(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(S(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = I(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...h.Children.toArray(r.props.children), ...e]
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
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = I(e);
      t.push(...c), o.appendChild(l);
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
const k = Q(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = X(), [l, c] = Z([]);
  return $(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(r, a), o && a.classList.add(...o.split(" ")), s) {
        const f = ke(s);
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
        } = I(n);
        i = m, c(f), i.style.display = "contents", _(), (w = e.current) == null || w.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), d.observe(n, {
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
  }, [n, t, o, s, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function R(n) {
  return D(() => je(n), [n]);
}
function B(n, t) {
  return n.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const s = {
      ...o.props
    };
    let r = s;
    Object.keys(o.slots).forEach((l) => {
      if (!o.slots[l] || !(o.slots[l] instanceof Element) && !o.slots[l].el)
        return;
      const c = l.split(".");
      c.forEach((a, f) => {
        r[a] || (r[a] = {}), f !== c.length - 1 && (r = s[a]);
      });
      const i = o.slots[l];
      let _, d, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, d = i.callback, p = i.clone || !1), r[c[c.length - 1]] = _ ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ g.jsx(k, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ g.jsx(k, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : r[c[c.length - 1]], r = s;
    });
    const e = "children";
    return o[e] && (s[e] = B(o[e], t)), s;
  });
}
const Le = Oe(({
  slots: n,
  children: t,
  onValueChange: o,
  filterOption: s,
  onChange: r,
  options: e,
  validateSearch: l,
  optionItems: c,
  getPopupContainer: i,
  elRef: _,
  ...d
}) => {
  const p = R(i), a = R(s), f = R(l);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(te, {
      ...d,
      ref: _,
      options: D(() => e || B(c), [c, e]),
      onChange: (m, ...w) => {
        r == null || r(m, ...w), o(m);
      },
      validateSearch: f,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ g.jsx(k, {
        slot: n.notFoundContent
      }) : d.notFoundContent,
      filterOption: a || s,
      getPopupContainer: p
    })]
  });
});
export {
  Le as Mentions,
  Le as default
};
