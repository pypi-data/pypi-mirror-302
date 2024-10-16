import { g as U, b as W } from "./Index-Db8gn6Cz.js";
function K() {
}
function X(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function Y(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return K;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function g(t) {
  let e;
  return Y(t, (o) => e = o)(), e;
}
const x = [];
function p(t, e = K) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function r(u) {
    if (X(t, u) && (t = u, o)) {
      const f = !x.length;
      for (const a of s)
        a[1](), x.push(a, t);
      if (f) {
        for (let a = 0; a < x.length; a += 2)
          x[a][0](x[a + 1]);
        x.length = 0;
      }
    }
  }
  function n(u) {
    r(u(t));
  }
  function i(u, f = K) {
    const a = [u, f];
    return s.add(a), s.size === 1 && (o = e(r, n) || K), u(t), () => {
      s.delete(a), s.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: r,
    update: n,
    subscribe: i
  };
}
const {
  getContext: B,
  setContext: F
} = window.__gradio__svelte__internal, Z = "$$ms-gr-slots-key";
function $() {
  const t = p({});
  return F(Z, t);
}
const ee = "$$ms-gr-render-slot-context-key";
function te() {
  const t = F(ee, p({}));
  return (e, o) => {
    t.update((s) => typeof o == "function" ? {
      ...s,
      [e]: o(s[e])
    } : {
      ...s,
      [e]: o
    });
  };
}
const se = "$$ms-gr-context-key";
function ne(t, e, o) {
  var d;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const s = H(), r = ie({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  s && s.subscribe((c) => {
    r.slotKey.set(c);
  }), oe();
  const n = B(se), i = ((d = g(n)) == null ? void 0 : d.as_item) || t.as_item, u = n ? i ? g(n)[i] : g(n) : {}, f = (c, m) => c ? U({
    ...c,
    ...m || {}
  }, e) : void 0, a = p({
    ...t,
    ...u,
    restProps: f(t.restProps, u),
    originalRestProps: t.restProps
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: m
    } = g(a);
    m && (c = c[m]), a.update((b) => ({
      ...b,
      ...c,
      restProps: f(b.restProps, c)
    }));
  }), [a, (c) => {
    const m = c.as_item ? g(n)[c.as_item] : g(n);
    return a.set({
      ...c,
      ...m,
      restProps: f(c.restProps, m),
      originalRestProps: c.restProps
    });
  }]) : [a, (c) => {
    a.set({
      ...c,
      restProps: f(c.restProps),
      originalRestProps: c.restProps
    });
  }];
}
const G = "$$ms-gr-slot-key";
function oe() {
  F(G, p(void 0));
}
function H() {
  return B(G);
}
const re = "$$ms-gr-component-slot-context-key";
function ie({
  slot: t,
  index: e,
  subIndex: o
}) {
  return F(re, {
    slotKey: p(t),
    slotIndex: p(e),
    subSlotIndex: p(o)
  });
}
function w(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function le(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var J = {
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
    function o() {
      for (var n = "", i = 0; i < arguments.length; i++) {
        var u = arguments[i];
        u && (n = r(n, s(u)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return o.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var i = "";
      for (var u in n)
        e.call(n, u) && n[u] && (i = r(i, u));
      return i;
    }
    function r(n, i) {
      return i ? n ? n + " " + i : n + i : n;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(J);
var ue = J.exports;
const ce = /* @__PURE__ */ le(ue), {
  getContext: ae,
  setContext: fe
} = window.__gradio__svelte__internal;
function de(t) {
  const e = `$$ms-gr-${t}-context-key`;
  function o(r = ["default"]) {
    const n = r.reduce((i, u) => (i[u] = p([]), i), {});
    return fe(e, {
      itemsMap: n,
      allowedSlots: r
    }), n;
  }
  function s() {
    const {
      itemsMap: r,
      allowedSlots: n
    } = ae(e);
    return function(i, u, f) {
      r && (i ? r[i].update((a) => {
        const d = [...a];
        return n.includes(i) ? d[u] = f : d[u] = void 0, d;
      }) : n.includes("default") && r.default.update((a) => {
        const d = [...a];
        return d[u] = f, d;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: s
  };
}
const {
  getItems: Fe,
  getSetItemFn: me
} = de("table-expandable"), {
  SvelteComponent: _e,
  assign: A,
  check_outros: pe,
  component_subscribe: E,
  compute_rest_props: T,
  create_slot: be,
  detach: ge,
  empty: V,
  exclude_internal_props: xe,
  flush: _,
  get_all_dirty_from_scope: ye,
  get_slot_changes: he,
  group_outros: Pe,
  init: Se,
  insert_hydration: Ce,
  safe_not_equal: Re,
  transition_in: k,
  transition_out: N,
  update_slot_base: Ie
} = window.__gradio__svelte__internal;
function D(t) {
  let e;
  const o = (
    /*#slots*/
    t[18].default
  ), s = be(
    o,
    t,
    /*$$scope*/
    t[17],
    null
  );
  return {
    c() {
      s && s.c();
    },
    l(r) {
      s && s.l(r);
    },
    m(r, n) {
      s && s.m(r, n), e = !0;
    },
    p(r, n) {
      s && s.p && (!e || n & /*$$scope*/
      131072) && Ie(
        s,
        o,
        r,
        /*$$scope*/
        r[17],
        e ? he(
          o,
          /*$$scope*/
          r[17],
          n,
          null
        ) : ye(
          /*$$scope*/
          r[17]
        ),
        null
      );
    },
    i(r) {
      e || (k(s, r), e = !0);
    },
    o(r) {
      N(s, r), e = !1;
    },
    d(r) {
      s && s.d(r);
    }
  };
}
function Ee(t) {
  let e, o, s = (
    /*$mergedProps*/
    t[0].visible && D(t)
  );
  return {
    c() {
      s && s.c(), e = V();
    },
    l(r) {
      s && s.l(r), e = V();
    },
    m(r, n) {
      s && s.m(r, n), Ce(r, e, n), o = !0;
    },
    p(r, [n]) {
      /*$mergedProps*/
      r[0].visible ? s ? (s.p(r, n), n & /*$mergedProps*/
      1 && k(s, 1)) : (s = D(r), s.c(), k(s, 1), s.m(e.parentNode, e)) : s && (Pe(), N(s, 1, 1, () => {
        s = null;
      }), pe());
    },
    i(r) {
      o || (k(s), o = !0);
    },
    o(r) {
      N(s), o = !1;
    },
    d(r) {
      r && ge(e), s && s.d(r);
    }
  };
}
function Ke(t, e, o) {
  const s = ["gradio", "props", "_internal", "as_item", "value", "visible", "elem_id", "elem_classes", "elem_style"];
  let r = T(e, s), n, i, u, f, {
    $$slots: a = {},
    $$scope: d
  } = e, {
    gradio: c
  } = e, {
    props: m = {}
  } = e;
  const b = p(m);
  E(t, b, (l) => o(16, f = l));
  let {
    _internal: h = {}
  } = e, {
    as_item: P
  } = e, {
    value: y
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: C = ""
  } = e, {
    elem_classes: R = []
  } = e, {
    elem_style: I = {}
  } = e;
  const j = H();
  E(t, j, (l) => o(15, u = l));
  const [q, L] = ne({
    gradio: c,
    props: f,
    _internal: h,
    visible: S,
    elem_id: C,
    elem_classes: R,
    elem_style: I,
    as_item: P,
    value: y,
    restProps: r
  });
  E(t, q, (l) => o(0, i = l));
  const O = $();
  E(t, O, (l) => o(14, n = l));
  const v = te(), Q = me();
  return t.$$set = (l) => {
    e = A(A({}, e), xe(l)), o(22, r = T(e, s)), "gradio" in l && o(6, c = l.gradio), "props" in l && o(7, m = l.props), "_internal" in l && o(8, h = l._internal), "as_item" in l && o(9, P = l.as_item), "value" in l && o(5, y = l.value), "visible" in l && o(10, S = l.visible), "elem_id" in l && o(11, C = l.elem_id), "elem_classes" in l && o(12, R = l.elem_classes), "elem_style" in l && o(13, I = l.elem_style), "$$scope" in l && o(17, d = l.$$scope);
  }, t.$$.update = () => {
    if (t.$$.dirty & /*props*/
    128 && b.update((l) => ({
      ...l,
      ...m
    })), t.$$.dirty & /*$mergedProps, $slotKey, $slots*/
    49153) {
      const l = W(i);
      Q(u, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: ce(i.elem_classes, "ms-gr-antd-table-expandable"),
          id: i.elem_id,
          expandedRowKeys: i.value,
          ...i.restProps,
          ...i.props,
          ...l,
          onExpandedRowsChange: (M) => {
            var z;
            (z = l == null ? void 0 : l.onExpandedRowsChange) == null || z.call(l, M), o(5, y = M);
          },
          expandedRowClassName: w(i.props.expandedRowClassName),
          expandedRowRender: w(i.props.expandedRowRender),
          rowExpandable: w(i.props.rowExpandable),
          expandIcon: i.props.expandIcon,
          columnTitle: i.props.columnTitle
        },
        slots: {
          ...n,
          expandIcon: {
            el: n.expandIcon,
            callback: v
          },
          expandedRowRender: {
            el: n.expandedRowRender,
            callback: v
          }
        }
      });
    }
    L({
      gradio: c,
      props: f,
      _internal: h,
      visible: S,
      elem_id: C,
      elem_classes: R,
      elem_style: I,
      as_item: P,
      value: y,
      restProps: r
    });
  }, [i, b, j, q, O, y, c, m, h, P, S, C, R, I, n, u, f, d, a];
}
class we extends _e {
  constructor(e) {
    super(), Se(this, e, Ke, Ee, Re, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      value: 5,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), _();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), _();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), _();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), _();
  }
  get value() {
    return this.$$.ctx[5];
  }
  set value(e) {
    this.$$set({
      value: e
    }), _();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), _();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), _();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), _();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), _();
  }
}
export {
  we as default
};
