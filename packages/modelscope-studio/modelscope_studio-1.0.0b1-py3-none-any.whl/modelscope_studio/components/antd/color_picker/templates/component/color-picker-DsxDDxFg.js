import { g as ne, w as x, d as re, a as y } from "./Index-CWfB_TDu.js";
const g = window.ms_globals.React, I = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, B = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, O = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.ColorPicker;
var V = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = g, le = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ie.call(t, l) && !ue.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: le,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
R.Fragment = ce;
R.jsx = q;
R.jsxs = q;
V.exports = R;
var b = V.exports;
const {
  SvelteComponent: de,
  assign: L,
  binding_callbacks: A,
  check_outros: fe,
  children: J,
  claim_element: Y,
  claim_space: pe,
  component_subscribe: F,
  compute_slots: _e,
  create_slot: he,
  detach: w,
  element: K,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: be,
  init: we,
  insert_hydration: v,
  safe_not_equal: ye,
  set_custom_element_data: Q,
  space: Ee,
  transition_in: S,
  transition_out: P,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Se,
  onDestroy: Ie,
  setContext: Re
} = window.__gradio__svelte__internal;
function H(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = he(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = Y(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = J(t);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && xe(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ge(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : me(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (S(o, e), r = !0);
    },
    o(e) {
      P(o, e), r = !1;
    },
    d(e) {
      e && w(t), o && o.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && H(n)
  );
  return {
    c() {
      t = K("react-portal-target"), r = Ee(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      t = Y(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(w), r = pe(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, t, c), n[8](t), v(s, r, c), e && e.m(s, c), v(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && S(e, 1)) : (e = H(s), e.c(), S(e, 1), e.m(l.parentNode, l)) : e && (be(), P(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      o || (S(e), o = !0);
    },
    o(s) {
      P(e), o = !1;
    },
    d(s) {
      s && (w(t), w(r), w(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ke(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = _e(e);
  let {
    svelteInit: i
  } = t;
  const p = x(M(t)), u = x();
  F(n, u, (d) => r(0, l = d));
  const _ = x();
  F(n, _, (d) => r(1, o = d));
  const a = [], f = Se("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: C
  } = ne() || {}, E = i({
    parent: f,
    props: p,
    target: u,
    slot: _,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: C,
    onDestroy(d) {
      a.push(d);
    }
  });
  Re("$$ms-gr-react-wrapper", E), ve(() => {
    p.set(M(t));
  }), Ie(() => {
    a.forEach((d) => d());
  });
  function Z(d) {
    A[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function $(d) {
    A[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return n.$$set = (d) => {
    r(17, t = L(L({}, t), D(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = D(t), [l, o, u, _, c, i, s, e, Z, $];
}
class Oe extends de {
  constructor(t) {
    super(), we(this, t, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, k = window.ms_globals.tree;
function Pe(n) {
  function t(r) {
    const l = x(), o = new Oe({
      ...r,
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
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, s], W({
            createPortal: O,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), W({
              createPortal: O,
              node: k
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
      r(t);
    });
  });
}
function je(n) {
  const [t, r] = U(() => y(n));
  return B(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Te(n) {
  const t = I(() => re(n, (r) => r), [n]);
  return je(t);
}
function Le(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function z(n) {
  return I(() => Le(n), [n]);
}
function Ae(n, t) {
  const r = I(() => g.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const c = y(e.props.node.slotIndex) || 0, i = y(s.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (y(e.props.node.subSlotIndex) || 0) - (y(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Te(r);
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ne(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Fe.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function j(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...g.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function De(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const T = ee(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = te(), [s, c] = U([]);
  return B(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), De(o, a), r && a.classList.add(...r.split(" ")), l) {
        const f = Ne(l);
        Object.keys(f).forEach((h) => {
          a.style[h] = f[h];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var m;
        const {
          portals: f,
          clonedElement: h
        } = j(n);
        i = h, c(f), i.style.display = "contents", p(), (m = e.current) == null || m.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, h;
        (f = e.current) != null && f.contains(i) && ((h = e.current) == null || h.removeChild(i)), a();
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
  }, [n, t, r, l, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function X(n, t) {
  return n.filter(Boolean).map((r) => {
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
      c.forEach((a, f) => {
        o[a] || (o[a] = {}), f !== c.length - 1 && (o = l[a]);
      });
      const i = r.slots[s];
      let p, u, _ = !1;
      i instanceof Element ? p = i : (p = i.el, u = i.callback, _ = i.clone || !1), o[c[c.length - 1]] = p ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ b.jsx(T, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ b.jsx(T, {
        slot: p,
        clone: _ || (t == null ? void 0 : t.clone)
      }) : o[c[c.length - 1]], o = l;
    });
    const e = "children";
    return r[e] && (l[e] = X(r[e], t)), l;
  });
}
function He(n, t) {
  return n ? /* @__PURE__ */ b.jsx(T, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function G({
  key: n,
  setSlotParams: t,
  slots: r
}, l) {
  return (...o) => (t(n, o), He(r[n], {
    clone: !0,
    ...l
  }));
}
const We = Pe(({
  onValueChange: n,
  onChange: t,
  panelRender: r,
  showText: l,
  value: o,
  presets: e,
  presetItems: s,
  children: c,
  value_format: i,
  setSlotParams: p,
  slots: u,
  ..._
}) => {
  const a = z(r), f = z(l), h = Ae(c);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [h.length === 0 && /* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: c
    }), /* @__PURE__ */ b.jsx(oe, {
      ..._,
      value: o,
      presets: I(() => e || X(s), [e, s]),
      showText: u.showText ? G({
        slots: u,
        setSlotParams: p,
        key: "showText"
      }) : f || l,
      panelRender: u.panelRender ? G({
        slots: u,
        setSlotParams: p,
        key: "panelRender"
      }) : a,
      onChange: (m, ...C) => {
        const E = {
          rgb: m.toRgbString(),
          hex: m.toHexString(),
          hsb: m.toHsbString()
        };
        t == null || t(E[i], ...C), n(E[i]);
      },
      children: h.length === 0 ? null : c
    })]
  });
});
export {
  We as ColorPicker,
  We as default
};
