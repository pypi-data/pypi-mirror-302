import { g as $, w as E } from "./Index-C74v0DGx.js";
const h = window.ms_globals.React, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, D = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Tour;
var M = {
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) oe.call(t, s) && !se.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: le.current
  };
}
x.Fragment = re;
x.jsx = W;
x.jsxs = W;
M.exports = x;
var g = M.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: P,
  check_outros: ie,
  children: z,
  claim_element: G,
  claim_space: ae,
  component_subscribe: j,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: U,
  empty: T,
  exclude_internal_props: L,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: H,
  space: ge,
  transition_in: v,
  transition_out: C,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = de(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = U("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = z(t);
      r && r.l(l), l.forEach(w), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && we(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : fe(
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
      C(r, e), o = !1;
    },
    d(e) {
      e && w(t), r && r.d(e), n[9](null);
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
      t = U("react-portal-target"), o = ge(), e && e.c(), s = T(), this.h();
    },
    l(l) {
      t = G(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(w), o = ae(l), e && e.l(l), s = T(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      y(l, t, i), n[8](t), y(l, o, i), e && e.m(l, i), y(l, s, i), r = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && v(e, 1)) : (e = N(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (pe(), C(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      r || (v(e), r = !0);
    },
    o(l) {
      C(e), r = !1;
    },
    d(l) {
      l && (w(t), w(o), w(s)), n[8](null), e && e.d(l);
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
function Ie(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = ue(e);
  let {
    svelteInit: c
  } = t;
  const _ = E(A(t)), u = E();
  j(n, u, (d) => o(0, s = d));
  const p = E();
  j(n, p, (d) => o(1, r = d));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: B
  } = $() || {}, J = c({
    parent: f,
    props: _,
    target: u,
    slot: p,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: B,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", J), be(() => {
    _.set(A(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function V(d) {
    P[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function Y(d) {
    P[d ? "unshift" : "push"](() => {
      r = d, p.set(r);
    });
  }
  return n.$$set = (d) => {
    o(17, t = k(k({}, t), L(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, l = d.$$scope);
  }, t = L(t), [s, r, u, p, i, c, l, e, V, Y];
}
class Re extends ce {
  constructor(t) {
    super(), me(this, t, Ie, xe, he, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const s = E(), r = new Re({
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
          }, i = e.parent ?? I;
          return i.nodes = [...i.nodes, l], F({
            createPortal: R,
            node: I
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), F({
              createPortal: R,
              node: I
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
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Se.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function S(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = S(r.props.el);
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
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, l, c);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = S(e);
      t.push(...i), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const O = K(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = Q(), [l, i] = X([]);
  return Z(() => {
    var p;
    if (!e.current || !n)
      return;
    let c = n;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(r, a), o && a.classList.add(...o.split(" ")), s) {
        const f = Oe(s);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: f,
          clonedElement: m
        } = S(n);
        c = m, i(f), c.style.display = "contents", _(), (b = e.current) == null || b.appendChild(c);
      };
      a(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(c) && ((m = e.current) == null || m.removeChild(c)), a();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (p = e.current) == null || p.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((f = e.current) == null || f.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, t, o, s, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function je(n) {
  return D(() => Pe(n), [n]);
}
function q(n, t) {
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
      const i = l.split(".");
      i.forEach((a, f) => {
        r[a] || (r[a] = {}), f !== i.length - 1 && (r = s[a]);
      });
      const c = o.slots[l];
      let _, u, p = !1;
      c instanceof Element ? _ = c : (_ = c.el, u = c.callback, p = c.clone || !1), r[i[i.length - 1]] = _ ? u ? (...a) => (u(i[i.length - 1], a), /* @__PURE__ */ g.jsx(O, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ g.jsx(O, {
        slot: _,
        clone: p || (t == null ? void 0 : t.clone)
      }) : r[i[i.length - 1]], r = s;
    });
    const e = "children";
    return o[e] && (s[e] = q(o[e], t)), s;
  });
}
const Le = Ce(({
  slots: n,
  steps: t,
  slotItems: o,
  children: s,
  onChange: r,
  onClose: e,
  onValueChange: l,
  getPopupContainer: i,
  ...c
}) => {
  const _ = je(i);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ g.jsx(ee, {
      ...c,
      steps: D(() => t || q(o), [t, o]),
      onChange: (u) => {
        r == null || r(u), l({
          open: !0,
          current: u
        });
      },
      closeIcon: n.closeIcon ? /* @__PURE__ */ g.jsx(O, {
        slot: n.closeIcon
      }) : c.closeIcon,
      getPopupContainer: _,
      onClose: (u, ...p) => {
        e == null || e(u, ...p), l({
          current: u,
          open: !1
        });
      }
    })]
  });
});
export {
  Le as Tour,
  Le as default
};
