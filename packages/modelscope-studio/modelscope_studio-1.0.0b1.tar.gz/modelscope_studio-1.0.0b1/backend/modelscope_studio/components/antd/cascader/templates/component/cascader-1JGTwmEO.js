import { g as de, w as v } from "./Index-BBUG1-3I.js";
const x = window.ms_globals.React, se = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ie = window.ms_globals.React.useState, ae = window.ms_globals.React.useEffect, B = window.ms_globals.React.useMemo, T = window.ms_globals.ReactDOM.createPortal, ue = window.ms_globals.antd.Cascader;
var V = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var fe = x, pe = Symbol.for("react.element"), _e = Symbol.for("react.fragment"), he = Object.prototype.hasOwnProperty, me = fe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ge = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) he.call(n, l) && !ge.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: pe,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: me.current
  };
}
k.Fragment = _e;
k.jsx = J;
k.jsxs = J;
V.exports = k;
var m = V.exports;
const {
  SvelteComponent: we,
  assign: D,
  binding_callbacks: M,
  check_outros: ye,
  children: Y,
  claim_element: K,
  claim_space: be,
  component_subscribe: W,
  compute_slots: Ee,
  create_slot: xe,
  detach: C,
  element: Q,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Ce,
  get_slot_changes: Re,
  group_outros: ve,
  init: Ie,
  insert_hydration: I,
  safe_not_equal: Se,
  set_custom_element_data: X,
  space: ke,
  transition_in: S,
  transition_out: L,
  update_slot_base: je
} = window.__gradio__svelte__internal, {
  beforeUpdate: Oe,
  getContext: Fe,
  onDestroy: Pe,
  setContext: Te
} = window.__gradio__svelte__internal;
function U(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = xe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = Q("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(n);
      o && o.l(s), s.forEach(C), this.h();
    },
    h() {
      X(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      I(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && je(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? Re(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : Ce(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (S(o, t), r = !0);
    },
    o(t) {
      L(o, t), r = !1;
    },
    d(t) {
      t && C(n), o && o.d(t), e[9](null);
    }
  };
}
function Le(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && U(e)
  );
  return {
    c() {
      n = Q("react-portal-target"), r = ke(), t && t.c(), l = z(), this.h();
    },
    l(s) {
      n = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(n).forEach(C), r = be(s), t && t.l(s), l = z(), this.h();
    },
    h() {
      X(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      I(s, n, i), e[8](n), I(s, r, i), t && t.m(s, i), I(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && S(t, 1)) : (t = U(s), t.c(), S(t, 1), t.m(l.parentNode, l)) : t && (ve(), L(t, 1, 1, () => {
        t = null;
      }), ye());
    },
    i(s) {
      o || (S(t), o = !0);
    },
    o(s) {
      L(t), o = !1;
    },
    d(s) {
      s && (C(n), C(r), C(l)), e[8](null), t && t.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ne(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = Ee(t);
  let {
    svelteInit: c
  } = n;
  const p = v(H(n)), f = v();
  W(e, f, (d) => r(0, l = d));
  const _ = v();
  W(e, _, (d) => r(1, o = d));
  const a = [], u = Fe("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: g,
    subSlotIndex: y
  } = de() || {}, j = c({
    parent: u,
    props: p,
    target: f,
    slot: _,
    slotKey: h,
    slotIndex: g,
    subSlotIndex: y,
    onDestroy(d) {
      a.push(d);
    }
  });
  Te("$$ms-gr-react-wrapper", j), Oe(() => {
    p.set(H(n));
  }), Pe(() => {
    a.forEach((d) => d());
  });
  function O(d) {
    M[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  function F(d) {
    M[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return e.$$set = (d) => {
    r(17, n = D(D({}, n), G(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = G(n), [l, o, f, _, i, c, s, t, O, F];
}
class Ae extends we {
  constructor(n) {
    super(), Ie(this, n, Ne, Le, Se, {
      svelteInit: 5
    });
  }
}
const q = window.ms_globals.rerender, P = window.ms_globals.tree;
function De(e) {
  function n(r) {
    const l = v(), o = new Ae({
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
          }, i = t.parent ?? P;
          return i.nodes = [...i.nodes, s], q({
            createPortal: T,
            node: P
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), q({
              createPortal: T,
              node: P
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
const Me = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function We(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !Me.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function N(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(T(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: x.Children.toArray(e._reactElement.props.children).map((o) => {
        if (x.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = N(o.props.el);
          return x.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...x.Children.toArray(o.props.children), ...t]
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
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = N(t);
      n.push(...i), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function ze(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = se(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = ce(), [s, i] = ie([]);
  return ae(() => {
    var _;
    if (!t.current || !e)
      return;
    let c = e;
    function p() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ze(o, a), r && a.classList.add(...r.split(" ")), l) {
        const u = We(l);
        Object.keys(u).forEach((h) => {
          a.style[h] = u[h];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var g;
        const {
          portals: u,
          clonedElement: h
        } = N(e);
        c = h, i(u), c.style.display = "contents", p(), (g = t.current) == null || g.appendChild(c);
      };
      a(), f = new window.MutationObserver(() => {
        var u, h;
        (u = t.current) != null && u.contains(c) && ((h = t.current) == null || h.removeChild(c)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", p(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var a, u;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((u = t.current) == null || u.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, n, r, l, o]), x.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ge(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function w(e) {
  return B(() => Ge(e), [e]);
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
      const i = s.split(".");
      i.forEach((a, u) => {
        o[a] || (o[a] = {}), u !== i.length - 1 && (o = l[a]);
      });
      const c = r.slots[s];
      let p, f, _ = !1;
      c instanceof Element ? p = c : (p = c.el, f = c.callback, _ = c.clone || !1), o[i[i.length - 1]] = p ? f ? (...a) => (f(i[i.length - 1], a), /* @__PURE__ */ m.jsx(b, {
        slot: p,
        clone: _ || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ m.jsx(b, {
        slot: p,
        clone: _ || (n == null ? void 0 : n.clone)
      }) : o[i[i.length - 1]], o = l;
    });
    const t = "children";
    return r[t] && (l[t] = Z(r[t], n)), l;
  });
}
function Ue(e, n) {
  return e ? /* @__PURE__ */ m.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function R({
  key: e,
  setSlotParams: n,
  slots: r
}, l) {
  return (...o) => (n(e, o), Ue(r[e], {
    clone: !0,
    ...l
  }));
}
function He(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Be = De(({
  slots: e,
  children: n,
  onValueChange: r,
  onChange: l,
  displayRender: o,
  elRef: t,
  getPopupContainer: s,
  tagRender: i,
  maxTagPlaceholder: c,
  dropdownRender: p,
  optionRender: f,
  onLoadData: _,
  showSearch: a,
  optionItems: u,
  options: h,
  setSlotParams: g,
  ...y
}) => {
  const j = w(s), O = w(o), F = w(i), d = w(f), $ = w(p), ee = w(c), te = typeof a == "object" || e["showSearch.render"], E = He(a), ne = w(E.filter), re = w(E.render), oe = w(E.sort);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ m.jsx(ue, {
      ...y,
      ref: t,
      options: B(() => h || Z(u), [h, u]),
      showSearch: te ? {
        ...E,
        filter: ne || E.filter,
        render: e["showSearch.render"] ? R({
          slots: e,
          setSlotParams: g,
          key: "showSearch.render"
        }) : re || E.render,
        sort: oe || E.sort
      } : a,
      loadData: _,
      optionRender: d,
      getPopupContainer: j,
      dropdownRender: e.dropdownRender ? R({
        slots: e,
        setSlotParams: g,
        key: "dropdownRender"
      }) : $,
      displayRender: e.displayRender ? R({
        slots: e,
        setSlotParams: g,
        key: "displayRender"
      }) : O,
      tagRender: e.tagRender ? R({
        slots: e,
        setSlotParams: g,
        key: "tagRender"
      }) : F,
      onChange: (A, ...le) => {
        l == null || l(A, ...le), r(A);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.suffixIcon
      }) : y.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.expandIcon
      }) : y.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.removeIcon
      }) : y.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ m.jsx(b, {
        slot: e.notFoundContent
      }) : y.notFoundContent,
      maxTagPlaceholder: e.maxTagPlaceholder ? R({
        slots: e,
        setSlotParams: g,
        key: "maxTagPlaceholder"
      }) : ee || c,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : y.allowClear
    })]
  });
});
export {
  Be as Cascader,
  Be as default
};
