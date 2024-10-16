import { g as Pe, b as xe } from "./Index-fE0ano7C.js";
const b = window.ms_globals.React, we = window.ms_globals.React.forwardRef, Ee = window.ms_globals.React.useRef, Ie = window.ms_globals.React.useState, Se = window.ms_globals.React.useEffect, Ce = window.ms_globals.ReactDOM.createPortal;
function k() {
}
function Re(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function Oe(t, ...e) {
  if (t == null) {
    for (const r of e)
      r(void 0);
    return k;
  }
  const n = t.subscribe(...e);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function P(t) {
  let e;
  return Oe(t, (n) => e = n)(), e;
}
const x = [];
function h(t, e = k) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function o(i) {
    if (Re(t, i) && (t = i, n)) {
      const c = !x.length;
      for (const d of r)
        d[1](), x.push(d, t);
      if (c) {
        for (let d = 0; d < x.length; d += 2)
          x[d][0](x[d + 1]);
        x.length = 0;
      }
    }
  }
  function s(i) {
    o(i(t));
  }
  function l(i, c = k) {
    const d = [i, c];
    return r.add(d), r.size === 1 && (n = e(o, s) || k), i(t), () => {
      r.delete(d), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: l
  };
}
const {
  getContext: ae,
  setContext: F
} = window.__gradio__svelte__internal, ve = "$$ms-gr-slots-key";
function je() {
  const t = h({});
  return F(ve, t);
}
const ke = "$$ms-gr-render-slot-context-key";
function Ne() {
  const t = F(ke, h({}));
  return (e, n) => {
    t.update((r) => typeof n == "function" ? {
      ...r,
      [e]: n(r[e])
    } : {
      ...r,
      [e]: n
    });
  };
}
const Fe = "$$ms-gr-context-key";
function Le(t, e, n) {
  var m;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = me(), o = Ke({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  r && r.subscribe((f) => {
    o.slotKey.set(f);
  }), Me();
  const s = ae(Fe), l = ((m = P(s)) == null ? void 0 : m.as_item) || t.as_item, i = s ? l ? P(s)[l] : P(s) : {}, c = (f, a) => f ? Pe({
    ...f,
    ...a || {}
  }, e) : void 0, d = h({
    ...t,
    ...i,
    restProps: c(t.restProps, i),
    originalRestProps: t.restProps
  });
  return s ? (s.subscribe((f) => {
    const {
      as_item: a
    } = P(d);
    a && (f = f[a]), d.update((p) => ({
      ...p,
      ...f,
      restProps: c(p.restProps, f)
    }));
  }), [d, (f) => {
    const a = f.as_item ? P(s)[f.as_item] : P(s);
    return d.set({
      ...f,
      ...a,
      restProps: c(f.restProps, a),
      originalRestProps: f.restProps
    });
  }]) : [d, (f) => {
    d.set({
      ...f,
      restProps: c(f.restProps),
      originalRestProps: f.restProps
    });
  }];
}
const fe = "$$ms-gr-slot-key";
function Me() {
  F(fe, h(void 0));
}
function me() {
  return ae(fe);
}
const Ae = "$$ms-gr-component-slot-context-key";
function Ke({
  slot: t,
  index: e,
  subIndex: n
}) {
  return F(Ae, {
    slotKey: h(t),
    slotIndex: h(e),
    subSlotIndex: h(n)
  });
}
function qe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Be(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var pe = {
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
var Te = b, ze = Symbol.for("react.element"), De = Symbol.for("react.fragment"), We = Object.prototype.hasOwnProperty, Ge = Te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, He = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function _e(t, e, n) {
  var r, o = {}, s = null, l = null;
  n !== void 0 && (s = "" + n), e.key !== void 0 && (s = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (r in e) We.call(e, r) && !He.hasOwnProperty(r) && (o[r] = e[r]);
  if (t && t.defaultProps) for (r in e = t.defaultProps, e) o[r] === void 0 && (o[r] = e[r]);
  return {
    $$typeof: ze,
    type: t,
    key: s,
    ref: l,
    props: o,
    _owner: Ge.current
  };
}
L.Fragment = De;
L.jsx = _e;
L.jsxs = _e;
pe.exports = L;
var K = pe.exports;
const Ue = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ve(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const r = t[n];
    return typeof r == "number" && !Ue.includes(n) ? e[n] = r + "px" : e[n] = r, e;
  }, {}) : {};
}
function q(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(Ce(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: b.Children.toArray(t._reactElement.props.children).map((o) => {
        if (b.isValidElement(o) && o.props.__slot__) {
          const {
            portals: s,
            clonedElement: l
          } = q(o.props.el);
          return b.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...b.Children.toArray(o.props.children), ...s]
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
      useCapture: c
    }) => {
      n.addEventListener(i, l, c);
    });
  });
  const r = Array.from(t.childNodes);
  for (let o = 0; o < r.length; o++) {
    const s = r[o];
    if (s.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = q(s);
      e.push(...i), n.appendChild(l);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function Je(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const B = we(({
  slot: t,
  clone: e,
  className: n,
  style: r
}, o) => {
  const s = Ee(), [l, i] = Ie([]);
  return Se(() => {
    var f;
    if (!s.current || !t)
      return;
    let c = t;
    function d() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Je(o, a), n && a.classList.add(...n.split(" ")), r) {
        const p = Ve(r);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let m = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var y;
        const {
          portals: p,
          clonedElement: _
        } = q(t);
        c = _, i(p), c.style.display = "contents", d(), (y = s.current) == null || y.appendChild(c);
      };
      a(), m = new window.MutationObserver(() => {
        var p, _;
        (p = s.current) != null && p.contains(c) && ((_ = s.current) == null || _.removeChild(c)), a();
      }), m.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", d(), (f = s.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = s.current) != null && a.contains(c) && ((p = s.current) == null || p.removeChild(c)), m == null || m.disconnect();
    };
  }, [t, e, n, r, o]), b.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...l);
});
function T(t, e) {
  return t.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return n;
    const r = {
      ...n.props
    };
    let o = r;
    Object.keys(n.slots).forEach((l) => {
      if (!n.slots[l] || !(n.slots[l] instanceof Element) && !n.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((a, p) => {
        o[a] || (o[a] = {}), p !== i.length - 1 && (o = r[a]);
      });
      const c = n.slots[l];
      let d, m, f = !1;
      c instanceof Element ? d = c : (d = c.el, m = c.callback, f = c.clone || !1), o[i[i.length - 1]] = d ? m ? (...a) => (m(i[i.length - 1], a), /* @__PURE__ */ K.jsx(B, {
        slot: d,
        clone: f || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ K.jsx(B, {
        slot: d,
        clone: f || (e == null ? void 0 : e.clone)
      }) : o[i[i.length - 1]], o = r;
    });
    const s = "children";
    return n[s] && (r[s] = T(n[s], e)), r;
  });
}
function z(t, e) {
  return t ? /* @__PURE__ */ K.jsx(B, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function A({
  key: t,
  setSlotParams: e,
  slots: n
}, r) {
  return (...o) => (e(t, o), z(n[t], {
    clone: !0,
    ...r
  }));
}
var ge = {
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
      for (var s = "", l = 0; l < arguments.length; l++) {
        var i = arguments[l];
        i && (s = o(s, r(i)));
      }
      return s;
    }
    function r(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return n.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var l = "";
      for (var i in s)
        e.call(s, i) && s[i] && (l = o(l, i));
      return l;
    }
    function o(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (n.default = n, t.exports = n) : window.classNames = n;
  })();
})(ge);
var Ye = ge.exports;
const Qe = /* @__PURE__ */ Be(Ye), {
  getContext: Xe,
  setContext: Ze
} = window.__gradio__svelte__internal;
function he(t) {
  const e = `$$ms-gr-${t}-context-key`;
  function n(o = ["default"]) {
    const s = o.reduce((l, i) => (l[i] = h([]), l), {});
    return Ze(e, {
      itemsMap: s,
      allowedSlots: o
    }), s;
  }
  function r() {
    const {
      itemsMap: o,
      allowedSlots: s
    } = Xe(e);
    return function(l, i, c) {
      o && (l ? o[l].update((d) => {
        const m = [...d];
        return s.includes(l) ? m[i] = c : m[i] = void 0, m;
      }) : s.includes("default") && o.default.update((d) => {
        const m = [...d];
        return m[i] = c, m;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: $e,
  getSetItemFn: gt
} = he("menu"), {
  getItems: ht,
  getSetItemFn: et
} = he("breadcrumb"), {
  SvelteComponent: tt,
  assign: ie,
  check_outros: nt,
  component_subscribe: w,
  compute_rest_props: ce,
  create_slot: rt,
  detach: st,
  empty: ue,
  exclude_internal_props: ot,
  flush: g,
  get_all_dirty_from_scope: lt,
  get_slot_changes: it,
  group_outros: ct,
  init: ut,
  insert_hydration: dt,
  safe_not_equal: at,
  transition_in: N,
  transition_out: D,
  update_slot_base: ft
} = window.__gradio__svelte__internal;
function de(t) {
  let e;
  const n = (
    /*#slots*/
    t[22].default
  ), r = rt(
    n,
    t,
    /*$$scope*/
    t[21],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(o) {
      r && r.l(o);
    },
    m(o, s) {
      r && r.m(o, s), e = !0;
    },
    p(o, s) {
      r && r.p && (!e || s & /*$$scope*/
      2097152) && ft(
        r,
        n,
        o,
        /*$$scope*/
        o[21],
        e ? it(
          n,
          /*$$scope*/
          o[21],
          s,
          null
        ) : lt(
          /*$$scope*/
          o[21]
        ),
        null
      );
    },
    i(o) {
      e || (N(r, o), e = !0);
    },
    o(o) {
      D(r, o), e = !1;
    },
    d(o) {
      r && r.d(o);
    }
  };
}
function mt(t) {
  let e, n, r = (
    /*$mergedProps*/
    t[0].visible && de(t)
  );
  return {
    c() {
      r && r.c(), e = ue();
    },
    l(o) {
      r && r.l(o), e = ue();
    },
    m(o, s) {
      r && r.m(o, s), dt(o, e, s), n = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? r ? (r.p(o, s), s & /*$mergedProps*/
      1 && N(r, 1)) : (r = de(o), r.c(), N(r, 1), r.m(e.parentNode, e)) : r && (ct(), D(r, 1, 1, () => {
        r = null;
      }), nt());
    },
    i(o) {
      n || (N(r), n = !0);
    },
    o(o) {
      D(r), n = !1;
    },
    d(o) {
      o && st(e), r && r.d(o);
    }
  };
}
function pt(t, e, n) {
  const r = ["gradio", "props", "_internal", "title", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = ce(e, r), s, l, i, c, d, m, {
    $$slots: f = {},
    $$scope: a
  } = e, {
    gradio: p
  } = e, {
    props: _ = {}
  } = e;
  const y = h(_);
  w(t, y, (u) => n(20, m = u));
  let {
    _internal: I = {}
  } = e, {
    title: E = ""
  } = e, {
    as_item: S
  } = e, {
    visible: C = !0
  } = e, {
    elem_id: R = ""
  } = e, {
    elem_classes: O = []
  } = e, {
    elem_style: v = {}
  } = e;
  const W = me();
  w(t, W, (u) => n(17, i = u));
  const [G, be] = Le({
    gradio: p,
    props: m,
    _internal: I,
    visible: C,
    elem_id: R,
    elem_classes: O,
    elem_style: v,
    as_item: S,
    title: E,
    restProps: o
  });
  w(t, G, (u) => n(0, l = u));
  const H = je();
  w(t, H, (u) => n(16, s = u));
  const ye = et(), M = Ne(), {
    "menu.items": U,
    "dropdownProps.menu.items": V
  } = $e(["menu.items", "dropdownProps.menu.items"]);
  return w(t, U, (u) => n(19, d = u)), w(t, V, (u) => n(18, c = u)), t.$$set = (u) => {
    e = ie(ie({}, e), ot(u)), n(26, o = ce(e, r)), "gradio" in u && n(7, p = u.gradio), "props" in u && n(8, _ = u.props), "_internal" in u && n(9, I = u._internal), "title" in u && n(10, E = u.title), "as_item" in u && n(11, S = u.as_item), "visible" in u && n(12, C = u.visible), "elem_id" in u && n(13, R = u.elem_id), "elem_classes" in u && n(14, O = u.elem_classes), "elem_style" in u && n(15, v = u.elem_style), "$$scope" in u && n(21, a = u.$$scope);
  }, t.$$.update = () => {
    var u, J, Y, Q, X, Z, $, ee, te, ne, re;
    if (t.$$.dirty & /*props*/
    256 && y.update((j) => ({
      ...j,
      ..._
    })), be({
      gradio: p,
      props: m,
      _internal: I,
      visible: C,
      elem_id: R,
      elem_classes: O,
      elem_style: v,
      as_item: S,
      title: E,
      restProps: o
    }), t.$$.dirty & /*$mergedProps, $menuItems, $slots, $dropdownMenuItems, title, $slotKey*/
    984065) {
      const j = {
        ...l.props.menu || {},
        items: (u = l.props.menu) != null && u.items || d.length > 0 ? T(d) : void 0,
        expandIcon: A({
          setSlotParams: M,
          slots: s,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) || ((J = l.props.menu) == null ? void 0 : J.expandIcon),
        overflowedIndicator: z(s["menu.overflowedIndicator"]) || ((Y = l.props.menu) == null ? void 0 : Y.overflowedIndicator)
      }, se = {
        ...((Q = l.props.dropdownProps) == null ? void 0 : Q.menu) || {},
        items: (Z = (X = l.props.dropdownProps) == null ? void 0 : X.menu) != null && Z.items || c.length > 0 ? T(c) : void 0,
        expandIcon: A({
          setSlotParams: M,
          slots: s,
          key: "dropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((ee = ($ = l.props.dropdownProps) == null ? void 0 : $.menu) == null ? void 0 : ee.expandIcon),
        overflowedIndicator: z(s["dropdownProps.menu.overflowedIndicator"]) || ((ne = (te = l.props.dropdownProps) == null ? void 0 : te.menu) == null ? void 0 : ne.overflowedIndicator)
      }, oe = {
        ...l.props.dropdownProps || {},
        dropdownRender: s["dropdownProps.dropdownRender"] ? A({
          setSlotParams: M,
          slots: s,
          key: "dropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : qe((re = l.props.dropdownProps) == null ? void 0 : re.dropdownRender),
        menu: Object.values(se).filter(Boolean).length > 0 ? se : void 0
      }, le = {
        ...l,
        props: {
          ...l.restProps,
          ...l.props,
          title: l.props.title || E,
          menu: Object.values(j).filter(Boolean).length > 0 ? j : void 0,
          dropdownProps: Object.values(oe).filter(Boolean).length > 0 ? oe : void 0
        }
      };
      ye(i, l._internal.index || 0, {
        props: {
          style: l.elem_style,
          className: Qe(l.elem_classes, "ms-gr-antd-breadcrumb-item"),
          id: l.elem_id,
          ...le.props,
          ...xe(le)
        },
        slots: {
          title: s.title
        }
      });
    }
  }, [l, y, W, G, H, U, V, p, _, I, E, S, C, R, O, v, s, i, c, d, m, a, f];
}
class bt extends tt {
  constructor(e) {
    super(), ut(this, e, pt, mt, at, {
      gradio: 7,
      props: 8,
      _internal: 9,
      title: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
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
  get title() {
    return this.$$.ctx[10];
  }
  set title(e) {
    this.$$set({
      title: e
    }), g();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), g();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), g();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), g();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), g();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), g();
  }
}
export {
  bt as default
};
