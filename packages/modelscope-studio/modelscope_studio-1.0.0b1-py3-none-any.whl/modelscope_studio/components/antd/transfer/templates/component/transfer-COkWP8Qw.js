import { g as ne, w as S, d as re, a as E } from "./Index-xrNur1Qe.js";
const b = window.ms_globals.React, F = window.ms_globals.React.useMemo, q = window.ms_globals.React.useState, B = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, T = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Transfer;
var J = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = b, le = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(t, n, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ce.call(n, l) && !ue.hasOwnProperty(l) && (r[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: le,
    type: t,
    key: e,
    ref: s,
    props: r,
    _owner: ae.current
  };
}
O.Fragment = ie;
O.jsx = K;
O.jsxs = K;
J.exports = O;
var g = J.exports;
const {
  SvelteComponent: de,
  assign: P,
  binding_callbacks: N,
  check_outros: fe,
  children: Y,
  claim_element: Q,
  claim_space: pe,
  component_subscribe: D,
  compute_slots: _e,
  create_slot: me,
  detach: v,
  element: X,
  empty: M,
  exclude_internal_props: W,
  get_all_dirty_from_scope: ge,
  get_slot_changes: he,
  group_outros: be,
  init: we,
  insert_hydration: C,
  safe_not_equal: ye,
  set_custom_element_data: Z,
  space: ve,
  transition_in: R,
  transition_out: j,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ie,
  onDestroy: Se,
  setContext: Ce
} = window.__gradio__svelte__internal;
function z(t) {
  let n, o;
  const l = (
    /*#slots*/
    t[7].default
  ), r = me(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = X("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = Q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(n);
      r && r.l(s), s.forEach(v), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, n, s), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ee(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? he(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ge(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (R(r, e), o = !0);
    },
    o(e) {
      j(r, e), o = !1;
    },
    d(e) {
      e && v(n), r && r.d(e), t[9](null);
    }
  };
}
function Re(t) {
  let n, o, l, r, e = (
    /*$$slots*/
    t[4].default && z(t)
  );
  return {
    c() {
      n = X("react-portal-target"), o = ve(), e && e.c(), l = M(), this.h();
    },
    l(s) {
      n = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(n).forEach(v), o = pe(s), e && e.l(s), l = M(), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, n, c), t[8](n), C(s, o, c), e && e.m(s, c), C(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = z(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (be(), j(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      r || (R(e), r = !0);
    },
    o(s) {
      j(e), r = !1;
    },
    d(s) {
      s && (v(n), v(o), v(l)), t[8](null), e && e.d(s);
    }
  };
}
function G(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Oe(t, n, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = _e(e);
  let {
    svelteInit: i
  } = n;
  const h = S(G(n)), d = S();
  D(t, d, (u) => o(0, l = u));
  const m = S();
  D(t, m, (u) => o(1, r = u));
  const a = [], f = Ie("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: y,
    subSlotIndex: k
  } = ne() || {}, p = i({
    parent: f,
    props: h,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: y,
    subSlotIndex: k,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", p), xe(() => {
    h.set(G(n));
  }), Se(() => {
    a.forEach((u) => u());
  });
  function w(u) {
    N[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function $(u) {
    N[u ? "unshift" : "push"](() => {
      r = u, m.set(r);
    });
  }
  return t.$$set = (u) => {
    o(17, n = P(P({}, n), W(u))), "svelteInit" in u && o(5, i = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, n = W(n), [l, r, d, m, c, i, s, e, w, $];
}
class ke extends de {
  constructor(n) {
    super(), we(this, n, Oe, Re, ye, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, L = window.ms_globals.tree;
function Le(t) {
  function n(o) {
    const l = S(), r = new ke({
      ...o,
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
          }, c = e.parent ?? L;
          return c.nodes = [...c.nodes, s], U({
            createPortal: T,
            node: L
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), U({
              createPortal: T,
              node: L
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
      o(n);
    });
  });
}
function Te(t) {
  const [n, o] = q(() => E(t));
  return B(() => {
    let l = !0;
    return t.subscribe((e) => {
      l && (l = !1, e === n) || o(e);
    });
  }, [t]), n;
}
function je(t) {
  const n = F(() => re(t, (o) => o), [t]);
  return Te(n);
}
const Ae = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const l = t[o];
    return typeof l == "number" && !Ae.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function A(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(T(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: b.Children.toArray(t._reactElement.props.children).map((r) => {
        if (b.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = A(r.props.el);
          return b.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...b.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = A(e);
      n.push(...c), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Pe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const x = ee(({
  slot: t,
  clone: n,
  className: o,
  style: l
}, r) => {
  const e = te(), [s, c] = q([]);
  return B(() => {
    var m;
    if (!e.current || !t)
      return;
    let i = t;
    function h() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(r, a), o && a.classList.add(...o.split(" ")), l) {
        const f = Fe(l);
        Object.keys(f).forEach((_) => {
          a.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y;
        const {
          portals: f,
          clonedElement: _
        } = A(t);
        i = _, c(f), i.style.display = "contents", h(), (y = e.current) == null || y.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var f, _;
        (f = e.current) != null && f.contains(i) && ((_ = e.current) == null || _.removeChild(i)), a();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, o, l, r]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function I(t) {
  return F(() => Ne(t), [t]);
}
function H(t, n) {
  const o = F(() => b.Children.toArray(t).filter((e) => e.props.node && (!n && !e.props.nodeSlotKey || n && n === e.props.nodeSlotKey)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const c = E(e.props.node.slotIndex) || 0, i = E(s.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (E(e.props.node.subSlotIndex) || 0) - (E(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return je(o);
}
function De(t, n) {
  return t ? /* @__PURE__ */ g.jsx(x, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function V({
  key: t,
  setSlotParams: n,
  slots: o
}, l) {
  return (...r) => (n(t, r), De(o[t], {
    clone: !0,
    ...l
  }));
}
const We = Le(({
  slots: t,
  children: n,
  render: o,
  filterOption: l,
  footer: r,
  listStyle: e,
  locale: s,
  onChange: c,
  onValueChange: i,
  setSlotParams: h,
  ...d
}) => {
  const m = H(n, "titles"), a = H(n, "selectAllLabels"), f = I(o), _ = I(e), y = I(r), k = I(l);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ g.jsx(oe, {
      ...d,
      onChange: (p, ...w) => {
        c == null || c(p, ...w), i(p);
      },
      selectionsIcon: t.selectionsIcon ? /* @__PURE__ */ g.jsx(x, {
        slot: t.selectionsIcon
      }) : d.selectionsIcon,
      locale: t["locale.notFoundContent"] ? {
        ...s,
        notFoundContent: /* @__PURE__ */ g.jsx(x, {
          slot: t["locale.notFoundContent"]
        })
      } : s,
      render: t.render ? V({
        slots: t,
        setSlotParams: h,
        key: "render"
      }) : f || ((p) => ({
        label: p.title || p.label,
        value: p.value || p.title || p.label
      })),
      filterOption: k,
      footer: t.footer ? V({
        slots: t,
        setSlotParams: h,
        key: "footer"
      }) : y || r,
      titles: m.length > 0 ? m.map((p, w) => /* @__PURE__ */ g.jsx(x, {
        slot: p
      }, w)) : d.titles,
      listStyle: _ || e,
      selectAllLabels: a.length > 0 ? a.map((p, w) => /* @__PURE__ */ g.jsx(x, {
        slot: p
      }, w)) : d.selectAllLabels
    })]
  });
});
export {
  We as Transfer,
  We as default
};
