import { g as Y, w as d } from "./Index-DIYYDuSF.js";
const B = window.ms_globals.React, G = window.ms_globals.React.useMemo, J = window.ms_globals.React.useEffect, v = window.ms_globals.ReactDOM.createPortal, I = window.ms_globals.antd.Form;
var T = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var H = B, Q = Symbol.for("react.element"), V = Symbol.for("react.fragment"), X = Object.prototype.hasOwnProperty, Z = H.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $ = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(o, t, r) {
  var l, n = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) X.call(t, l) && !$.hasOwnProperty(l) && (n[l] = t[l]);
  if (o && o.defaultProps) for (l in t = o.defaultProps, t) n[l] === void 0 && (n[l] = t[l]);
  return {
    $$typeof: Q,
    type: o,
    key: e,
    ref: s,
    props: n,
    _owner: Z.current
  };
}
b.Fragment = V;
b.jsx = j;
b.jsxs = j;
T.exports = b;
var ee = T.exports;
const {
  SvelteComponent: te,
  assign: k,
  binding_callbacks: E,
  check_outros: se,
  children: D,
  claim_element: L,
  claim_space: oe,
  component_subscribe: R,
  compute_slots: ne,
  create_slot: re,
  detach: u,
  element: C,
  empty: S,
  exclude_internal_props: x,
  get_all_dirty_from_scope: le,
  get_slot_changes: ce,
  group_outros: ie,
  init: ae,
  insert_hydration: m,
  safe_not_equal: ue,
  set_custom_element_data: A,
  space: _e,
  transition_in: p,
  transition_out: g,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: de,
  getContext: me,
  onDestroy: pe,
  setContext: be
} = window.__gradio__svelte__internal;
function F(o) {
  let t, r;
  const l = (
    /*#slots*/
    o[7].default
  ), n = re(
    l,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = C("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = D(t);
      n && n.l(s), s.forEach(u), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      m(e, t, s), n && n.m(t, null), o[9](t), r = !0;
    },
    p(e, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && fe(
        n,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ce(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : le(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (p(n, e), r = !0);
    },
    o(e) {
      g(n, e), r = !1;
    },
    d(e) {
      e && u(t), n && n.d(e), o[9](null);
    }
  };
}
function we(o) {
  let t, r, l, n, e = (
    /*$$slots*/
    o[4].default && F(o)
  );
  return {
    c() {
      t = C("react-portal-target"), r = _e(), e && e.c(), l = S(), this.h();
    },
    l(s) {
      t = L(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(u), r = oe(s), e && e.l(s), l = S(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      m(s, t, i), o[8](t), m(s, r, i), e && e.m(s, i), m(s, l, i), n = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && p(e, 1)) : (e = F(s), e.c(), p(e, 1), e.m(l.parentNode, l)) : e && (ie(), g(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      n || (p(e), n = !0);
    },
    o(s) {
      g(e), n = !1;
    },
    d(s) {
      s && (u(t), u(r), u(l)), o[8](null), e && e.d(s);
    }
  };
}
function O(o) {
  const {
    svelteInit: t,
    ...r
  } = o;
  return r;
}
function ge(o, t, r) {
  let l, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = ne(e);
  let {
    svelteInit: a
  } = t;
  const y = d(O(t)), _ = d();
  R(o, _, (c) => r(0, l = c));
  const f = d();
  R(o, f, (c) => r(1, n = c));
  const h = [], N = me("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: M
  } = Y() || {}, U = a({
    parent: N,
    props: y,
    target: _,
    slot: f,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: M,
    onDestroy(c) {
      h.push(c);
    }
  });
  be("$$ms-gr-react-wrapper", U), de(() => {
    y.set(O(t));
  }), pe(() => {
    h.forEach((c) => c());
  });
  function W(c) {
    E[c ? "unshift" : "push"](() => {
      l = c, _.set(l);
    });
  }
  function z(c) {
    E[c ? "unshift" : "push"](() => {
      n = c, f.set(n);
    });
  }
  return o.$$set = (c) => {
    r(17, t = k(k({}, t), x(c))), "svelteInit" in c && r(5, a = c.svelteInit), "$$scope" in c && r(6, s = c.$$scope);
  }, t = x(t), [l, n, _, f, i, a, s, e, W, z];
}
class ye extends te {
  constructor(t) {
    super(), ae(this, t, ge, we, ue, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function he(o) {
  function t(r) {
    const l = d(), n = new ye({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? w;
          return i.nodes = [...i.nodes, s], P({
            createPortal: v,
            node: w
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((a) => a.svelteInstance !== l), P({
              createPortal: v,
              node: w
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function ve(o) {
  try {
    return typeof o == "string" ? new Function(`return (...args) => (${o})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Ie(o) {
  return G(() => ve(o), [o]);
}
const Ee = he(({
  value: o,
  onValueChange: t,
  onValuesChange: r,
  feedbackIcons: l,
  ...n
}) => {
  const [e] = I.useForm(), s = Ie(l);
  return J(() => {
    e.setFieldsValue(o);
  }, [e, o]), /* @__PURE__ */ ee.jsx(I, {
    ...n,
    initialValues: o,
    form: e,
    feedbackIcons: s,
    onValuesChange: (i, a) => {
      t(a), r == null || r(i, a);
    }
  });
});
export {
  Ee as Form,
  Ee as default
};
