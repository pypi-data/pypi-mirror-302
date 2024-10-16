import { g as Ce, w as N } from "./Index-LB9QnVQ9.js";
const C = window.ms_globals.React, ge = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, me = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, L = window.ms_globals.React.useMemo, B = window.ms_globals.ReactDOM.createPortal, R = window.ms_globals.antd.Table;
var Z = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var be = C, Ee = Symbol.for("react.element"), ye = Symbol.for("react.fragment"), Oe = Object.prototype.hasOwnProperty, ve = be.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(n, e, r) {
  var l, o = {}, t = null, i = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (l in e) Oe.call(e, l) && !Re.hasOwnProperty(l) && (o[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: Ee,
    type: n,
    key: t,
    ref: i,
    props: o,
    _owner: ve.current
  };
}
F.Fragment = ye;
F.jsx = $;
F.jsxs = $;
Z.exports = F;
var h = Z.exports;
const {
  SvelteComponent: Se,
  assign: Q,
  binding_callbacks: W,
  check_outros: ke,
  children: ee,
  claim_element: te,
  claim_space: xe,
  component_subscribe: z,
  compute_slots: Te,
  create_slot: Le,
  detach: O,
  element: ne,
  empty: X,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Ne,
  get_slot_changes: Ie,
  group_outros: je,
  init: Pe,
  insert_hydration: I,
  safe_not_equal: Fe,
  set_custom_element_data: re,
  space: Ae,
  transition_in: j,
  transition_out: G,
  update_slot_base: Me
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ue,
  getContext: De,
  onDestroy: Be,
  setContext: Ge
} = window.__gradio__svelte__internal;
function V(n) {
  let e, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = Le(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = ne("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = te(t, "SVELTE-SLOT", {
        class: !0
      });
      var i = ee(e);
      o && o.l(i), i.forEach(O), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(t, i) {
      I(t, e, i), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, i) {
      o && o.p && (!r || i & /*$$scope*/
      64) && Me(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? Ie(
          l,
          /*$$scope*/
          t[6],
          i,
          null
        ) : Ne(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (j(o, t), r = !0);
    },
    o(t) {
      G(o, t), r = !1;
    },
    d(t) {
      t && O(e), o && o.d(t), n[9](null);
    }
  };
}
function Je(n) {
  let e, r, l, o, t = (
    /*$$slots*/
    n[4].default && V(n)
  );
  return {
    c() {
      e = ne("react-portal-target"), r = Ae(), t && t.c(), l = X(), this.h();
    },
    l(i) {
      e = te(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(e).forEach(O), r = xe(i), t && t.l(i), l = X(), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      I(i, e, s), n[8](e), I(i, r, s), t && t.m(i, s), I(i, l, s), o = !0;
    },
    p(i, [s]) {
      /*$$slots*/
      i[4].default ? t ? (t.p(i, s), s & /*$$slots*/
      16 && j(t, 1)) : (t = V(i), t.c(), j(t, 1), t.m(l.parentNode, l)) : t && (je(), G(t, 1, 1, () => {
        t = null;
      }), ke());
    },
    i(i) {
      o || (j(t), o = !0);
    },
    o(i) {
      G(t), o = !1;
    },
    d(i) {
      i && (O(e), O(r), O(l)), n[8](null), t && t.d(i);
    }
  };
}
function K(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function He(n, e, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: i
  } = e;
  const s = Te(t);
  let {
    svelteInit: c
  } = e;
  const p = N(K(e)), f = N();
  z(n, f, (u) => r(0, l = u));
  const _ = N();
  z(n, _, (u) => r(1, o = u));
  const a = [], d = De("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: E,
    subSlotIndex: A
  } = Ce() || {}, y = c({
    parent: d,
    props: p,
    target: f,
    slot: _,
    slotKey: g,
    slotIndex: E,
    subSlotIndex: A,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ge("$$ms-gr-react-wrapper", y), Ue(() => {
    p.set(K(e));
  }), Be(() => {
    a.forEach((u) => u());
  });
  function v(u) {
    W[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function M(u) {
    W[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return n.$$set = (u) => {
    r(17, e = Q(Q({}, e), q(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, i = u.$$scope);
  }, e = q(e), [l, o, f, _, s, c, i, t, v, M];
}
class Qe extends Se {
  constructor(e) {
    super(), Pe(this, e, He, Je, Fe, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, D = window.ms_globals.tree;
function We(n) {
  function e(r) {
    const l = N(), o = new Qe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, s = t.parent ?? D;
          return s.nodes = [...s.nodes, i], Y({
            createPortal: B,
            node: D
          }), t.onDestroy(() => {
            s.nodes = s.nodes.filter((c) => c.svelteInstance !== l), Y({
              createPortal: B,
              node: D
            });
          }), i;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Xe(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const l = n[r];
    return typeof l == "number" && !ze.includes(r) ? e[r] = l + "px" : e[r] = l, e;
  }, {}) : {};
}
function J(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(B(C.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: C.Children.toArray(n._reactElement.props.children).map((o) => {
        if (C.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: i
          } = J(o.props.el);
          return C.cloneElement(o, {
            ...o.props,
            el: i,
            children: [...C.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: i,
      type: s,
      useCapture: c
    }) => {
      r.addEventListener(s, i, c);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: i,
        portals: s
      } = J(t);
      e.push(...s), r.appendChild(i);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function qe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const b = ge(({
  slot: n,
  clone: e,
  className: r,
  style: l
}, o) => {
  const t = he(), [i, s] = me([]);
  return we(() => {
    var _;
    if (!t.current || !n)
      return;
    let c = n;
    function p() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), qe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const d = Xe(l);
        Object.keys(d).forEach((g) => {
          a.style[g] = d[g];
        });
      }
    }
    let f = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var E;
        const {
          portals: d,
          clonedElement: g
        } = J(n);
        c = g, s(d), c.style.display = "contents", p(), (E = t.current) == null || E.appendChild(c);
      };
      a(), f = new window.MutationObserver(() => {
        var d, g;
        (d = t.current) != null && d.contains(c) && ((g = t.current) == null || g.removeChild(c)), a();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", p(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var a, d;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((d = t.current) == null || d.removeChild(c)), f == null || f.disconnect();
    };
  }, [n, e, r, l, o]), C.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...i);
});
function Ve(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function m(n) {
  return L(() => Ve(n), [n]);
}
function Ke(n) {
  return Object.keys(n).reduce((e, r) => (n[r] !== void 0 && (e[r] = n[r]), e), {});
}
function P(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((i) => {
      if (!r.slots[i] || !(r.slots[i] instanceof Element) && !r.slots[i].el)
        return;
      const s = i.split(".");
      s.forEach((a, d) => {
        o[a] || (o[a] = {}), d !== s.length - 1 && (o = l[a]);
      });
      const c = r.slots[i];
      let p, f, _ = !1;
      c instanceof Element ? p = c : (p = c.el, f = c.callback, _ = c.clone || !1), o[s[s.length - 1]] = p ? f ? (...a) => (f(s[s.length - 1], a), /* @__PURE__ */ h.jsx(b, {
        slot: p,
        clone: _ || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ h.jsx(b, {
        slot: p,
        clone: _ || (e == null ? void 0 : e.clone)
      }) : o[s[s.length - 1]], o = l;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (l[t] = P(r[t], e)), l;
  });
}
function Ye(n, e) {
  return n ? /* @__PURE__ */ h.jsx(b, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function x({
  key: n,
  setSlotParams: e,
  slots: r
}, l) {
  return (...o) => (e(n, o), Ye(r[n], {
    clone: !0,
    ...l
  }));
}
function T(n) {
  return typeof n == "object" && n !== null ? n : {};
}
const $e = We(({
  children: n,
  slots: e,
  columnItems: r,
  columns: l,
  getPopupContainer: o,
  pagination: t,
  loading: i,
  rowKey: s,
  summary: c,
  rowSelection: p,
  rowSelectionItems: f,
  expandableItems: _,
  expandable: a,
  sticky: d,
  showSorterTooltip: g,
  onRow: E,
  onHeaderRow: A,
  setSlotParams: y,
  ...v
}) => {
  const M = m(o), u = e["loading.tip"] || e["loading.indicator"], U = T(i), oe = e["pagination.showQuickJumper.goButton"] || e["pagination.itemRender"], S = T(t), le = m(S.showTotal), ie = m(s), se = e["showSorterTooltip.title"] || typeof g == "object", k = T(g), ce = m(k.afterOpenChange), ae = m(k.getPopupContainer), ue = typeof d == "object", H = T(d), de = m(H.getContainer), fe = m(E), pe = m(A), _e = m(c);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ h.jsx(R, {
      ...v,
      columns: L(() => (l == null ? void 0 : l.map((w) => w === "EXPAND_COLUMN" ? R.EXPAND_COLUMN : w === "SELECTION_COLUMN" ? R.SELECTION_COLUMN : w)) || P(r, {
        fallback: (w) => w === "EXPAND_COLUMN" ? R.EXPAND_COLUMN : w === "SELECTION_COLUMN" ? R.SELECTION_COLUMN : w
      }), [r, l]),
      onRow: fe,
      onHeaderRow: pe,
      summary: e.summary ? x({
        slots: e,
        setSlotParams: y,
        key: "summary"
      }) : _e,
      rowSelection: L(() => p || P(f)[0], [p, f]),
      expandable: L(() => a || P(_)[0], [a, _]),
      rowKey: ie || s,
      sticky: ue ? {
        ...H,
        getContainer: de
      } : d,
      showSorterTooltip: se ? {
        ...k,
        afterOpenChange: ce,
        getPopupContainer: ae,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["showSorterTooltip.title"]
        }) : k.title
      } : g,
      pagination: oe ? Ke({
        ...S,
        showTotal: le,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ h.jsx(b, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : S.showQuickJumper,
        itemRender: e["pagination.itemRender"] ? x({
          slots: e,
          setSlotParams: y,
          key: "pagination.itemRender"
        }) : S.itemRender
      }) : t,
      getPopupContainer: M,
      loading: u ? {
        ...U,
        tip: e["loading.tip"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["loading.tip"]
        }) : U.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["loading.indicator"]
        }) : U.indicator
      } : i,
      footer: e.footer ? x({
        slots: e,
        setSlotParams: y,
        key: "footer"
      }) : v.footer,
      title: e.title ? x({
        slots: e,
        setSlotParams: y,
        key: "title"
      }) : v.title
    })]
  });
});
export {
  $e as Table,
  $e as default
};
