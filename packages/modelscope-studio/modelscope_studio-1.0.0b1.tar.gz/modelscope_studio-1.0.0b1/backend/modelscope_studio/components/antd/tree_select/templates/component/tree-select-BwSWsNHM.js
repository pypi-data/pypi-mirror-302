import { g as oe, w as k } from "./Index-CdfprRD7.js";
const w = window.ms_globals.React, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, ne = window.ms_globals.React.useState, re = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, le = window.ms_globals.antd.TreeSelect;
var B = {
  exports: {}
}, T = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = w, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, r) {
  var s, o = {}, n = null, l = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ae.call(t, s) && !de.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: ce,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: ue.current
  };
}
T.Fragment = ie;
T.jsx = V;
T.jsxs = V;
B.exports = T;
var m = B.exports;
const {
  SvelteComponent: fe,
  assign: A,
  binding_callbacks: D,
  check_outros: _e,
  children: J,
  claim_element: Y,
  claim_space: pe,
  component_subscribe: M,
  compute_slots: he,
  create_slot: me,
  detach: y,
  element: K,
  empty: U,
  exclude_internal_props: W,
  get_all_dirty_from_scope: ge,
  get_slot_changes: we,
  group_outros: be,
  init: ye,
  insert_hydration: O,
  safe_not_equal: Ee,
  set_custom_element_data: Q,
  space: ve,
  transition_in: S,
  transition_out: P,
  update_slot_base: Re
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ce,
  onDestroy: Ie,
  setContext: ke
} = window.__gradio__svelte__internal;
function z(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = me(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(t);
      o && o.l(l), l.forEach(y), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      O(n, t, l), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && Re(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? we(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : ge(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (S(o, n), r = !0);
    },
    o(n) {
      P(o, n), r = !1;
    },
    d(n) {
      n && y(t), o && o.d(n), e[9](null);
    }
  };
}
function Oe(e) {
  let t, r, s, o, n = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      t = K("react-portal-target"), r = ve(), n && n.c(), s = U(), this.h();
    },
    l(l) {
      t = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(y), r = pe(l), n && n.l(l), s = U(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      O(l, t, i), e[8](t), O(l, r, i), n && n.m(l, i), O(l, s, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, i), i & /*$$slots*/
      16 && S(n, 1)) : (n = z(l), n.c(), S(n, 1), n.m(s.parentNode, s)) : n && (be(), P(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(l) {
      o || (S(n), o = !0);
    },
    o(l) {
      P(n), o = !1;
    },
    d(l) {
      l && (y(t), y(r), y(s)), e[8](null), n && n.d(l);
    }
  };
}
function G(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Se(e, t, r) {
  let s, o, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const i = he(n);
  let {
    svelteInit: c
  } = t;
  const h = k(G(t)), f = k();
  M(e, f, (u) => r(0, s = u));
  const p = k();
  M(e, p, (u) => r(1, o = u));
  const a = [], d = Ce("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: R
  } = oe() || {}, x = c({
    parent: d,
    props: h,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: R,
    onDestroy(u) {
      a.push(u);
    }
  });
  ke("$$ms-gr-react-wrapper", x), xe(() => {
    h.set(G(t));
  }), Ie(() => {
    a.forEach((u) => u());
  });
  function C(u) {
    D[u ? "unshift" : "push"](() => {
      s = u, f.set(s);
    });
  }
  function I(u) {
    D[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, t = A(A({}, t), W(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, t = W(t), [s, o, f, p, i, c, l, n, C, I];
}
class Te extends fe {
  constructor(t) {
    super(), ye(this, t, Se, Oe, Ee, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, j = window.ms_globals.tree;
function je(e) {
  function t(r) {
    const s = k(), o = new Te({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
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
          }, i = n.parent ?? j;
          return i.nodes = [...i.nodes, l], H({
            createPortal: F,
            node: j
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), H({
              createPortal: F,
              node: j
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return typeof s == "number" && !Fe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function L(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...w.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(n);
      t.push(...i), r.appendChild(l);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Le(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const E = ee(({
  slot: e,
  clone: t,
  className: r,
  style: s
}, o) => {
  const n = te(), [l, i] = ne([]);
  return re(() => {
    var p;
    if (!n.current || !e)
      return;
    let c = e;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Le(o, a), r && a.classList.add(...r.split(" ")), s) {
        const d = Pe(s);
        Object.keys(d).forEach((_) => {
          a.style[_] = d[_];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var g;
        const {
          portals: d,
          clonedElement: _
        } = L(e);
        c = _, i(d), c.style.display = "contents", h(), (g = n.current) == null || g.appendChild(c);
      };
      a(), f = new window.MutationObserver(() => {
        var d, _;
        (d = n.current) != null && d.contains(c) && ((_ = n.current) == null || _.removeChild(c)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", h(), (p = n.current) == null || p.appendChild(c);
    return () => {
      var a, d;
      c.style.display = "", (a = n.current) != null && a.contains(c) && ((d = n.current) == null || d.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, t, r, s, o]), w.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ne(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function b(e) {
  return q(() => Ne(e), [e]);
}
function Ae(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function X(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let o = s;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((a, d) => {
        o[a] || (o[a] = {}), d !== i.length - 1 && (o = s[a]);
      });
      const c = r.slots[l];
      let h, f, p = !1;
      c instanceof Element ? h = c : (h = c.el, f = c.callback, p = c.clone || !1), o[i[i.length - 1]] = h ? f ? (...a) => (f(i[i.length - 1], a), /* @__PURE__ */ m.jsx(E, {
        slot: h,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(E, {
        slot: h,
        clone: p || (t == null ? void 0 : t.clone)
      }) : o[i[i.length - 1]], o = s;
    });
    const n = "children";
    return r[n] && (s[n] = X(r[n], t)), s;
  });
}
function De(e, t) {
  return e ? /* @__PURE__ */ m.jsx(E, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function v({
  key: e,
  setSlotParams: t,
  slots: r
}, s) {
  return (...o) => (t(e, o), De(r[e], {
    clone: !0,
    ...s
  }));
}
const Ue = je(({
  slots: e,
  filterTreeNode: t,
  getPopupContainer: r,
  dropdownRender: s,
  tagRender: o,
  treeTitleRender: n,
  treeData: l,
  onValueChange: i,
  onChange: c,
  children: h,
  slotItems: f,
  maxTagPlaceholder: p,
  elRef: a,
  setSlotParams: d,
  ..._
}) => {
  const g = b(t), R = b(r), x = b(p), C = b(o), I = b(s), u = b(n), Z = q(() => ({
    ..._,
    treeData: l || X(f),
    dropdownRender: e.dropdownRender ? v({
      slots: e,
      setSlotParams: d,
      key: "dropdownRender"
    }) : I,
    allowClear: e["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ m.jsx(E, {
        slot: e["allowClear.clearIcon"]
      })
    } : _.allowClear,
    suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(E, {
      slot: e.suffixIcon
    }) : _.suffixIcon,
    switcherIcon: e.switcherIcon ? v({
      slots: e,
      setSlotParams: d,
      key: "switcherIcon"
    }) : _.switcherIcon,
    getPopupContainer: R,
    tagRender: e.tagRender ? v({
      slots: e,
      setSlotParams: d,
      key: "tagRender"
    }) : C,
    treeTitleRender: e.treeTitleRender ? v({
      slots: e,
      setSlotParams: d,
      key: "treeTitleRender"
    }) : u,
    filterTreeNode: g || t,
    maxTagPlaceholder: e.maxTagPlaceholder ? v({
      slots: e,
      setSlotParams: d,
      key: "maxTagPlaceholder"
    }) : x || p,
    notFoundContent: e.notFoundContent ? /* @__PURE__ */ m.jsx(E, {
      slot: e.notFoundContent
    }) : _.notFoundContent
  }), [I, t, g, R, p, x, _, d, f, e, C, l, u]);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: h
    }), /* @__PURE__ */ m.jsx(le, {
      ...Ae(Z),
      ref: a,
      onChange: (N, ...$) => {
        c == null || c(N, ...$), i(N);
      }
    })]
  });
});
export {
  Ue as TreeSelect,
  Ue as default
};
