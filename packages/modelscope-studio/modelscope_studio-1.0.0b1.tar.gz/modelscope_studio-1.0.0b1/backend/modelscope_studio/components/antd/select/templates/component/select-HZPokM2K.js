import { g as se, w as v } from "./Index-B2N6ljj3.js";
const E = window.ms_globals.React, re = window.ms_globals.React.forwardRef, le = window.ms_globals.React.useRef, oe = window.ms_globals.React.useState, ce = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, ae = window.ms_globals.antd.Select;
var B = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ie = E, de = Symbol.for("react.element"), ue = Symbol.for("react.fragment"), fe = Object.prototype.hasOwnProperty, _e = ie.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, me = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, l) {
  var o, r = {}, n = null, c = null;
  l !== void 0 && (n = "" + l), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (c = t.ref);
  for (o in t) fe.call(t, o) && !me.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: de,
    type: e,
    key: n,
    ref: c,
    props: r,
    _owner: _e.current
  };
}
S.Fragment = ue;
S.jsx = V;
S.jsxs = V;
B.exports = S;
var h = B.exports;
const {
  SvelteComponent: he,
  assign: A,
  binding_callbacks: D,
  check_outros: pe,
  children: J,
  claim_element: Y,
  claim_space: ge,
  component_subscribe: M,
  compute_slots: we,
  create_slot: be,
  detach: I,
  element: K,
  empty: W,
  exclude_internal_props: z,
  get_all_dirty_from_scope: ye,
  get_slot_changes: Ee,
  group_outros: Ie,
  init: Re,
  insert_hydration: x,
  safe_not_equal: ve,
  set_custom_element_data: Q,
  space: xe,
  transition_in: C,
  transition_out: T,
  update_slot_base: Ce
} = window.__gradio__svelte__internal, {
  beforeUpdate: Se,
  getContext: ke,
  onDestroy: Oe,
  setContext: je
} = window.__gradio__svelte__internal;
function G(e) {
  let t, l;
  const o = (
    /*#slots*/
    e[7].default
  ), r = be(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var c = J(t);
      r && r.l(c), c.forEach(I), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      x(n, t, c), r && r.m(t, null), e[9](t), l = !0;
    },
    p(n, c) {
      r && r.p && (!l || c & /*$$scope*/
      64) && Ce(
        r,
        o,
        n,
        /*$$scope*/
        n[6],
        l ? Ee(
          o,
          /*$$scope*/
          n[6],
          c,
          null
        ) : ye(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (C(r, n), l = !0);
    },
    o(n) {
      T(r, n), l = !1;
    },
    d(n) {
      n && I(t), r && r.d(n), e[9](null);
    }
  };
}
function Fe(e) {
  let t, l, o, r, n = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      t = K("react-portal-target"), l = xe(), n && n.c(), o = W(), this.h();
    },
    l(c) {
      t = Y(c, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(I), l = ge(c), n && n.l(c), o = W(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(c, s) {
      x(c, t, s), e[8](t), x(c, l, s), n && n.m(c, s), x(c, o, s), r = !0;
    },
    p(c, [s]) {
      /*$$slots*/
      c[4].default ? n ? (n.p(c, s), s & /*$$slots*/
      16 && C(n, 1)) : (n = G(c), n.c(), C(n, 1), n.m(o.parentNode, o)) : n && (Ie(), T(n, 1, 1, () => {
        n = null;
      }), pe());
    },
    i(c) {
      r || (C(n), r = !0);
    },
    o(c) {
      T(n), r = !1;
    },
    d(c) {
      c && (I(t), I(l), I(o)), e[8](null), n && n.d(c);
    }
  };
}
function U(e) {
  const {
    svelteInit: t,
    ...l
  } = e;
  return l;
}
function Pe(e, t, l) {
  let o, r, {
    $$slots: n = {},
    $$scope: c
  } = t;
  const s = we(n);
  let {
    svelteInit: a
  } = t;
  const _ = v(U(t)), u = v();
  M(e, u, (d) => l(0, o = d));
  const m = v();
  M(e, m, (d) => l(1, r = d));
  const i = [], f = ke("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: w
  } = se() || {}, k = a({
    parent: f,
    props: _,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: w,
    onDestroy(d) {
      i.push(d);
    }
  });
  je("$$ms-gr-react-wrapper", k), Se(() => {
    _.set(U(t));
  }), Oe(() => {
    i.forEach((d) => d());
  });
  function O(d) {
    D[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function j(d) {
    D[d ? "unshift" : "push"](() => {
      r = d, m.set(r);
    });
  }
  return e.$$set = (d) => {
    l(17, t = A(A({}, t), z(d))), "svelteInit" in d && l(5, a = d.svelteInit), "$$scope" in d && l(6, c = d.$$scope);
  }, t = z(t), [o, r, u, m, s, a, c, n, O, j];
}
class Te extends he {
  constructor(t) {
    super(), Re(this, t, Pe, Fe, ve, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, F = window.ms_globals.tree;
function Le(e) {
  function t(l) {
    const o = v(), r = new Te({
      ...l,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, s = n.parent ?? F;
          return s.nodes = [...s.nodes, c], H({
            createPortal: P,
            node: F
          }), n.onDestroy(() => {
            s.nodes = s.nodes.filter((a) => a.svelteInstance !== o), H({
              createPortal: P,
              node: F
            });
          }), c;
        },
        ...l.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Ne = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(e) {
  return e ? Object.keys(e).reduce((t, l) => {
    const o = e[l];
    return typeof o == "number" && !Ne.includes(l) ? t[l] = o + "px" : t[l] = o, t;
  }, {}) : {};
}
function L(e) {
  const t = [], l = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(P(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((r) => {
        if (E.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: c
          } = L(r.props.el);
          return E.cloneElement(r, {
            ...r.props,
            el: c,
            children: [...E.Children.toArray(r.props.children), ...n]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: c,
      type: s,
      useCapture: a
    }) => {
      l.addEventListener(s, c, a);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const n = o[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: c,
        portals: s
      } = L(n);
      t.push(...s), l.appendChild(c);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function De(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = re(({
  slot: e,
  clone: t,
  className: l,
  style: o
}, r) => {
  const n = le(), [c, s] = oe([]);
  return ce(() => {
    var m;
    if (!n.current || !e)
      return;
    let a = e;
    function _() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), De(r, i), l && i.classList.add(...l.split(" ")), o) {
        const f = Ae(o);
        Object.keys(f).forEach((p) => {
          i.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var g;
        const {
          portals: f,
          clonedElement: p
        } = L(e);
        a = p, s(f), a.style.display = "contents", _(), (g = n.current) == null || g.appendChild(a);
      };
      i(), u = new window.MutationObserver(() => {
        var f, p;
        (f = n.current) != null && f.contains(a) && ((p = n.current) == null || p.removeChild(a)), i();
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", _(), (m = n.current) == null || m.appendChild(a);
    return () => {
      var i, f;
      a.style.display = "", (i = n.current) != null && i.contains(a) && ((f = n.current) == null || f.removeChild(a)), u == null || u.disconnect();
    };
  }, [e, t, l, o, r]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...c);
});
function Me(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function b(e) {
  return q(() => Me(e), [e]);
}
function X(e, t) {
  return e.filter(Boolean).map((l) => {
    if (typeof l != "object")
      return t != null && t.fallback ? t.fallback(l) : l;
    const o = {
      ...l.props
    };
    let r = o;
    Object.keys(l.slots).forEach((c) => {
      if (!l.slots[c] || !(l.slots[c] instanceof Element) && !l.slots[c].el)
        return;
      const s = c.split(".");
      s.forEach((i, f) => {
        r[i] || (r[i] = {}), f !== s.length - 1 && (r = o[i]);
      });
      const a = l.slots[c];
      let _, u, m = !1;
      a instanceof Element ? _ = a : (_ = a.el, u = a.callback, m = a.clone || !1), r[s[s.length - 1]] = _ ? u ? (...i) => (u(s[s.length - 1], i), /* @__PURE__ */ h.jsx(y, {
        slot: _,
        clone: m || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(y, {
        slot: _,
        clone: m || (t == null ? void 0 : t.clone)
      }) : r[s[s.length - 1]], r = o;
    });
    const n = (t == null ? void 0 : t.children) || "children";
    return l[n] && (o[n] = X(l[n], t)), o;
  });
}
function We(e, t) {
  return e ? /* @__PURE__ */ h.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function R({
  key: e,
  setSlotParams: t,
  slots: l
}, o) {
  return (...r) => (t(e, r), We(l[e], {
    clone: !0,
    ...o
  }));
}
const Ge = Le(({
  slots: e,
  children: t,
  onValueChange: l,
  filterOption: o,
  onChange: r,
  options: n,
  optionItems: c,
  getPopupContainer: s,
  dropdownRender: a,
  optionRender: _,
  tagRender: u,
  labelRender: m,
  filterSort: i,
  maxTagPlaceholder: f,
  elRef: p,
  setSlotParams: g,
  ...w
}) => {
  const k = b(s), O = b(o), j = b(a), d = b(i), Z = b(_), $ = b(u), ee = b(m), te = b(f);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ h.jsx(ae, {
      ...w,
      ref: p,
      options: q(() => n || X(c, {
        children: "options",
        clone: !0
      }), [c, n]),
      onChange: (N, ...ne) => {
        r == null || r(N, ...ne), l(N);
      },
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : w.allowClear,
      removeIcon: e.removeIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.removeIcon
      }) : w.removeIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.suffixIcon
      }) : w.suffixIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ h.jsx(y, {
        slot: e.notFoundContent
      }) : w.notFoundContent,
      menuItemSelectedIcon: e.menuItemSelectedIcon ? /* @__PURE__ */ h.jsx(y, {
        slot: e.menuItemSelectedIcon
      }) : w.menuItemSelectedIcon,
      filterOption: O || o,
      maxTagPlaceholder: e.maxTagPlaceholder ? R({
        slots: e,
        setSlotParams: g,
        key: "maxTagPlaceholder"
      }) : te,
      getPopupContainer: k,
      dropdownRender: e.dropdownRender ? R({
        slots: e,
        setSlotParams: g,
        key: "dropdownRender"
      }) : j,
      optionRender: e.optionRender ? R({
        slots: e,
        setSlotParams: g,
        key: "optionRender"
      }) : Z,
      tagRender: e.tagRender ? R({
        slots: e,
        setSlotParams: g,
        key: "tagRender"
      }) : $,
      labelRender: e.labelRender ? R({
        slots: e,
        setSlotParams: g,
        key: "labelRender"
      }) : ee,
      filterSort: d
    })]
  });
});
export {
  Ge as Select,
  Ge as default
};
