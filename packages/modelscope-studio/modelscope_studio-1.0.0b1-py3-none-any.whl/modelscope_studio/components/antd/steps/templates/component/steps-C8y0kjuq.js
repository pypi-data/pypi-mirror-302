import { g as $, w as E } from "./Index-Bo-cw7h2.js";
const h = window.ms_globals.React, F = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, x = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Steps;
var M = {
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !se.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: le.current
  };
}
C.Fragment = re;
C.jsx = W;
C.jsxs = W;
M.exports = C;
var g = M.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: j,
  check_outros: ie,
  children: z,
  claim_element: G,
  claim_space: ae,
  component_subscribe: P,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: U,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: H,
  space: ge,
  transition_in: v,
  transition_out: R,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = de(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = U("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(t);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          l,
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
      r || (v(o, e), r = !0);
    },
    o(e) {
      R(o, e), r = !1;
    },
    d(e) {
      e && w(t), o && o.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = U("react-portal-target"), r = ge(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(w), r = ae(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), n[8](t), y(s, r, c), e && e.m(s, c), y(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (pe(), R(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      o || (v(e), o = !0);
    },
    o(s) {
      R(e), o = !1;
    },
    d(s) {
      s && (w(t), w(r), w(l)), n[8](null), e && e.d(s);
    }
  };
}
function A(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Se(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ue(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(A(t)), d = E();
  P(n, d, (u) => r(0, l = u));
  const p = E();
  P(n, p, (u) => r(1, o = u));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: B
  } = $() || {}, V = i({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: B,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", V), be(() => {
    _.set(A(t));
  }), ye(() => {
    a.forEach((u) => u());
  });
  function J(u) {
    j[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function Y(u) {
    j[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return n.$$set = (u) => {
    r(17, t = k(k({}, t), T(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = T(t), [l, o, d, p, c, i, s, e, J, Y];
}
class xe extends ce {
  constructor(t) {
    super(), me(this, t, Se, Ce, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const l = E(), o = new xe({
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
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, s], D({
            createPortal: x,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: x,
              node: S
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
function Ie(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Oe(n) {
  return F(() => Ie(n), [n]);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !ke.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function I(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(x(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = I(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...e]
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
      } = I(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Pe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const O = K(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = Q(), [s, c] = X([]);
  return Z(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const f = je(l);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: f,
          clonedElement: m
        } = I(n);
        i = m, c(f), i.style.display = "contents", _(), (b = e.current) == null || b.appendChild(i);
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
  }, [n, t, r, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function q(n, t) {
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
      let _, d, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, d = i.callback, p = i.clone || !1), o[c[c.length - 1]] = _ ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ g.jsx(O, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ g.jsx(O, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : o[c[c.length - 1]], o = l;
    });
    const e = "children";
    return r[e] && (l[e] = q(r[e], t)), l;
  });
}
function Le(n, t) {
  return n ? /* @__PURE__ */ g.jsx(O, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: t,
  slots: r
}, l) {
  return (...o) => (t(n, o), Le(r[n], {
    clone: !0,
    ...l
  }));
}
const Ae = Re(({
  slots: n,
  items: t,
  slotItems: r,
  setSlotParams: l,
  children: o,
  progressDot: e,
  ...s
}) => {
  const c = Oe(e);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ g.jsx(ee, {
      ...s,
      items: F(() => t || q(r), [t, r]),
      progressDot: n.progressDot ? Te({
        slots: n,
        setSlotParams: l,
        key: "progressDot"
      }, {
        clone: !0
      }) : c || e
    })]
  });
});
export {
  Ae as Steps,
  Ae as default
};
