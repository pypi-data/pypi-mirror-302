import { g as re, w as R } from "./Index-Cg5stkQO.js";
const p = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, K = window.ms_globals.ReactDOM.createPortal, D = window.ms_globals.antd.Tree;
var B = {
  exports: {}
}, L = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = p, le = Symbol.for("react.element"), se = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ie = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ce.call(n, l) && !ae.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: le,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: ie.current
  };
}
L.Fragment = se;
L.jsx = J;
L.jsxs = J;
B.exports = L;
var w = B.exports;
const {
  SvelteComponent: de,
  assign: F,
  binding_callbacks: A,
  check_outros: ue,
  children: Y,
  claim_element: Q,
  claim_space: fe,
  component_subscribe: M,
  compute_slots: _e,
  create_slot: he,
  detach: y,
  element: V,
  empty: U,
  exclude_internal_props: W,
  get_all_dirty_from_scope: me,
  get_slot_changes: we,
  group_outros: ge,
  init: pe,
  insert_hydration: C,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: be,
  transition_in: k,
  transition_out: P,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ie,
  onDestroy: xe,
  setContext: Re
} = window.__gradio__svelte__internal;
function z(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = he(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = V("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = Q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(n);
      o && o.l(s), s.forEach(y), this.h();
    },
    h() {
      X(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      C(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? we(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (k(o, t), r = !0);
    },
    o(t) {
      P(o, t), r = !1;
    },
    d(t) {
      t && y(n), o && o.d(t), e[9](null);
    }
  };
}
function Ce(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      n = V("react-portal-target"), r = be(), t && t.c(), l = U(), this.h();
    },
    l(s) {
      n = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(n).forEach(y), r = fe(s), t && t.l(s), l = U(), this.h();
    },
    h() {
      X(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, n, c), e[8](n), C(s, r, c), t && t.m(s, c), C(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && k(t, 1)) : (t = z(s), t.c(), k(t, 1), t.m(l.parentNode, l)) : t && (ge(), P(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(s) {
      o || (k(t), o = !0);
    },
    o(s) {
      P(t), o = !1;
    },
    d(s) {
      s && (y(n), y(r), y(l)), e[8](null), t && t.d(s);
    }
  };
}
function G(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function ke(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = _e(t);
  let {
    svelteInit: i
  } = n;
  const h = R(G(n)), f = R();
  M(e, f, (u) => r(0, l = u));
  const _ = R();
  M(e, _, (u) => r(1, o = u));
  const a = [], d = Ie("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: b
  } = re() || {}, O = i({
    parent: d,
    props: h,
    target: f,
    slot: _,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: b,
    onDestroy(u) {
      a.push(u);
    }
  });
  Re("$$ms-gr-react-wrapper", O), ve(() => {
    h.set(G(n));
  }), xe(() => {
    a.forEach((u) => u());
  });
  function j(u) {
    A[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function S(u) {
    A[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, n = F(F({}, n), W(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, n = W(n), [l, o, f, _, c, i, s, t, j, S];
}
class Le extends de {
  constructor(n) {
    super(), pe(this, n, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, T = window.ms_globals.tree;
function Oe(e) {
  function n(r) {
    const l = R(), o = new Le({
      ...r,
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
          }, c = t.parent ?? T;
          return c.nodes = [...c.nodes, s], H({
            createPortal: K,
            node: T
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), H({
              createPortal: K,
              node: T
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !je.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function N(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(K(p.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: p.Children.toArray(e._reactElement.props.children).map((o) => {
        if (p.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = N(o.props.el);
          return p.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...p.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = N(t);
      n.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Te(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const v = $(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = ee(), [s, c] = te([]);
  return ne(() => {
    var _;
    if (!t.current || !e)
      return;
    let i = e;
    function h() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Te(o, a), r && a.classList.add(...r.split(" ")), l) {
        const d = Se(l);
        Object.keys(d).forEach((m) => {
          a.style[m] = d[m];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var g;
        const {
          portals: d,
          clonedElement: m
        } = N(e);
        i = m, c(d), i.style.display = "contents", h(), (g = t.current) == null || g.appendChild(i);
      };
      a(), f = new window.MutationObserver(() => {
        var d, m;
        (d = t.current) != null && d.contains(i) && ((m = t.current) == null || m.removeChild(i)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (_ = t.current) == null || _.appendChild(i);
    return () => {
      var a, d;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((d = t.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, n, r, l, o]), p.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ke(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function I(e) {
  return q(() => Ke(e), [e]);
}
function Pe(e) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (n[r] = e[r]), n), {});
}
function Z(e, n) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, d) => {
        o[a] || (o[a] = {}), d !== c.length - 1 && (o = l[a]);
      });
      const i = r.slots[s];
      let h, f, _ = !1;
      i instanceof Element ? h = i : (h = i.el, f = i.callback, _ = i.clone || !1), o[c[c.length - 1]] = h ? f ? (...a) => (f(c[c.length - 1], a), /* @__PURE__ */ w.jsx(v, {
        slot: h,
        clone: _ || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ w.jsx(v, {
        slot: h,
        clone: _ || (n == null ? void 0 : n.clone)
      }) : o[c[c.length - 1]], o = l;
    });
    const t = "children";
    return r[t] && (l[t] = Z(r[t], n)), l;
  });
}
function Ne(e, n) {
  return e ? /* @__PURE__ */ w.jsx(v, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function x({
  key: e,
  setSlotParams: n,
  slots: r
}, l) {
  return (...o) => (n(e, o), Ne(r[e], {
    clone: !0,
    ...l
  }));
}
const Fe = Oe(({
  slots: e,
  filterTreeNode: n,
  treeData: r,
  draggable: l,
  allowDrop: o,
  onValueChange: t,
  onCheck: s,
  onSelect: c,
  onExpand: i,
  children: h,
  directory: f,
  slotItems: _,
  setSlotParams: a,
  ...d
}) => {
  const m = I(n), g = I(l), b = I(typeof l == "object" ? l.nodeDraggable : void 0), O = I(o), j = f ? D.DirectoryTree : D, S = q(() => ({
    ...d,
    treeData: r || Z(_),
    showLine: e["showLine.showLeafIcon"] ? {
      showLeafIcon: x({
        slots: e,
        setSlotParams: a,
        key: "showLine.showLeafIcon"
      })
    } : d.showLine,
    icon: e.icon ? x({
      slots: e,
      setSlotParams: a,
      key: "icon"
    }) : d.icon,
    switcherLoadingIcon: e.switcherLoadingIcon ? /* @__PURE__ */ w.jsx(v, {
      slot: e.switcherLoadingIcon
    }) : d.switcherLoadingIcon,
    switcherIcon: e.switcherIcon ? x({
      slots: e,
      setSlotParams: a,
      key: "switcherIcon"
    }) : d.switcherIcon,
    titleRender: e.titleRender ? x({
      slots: e,
      setSlotParams: a,
      key: "titleRender"
    }) : d.titleRender,
    draggable: e["draggable.icon"] || b ? {
      icon: e["draggable.icon"] ? /* @__PURE__ */ w.jsx(v, {
        slot: e["draggable.icon"]
      }) : typeof l == "object" ? l.icon : void 0,
      nodeDraggable: b
    } : g || l
  }), [l, g, b, d, _, e, r, a]);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: h
    }), /* @__PURE__ */ w.jsx(j, {
      ...Pe(S),
      filterTreeNode: m,
      allowDrop: O,
      onSelect: (u, ...E) => {
        c == null || c(u, ...E), t({
          selectedKeys: u,
          expandedKeys: d.expandedKeys,
          checkedKeys: d.checkedKeys
        });
      },
      onExpand: (u, ...E) => {
        i == null || i(u, ...E), t({
          expandedKeys: u,
          selectedKeys: d.selectedKeys,
          checkedKeys: d.checkedKeys
        });
      },
      onCheck: (u, ...E) => {
        s == null || s(u, ...E), t({
          checkedKeys: u,
          selectedKeys: d.selectedKeys,
          expandedKeys: d.expandedKeys
        });
      }
    })]
  });
});
export {
  Fe as Tree,
  Fe as default
};
