import { g as re, w as I, d as se, a as x, c as le } from "./Index-DQxPQCoZ.js";
const b = window.ms_globals.React, T = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, ne = window.ms_globals.React.forwardRef, oe = window.ms_globals.React.useRef, D = window.ms_globals.ReactDOM.createPortal, C = window.ms_globals.antd.Typography;
var Q = {
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
var ie = b, ae = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), de = Object.prototype.hasOwnProperty, ue = ie.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, pe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function X(t, n, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) de.call(n, s) && !pe.hasOwnProperty(s) && (r[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: ae,
    type: t,
    key: e,
    ref: l,
    props: r,
    _owner: ue.current
  };
}
k.Fragment = ce;
k.jsx = X;
k.jsxs = X;
Q.exports = k;
var _ = Q.exports;
const {
  SvelteComponent: fe,
  assign: W,
  binding_callbacks: z,
  check_outros: _e,
  children: Z,
  claim_element: $,
  claim_space: me,
  component_subscribe: G,
  compute_slots: ge,
  create_slot: he,
  detach: E,
  element: ee,
  empty: U,
  exclude_internal_props: B,
  get_all_dirty_from_scope: be,
  get_slot_changes: ye,
  group_outros: we,
  init: Ee,
  insert_hydration: S,
  safe_not_equal: xe,
  set_custom_element_data: te,
  space: Ce,
  transition_in: R,
  transition_out: F,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ie,
  getContext: Se,
  onDestroy: Re,
  setContext: Te
} = window.__gradio__svelte__internal;
function H(t) {
  let n, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = he(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = ee("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = $(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = Z(n);
      r && r.l(l), l.forEach(E), this.h();
    },
    h() {
      te(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      S(e, n, l), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ve(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? ye(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : be(
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
      F(r, e), o = !1;
    },
    d(e) {
      e && E(n), r && r.d(e), t[9](null);
    }
  };
}
function ke(t) {
  let n, o, s, r, e = (
    /*$$slots*/
    t[4].default && H(t)
  );
  return {
    c() {
      n = ee("react-portal-target"), o = Ce(), e && e.c(), s = U(), this.h();
    },
    l(l) {
      n = $(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(n).forEach(E), o = me(l), e && e.l(l), s = U(), this.h();
    },
    h() {
      te(n, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      S(l, n, a), t[8](n), S(l, o, a), e && e.m(l, a), S(l, s, a), r = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && R(e, 1)) : (e = H(l), e.c(), R(e, 1), e.m(s.parentNode, s)) : e && (we(), F(e, 1, 1, () => {
        e = null;
      }), _e());
    },
    i(l) {
      r || (R(e), r = !0);
    },
    o(l) {
      F(e), r = !1;
    },
    d(l) {
      l && (E(n), E(o), E(s)), t[8](null), e && e.d(l);
    }
  };
}
function K(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Oe(t, n, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const a = ge(e);
  let {
    svelteInit: i
  } = n;
  const m = I(K(n)), p = I();
  G(t, p, (c) => o(0, s = c));
  const g = I();
  G(t, g, (c) => o(1, r = c));
  const d = [], u = Se("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: h,
    subSlotIndex: w
  } = re() || {}, O = i({
    parent: u,
    props: m,
    target: p,
    slot: g,
    slotKey: f,
    slotIndex: h,
    subSlotIndex: w,
    onDestroy(c) {
      d.push(c);
    }
  });
  Te("$$ms-gr-react-wrapper", O), Ie(() => {
    m.set(K(n));
  }), Re(() => {
    d.forEach((c) => c());
  });
  function j(c) {
    z[c ? "unshift" : "push"](() => {
      s = c, p.set(s);
    });
  }
  function P(c) {
    z[c ? "unshift" : "push"](() => {
      r = c, g.set(r);
    });
  }
  return t.$$set = (c) => {
    o(17, n = W(W({}, n), B(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, l = c.$$scope);
  }, n = B(n), [s, r, p, g, a, i, l, e, j, P];
}
class je extends fe {
  constructor(n) {
    super(), Ee(this, n, Oe, ke, xe, {
      svelteInit: 5
    });
  }
}
const V = window.ms_globals.rerender, N = window.ms_globals.tree;
function Pe(t) {
  function n(o) {
    const s = I(), r = new je({
      ...o,
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
          }, a = e.parent ?? N;
          return a.nodes = [...a.nodes, l], V({
            createPortal: D,
            node: N
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), V({
              createPortal: D,
              node: N
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
      o(n);
    });
  });
}
function Le(t) {
  const [n, o] = J(() => x(t));
  return Y(() => {
    let s = !0;
    return t.subscribe((e) => {
      s && (s = !1, e === n) || o(e);
    });
  }, [t]), n;
}
function Ae(t) {
  const n = T(() => se(t, (o) => o), [t]);
  return Le(n);
}
const Ne = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function De(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const s = t[o];
    return typeof s == "number" && !Ne.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function M(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(D(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: b.Children.toArray(t._reactElement.props.children).map((r) => {
        if (b.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = M(r.props.el);
          return b.cloneElement(r, {
            ...r.props,
            el: l,
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
      listener: l,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = M(e);
      n.push(...a), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Fe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const y = ne(({
  slot: t,
  clone: n,
  className: o,
  style: s
}, r) => {
  const e = oe(), [l, a] = J([]);
  return Y(() => {
    var g;
    if (!e.current || !t)
      return;
    let i = t;
    function m() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Fe(r, d), o && d.classList.add(...o.split(" ")), s) {
        const u = De(s);
        Object.keys(u).forEach((f) => {
          d.style[f] = u[f];
        });
      }
    }
    let p = null;
    if (n && window.MutationObserver) {
      let d = function() {
        var h;
        const {
          portals: u,
          clonedElement: f
        } = M(t);
        i = f, a(u), i.style.display = "contents", m(), (h = e.current) == null || h.appendChild(i);
      };
      d(), p = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d();
      }), p.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (g = e.current) == null || g.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), p == null || p.disconnect();
    };
  }, [t, n, o, s, r]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Me(t) {
  return T(() => {
    const n = b.Children.toArray(t), o = [], s = [];
    return n.forEach((r) => {
      r.props.node && r.props.nodeSlotKey ? o.push(r) : s.push(r);
    }), [o, s];
  }, [t]);
}
function We(t, n) {
  return t ? /* @__PURE__ */ _.jsx(y, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function ze({
  key: t,
  setSlotParams: n,
  slots: o
}, s) {
  return (...r) => (n(t, r), We(o[t], {
    clone: !0,
    ...s
  }));
}
function q(t, n) {
  const o = T(() => b.Children.toArray(t).filter((e) => e.props.node && (!n && !e.props.nodeSlotKey || n && n === e.props.nodeSlotKey)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = x(e.props.node.slotIndex) || 0, i = x(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (x(e.props.node.subSlotIndex) || 0) - (x(l.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return Ae(o);
}
function v(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const Ue = Pe(({
  component: t,
  className: n,
  slots: o,
  children: s,
  copyable: r,
  editable: e,
  ellipsis: l,
  setSlotParams: a,
  ...i
}) => {
  var c;
  const m = q(s, "copyable.tooltips"), p = q(s, "copyable.icon"), g = o["copyable.icon"] || m.length > 0 || r, d = o["editable.icon"] || o["editable.tooltip"] || o["editable.enterIcon"] || e, u = o["ellipsis.symbol"] || o["ellipsis.tooltip"] || o["ellipsis.tooltip.title"] || l, f = v(r), h = v(e), w = v(l), O = T(() => {
    switch (t) {
      case "title":
        return C.Title;
      case "paragraph":
        return C.Paragraph;
      case "text":
        return C.Text;
      case "link":
        return C.Link;
    }
  }, [t]), [j, P] = Me(s);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: j
    }), /* @__PURE__ */ _.jsx(O, {
      ...i,
      className: le(n, `ms-gr-antd-typography-${t}`),
      copyable: g ? {
        ...v(r),
        tooltips: m.length > 0 ? m.map((L, A) => /* @__PURE__ */ _.jsx(y, {
          slot: L
        }, A)) : f.tooltips,
        icon: p.length > 0 ? p.map((L, A) => /* @__PURE__ */ _.jsx(y, {
          slot: L
        }, A)) : f.icon
      } : void 0,
      editable: d ? {
        ...h,
        icon: o["editable.icon"] ? /* @__PURE__ */ _.jsx(y, {
          slot: o["editable.icon"]
        }) : h.icon,
        tooltip: o["editable.tooltip"] ? /* @__PURE__ */ _.jsx(y, {
          slot: o["editable.tooltip"]
        }) : h.tooltip,
        enterIcon: o["editable.enterIcon"] ? /* @__PURE__ */ _.jsx(y, {
          slot: o["editable.enterIcon"]
        }) : h.enterIcon
      } : void 0,
      ellipsis: t === "link" ? !!u : u ? {
        ...w,
        symbol: o["ellipsis.symbol"] ? ze({
          key: "ellipsis.symbol",
          setSlotParams: a,
          slots: o
        }, {
          clone: !0
        }) : w.symbol,
        tooltip: o["ellipsis.tooltip"] ? /* @__PURE__ */ _.jsx(y, {
          slot: o["ellipsis.tooltip"]
        }) : {
          ...w.tooltip,
          title: o["ellipsis.tooltip.title"] ? /* @__PURE__ */ _.jsx(y, {
            slot: o["ellipsis.tooltip.title"]
          }) : (c = w.tooltip) == null ? void 0 : c.title
        }
      } : void 0,
      children: P
    })]
  });
});
export {
  Ue as TypographyBase,
  Ue as default
};
