import { g as G, w as d } from "./Index-DH7WuPkr.js";
const z = window.ms_globals.React, B = window.ms_globals.React.useMemo, h = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Input;
var T = {
  exports: {}
}, w = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var V = z, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) Q.call(t, l) && !Z.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: Y,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: X.current
  };
}
w.Fragment = H;
w.jsx = j;
w.jsxs = j;
T.exports = w;
var $ = T.exports;
const {
  SvelteComponent: ee,
  assign: I,
  binding_callbacks: k,
  check_outros: te,
  children: D,
  claim_element: F,
  claim_space: se,
  component_subscribe: R,
  compute_slots: oe,
  create_slot: ne,
  detach: a,
  element: L,
  empty: E,
  exclude_internal_props: O,
  get_all_dirty_from_scope: re,
  get_slot_changes: le,
  group_outros: ie,
  init: ce,
  insert_hydration: p,
  safe_not_equal: ae,
  set_custom_element_data: C,
  space: ue,
  transition_in: m,
  transition_out: g,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: de,
  onDestroy: pe,
  setContext: me
} = window.__gradio__svelte__internal;
function S(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ne(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = L("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = F(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = D(t);
      o && o.l(s), s.forEach(a), this.h();
    },
    h() {
      C(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && _e(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? le(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : re(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (m(o, e), r = !0);
    },
    o(e) {
      g(o, e), r = !1;
    },
    d(e) {
      e && a(t), o && o.d(e), n[9](null);
    }
  };
}
function we(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = L("react-portal-target"), r = ue(), e && e.c(), l = E(), this.h();
    },
    l(s) {
      t = F(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(a), r = se(s), e && e.l(s), l = E(), this.h();
    },
    h() {
      C(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      p(s, t, c), n[8](t), p(s, r, c), e && e.m(s, c), p(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && m(e, 1)) : (e = S(s), e.c(), m(e, 1), e.m(l.parentNode, l)) : e && (ie(), g(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(s) {
      o || (m(e), o = !0);
    },
    o(s) {
      g(e), o = !1;
    },
    d(s) {
      s && (a(t), a(r), a(l)), n[8](null), e && e.d(s);
    }
  };
}
function x(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function be(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = oe(e);
  let {
    svelteInit: u
  } = t;
  const v = d(x(t)), _ = d();
  R(n, _, (i) => r(0, l = i));
  const f = d();
  R(n, f, (i) => r(1, o = i));
  const y = [], A = de("$$ms-gr-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K
  } = G() || {}, M = u({
    parent: A,
    props: v,
    target: _,
    slot: f,
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K,
    onDestroy(i) {
      y.push(i);
    }
  });
  me("$$ms-gr-react-wrapper", M), fe(() => {
    v.set(x(t));
  }), pe(() => {
    y.forEach((i) => i());
  });
  function U(i) {
    k[i ? "unshift" : "push"](() => {
      l = i, _.set(l);
    });
  }
  function W(i) {
    k[i ? "unshift" : "push"](() => {
      o = i, f.set(o);
    });
  }
  return n.$$set = (i) => {
    r(17, t = I(I({}, t), O(i))), "svelteInit" in i && r(5, u = i.svelteInit), "$$scope" in i && r(6, s = i.$$scope);
  }, t = O(t), [l, o, _, f, c, u, s, e, U, W];
}
class ge extends ee {
  constructor(t) {
    super(), ce(this, t, be, we, ae, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, b = window.ms_globals.tree;
function ve(n) {
  function t(r) {
    const l = d(), o = new ge({
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
          }, c = e.parent ?? b;
          return c.nodes = [...c.nodes, s], P({
            createPortal: h,
            node: b
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== l), P({
              createPortal: h,
              node: b
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
function ye(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function he(n) {
  return B(() => ye(n), [n]);
}
const ke = ve(({
  formatter: n,
  onValueChange: t,
  onChange: r,
  elRef: l,
  ...o
}) => {
  const e = he(n);
  return /* @__PURE__ */ $.jsx(J.OTP, {
    ...o,
    ref: l,
    formatter: e,
    onChange: (s) => {
      r == null || r(s), t(s);
    }
  });
});
export {
  ke as InputOTP,
  ke as default
};
