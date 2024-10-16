import { g as le, b as ie } from "./Index-CJvwmqWh.js";
const y = window.ms_globals.React, ce = window.ms_globals.React.forwardRef, ue = window.ms_globals.React.useRef, ae = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, de = window.ms_globals.ReactDOM.createPortal;
function v() {
}
function me(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function _e(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return v;
  }
  const n = t.subscribe(...e);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function x(t) {
  let e;
  return _e(t, (n) => e = n)(), e;
}
const C = [];
function h(t, e = v) {
  let n;
  const s = /* @__PURE__ */ new Set();
  function o(i) {
    if (me(t, i) && (t = i, n)) {
      const u = !C.length;
      for (const a of s)
        a[1](), C.push(a, t);
      if (u) {
        for (let a = 0; a < C.length; a += 2)
          C[a][0](C[a + 1]);
        C.length = 0;
      }
    }
  }
  function r(i) {
    o(i(t));
  }
  function l(i, u = v) {
    const a = [i, u];
    return s.add(a), s.size === 1 && (n = e(o, r) || v), i(t), () => {
      s.delete(a), s.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: r,
    subscribe: l
  };
}
const {
  getContext: J,
  setContext: j
} = window.__gradio__svelte__internal, pe = "$$ms-gr-slots-key";
function ge() {
  const t = h({});
  return j(pe, t);
}
const he = "$$ms-gr-render-slot-context-key";
function be() {
  const t = j(he, h({}));
  return (e, n) => {
    t.update((s) => typeof n == "function" ? {
      ...s,
      [e]: n(s[e])
    } : {
      ...s,
      [e]: n
    });
  };
}
const ye = "$$ms-gr-context-key";
function xe(t, e, n) {
  var m;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const s = Q(), o = Pe({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  s && s.subscribe((d) => {
    o.slotKey.set(d);
  }), Ce();
  const r = J(ye), l = ((m = x(r)) == null ? void 0 : m.as_item) || t.as_item, i = r ? l ? x(r)[l] : x(r) : {}, u = (d, f) => d ? le({
    ...d,
    ...f || {}
  }, e) : void 0, a = h({
    ...t,
    ...i,
    restProps: u(t.restProps, i),
    originalRestProps: t.restProps
  });
  return r ? (r.subscribe((d) => {
    const {
      as_item: f
    } = x(a);
    f && (d = d[f]), a.update((_) => ({
      ..._,
      ...d,
      restProps: u(_.restProps, d)
    }));
  }), [a, (d) => {
    const f = d.as_item ? x(r)[d.as_item] : x(r);
    return a.set({
      ...d,
      ...f,
      restProps: u(d.restProps, f),
      originalRestProps: d.restProps
    });
  }]) : [a, (d) => {
    a.set({
      ...d,
      restProps: u(d.restProps),
      originalRestProps: d.restProps
    });
  }];
}
const Y = "$$ms-gr-slot-key";
function Ce() {
  j(Y, h(void 0));
}
function Q() {
  return J(Y);
}
const Se = "$$ms-gr-component-slot-context-key";
function Pe({
  slot: t,
  index: e,
  subIndex: n
}) {
  return j(Se, {
    slotKey: h(t),
    slotIndex: h(e),
    subSlotIndex: h(n)
  });
}
function N(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Ee(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var X = {
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
var we = y, Re = Symbol.for("react.element"), Ie = Symbol.for("react.fragment"), Oe = Object.prototype.hasOwnProperty, ve = we.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ke = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(t, e, n) {
  var s, o = {}, r = null, l = null;
  n !== void 0 && (r = "" + n), e.key !== void 0 && (r = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) Oe.call(e, s) && !ke.hasOwnProperty(s) && (o[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: Re,
    type: t,
    key: r,
    ref: l,
    props: o,
    _owner: ve.current
  };
}
F.Fragment = Ie;
F.jsx = Z;
F.jsxs = Z;
X.exports = F;
var W = X.exports;
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const s = t[n];
    return typeof s == "number" && !je.includes(n) ? e[n] = s + "px" : e[n] = s, e;
  }, {}) : {};
}
function L(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(de(y.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: y.Children.toArray(t._reactElement.props.children).map((o) => {
        if (y.isValidElement(o) && o.props.__slot__) {
          const {
            portals: r,
            clonedElement: l
          } = L(o.props.el);
          return y.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...y.Children.toArray(o.props.children), ...r]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: u
    }) => {
      n.addEventListener(i, l, u);
    });
  });
  const s = Array.from(t.childNodes);
  for (let o = 0; o < s.length; o++) {
    const r = s[o];
    if (r.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(r);
      e.push(...i), n.appendChild(l);
    } else r.nodeType === 3 && n.appendChild(r.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function Ne(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const G = ce(({
  slot: t,
  clone: e,
  className: n,
  style: s
}, o) => {
  const r = ue(), [l, i] = ae([]);
  return fe(() => {
    var d;
    if (!r.current || !t)
      return;
    let u = t;
    function a() {
      let f = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (f = u.children[0], f.tagName.toLowerCase() === "react-portal-target" && f.children[0] && (f = f.children[0])), Ne(o, f), n && f.classList.add(...n.split(" ")), s) {
        const _ = Fe(s);
        Object.keys(_).forEach((p) => {
          f.style[p] = _[p];
        });
      }
    }
    let m = null;
    if (e && window.MutationObserver) {
      let f = function() {
        var b;
        const {
          portals: _,
          clonedElement: p
        } = L(t);
        u = p, i(_), u.style.display = "contents", a(), (b = r.current) == null || b.appendChild(u);
      };
      f(), m = new window.MutationObserver(() => {
        var _, p;
        (_ = r.current) != null && _.contains(u) && ((p = r.current) == null || p.removeChild(u)), f();
      }), m.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", a(), (d = r.current) == null || d.appendChild(u);
    return () => {
      var f, _;
      u.style.display = "", (f = r.current) != null && f.contains(u) && ((_ = r.current) == null || _.removeChild(u)), m == null || m.disconnect();
    };
  }, [t, e, n, s, o]), y.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...l);
});
function $(t, e) {
  return t.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return n;
    const s = {
      ...n.props
    };
    let o = s;
    Object.keys(n.slots).forEach((l) => {
      if (!n.slots[l] || !(n.slots[l] instanceof Element) && !n.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((f, _) => {
        o[f] || (o[f] = {}), _ !== i.length - 1 && (o = s[f]);
      });
      const u = n.slots[l];
      let a, m, d = !1;
      u instanceof Element ? a = u : (a = u.el, m = u.callback, d = u.clone || !1), o[i[i.length - 1]] = a ? m ? (...f) => (m(i[i.length - 1], f), /* @__PURE__ */ W.jsx(G, {
        slot: a,
        clone: d || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ W.jsx(G, {
        slot: a,
        clone: d || (e == null ? void 0 : e.clone)
      }) : o[i[i.length - 1]], o = s;
    });
    const r = "children";
    return n[r] && (s[r] = $(n[r], e)), s;
  });
}
var ee = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function n() {
      for (var r = "", l = 0; l < arguments.length; l++) {
        var i = arguments[l];
        i && (r = o(r, s(i)));
      }
      return r;
    }
    function s(r) {
      if (typeof r == "string" || typeof r == "number")
        return r;
      if (typeof r != "object")
        return "";
      if (Array.isArray(r))
        return n.apply(null, r);
      if (r.toString !== Object.prototype.toString && !r.toString.toString().includes("[native code]"))
        return r.toString();
      var l = "";
      for (var i in r)
        e.call(r, i) && r[i] && (l = o(l, i));
      return l;
    }
    function o(r, l) {
      return l ? r ? r + " " + l : r + l : r;
    }
    t.exports ? (n.default = n, t.exports = n) : window.classNames = n;
  })();
})(ee);
var Le = ee.exports;
const Te = /* @__PURE__ */ Ee(Le), {
  getContext: Ke,
  setContext: Ae
} = window.__gradio__svelte__internal;
function te(t) {
  const e = `$$ms-gr-${t}-context-key`;
  function n(o = ["default"]) {
    const r = o.reduce((l, i) => (l[i] = h([]), l), {});
    return Ae(e, {
      itemsMap: r,
      allowedSlots: o
    }), r;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: r
    } = Ke(e);
    return function(l, i, u) {
      o && (l ? o[l].update((a) => {
        const m = [...a];
        return r.includes(l) ? m[i] = u : m[i] = void 0, m;
      }) : r.includes("default") && o.default.update((a) => {
        const m = [...a];
        return m[i] = u, m;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: s
  };
}
const {
  getItems: qe,
  getSetItemFn: tt
} = te("table-row-selection-selection"), {
  getItems: nt,
  getSetItemFn: Me
} = te("table-row-selection"), {
  SvelteComponent: ze,
  assign: H,
  check_outros: De,
  component_subscribe: P,
  compute_rest_props: U,
  create_slot: We,
  detach: Ge,
  empty: V,
  exclude_internal_props: He,
  flush: g,
  get_all_dirty_from_scope: Ue,
  get_slot_changes: Ve,
  group_outros: Be,
  init: Je,
  insert_hydration: Ye,
  safe_not_equal: Qe,
  transition_in: k,
  transition_out: T,
  update_slot_base: Xe
} = window.__gradio__svelte__internal;
function B(t) {
  let e;
  const n = (
    /*#slots*/
    t[20].default
  ), s = We(
    n,
    t,
    /*$$scope*/
    t[19],
    null
  );
  return {
    c() {
      s && s.c();
    },
    l(o) {
      s && s.l(o);
    },
    m(o, r) {
      s && s.m(o, r), e = !0;
    },
    p(o, r) {
      s && s.p && (!e || r & /*$$scope*/
      524288) && Xe(
        s,
        n,
        o,
        /*$$scope*/
        o[19],
        e ? Ve(
          n,
          /*$$scope*/
          o[19],
          r,
          null
        ) : Ue(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      e || (k(s, o), e = !0);
    },
    o(o) {
      T(s, o), e = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Ze(t) {
  let e, n, s = (
    /*$mergedProps*/
    t[0].visible && B(t)
  );
  return {
    c() {
      s && s.c(), e = V();
    },
    l(o) {
      s && s.l(o), e = V();
    },
    m(o, r) {
      s && s.m(o, r), Ye(o, e, r), n = !0;
    },
    p(o, [r]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, r), r & /*$mergedProps*/
      1 && k(s, 1)) : (s = B(o), s.c(), k(s, 1), s.m(e.parentNode, e)) : s && (Be(), T(s, 1, 1, () => {
        s = null;
      }), De());
    },
    i(o) {
      n || (k(s), n = !0);
    },
    o(o) {
      T(s), n = !1;
    },
    d(o) {
      o && Ge(e), s && s.d(o);
    }
  };
}
function $e(t, e, n) {
  const s = ["gradio", "props", "_internal", "as_item", "value", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = U(e, s), r, l, i, u, a, {
    $$slots: m = {},
    $$scope: d
  } = e, {
    gradio: f
  } = e, {
    props: _ = {}
  } = e;
  const p = h(_);
  P(t, p, (c) => n(18, a = c));
  let {
    _internal: b = {}
  } = e, {
    as_item: E
  } = e, {
    value: S
  } = e, {
    visible: w = !0
  } = e, {
    elem_id: R = ""
  } = e, {
    elem_classes: I = []
  } = e, {
    elem_style: O = {}
  } = e;
  const K = Q();
  P(t, K, (c) => n(17, u = c));
  const [A, ne] = xe({
    gradio: f,
    props: a,
    _internal: b,
    visible: w,
    elem_id: R,
    elem_classes: I,
    elem_style: O,
    as_item: E,
    value: S,
    restProps: o
  });
  P(t, A, (c) => n(0, l = c));
  const q = be(), M = ge();
  P(t, M, (c) => n(15, r = c));
  const {
    selections: z
  } = qe(["selections"]);
  P(t, z, (c) => n(16, i = c));
  const se = Me();
  return t.$$set = (c) => {
    e = H(H({}, e), He(c)), n(24, o = U(e, s)), "gradio" in c && n(7, f = c.gradio), "props" in c && n(8, _ = c.props), "_internal" in c && n(9, b = c._internal), "as_item" in c && n(10, E = c.as_item), "value" in c && n(6, S = c.value), "visible" in c && n(11, w = c.visible), "elem_id" in c && n(12, R = c.elem_id), "elem_classes" in c && n(13, I = c.elem_classes), "elem_style" in c && n(14, O = c.elem_style), "$$scope" in c && n(19, d = c.$$scope);
  }, t.$$.update = () => {
    if (t.$$.dirty & /*props*/
    256 && p.update((c) => ({
      ...c,
      ..._
    })), t.$$.dirty & /*$mergedProps, $slotKey, $selectionsItems, $slots*/
    229377) {
      const c = ie(l);
      se(u, l._internal.index || 0, {
        props: {
          style: l.elem_style,
          className: Te(l.elem_classes, "ms-gr-antd-table-row-selection"),
          id: l.elem_id,
          selectedRowKeys: l.value,
          selections: l.props.selections || $(i),
          ...l.restProps,
          ...l.props,
          ...c,
          onChange: (re, ...oe) => {
            var D;
            n(6, S = re), (D = c == null ? void 0 : c.onChange) == null || D.call(c, ...oe);
          },
          onCell: N(l.props.onCell),
          getCheckboxProps: N(l.props.getCheckboxProps),
          renderCell: N(l.props.renderCell),
          columnTitle: l.props.columnTitle
        },
        slots: {
          ...r,
          columnTitle: {
            el: r.columnTitle,
            fallback: q
          },
          renderCell: {
            el: r.renderCell,
            fallback: q
          }
        }
      });
    }
    ne({
      gradio: f,
      props: a,
      _internal: b,
      visible: w,
      elem_id: R,
      elem_classes: I,
      elem_style: O,
      as_item: E,
      value: S,
      restProps: o
    });
  }, [l, p, K, A, M, z, S, f, _, b, E, w, R, I, O, r, i, u, a, d, m];
}
class st extends ze {
  constructor(e) {
    super(), Je(this, e, $e, Ze, Qe, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      value: 6,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), g();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), g();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), g();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), g();
  }
  get value() {
    return this.$$.ctx[6];
  }
  set value(e) {
    this.$$set({
      value: e
    }), g();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), g();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), g();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), g();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), g();
  }
}
export {
  st as default
};
