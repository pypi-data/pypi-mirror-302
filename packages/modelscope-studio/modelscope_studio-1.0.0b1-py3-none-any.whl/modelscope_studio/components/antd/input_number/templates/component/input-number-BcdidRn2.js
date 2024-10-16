import { g as $, w as E } from "./Index-B4MY-gG8.js";
const w = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.InputNumber;
var B = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = w, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(t, n, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) re.call(n, s) && !le.hasOwnProperty(s) && (o[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: l,
    props: o,
    _owner: se.current
  };
}
I.Fragment = oe;
I.jsx = M;
I.jsxs = M;
B.exports = I;
var _ = B.exports;
const {
  SvelteComponent: ie,
  assign: j,
  binding_callbacks: k,
  check_outros: ce,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: P,
  compute_slots: de,
  create_slot: ue,
  detach: b,
  element: G,
  empty: A,
  exclude_internal_props: L,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: v,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: we,
  transition_in: x,
  transition_out: S,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(t) {
  let n, r;
  const s = (
    /*#slots*/
    t[7].default
  ), o = ue(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = G("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = W(n);
      o && o.l(l), l.forEach(b), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, n, l), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ge(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
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
      r || (x(o, e), r = !0);
    },
    o(e) {
      S(o, e), r = !1;
    },
    d(e) {
      e && b(n), o && o.d(e), t[9](null);
    }
  };
}
function xe(t) {
  let n, r, s, o, e = (
    /*$$slots*/
    t[4].default && N(t)
  );
  return {
    c() {
      n = G("react-portal-target"), r = we(), e && e.c(), s = A(), this.h();
    },
    l(l) {
      n = z(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(n).forEach(b), r = ae(l), e && e.l(l), s = A(), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      v(l, n, i), t[8](n), v(l, r, i), e && e.m(l, i), v(l, s, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && x(e, 1)) : (e = N(l), e.c(), x(e, 1), e.m(s.parentNode, s)) : e && (pe(), S(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      o || (x(e), o = !0);
    },
    o(l) {
      S(e), o = !1;
    },
    d(l) {
      l && (b(n), b(r), b(s)), t[8](null), e && e.d(l);
    }
  };
}
function T(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function Ie(t, n, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const i = de(e);
  let {
    svelteInit: c
  } = n;
  const m = E(T(n)), u = E();
  P(t, u, (a) => r(0, s = a));
  const h = E();
  P(t, h, (a) => r(1, o = a));
  const d = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: H
  } = $() || {}, K = c({
    parent: f,
    props: m,
    target: u,
    slot: h,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: H,
    onDestroy(a) {
      d.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", K), be(() => {
    m.set(T(n));
  }), Ee(() => {
    d.forEach((a) => a());
  });
  function q(a) {
    k[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  function V(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, h.set(o);
    });
  }
  return t.$$set = (a) => {
    r(17, n = j(j({}, n), L(a))), "svelteInit" in a && r(5, c = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, n = L(n), [s, o, u, h, i, c, l, e, q, V];
}
class Ce extends ie {
  constructor(n) {
    super(), me(this, n, Ie, xe, he, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, C = window.ms_globals.tree;
function Re(t) {
  function n(r) {
    const s = E(), o = new Ce({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? C;
          return i.nodes = [...i.nodes, l], F({
            createPortal: R,
            node: C
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), F({
              createPortal: R,
              node: C
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
      r(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const s = t[r];
    return typeof s == "number" && !Se.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function O(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(R(w.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: w.Children.toArray(t._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...w.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(t.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = O(e);
      n.push(...i), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function je(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const g = J(({
  slot: t,
  clone: n,
  className: r,
  style: s
}, o) => {
  const e = Y(), [l, i] = Q([]);
  return X(() => {
    var h;
    if (!e.current || !t)
      return;
    let c = t;
    function m() {
      let d = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (d = c.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), je(o, d), r && d.classList.add(...r.split(" ")), s) {
        const f = Oe(s);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let d = function() {
        var y;
        const {
          portals: f,
          clonedElement: p
        } = O(t);
        c = p, i(f), c.style.display = "contents", m(), (y = e.current) == null || y.appendChild(c);
      };
      d(), u = new window.MutationObserver(() => {
        var f, p;
        (f = e.current) != null && f.contains(c) && ((p = e.current) == null || p.removeChild(c)), d();
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", m(), (h = e.current) == null || h.appendChild(c);
    return () => {
      var d, f;
      c.style.display = "", (d = e.current) != null && d.contains(c) && ((f = e.current) == null || f.removeChild(c)), u == null || u.disconnect();
    };
  }, [t, n, r, s, o]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function ke(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function D(t) {
  return Z(() => ke(t), [t]);
}
const Ae = Re(({
  slots: t,
  children: n,
  onValueChange: r,
  onChange: s,
  formatter: o,
  parser: e,
  elRef: l,
  ...i
}) => {
  const c = D(o), m = D(e);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ _.jsx(ee, {
      ...i,
      ref: l,
      onChange: (u) => {
        s == null || s(u), r(u);
      },
      parser: m,
      formatter: c,
      controls: t["controls.upIcon"] || t["controls.downIcon"] ? {
        upIcon: t["controls.upIcon"] ? /* @__PURE__ */ _.jsx(g, {
          slot: t["controls.upIcon"]
        }) : typeof i.controls == "object" ? i.controls.upIcon : void 0,
        downIcon: t["controls.downIcon"] ? /* @__PURE__ */ _.jsx(g, {
          slot: t["controls.downIcon"]
        }) : typeof i.controls == "object" ? i.controls.downIcon : void 0
      } : i.controls,
      addonAfter: t.addonAfter ? /* @__PURE__ */ _.jsx(g, {
        slot: t.addonAfter
      }) : i.addonAfter,
      addonBefore: t.addonBefore ? /* @__PURE__ */ _.jsx(g, {
        slot: t.addonBefore
      }) : i.addonBefore,
      prefix: t.prefix ? /* @__PURE__ */ _.jsx(g, {
        slot: t.prefix
      }) : i.prefix,
      suffix: t.suffix ? /* @__PURE__ */ _.jsx(g, {
        slot: t.suffix
      }) : i.suffix
    })]
  });
});
export {
  Ae as InputNumber,
  Ae as default
};
