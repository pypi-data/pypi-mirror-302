import { g as Ne, w as I, c as je } from "./Index-C2ZpzuC_.js";
const S = window.ms_globals.React, Me = window.ms_globals.React.forwardRef, Te = window.ms_globals.React.useRef, ge = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, Le = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, He = window.ms_globals.antdCssinjs.StyleProvider, Ke = window.ms_globals.antd.ConfigProvider, K = window.ms_globals.antd.theme, be = window.ms_globals.dayjs;
var Pe = {
  exports: {}
}, T = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ue = S, Be = Symbol.for("react.element"), Ge = Symbol.for("react.fragment"), We = Object.prototype.hasOwnProperty, Ze = Ue.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, qe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Se(e, t, r) {
  var n, i = {}, o = null, s = null;
  r !== void 0 && (o = "" + r), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) We.call(t, n) && !qe.hasOwnProperty(n) && (i[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) i[n] === void 0 && (i[n] = t[n]);
  return {
    $$typeof: Be,
    type: e,
    key: o,
    ref: s,
    props: i,
    _owner: Ze.current
  };
}
T.Fragment = Ge;
T.jsx = Se;
T.jsxs = Se;
Pe.exports = T;
var A = Pe.exports;
const {
  SvelteComponent: Je,
  assign: ne,
  binding_callbacks: oe,
  check_outros: Qe,
  children: Ee,
  claim_element: ve,
  claim_space: Xe,
  component_subscribe: ie,
  compute_slots: Ve,
  create_slot: $e,
  detach: k,
  element: ke,
  empty: se,
  exclude_internal_props: le,
  get_all_dirty_from_scope: et,
  get_slot_changes: tt,
  group_outros: rt,
  init: nt,
  insert_hydration: D,
  safe_not_equal: ot,
  set_custom_element_data: Ce,
  space: it,
  transition_in: Y,
  transition_out: Z,
  update_slot_base: st
} = window.__gradio__svelte__internal, {
  beforeUpdate: lt,
  getContext: ct,
  onDestroy: ut,
  setContext: ft
} = window.__gradio__svelte__internal;
function ce(e) {
  let t, r;
  const n = (
    /*#slots*/
    e[7].default
  ), i = $e(
    n,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ke("svelte-slot"), i && i.c(), this.h();
    },
    l(o) {
      t = ve(o, "SVELTE-SLOT", {
        class: !0
      });
      var s = Ee(t);
      i && i.l(s), s.forEach(k), this.h();
    },
    h() {
      Ce(t, "class", "svelte-1rt0kpf");
    },
    m(o, s) {
      D(o, t, s), i && i.m(t, null), e[9](t), r = !0;
    },
    p(o, s) {
      i && i.p && (!r || s & /*$$scope*/
      64) && st(
        i,
        n,
        o,
        /*$$scope*/
        o[6],
        r ? tt(
          n,
          /*$$scope*/
          o[6],
          s,
          null
        ) : et(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      r || (Y(i, o), r = !0);
    },
    o(o) {
      Z(i, o), r = !1;
    },
    d(o) {
      o && k(t), i && i.d(o), e[9](null);
    }
  };
}
function at(e) {
  let t, r, n, i, o = (
    /*$$slots*/
    e[4].default && ce(e)
  );
  return {
    c() {
      t = ke("react-portal-target"), r = it(), o && o.c(), n = se(), this.h();
    },
    l(s) {
      t = ve(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Ee(t).forEach(k), r = Xe(s), o && o.l(s), n = se(), this.h();
    },
    h() {
      Ce(t, "class", "svelte-1rt0kpf");
    },
    m(s, l) {
      D(s, t, l), e[8](t), D(s, r, l), o && o.m(s, l), D(s, n, l), i = !0;
    },
    p(s, [l]) {
      /*$$slots*/
      s[4].default ? o ? (o.p(s, l), l & /*$$slots*/
      16 && Y(o, 1)) : (o = ce(s), o.c(), Y(o, 1), o.m(n.parentNode, n)) : o && (rt(), Z(o, 1, 1, () => {
        o = null;
      }), Qe());
    },
    i(s) {
      i || (Y(o), i = !0);
    },
    o(s) {
      Z(o), i = !1;
    },
    d(s) {
      s && (k(t), k(r), k(n)), e[8](null), o && o.d(s);
    }
  };
}
function ue(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function _t(e, t, r) {
  let n, i, {
    $$slots: o = {},
    $$scope: s
  } = t;
  const l = Ve(o);
  let {
    svelteInit: c
  } = t;
  const h = I(ue(t)), a = I();
  ie(e, a, (f) => r(0, n = f));
  const g = I();
  ie(e, g, (f) => r(1, i = f));
  const u = [], _ = ct("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: b
  } = Ne() || {}, Ye = c({
    parent: _,
    props: h,
    target: a,
    slot: g,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: b,
    onDestroy(f) {
      u.push(f);
    }
  });
  ft("$$ms-gr-react-wrapper", Ye), lt(() => {
    h.set(ue(t));
  }), ut(() => {
    u.forEach((f) => f());
  });
  function xe(f) {
    oe[f ? "unshift" : "push"](() => {
      n = f, a.set(n);
    });
  }
  function Fe(f) {
    oe[f ? "unshift" : "push"](() => {
      i = f, g.set(i);
    });
  }
  return e.$$set = (f) => {
    r(17, t = ne(ne({}, t), le(f))), "svelteInit" in f && r(5, c = f.svelteInit), "$$scope" in f && r(6, s = f.$$scope);
  }, t = le(t), [n, i, a, g, l, c, s, o, xe, Fe];
}
class dt extends Je {
  constructor(t) {
    super(), nt(this, t, _t, at, ot, {
      svelteInit: 5
    });
  }
}
const fe = window.ms_globals.rerender, U = window.ms_globals.tree;
function mt(e) {
  function t(r) {
    const n = I(), i = new dt({
      ...r,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            slotKey: o.slotKey,
            nodes: []
          }, l = o.parent ?? U;
          return l.nodes = [...l.nodes, s], fe({
            createPortal: W,
            node: U
          }), o.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== n), fe({
              createPortal: W,
              node: U
            });
          }), s;
        },
        ...r.props
      }
    });
    return n.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const ht = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function pt(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return typeof n == "number" && !ht.includes(r) ? t[r] = n + "px" : t[r] = n, t;
  }, {}) : {};
}
function q(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(W(S.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: S.Children.toArray(e._reactElement.props.children).map((i) => {
        if (S.isValidElement(i) && i.props.__slot__) {
          const {
            portals: o,
            clonedElement: s
          } = q(i.props.el);
          return S.cloneElement(i, {
            ...i.props,
            el: s,
            children: [...S.Children.toArray(i.props.children), ...o]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((i) => {
    e.getEventListeners(i).forEach(({
      listener: s,
      type: l,
      useCapture: c
    }) => {
      r.addEventListener(l, s, c);
    });
  });
  const n = Array.from(e.childNodes);
  for (let i = 0; i < n.length; i++) {
    const o = n[i];
    if (o.nodeType === 1) {
      const {
        clonedElement: s,
        portals: l
      } = q(o);
      t.push(...l), r.appendChild(s);
    } else o.nodeType === 3 && r.appendChild(o.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function yt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const gt = Me(({
  slot: e,
  clone: t,
  className: r,
  style: n
}, i) => {
  const o = Te(), [s, l] = ge([]);
  return we(() => {
    var g;
    if (!o.current || !e)
      return;
    let c = e;
    function h() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), yt(i, u), r && u.classList.add(...r.split(" ")), n) {
        const _ = pt(n);
        Object.keys(_).forEach((p) => {
          u.style[p] = _[p];
        });
      }
    }
    let a = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w;
        const {
          portals: _,
          clonedElement: p
        } = q(e);
        c = p, l(_), c.style.display = "contents", h(), (w = o.current) == null || w.appendChild(c);
      };
      u(), a = new window.MutationObserver(() => {
        var _, p;
        (_ = o.current) != null && _.contains(c) && ((p = o.current) == null || p.removeChild(c)), u();
      }), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", h(), (g = o.current) == null || g.appendChild(c);
    return () => {
      var u, _;
      c.style.display = "", (u = o.current) != null && u.contains(c) && ((_ = o.current) == null || _.removeChild(c)), a == null || a.disconnect();
    };
  }, [e, t, r, n, i]), S.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...s);
});
function wt(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function ae(e) {
  return Le(() => wt(e), [e]);
}
var ze = Symbol.for("immer-nothing"), _e = Symbol.for("immer-draftable"), d = Symbol.for("immer-state");
function y(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var C = Object.getPrototypeOf;
function z(e) {
  return !!e && !!e[d];
}
function E(e) {
  var t;
  return e ? Re(e) || Array.isArray(e) || !!e[_e] || !!((t = e.constructor) != null && t[_e]) || N(e) || j(e) : !1;
}
var bt = Object.prototype.constructor.toString();
function Re(e) {
  if (!e || typeof e != "object") return !1;
  const t = C(e);
  if (t === null)
    return !0;
  const r = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return r === Object ? !0 : typeof r == "function" && Function.toString.call(r) === bt;
}
function x(e, t) {
  L(e) === 0 ? Reflect.ownKeys(e).forEach((r) => {
    t(r, e[r], e);
  }) : e.forEach((r, n) => t(n, r, e));
}
function L(e) {
  const t = e[d];
  return t ? t.type_ : Array.isArray(e) ? 1 : N(e) ? 2 : j(e) ? 3 : 0;
}
function J(e, t) {
  return L(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function Oe(e, t, r) {
  const n = L(e);
  n === 2 ? e.set(t, r) : n === 3 ? e.add(r) : e[t] = r;
}
function Pt(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function N(e) {
  return e instanceof Map;
}
function j(e) {
  return e instanceof Set;
}
function P(e) {
  return e.copy_ || e.base_;
}
function Q(e, t) {
  if (N(e))
    return new Map(e);
  if (j(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const r = Re(e);
  if (t === !0 || t === "class_only" && !r) {
    const n = Object.getOwnPropertyDescriptors(e);
    delete n[d];
    let i = Reflect.ownKeys(n);
    for (let o = 0; o < i.length; o++) {
      const s = i[o], l = n[s];
      l.writable === !1 && (l.writable = !0, l.configurable = !0), (l.get || l.set) && (n[s] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: l.enumerable,
        value: e[s]
      });
    }
    return Object.create(C(e), n);
  } else {
    const n = C(e);
    if (n !== null && r)
      return {
        ...e
      };
    const i = Object.create(n);
    return Object.assign(i, e);
  }
}
function te(e, t = !1) {
  return H(e) || z(e) || !E(e) || (L(e) > 1 && (e.set = e.add = e.clear = e.delete = St), Object.freeze(e), t && Object.entries(e).forEach(([r, n]) => te(n, !0))), e;
}
function St() {
  y(2);
}
function H(e) {
  return Object.isFrozen(e);
}
var Et = {};
function v(e) {
  const t = Et[e];
  return t || y(0, e), t;
}
var R;
function Ie() {
  return R;
}
function vt(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function de(e, t) {
  t && (v("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function X(e) {
  V(e), e.drafts_.forEach(kt), e.drafts_ = null;
}
function V(e) {
  e === R && (R = e.parent_);
}
function me(e) {
  return R = vt(R, e);
}
function kt(e) {
  const t = e[d];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function he(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const r = t.drafts_[0];
  return e !== void 0 && e !== r ? (r[d].modified_ && (X(t), y(4)), E(e) && (e = F(t, e), t.parent_ || M(t, e)), t.patches_ && v("Patches").generateReplacementPatches_(r[d].base_, e, t.patches_, t.inversePatches_)) : e = F(t, r, []), X(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== ze ? e : void 0;
}
function F(e, t, r) {
  if (H(t)) return t;
  const n = t[d];
  if (!n)
    return x(t, (i, o) => pe(e, n, t, i, o, r)), t;
  if (n.scope_ !== e) return t;
  if (!n.modified_)
    return M(e, n.base_, !0), n.base_;
  if (!n.finalized_) {
    n.finalized_ = !0, n.scope_.unfinalizedDrafts_--;
    const i = n.copy_;
    let o = i, s = !1;
    n.type_ === 3 && (o = new Set(i), i.clear(), s = !0), x(o, (l, c) => pe(e, n, i, l, c, r, s)), M(e, i, !1), r && e.patches_ && v("Patches").generatePatches_(n, r, e.patches_, e.inversePatches_);
  }
  return n.copy_;
}
function pe(e, t, r, n, i, o, s) {
  if (z(i)) {
    const l = o && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !J(t.assigned_, n) ? o.concat(n) : void 0, c = F(e, i, l);
    if (Oe(r, n, c), z(c))
      e.canAutoFreeze_ = !1;
    else return;
  } else s && r.add(i);
  if (E(i) && !H(i)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    F(e, i), (!t || !t.scope_.parent_) && typeof n != "symbol" && Object.prototype.propertyIsEnumerable.call(r, n) && M(e, i);
  }
}
function M(e, t, r = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && te(t, r);
}
function Ct(e, t) {
  const r = Array.isArray(e), n = {
    type_: r ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : Ie(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let i = n, o = re;
  r && (i = [n], o = O);
  const {
    revoke: s,
    proxy: l
  } = Proxy.revocable(i, o);
  return n.draft_ = l, n.revoke_ = s, l;
}
var re = {
  get(e, t) {
    if (t === d) return e;
    const r = P(e);
    if (!J(r, t))
      return zt(e, r, t);
    const n = r[t];
    return e.finalized_ || !E(n) ? n : n === B(e.base_, t) ? (G(e), e.copy_[t] = ee(n, e)) : n;
  },
  has(e, t) {
    return t in P(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(P(e));
  },
  set(e, t, r) {
    const n = Ae(P(e), t);
    if (n != null && n.set)
      return n.set.call(e.draft_, r), !0;
    if (!e.modified_) {
      const i = B(P(e), t), o = i == null ? void 0 : i[d];
      if (o && o.base_ === r)
        return e.copy_[t] = r, e.assigned_[t] = !1, !0;
      if (Pt(r, i) && (r !== void 0 || J(e.base_, t))) return !0;
      G(e), $(e);
    }
    return e.copy_[t] === r && // special case: handle new props with value 'undefined'
    (r !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(r) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = r, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return B(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, G(e), $(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const r = P(e), n = Reflect.getOwnPropertyDescriptor(r, t);
    return n && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: n.enumerable,
      value: r[t]
    };
  },
  defineProperty() {
    y(11);
  },
  getPrototypeOf(e) {
    return C(e.base_);
  },
  setPrototypeOf() {
    y(12);
  }
}, O = {};
x(re, (e, t) => {
  O[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
O.deleteProperty = function(e, t) {
  return O.set.call(this, e, t, void 0);
};
O.set = function(e, t, r) {
  return re.set.call(this, e[0], t, r, e[0]);
};
function B(e, t) {
  const r = e[d];
  return (r ? P(r) : e)[t];
}
function zt(e, t, r) {
  var i;
  const n = Ae(t, r);
  return n ? "value" in n ? n.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (i = n.get) == null ? void 0 : i.call(e.draft_)
  ) : void 0;
}
function Ae(e, t) {
  if (!(t in e)) return;
  let r = C(e);
  for (; r; ) {
    const n = Object.getOwnPropertyDescriptor(r, t);
    if (n) return n;
    r = C(r);
  }
}
function $(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && $(e.parent_));
}
function G(e) {
  e.copy_ || (e.copy_ = Q(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var Rt = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, r, n) => {
      if (typeof t == "function" && typeof r != "function") {
        const o = r;
        r = t;
        const s = this;
        return function(c = o, ...h) {
          return s.produce(c, (a) => r.call(this, a, ...h));
        };
      }
      typeof r != "function" && y(6), n !== void 0 && typeof n != "function" && y(7);
      let i;
      if (E(t)) {
        const o = me(this), s = ee(t, void 0);
        let l = !0;
        try {
          i = r(s), l = !1;
        } finally {
          l ? X(o) : V(o);
        }
        return de(o, n), he(i, o);
      } else if (!t || typeof t != "object") {
        if (i = r(t), i === void 0 && (i = t), i === ze && (i = void 0), this.autoFreeze_ && te(i, !0), n) {
          const o = [], s = [];
          v("Patches").generateReplacementPatches_(t, i, o, s), n(o, s);
        }
        return i;
      } else y(1, t);
    }, this.produceWithPatches = (t, r) => {
      if (typeof t == "function")
        return (s, ...l) => this.produceWithPatches(s, (c) => t(c, ...l));
      let n, i;
      return [this.produce(t, r, (s, l) => {
        n = s, i = l;
      }), n, i];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    E(e) || y(8), z(e) && (e = Ot(e));
    const t = me(this), r = ee(e, void 0);
    return r[d].isManual_ = !0, V(t), r;
  }
  finishDraft(e, t) {
    const r = e && e[d];
    (!r || !r.isManual_) && y(9);
    const {
      scope_: n
    } = r;
    return de(n, t), he(void 0, n);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let r;
    for (r = t.length - 1; r >= 0; r--) {
      const i = t[r];
      if (i.path.length === 0 && i.op === "replace") {
        e = i.value;
        break;
      }
    }
    r > -1 && (t = t.slice(r + 1));
    const n = v("Patches").applyPatches_;
    return z(e) ? n(e, t) : this.produce(e, (i) => n(i, t));
  }
};
function ee(e, t) {
  const r = N(e) ? v("MapSet").proxyMap_(e, t) : j(e) ? v("MapSet").proxySet_(e, t) : Ct(e, t);
  return (t ? t.scope_ : Ie()).drafts_.push(r), r;
}
function Ot(e) {
  return z(e) || y(10, e), De(e);
}
function De(e) {
  if (!E(e) || H(e)) return e;
  const t = e[d];
  let r;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, r = Q(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    r = Q(e, !0);
  return x(r, (n, i) => {
    Oe(r, n, De(i));
  }), t && (t.finalized_ = !1), r;
}
var m = new Rt(), It = m.produce;
m.produceWithPatches.bind(m);
m.setAutoFreeze.bind(m);
m.setUseStrictShallowCopy.bind(m);
m.applyPatches.bind(m);
m.createDraft.bind(m);
m.finishDraft.bind(m);
var At = {
  exports: {}
};
(function(e, t) {
  (function(r, n) {
    e.exports = n(be);
  })(je, function(r) {
    function n(s) {
      return s && typeof s == "object" && "default" in s ? s : {
        default: s
      };
    }
    var i = n(r), o = {
      name: "zh-cn",
      weekdays: "星期日_星期一_星期二_星期三_星期四_星期五_星期六".split("_"),
      weekdaysShort: "周日_周一_周二_周三_周四_周五_周六".split("_"),
      weekdaysMin: "日_一_二_三_四_五_六".split("_"),
      months: "一月_二月_三月_四月_五月_六月_七月_八月_九月_十月_十一月_十二月".split("_"),
      monthsShort: "1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),
      ordinal: function(s, l) {
        return l === "W" ? s + "周" : s + "日";
      },
      weekStart: 1,
      yearStart: 4,
      formats: {
        LT: "HH:mm",
        LTS: "HH:mm:ss",
        L: "YYYY/MM/DD",
        LL: "YYYY年M月D日",
        LLL: "YYYY年M月D日Ah点mm分",
        LLLL: "YYYY年M月D日ddddAh点mm分",
        l: "YYYY/M/D",
        ll: "YYYY年M月D日",
        lll: "YYYY年M月D日 HH:mm",
        llll: "YYYY年M月D日dddd HH:mm"
      },
      relativeTime: {
        future: "%s内",
        past: "%s前",
        s: "几秒",
        m: "1 分钟",
        mm: "%d 分钟",
        h: "1 小时",
        hh: "%d 小时",
        d: "1 天",
        dd: "%d 天",
        M: "1 个月",
        MM: "%d 个月",
        y: "1 年",
        yy: "%d 年"
      },
      meridiem: function(s, l) {
        var c = 100 * s + l;
        return c < 600 ? "凌晨" : c < 900 ? "早上" : c < 1100 ? "上午" : c < 1300 ? "中午" : c < 1800 ? "下午" : "晚上";
      }
    };
    return i.default.locale(o, null, !0), o;
  });
})(At);
const ye = {
  ar_EG: () => import("./ar_EG-D553ypS1.js").then((e) => e.a),
  az_AZ: () => import("./az_AZ-B1qxblCr.js").then((e) => e.a),
  bg_BG: () => import("./bg_BG-BfYYp8wb.js").then((e) => e.b),
  bn_BD: () => import("./bn_BD-DqLTTW4J.js").then((e) => e.b),
  by_BY: () => import("./by_BY-B3PuVLlL.js").then((e) => e.b),
  ca_ES: () => import("./ca_ES-DRxZD9CU.js").then((e) => e.c),
  cs_CZ: () => import("./cs_CZ-BiLAYPOh.js").then((e) => e.c),
  da_DK: () => import("./da_DK-CcQZAX18.js").then((e) => e.d),
  de_DE: () => import("./de_DE-D68mBChM.js").then((e) => e.d),
  el_GR: () => import("./el_GR-C2H2J8vV.js").then((e) => e.e),
  en_GB: () => import("./en_GB-C0vvEUve.js").then((e) => e.e),
  en_US: () => import("./en_US-D8Ozdcyy.js").then((e) => e.e),
  es_ES: () => import("./es_ES-D7lqiwht.js").then((e) => e.e),
  et_EE: () => import("./et_EE-D5RHxNyg.js").then((e) => e.e),
  eu_ES: () => import("./eu_ES-BzfG6jGp.js").then((e) => e.e),
  fa_IR: () => import("./fa_IR-DcjdyuIY.js").then((e) => e.f),
  fi_FI: () => import("./fi_FI-CRGkNU4R.js").then((e) => e.f),
  fr_BE: () => import("./fr_BE-DqRBAWV2.js").then((e) => e.f),
  fr_CA: () => import("./fr_CA-Cg0imjm5.js").then((e) => e.f),
  fr_FR: () => import("./fr_FR-BjdgMRoj.js").then((e) => e.f),
  ga_IE: () => import("./ga_IE-KbG7mHMO.js").then((e) => e.g),
  gl_ES: () => import("./gl_ES-x9M42qWa.js").then((e) => e.g),
  he_IL: () => import("./he_IL-C8K5u0Sf.js").then((e) => e.h),
  hi_IN: () => import("./hi_IN-DdgmNLkK.js").then((e) => e.h),
  hr_HR: () => import("./hr_HR-C_LvhpNs.js").then((e) => e.h),
  hu_HU: () => import("./hu_HU-BClngNPS.js").then((e) => e.h),
  hy_AM: () => import("./hy_AM-BLf5ejhZ.js").then((e) => e.h),
  id_ID: () => import("./id_ID-C65TSkTS.js").then((e) => e.i),
  is_IS: () => import("./is_IS-DYIwfED1.js").then((e) => e.i),
  it_IT: () => import("./it_IT-Div9Rv9f.js").then((e) => e.i),
  ja_JP: () => import("./ja_JP-DBTSMoYB.js").then((e) => e.j),
  ka_GE: () => import("./ka_GE-ChoH7mDd.js").then((e) => e.k),
  kk_KZ: () => import("./kk_KZ-kCcfFV21.js").then((e) => e.k),
  km_KH: () => import("./km_KH-B0ddKCVi.js").then((e) => e.k),
  kmr_IQ: () => import("./kmr_IQ-BRpb5fOW.js").then((e) => e.k),
  kn_IN: () => import("./kn_IN-CgK2yDut.js").then((e) => e.k),
  ko_KR: () => import("./ko_KR-DZNmxX8t.js").then((e) => e.k),
  ku_IQ: () => import("./ku_IQ-BabE_YF9.js").then((e) => e.k),
  lt_LT: () => import("./lt_LT-PXsV3AKK.js").then((e) => e.l),
  lv_LV: () => import("./lv_LV-AvAZk3v6.js").then((e) => e.l),
  mk_MK: () => import("./mk_MK-BDcQTaEC.js").then((e) => e.m),
  ml_IN: () => import("./ml_IN-BMdB1lVa.js").then((e) => e.m),
  mn_MN: () => import("./mn_MN-BXXY_xWn.js").then((e) => e.m),
  ms_MY: () => import("./ms_MY-r8tOooK9.js").then((e) => e.m),
  my_MM: () => import("./my_MM-M0AdCBi1.js").then((e) => e.m),
  nb_NO: () => import("./nb_NO-DvUIh2WA.js").then((e) => e.n),
  ne_NP: () => import("./ne_NP-wQlylnh5.js").then((e) => e.n),
  nl_BE: () => import("./nl_BE-DhUw9IxE.js").then((e) => e.n),
  nl_NL: () => import("./nl_NL-DTrGx357.js").then((e) => e.n),
  pl_PL: () => import("./pl_PL-67n4X6yD.js").then((e) => e.p),
  pt_BR: () => import("./pt_BR-BpJIXkHY.js").then((e) => e.p),
  pt_PT: () => import("./pt_PT-BbYjX4MZ.js").then((e) => e.p),
  ro_RO: () => import("./ro_RO-BI2POAq1.js").then((e) => e.r),
  ru_RU: () => import("./ru_RU-dmLY8fh_.js").then((e) => e.r),
  si_LK: () => import("./si_LK-CBS1pNUv.js").then((e) => e.s),
  sk_SK: () => import("./sk_SK-DNnxpe8x.js").then((e) => e.s),
  sl_SI: () => import("./sl_SI-BfmwtKUU.js").then((e) => e.s),
  sr_RS: () => import("./sr_RS-2AOudpbq.js").then((e) => e.s),
  sv_SE: () => import("./sv_SE-DAbws2WA.js").then((e) => e.s),
  ta_IN: () => import("./ta_IN-DG6KnDfb.js").then((e) => e.t),
  th_TH: () => import("./th_TH-BhyKMqXx.js").then((e) => e.t),
  tk_TK: () => import("./tk_TK-DnuxZbHW.js").then((e) => e.t),
  tr_TR: () => import("./tr_TR-CO97rE40.js").then((e) => e.t),
  uk_UA: () => import("./uk_UA-BF7OQR9d.js").then((e) => e.u),
  ur_PK: () => import("./ur_PK-CNsqLJtc.js").then((e) => e.u),
  uz_UZ: () => import("./uz_UZ-slEQ8BcT.js").then((e) => e.u),
  vi_VN: () => import("./vi_VN-BGcrc0Bo.js").then((e) => e.v),
  zh_CN: () => import("./zh_CN-Co0mJyuD.js").then((e) => e.z),
  zh_HK: () => import("./zh_HK-BvMKCsKy.js").then((e) => e.z),
  zh_TW: () => import("./zh_TW-IISFKayy.js").then((e) => e.z)
}, Dt = (e, t) => It(e, (r) => {
  Object.keys(t).forEach((n) => {
    const i = n.split(".");
    let o = r;
    for (let s = 0; s < i.length - 1; s++) {
      const l = i[s];
      o[l] || (o[l] = {}), o = o[l];
    }
    o[i[i.length - 1]] = /* @__PURE__ */ A.jsx(gt, {
      slot: t[n],
      clone: !0
    });
  });
}), xt = mt(({
  slots: e,
  themeMode: t,
  id: r,
  className: n,
  style: i,
  locale: o,
  getTargetContainer: s,
  getPopupContainer: l,
  children: c,
  ...h
}) => {
  var w;
  const [a, g] = ge(), u = {
    dark: t === "dark",
    ...((w = h.theme) == null ? void 0 : w.algorithm) || {}
  }, _ = ae(l), p = ae(s);
  return we(() => {
    o && ye[o] && ye[o]().then((b) => {
      g(b.default), o === "zh_CN" && be.locale("zh-cn");
    });
  }, [o]), /* @__PURE__ */ A.jsx("div", {
    id: r,
    className: n,
    style: i,
    children: /* @__PURE__ */ A.jsx(He, {
      hashPriority: "high",
      container: document.body,
      children: /* @__PURE__ */ A.jsx(Ke, {
        prefixCls: "ms-gr-ant",
        ...Dt(h, e),
        locale: a,
        getPopupContainer: _,
        getTargetContainer: p,
        theme: {
          cssVar: !0,
          ...h.theme,
          algorithm: Object.keys(u).map((b) => {
            switch (b) {
              case "dark":
                return u[b] ? K.darkAlgorithm : K.defaultAlgorithm;
              case "compact":
                return u[b] ? K.compactAlgorithm : null;
              default:
                return null;
            }
          }).filter(Boolean)
        },
        children: c
      })
    })
  });
});
export {
  xt as ConfigProvider,
  xt as default
};
