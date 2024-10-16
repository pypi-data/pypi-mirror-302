var Tt = typeof global == "object" && global && global.Object === Object && global, an = typeof self == "object" && self && self.Object === Object && self, E = Tt || an || Function("return this")(), A = E.Symbol, Pt = Object.prototype, sn = Pt.hasOwnProperty, un = Pt.toString, Y = A ? A.toStringTag : void 0;
function ln(e) {
  var t = sn.call(e, Y), n = e[Y];
  try {
    e[Y] = void 0;
    var r = !0;
  } catch {
  }
  var i = un.call(e);
  return r && (t ? e[Y] = n : delete e[Y]), i;
}
var fn = Object.prototype, cn = fn.toString;
function pn(e) {
  return cn.call(e);
}
var gn = "[object Null]", dn = "[object Undefined]", ze = A ? A.toStringTag : void 0;
function N(e) {
  return e == null ? e === void 0 ? dn : gn : ze && ze in Object(e) ? ln(e) : pn(e);
}
function x(e) {
  return e != null && typeof e == "object";
}
var _n = "[object Symbol]";
function Ae(e) {
  return typeof e == "symbol" || x(e) && N(e) == _n;
}
function At(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = Array(r); ++n < r; )
    i[n] = t(e[n], n, e);
  return i;
}
var w = Array.isArray, hn = 1 / 0, He = A ? A.prototype : void 0, qe = He ? He.toString : void 0;
function Ot(e) {
  if (typeof e == "string")
    return e;
  if (w(e))
    return At(e, Ot) + "";
  if (Ae(e))
    return qe ? qe.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -hn ? "-0" : t;
}
function q(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function wt(e) {
  return e;
}
var bn = "[object AsyncFunction]", mn = "[object Function]", yn = "[object GeneratorFunction]", vn = "[object Proxy]";
function $t(e) {
  if (!q(e))
    return !1;
  var t = N(e);
  return t == mn || t == yn || t == bn || t == vn;
}
var ge = E["__core-js_shared__"], Ye = function() {
  var e = /[^.]+$/.exec(ge && ge.keys && ge.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function Tn(e) {
  return !!Ye && Ye in e;
}
var Pn = Function.prototype, An = Pn.toString;
function D(e) {
  if (e != null) {
    try {
      return An.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var On = /[\\^$.*+?()[\]{}|]/g, wn = /^\[object .+?Constructor\]$/, $n = Function.prototype, Sn = Object.prototype, Cn = $n.toString, En = Sn.hasOwnProperty, jn = RegExp("^" + Cn.call(En).replace(On, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function In(e) {
  if (!q(e) || Tn(e))
    return !1;
  var t = $t(e) ? jn : wn;
  return t.test(D(e));
}
function xn(e, t) {
  return e == null ? void 0 : e[t];
}
function U(e, t) {
  var n = xn(e, t);
  return In(n) ? n : void 0;
}
var be = U(E, "WeakMap"), Xe = Object.create, Mn = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!q(t))
      return {};
    if (Xe)
      return Xe(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function Fn(e, t, n) {
  switch (n.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, n[0]);
    case 2:
      return e.call(t, n[0], n[1]);
    case 3:
      return e.call(t, n[0], n[1], n[2]);
  }
  return e.apply(t, n);
}
function Rn(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Ln = 800, Nn = 16, Dn = Date.now;
function Un(e) {
  var t = 0, n = 0;
  return function() {
    var r = Dn(), i = Nn - (r - n);
    if (n = r, i > 0) {
      if (++t >= Ln)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Gn(e) {
  return function() {
    return e;
  };
}
var oe = function() {
  try {
    var e = U(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), Kn = oe ? function(e, t) {
  return oe(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Gn(t),
    writable: !0
  });
} : wt, Bn = Un(Kn);
function zn(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var Hn = 9007199254740991, qn = /^(?:0|[1-9]\d*)$/;
function St(e, t) {
  var n = typeof e;
  return t = t ?? Hn, !!t && (n == "number" || n != "symbol" && qn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function Oe(e, t, n) {
  t == "__proto__" && oe ? oe(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function we(e, t) {
  return e === t || e !== e && t !== t;
}
var Yn = Object.prototype, Xn = Yn.hasOwnProperty;
function Ct(e, t, n) {
  var r = e[t];
  (!(Xn.call(e, t) && we(r, n)) || n === void 0 && !(t in e)) && Oe(e, t, n);
}
function Q(e, t, n, r) {
  var i = !n;
  n || (n = {});
  for (var o = -1, a = t.length; ++o < a; ) {
    var s = t[o], l = void 0;
    l === void 0 && (l = e[s]), i ? Oe(n, s, l) : Ct(n, s, l);
  }
  return n;
}
var Ze = Math.max;
function Zn(e, t, n) {
  return t = Ze(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, i = -1, o = Ze(r.length - t, 0), a = Array(o); ++i < o; )
      a[i] = r[t + i];
    i = -1;
    for (var s = Array(t + 1); ++i < t; )
      s[i] = r[i];
    return s[t] = n(a), Fn(e, this, s);
  };
}
var Wn = 9007199254740991;
function $e(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= Wn;
}
function Et(e) {
  return e != null && $e(e.length) && !$t(e);
}
var Jn = Object.prototype;
function Se(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || Jn;
  return e === n;
}
function Qn(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var Vn = "[object Arguments]";
function We(e) {
  return x(e) && N(e) == Vn;
}
var jt = Object.prototype, kn = jt.hasOwnProperty, er = jt.propertyIsEnumerable, Ce = We(/* @__PURE__ */ function() {
  return arguments;
}()) ? We : function(e) {
  return x(e) && kn.call(e, "callee") && !er.call(e, "callee");
};
function tr() {
  return !1;
}
var It = typeof exports == "object" && exports && !exports.nodeType && exports, Je = It && typeof module == "object" && module && !module.nodeType && module, nr = Je && Je.exports === It, Qe = nr ? E.Buffer : void 0, rr = Qe ? Qe.isBuffer : void 0, ie = rr || tr, or = "[object Arguments]", ir = "[object Array]", ar = "[object Boolean]", sr = "[object Date]", ur = "[object Error]", lr = "[object Function]", fr = "[object Map]", cr = "[object Number]", pr = "[object Object]", gr = "[object RegExp]", dr = "[object Set]", _r = "[object String]", hr = "[object WeakMap]", br = "[object ArrayBuffer]", mr = "[object DataView]", yr = "[object Float32Array]", vr = "[object Float64Array]", Tr = "[object Int8Array]", Pr = "[object Int16Array]", Ar = "[object Int32Array]", Or = "[object Uint8Array]", wr = "[object Uint8ClampedArray]", $r = "[object Uint16Array]", Sr = "[object Uint32Array]", y = {};
y[yr] = y[vr] = y[Tr] = y[Pr] = y[Ar] = y[Or] = y[wr] = y[$r] = y[Sr] = !0;
y[or] = y[ir] = y[br] = y[ar] = y[mr] = y[sr] = y[ur] = y[lr] = y[fr] = y[cr] = y[pr] = y[gr] = y[dr] = y[_r] = y[hr] = !1;
function Cr(e) {
  return x(e) && $e(e.length) && !!y[N(e)];
}
function Ee(e) {
  return function(t) {
    return e(t);
  };
}
var xt = typeof exports == "object" && exports && !exports.nodeType && exports, X = xt && typeof module == "object" && module && !module.nodeType && module, Er = X && X.exports === xt, de = Er && Tt.process, H = function() {
  try {
    var e = X && X.require && X.require("util").types;
    return e || de && de.binding && de.binding("util");
  } catch {
  }
}(), Ve = H && H.isTypedArray, Mt = Ve ? Ee(Ve) : Cr, jr = Object.prototype, Ir = jr.hasOwnProperty;
function Ft(e, t) {
  var n = w(e), r = !n && Ce(e), i = !n && !r && ie(e), o = !n && !r && !i && Mt(e), a = n || r || i || o, s = a ? Qn(e.length, String) : [], l = s.length;
  for (var u in e)
    (t || Ir.call(e, u)) && !(a && // Safari 9 has enumerable `arguments.length` in strict mode.
    (u == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    i && (u == "offset" || u == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    o && (u == "buffer" || u == "byteLength" || u == "byteOffset") || // Skip index properties.
    St(u, l))) && s.push(u);
  return s;
}
function Rt(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var xr = Rt(Object.keys, Object), Mr = Object.prototype, Fr = Mr.hasOwnProperty;
function Rr(e) {
  if (!Se(e))
    return xr(e);
  var t = [];
  for (var n in Object(e))
    Fr.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function V(e) {
  return Et(e) ? Ft(e) : Rr(e);
}
function Lr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Nr = Object.prototype, Dr = Nr.hasOwnProperty;
function Ur(e) {
  if (!q(e))
    return Lr(e);
  var t = Se(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Dr.call(e, r)) || n.push(r);
  return n;
}
function je(e) {
  return Et(e) ? Ft(e, !0) : Ur(e);
}
var Gr = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Kr = /^\w*$/;
function Ie(e, t) {
  if (w(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Ae(e) ? !0 : Kr.test(e) || !Gr.test(e) || t != null && e in Object(t);
}
var Z = U(Object, "create");
function Br() {
  this.__data__ = Z ? Z(null) : {}, this.size = 0;
}
function zr(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var Hr = "__lodash_hash_undefined__", qr = Object.prototype, Yr = qr.hasOwnProperty;
function Xr(e) {
  var t = this.__data__;
  if (Z) {
    var n = t[e];
    return n === Hr ? void 0 : n;
  }
  return Yr.call(t, e) ? t[e] : void 0;
}
var Zr = Object.prototype, Wr = Zr.hasOwnProperty;
function Jr(e) {
  var t = this.__data__;
  return Z ? t[e] !== void 0 : Wr.call(t, e);
}
var Qr = "__lodash_hash_undefined__";
function Vr(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = Z && t === void 0 ? Qr : t, this;
}
function L(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
L.prototype.clear = Br;
L.prototype.delete = zr;
L.prototype.get = Xr;
L.prototype.has = Jr;
L.prototype.set = Vr;
function kr() {
  this.__data__ = [], this.size = 0;
}
function le(e, t) {
  for (var n = e.length; n--; )
    if (we(e[n][0], t))
      return n;
  return -1;
}
var eo = Array.prototype, to = eo.splice;
function no(e) {
  var t = this.__data__, n = le(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : to.call(t, n, 1), --this.size, !0;
}
function ro(e) {
  var t = this.__data__, n = le(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function oo(e) {
  return le(this.__data__, e) > -1;
}
function io(e, t) {
  var n = this.__data__, r = le(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function M(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
M.prototype.clear = kr;
M.prototype.delete = no;
M.prototype.get = ro;
M.prototype.has = oo;
M.prototype.set = io;
var W = U(E, "Map");
function ao() {
  this.size = 0, this.__data__ = {
    hash: new L(),
    map: new (W || M)(),
    string: new L()
  };
}
function so(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function fe(e, t) {
  var n = e.__data__;
  return so(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function uo(e) {
  var t = fe(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function lo(e) {
  return fe(this, e).get(e);
}
function fo(e) {
  return fe(this, e).has(e);
}
function co(e, t) {
  var n = fe(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function F(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
F.prototype.clear = ao;
F.prototype.delete = uo;
F.prototype.get = lo;
F.prototype.has = fo;
F.prototype.set = co;
var po = "Expected a function";
function xe(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(po);
  var n = function() {
    var r = arguments, i = t ? t.apply(this, r) : r[0], o = n.cache;
    if (o.has(i))
      return o.get(i);
    var a = e.apply(this, r);
    return n.cache = o.set(i, a) || o, a;
  };
  return n.cache = new (xe.Cache || F)(), n;
}
xe.Cache = F;
var go = 500;
function _o(e) {
  var t = xe(e, function(r) {
    return n.size === go && n.clear(), r;
  }), n = t.cache;
  return t;
}
var ho = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, bo = /\\(\\)?/g, mo = _o(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(ho, function(n, r, i, o) {
    t.push(i ? o.replace(bo, "$1") : r || n);
  }), t;
});
function yo(e) {
  return e == null ? "" : Ot(e);
}
function ce(e, t) {
  return w(e) ? e : Ie(e, t) ? [e] : mo(yo(e));
}
var vo = 1 / 0;
function k(e) {
  if (typeof e == "string" || Ae(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -vo ? "-0" : t;
}
function Me(e, t) {
  t = ce(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[k(t[n++])];
  return n && n == r ? e : void 0;
}
function To(e, t, n) {
  var r = e == null ? void 0 : Me(e, t);
  return r === void 0 ? n : r;
}
function Fe(e, t) {
  for (var n = -1, r = t.length, i = e.length; ++n < r; )
    e[i + n] = t[n];
  return e;
}
var ke = A ? A.isConcatSpreadable : void 0;
function Po(e) {
  return w(e) || Ce(e) || !!(ke && e && e[ke]);
}
function Ao(e, t, n, r, i) {
  var o = -1, a = e.length;
  for (n || (n = Po), i || (i = []); ++o < a; ) {
    var s = e[o];
    n(s) ? Fe(i, s) : i[i.length] = s;
  }
  return i;
}
function Oo(e) {
  var t = e == null ? 0 : e.length;
  return t ? Ao(e) : [];
}
function wo(e) {
  return Bn(Zn(e, void 0, Oo), e + "");
}
var Re = Rt(Object.getPrototypeOf, Object), $o = "[object Object]", So = Function.prototype, Co = Object.prototype, Lt = So.toString, Eo = Co.hasOwnProperty, jo = Lt.call(Object);
function Io(e) {
  if (!x(e) || N(e) != $o)
    return !1;
  var t = Re(e);
  if (t === null)
    return !0;
  var n = Eo.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Lt.call(n) == jo;
}
function xo(e, t, n) {
  var r = -1, i = e.length;
  t < 0 && (t = -t > i ? 0 : i + t), n = n > i ? i : n, n < 0 && (n += i), i = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var o = Array(i); ++r < i; )
    o[r] = e[r + t];
  return o;
}
function Mo() {
  this.__data__ = new M(), this.size = 0;
}
function Fo(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Ro(e) {
  return this.__data__.get(e);
}
function Lo(e) {
  return this.__data__.has(e);
}
var No = 200;
function Do(e, t) {
  var n = this.__data__;
  if (n instanceof M) {
    var r = n.__data__;
    if (!W || r.length < No - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new F(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function S(e) {
  var t = this.__data__ = new M(e);
  this.size = t.size;
}
S.prototype.clear = Mo;
S.prototype.delete = Fo;
S.prototype.get = Ro;
S.prototype.has = Lo;
S.prototype.set = Do;
function Uo(e, t) {
  return e && Q(t, V(t), e);
}
function Go(e, t) {
  return e && Q(t, je(t), e);
}
var Nt = typeof exports == "object" && exports && !exports.nodeType && exports, et = Nt && typeof module == "object" && module && !module.nodeType && module, Ko = et && et.exports === Nt, tt = Ko ? E.Buffer : void 0, nt = tt ? tt.allocUnsafe : void 0;
function Bo(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = nt ? nt(n) : new e.constructor(n);
  return e.copy(r), r;
}
function zo(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = 0, o = []; ++n < r; ) {
    var a = e[n];
    t(a, n, e) && (o[i++] = a);
  }
  return o;
}
function Dt() {
  return [];
}
var Ho = Object.prototype, qo = Ho.propertyIsEnumerable, rt = Object.getOwnPropertySymbols, Le = rt ? function(e) {
  return e == null ? [] : (e = Object(e), zo(rt(e), function(t) {
    return qo.call(e, t);
  }));
} : Dt;
function Yo(e, t) {
  return Q(e, Le(e), t);
}
var Xo = Object.getOwnPropertySymbols, Ut = Xo ? function(e) {
  for (var t = []; e; )
    Fe(t, Le(e)), e = Re(e);
  return t;
} : Dt;
function Zo(e, t) {
  return Q(e, Ut(e), t);
}
function Gt(e, t, n) {
  var r = t(e);
  return w(e) ? r : Fe(r, n(e));
}
function me(e) {
  return Gt(e, V, Le);
}
function Kt(e) {
  return Gt(e, je, Ut);
}
var ye = U(E, "DataView"), ve = U(E, "Promise"), Te = U(E, "Set"), ot = "[object Map]", Wo = "[object Object]", it = "[object Promise]", at = "[object Set]", st = "[object WeakMap]", ut = "[object DataView]", Jo = D(ye), Qo = D(W), Vo = D(ve), ko = D(Te), ei = D(be), O = N;
(ye && O(new ye(new ArrayBuffer(1))) != ut || W && O(new W()) != ot || ve && O(ve.resolve()) != it || Te && O(new Te()) != at || be && O(new be()) != st) && (O = function(e) {
  var t = N(e), n = t == Wo ? e.constructor : void 0, r = n ? D(n) : "";
  if (r)
    switch (r) {
      case Jo:
        return ut;
      case Qo:
        return ot;
      case Vo:
        return it;
      case ko:
        return at;
      case ei:
        return st;
    }
  return t;
});
var ti = Object.prototype, ni = ti.hasOwnProperty;
function ri(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && ni.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var ae = E.Uint8Array;
function Ne(e) {
  var t = new e.constructor(e.byteLength);
  return new ae(t).set(new ae(e)), t;
}
function oi(e, t) {
  var n = t ? Ne(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var ii = /\w*$/;
function ai(e) {
  var t = new e.constructor(e.source, ii.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var lt = A ? A.prototype : void 0, ft = lt ? lt.valueOf : void 0;
function si(e) {
  return ft ? Object(ft.call(e)) : {};
}
function ui(e, t) {
  var n = t ? Ne(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var li = "[object Boolean]", fi = "[object Date]", ci = "[object Map]", pi = "[object Number]", gi = "[object RegExp]", di = "[object Set]", _i = "[object String]", hi = "[object Symbol]", bi = "[object ArrayBuffer]", mi = "[object DataView]", yi = "[object Float32Array]", vi = "[object Float64Array]", Ti = "[object Int8Array]", Pi = "[object Int16Array]", Ai = "[object Int32Array]", Oi = "[object Uint8Array]", wi = "[object Uint8ClampedArray]", $i = "[object Uint16Array]", Si = "[object Uint32Array]";
function Ci(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case bi:
      return Ne(e);
    case li:
    case fi:
      return new r(+e);
    case mi:
      return oi(e, n);
    case yi:
    case vi:
    case Ti:
    case Pi:
    case Ai:
    case Oi:
    case wi:
    case $i:
    case Si:
      return ui(e, n);
    case ci:
      return new r();
    case pi:
    case _i:
      return new r(e);
    case gi:
      return ai(e);
    case di:
      return new r();
    case hi:
      return si(e);
  }
}
function Ei(e) {
  return typeof e.constructor == "function" && !Se(e) ? Mn(Re(e)) : {};
}
var ji = "[object Map]";
function Ii(e) {
  return x(e) && O(e) == ji;
}
var ct = H && H.isMap, xi = ct ? Ee(ct) : Ii, Mi = "[object Set]";
function Fi(e) {
  return x(e) && O(e) == Mi;
}
var pt = H && H.isSet, Ri = pt ? Ee(pt) : Fi, Li = 1, Ni = 2, Di = 4, Bt = "[object Arguments]", Ui = "[object Array]", Gi = "[object Boolean]", Ki = "[object Date]", Bi = "[object Error]", zt = "[object Function]", zi = "[object GeneratorFunction]", Hi = "[object Map]", qi = "[object Number]", Ht = "[object Object]", Yi = "[object RegExp]", Xi = "[object Set]", Zi = "[object String]", Wi = "[object Symbol]", Ji = "[object WeakMap]", Qi = "[object ArrayBuffer]", Vi = "[object DataView]", ki = "[object Float32Array]", ea = "[object Float64Array]", ta = "[object Int8Array]", na = "[object Int16Array]", ra = "[object Int32Array]", oa = "[object Uint8Array]", ia = "[object Uint8ClampedArray]", aa = "[object Uint16Array]", sa = "[object Uint32Array]", m = {};
m[Bt] = m[Ui] = m[Qi] = m[Vi] = m[Gi] = m[Ki] = m[ki] = m[ea] = m[ta] = m[na] = m[ra] = m[Hi] = m[qi] = m[Ht] = m[Yi] = m[Xi] = m[Zi] = m[Wi] = m[oa] = m[ia] = m[aa] = m[sa] = !0;
m[Bi] = m[zt] = m[Ji] = !1;
function re(e, t, n, r, i, o) {
  var a, s = t & Li, l = t & Ni, u = t & Di;
  if (n && (a = i ? n(e, r, i, o) : n(e)), a !== void 0)
    return a;
  if (!q(e))
    return e;
  var p = w(e);
  if (p) {
    if (a = ri(e), !s)
      return Rn(e, a);
  } else {
    var f = O(e), g = f == zt || f == zi;
    if (ie(e))
      return Bo(e, s);
    if (f == Ht || f == Bt || g && !i) {
      if (a = l || g ? {} : Ei(e), !s)
        return l ? Zo(e, Go(a, e)) : Yo(e, Uo(a, e));
    } else {
      if (!m[f])
        return i ? e : {};
      a = Ci(e, f, s);
    }
  }
  o || (o = new S());
  var _ = o.get(e);
  if (_)
    return _;
  o.set(e, a), Ri(e) ? e.forEach(function(b) {
    a.add(re(b, t, n, b, e, o));
  }) : xi(e) && e.forEach(function(b, v) {
    a.set(v, re(b, t, n, v, e, o));
  });
  var h = u ? l ? Kt : me : l ? je : V, c = p ? void 0 : h(e);
  return zn(c || e, function(b, v) {
    c && (v = b, b = e[v]), Ct(a, v, re(b, t, n, v, e, o));
  }), a;
}
var ua = "__lodash_hash_undefined__";
function la(e) {
  return this.__data__.set(e, ua), this;
}
function fa(e) {
  return this.__data__.has(e);
}
function se(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new F(); ++t < n; )
    this.add(e[t]);
}
se.prototype.add = se.prototype.push = la;
se.prototype.has = fa;
function ca(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function pa(e, t) {
  return e.has(t);
}
var ga = 1, da = 2;
function qt(e, t, n, r, i, o) {
  var a = n & ga, s = e.length, l = t.length;
  if (s != l && !(a && l > s))
    return !1;
  var u = o.get(e), p = o.get(t);
  if (u && p)
    return u == t && p == e;
  var f = -1, g = !0, _ = n & da ? new se() : void 0;
  for (o.set(e, t), o.set(t, e); ++f < s; ) {
    var h = e[f], c = t[f];
    if (r)
      var b = a ? r(c, h, f, t, e, o) : r(h, c, f, e, t, o);
    if (b !== void 0) {
      if (b)
        continue;
      g = !1;
      break;
    }
    if (_) {
      if (!ca(t, function(v, P) {
        if (!pa(_, P) && (h === v || i(h, v, n, r, o)))
          return _.push(P);
      })) {
        g = !1;
        break;
      }
    } else if (!(h === c || i(h, c, n, r, o))) {
      g = !1;
      break;
    }
  }
  return o.delete(e), o.delete(t), g;
}
function _a(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, i) {
    n[++t] = [i, r];
  }), n;
}
function ha(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var ba = 1, ma = 2, ya = "[object Boolean]", va = "[object Date]", Ta = "[object Error]", Pa = "[object Map]", Aa = "[object Number]", Oa = "[object RegExp]", wa = "[object Set]", $a = "[object String]", Sa = "[object Symbol]", Ca = "[object ArrayBuffer]", Ea = "[object DataView]", gt = A ? A.prototype : void 0, _e = gt ? gt.valueOf : void 0;
function ja(e, t, n, r, i, o, a) {
  switch (n) {
    case Ea:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case Ca:
      return !(e.byteLength != t.byteLength || !o(new ae(e), new ae(t)));
    case ya:
    case va:
    case Aa:
      return we(+e, +t);
    case Ta:
      return e.name == t.name && e.message == t.message;
    case Oa:
    case $a:
      return e == t + "";
    case Pa:
      var s = _a;
    case wa:
      var l = r & ba;
      if (s || (s = ha), e.size != t.size && !l)
        return !1;
      var u = a.get(e);
      if (u)
        return u == t;
      r |= ma, a.set(e, t);
      var p = qt(s(e), s(t), r, i, o, a);
      return a.delete(e), p;
    case Sa:
      if (_e)
        return _e.call(e) == _e.call(t);
  }
  return !1;
}
var Ia = 1, xa = Object.prototype, Ma = xa.hasOwnProperty;
function Fa(e, t, n, r, i, o) {
  var a = n & Ia, s = me(e), l = s.length, u = me(t), p = u.length;
  if (l != p && !a)
    return !1;
  for (var f = l; f--; ) {
    var g = s[f];
    if (!(a ? g in t : Ma.call(t, g)))
      return !1;
  }
  var _ = o.get(e), h = o.get(t);
  if (_ && h)
    return _ == t && h == e;
  var c = !0;
  o.set(e, t), o.set(t, e);
  for (var b = a; ++f < l; ) {
    g = s[f];
    var v = e[g], P = t[g];
    if (r)
      var R = a ? r(P, v, g, t, e, o) : r(v, P, g, e, t, o);
    if (!(R === void 0 ? v === P || i(v, P, n, r, o) : R)) {
      c = !1;
      break;
    }
    b || (b = g == "constructor");
  }
  if (c && !b) {
    var j = e.constructor, I = t.constructor;
    j != I && "constructor" in e && "constructor" in t && !(typeof j == "function" && j instanceof j && typeof I == "function" && I instanceof I) && (c = !1);
  }
  return o.delete(e), o.delete(t), c;
}
var Ra = 1, dt = "[object Arguments]", _t = "[object Array]", te = "[object Object]", La = Object.prototype, ht = La.hasOwnProperty;
function Na(e, t, n, r, i, o) {
  var a = w(e), s = w(t), l = a ? _t : O(e), u = s ? _t : O(t);
  l = l == dt ? te : l, u = u == dt ? te : u;
  var p = l == te, f = u == te, g = l == u;
  if (g && ie(e)) {
    if (!ie(t))
      return !1;
    a = !0, p = !1;
  }
  if (g && !p)
    return o || (o = new S()), a || Mt(e) ? qt(e, t, n, r, i, o) : ja(e, t, l, n, r, i, o);
  if (!(n & Ra)) {
    var _ = p && ht.call(e, "__wrapped__"), h = f && ht.call(t, "__wrapped__");
    if (_ || h) {
      var c = _ ? e.value() : e, b = h ? t.value() : t;
      return o || (o = new S()), i(c, b, n, r, o);
    }
  }
  return g ? (o || (o = new S()), Fa(e, t, n, r, i, o)) : !1;
}
function De(e, t, n, r, i) {
  return e === t ? !0 : e == null || t == null || !x(e) && !x(t) ? e !== e && t !== t : Na(e, t, n, r, De, i);
}
var Da = 1, Ua = 2;
function Ga(e, t, n, r) {
  var i = n.length, o = i;
  if (e == null)
    return !o;
  for (e = Object(e); i--; ) {
    var a = n[i];
    if (a[2] ? a[1] !== e[a[0]] : !(a[0] in e))
      return !1;
  }
  for (; ++i < o; ) {
    a = n[i];
    var s = a[0], l = e[s], u = a[1];
    if (a[2]) {
      if (l === void 0 && !(s in e))
        return !1;
    } else {
      var p = new S(), f;
      if (!(f === void 0 ? De(u, l, Da | Ua, r, p) : f))
        return !1;
    }
  }
  return !0;
}
function Yt(e) {
  return e === e && !q(e);
}
function Ka(e) {
  for (var t = V(e), n = t.length; n--; ) {
    var r = t[n], i = e[r];
    t[n] = [r, i, Yt(i)];
  }
  return t;
}
function Xt(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function Ba(e) {
  var t = Ka(e);
  return t.length == 1 && t[0][2] ? Xt(t[0][0], t[0][1]) : function(n) {
    return n === e || Ga(n, e, t);
  };
}
function za(e, t) {
  return e != null && t in Object(e);
}
function Ha(e, t, n) {
  t = ce(t, e);
  for (var r = -1, i = t.length, o = !1; ++r < i; ) {
    var a = k(t[r]);
    if (!(o = e != null && n(e, a)))
      break;
    e = e[a];
  }
  return o || ++r != i ? o : (i = e == null ? 0 : e.length, !!i && $e(i) && St(a, i) && (w(e) || Ce(e)));
}
function qa(e, t) {
  return e != null && Ha(e, t, za);
}
var Ya = 1, Xa = 2;
function Za(e, t) {
  return Ie(e) && Yt(t) ? Xt(k(e), t) : function(n) {
    var r = To(n, e);
    return r === void 0 && r === t ? qa(n, e) : De(t, r, Ya | Xa);
  };
}
function Wa(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Ja(e) {
  return function(t) {
    return Me(t, e);
  };
}
function Qa(e) {
  return Ie(e) ? Wa(k(e)) : Ja(e);
}
function Va(e) {
  return typeof e == "function" ? e : e == null ? wt : typeof e == "object" ? w(e) ? Za(e[0], e[1]) : Ba(e) : Qa(e);
}
function ka(e) {
  return function(t, n, r) {
    for (var i = -1, o = Object(t), a = r(t), s = a.length; s--; ) {
      var l = a[++i];
      if (n(o[l], l, o) === !1)
        break;
    }
    return t;
  };
}
var es = ka();
function ts(e, t) {
  return e && es(e, t, V);
}
function ns(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function rs(e, t) {
  return t.length < 2 ? e : Me(e, xo(t, 0, -1));
}
function os(e, t) {
  var n = {};
  return t = Va(t), ts(e, function(r, i, o) {
    Oe(n, t(r, i, o), r);
  }), n;
}
function is(e, t) {
  return t = ce(t, e), e = rs(e, t), e == null || delete e[k(ns(t))];
}
function as(e) {
  return Io(e) ? void 0 : e;
}
var ss = 1, us = 2, ls = 4, Zt = wo(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = At(t, function(o) {
    return o = ce(o, e), r || (r = o.length > 1), o;
  }), Q(e, Kt(e), n), r && (n = re(n, ss | us | ls, as));
  for (var i = t.length; i--; )
    is(n, t[i]);
  return n;
});
async function fs() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function cs(e) {
  return await fs(), e().then((t) => t.default);
}
function ps(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, i) => i === 0 ? r.toLowerCase() : r.toUpperCase());
}
const Wt = ["interactive", "gradio", "server", "target", "theme_mode", "root", "name", "visible", "elem_id", "elem_classes", "elem_style", "_internal", "props", "value", "attached_events"];
function gs(e, t = {}) {
  return os(Zt(e, Wt), (n, r) => t[r] || ps(r));
}
function bt(e) {
  const {
    gradio: t,
    _internal: n,
    restProps: r,
    originalRestProps: i,
    ...o
  } = e;
  return Object.keys(n).reduce((a, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], p = u.split("_"), f = (..._) => {
        const h = _.map((c) => _ && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        return t.dispatch(u.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: h,
          component: {
            ...o,
            ...Zt(i, Wt)
          }
        });
      };
      if (p.length > 1) {
        let _ = {
          ...o.props[p[0]] || (r == null ? void 0 : r[p[0]]) || {}
        };
        a[p[0]] = _;
        for (let c = 1; c < p.length - 1; c++) {
          const b = {
            ...o.props[p[c]] || (r == null ? void 0 : r[p[c]]) || {}
          };
          _[p[c]] = b, _ = b;
        }
        const h = p[p.length - 1];
        return _[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = f, a;
      }
      const g = p[0];
      a[`on${g.slice(0, 1).toUpperCase()}${g.slice(1)}`] = f;
    }
    return a;
  }, {});
}
function B() {
}
function ds(e) {
  return e();
}
function _s(e) {
  e.forEach(ds);
}
function hs(e) {
  return typeof e == "function";
}
function bs(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Jt(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return B;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function G(e) {
  let t;
  return Jt(e, (n) => t = n)(), t;
}
const K = [];
function ms(e, t) {
  return {
    subscribe: C(e, t).subscribe
  };
}
function C(e, t = B) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function i(s) {
    if (bs(e, s) && (e = s, n)) {
      const l = !K.length;
      for (const u of r)
        u[1](), K.push(u, e);
      if (l) {
        for (let u = 0; u < K.length; u += 2)
          K[u][0](K[u + 1]);
        K.length = 0;
      }
    }
  }
  function o(s) {
    i(s(e));
  }
  function a(s, l = B) {
    const u = [s, l];
    return r.add(u), r.size === 1 && (n = t(i, o) || B), s(e), () => {
      r.delete(u), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: a
  };
}
function ru(e, t, n) {
  const r = !Array.isArray(e), i = r ? [e] : e;
  if (!i.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const o = t.length < 2;
  return ms(n, (a, s) => {
    let l = !1;
    const u = [];
    let p = 0, f = B;
    const g = () => {
      if (p)
        return;
      f();
      const h = t(r ? u[0] : u, a, s);
      o ? a(h) : f = hs(h) ? h : B;
    }, _ = i.map((h, c) => Jt(h, (b) => {
      u[c] = b, p &= ~(1 << c), l && g();
    }, () => {
      p |= 1 << c;
    }));
    return l = !0, g(), function() {
      _s(_), f(), l = !1;
    };
  });
}
const {
  getContext: Ue,
  setContext: pe
} = window.__gradio__svelte__internal, ys = "$$ms-gr-slots-key";
function vs() {
  const e = C({});
  return pe(ys, e);
}
const Ts = "$$ms-gr-render-slot-context-key";
function Ps() {
  const e = pe(Ts, C({}));
  return (t, n) => {
    e.update((r) => typeof n == "function" ? {
      ...r,
      [t]: n(r[t])
    } : {
      ...r,
      [t]: n
    });
  };
}
const As = "$$ms-gr-context-key";
function Os(e, t, n) {
  var p;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = $s(), i = Ss({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  r && r.subscribe((f) => {
    i.slotKey.set(f);
  }), ws();
  const o = Ue(As), a = ((p = G(o)) == null ? void 0 : p.as_item) || e.as_item, s = o ? a ? G(o)[a] : G(o) : {}, l = (f, g) => f ? gs({
    ...f,
    ...g || {}
  }, t) : void 0, u = C({
    ...e,
    ...s,
    restProps: l(e.restProps, s),
    originalRestProps: e.restProps
  });
  return o ? (o.subscribe((f) => {
    const {
      as_item: g
    } = G(u);
    g && (f = f[g]), u.update((_) => ({
      ..._,
      ...f,
      restProps: l(_.restProps, f)
    }));
  }), [u, (f) => {
    const g = f.as_item ? G(o)[f.as_item] : G(o);
    return u.set({
      ...f,
      ...g,
      restProps: l(f.restProps, g),
      originalRestProps: f.restProps
    });
  }]) : [u, (f) => {
    u.set({
      ...f,
      restProps: l(f.restProps),
      originalRestProps: f.restProps
    });
  }];
}
const Qt = "$$ms-gr-slot-key";
function ws() {
  pe(Qt, C(void 0));
}
function $s() {
  return Ue(Qt);
}
const Vt = "$$ms-gr-component-slot-context-key";
function Ss({
  slot: e,
  index: t,
  subIndex: n
}) {
  return pe(Vt, {
    slotKey: C(e),
    slotIndex: C(t),
    subSlotIndex: C(n)
  });
}
function ou() {
  return Ue(Vt);
}
function Cs(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var kt = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function n() {
      for (var o = "", a = 0; a < arguments.length; a++) {
        var s = arguments[a];
        s && (o = i(o, r(s)));
      }
      return o;
    }
    function r(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return n.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var a = "";
      for (var s in o)
        t.call(o, s) && o[s] && (a = i(a, s));
      return a;
    }
    function i(o, a) {
      return a ? o ? o + " " + a : o + a : o;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(kt);
var Es = kt.exports;
const mt = /* @__PURE__ */ Cs(Es), {
  getContext: js,
  setContext: Is
} = window.__gradio__svelte__internal;
function xs(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(i = ["default"]) {
    const o = i.reduce((a, s) => (a[s] = C([]), a), {});
    return Is(t, {
      itemsMap: o,
      allowedSlots: i
    }), o;
  }
  function r() {
    const {
      itemsMap: i,
      allowedSlots: o
    } = js(t);
    return function(a, s, l) {
      i && (a ? i[a].update((u) => {
        const p = [...u];
        return o.includes(a) ? p[s] = l : p[s] = void 0, p;
      }) : o.includes("default") && i.default.update((u) => {
        const p = [...u];
        return p[s] = l, p;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: Ms,
  getSetItemFn: iu
} = xs("color-picker"), {
  SvelteComponent: Fs,
  assign: Pe,
  check_outros: Rs,
  claim_component: Ls,
  component_subscribe: ne,
  compute_rest_props: yt,
  create_component: Ns,
  create_slot: Ds,
  destroy_component: Us,
  detach: en,
  empty: ue,
  exclude_internal_props: Gs,
  flush: $,
  get_all_dirty_from_scope: Ks,
  get_slot_changes: Bs,
  get_spread_object: he,
  get_spread_update: zs,
  group_outros: Hs,
  handle_promise: qs,
  init: Ys,
  insert_hydration: tn,
  mount_component: Xs,
  noop: T,
  safe_not_equal: Zs,
  transition_in: z,
  transition_out: J,
  update_await_block_branch: Ws,
  update_slot_base: Js
} = window.__gradio__svelte__internal;
function vt(e) {
  let t, n, r = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: eu,
    then: Vs,
    catch: Qs,
    value: 25,
    blocks: [, , ,]
  };
  return qs(
    /*AwaitedColorPicker*/
    e[5],
    r
  ), {
    c() {
      t = ue(), r.block.c();
    },
    l(i) {
      t = ue(), r.block.l(i);
    },
    m(i, o) {
      tn(i, t, o), r.block.m(i, r.anchor = o), r.mount = () => t.parentNode, r.anchor = t, n = !0;
    },
    p(i, o) {
      e = i, Ws(r, e, o);
    },
    i(i) {
      n || (z(r.block), n = !0);
    },
    o(i) {
      for (let o = 0; o < 3; o += 1) {
        const a = r.blocks[o];
        J(a);
      }
      n = !1;
    },
    d(i) {
      i && en(t), r.block.d(i), r.token = null, r = null;
    }
  };
}
function Qs(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function Vs(e) {
  let t, n;
  const r = [
    {
      style: (
        /*$mergedProps*/
        e[2].elem_style
      )
    },
    {
      className: mt(
        /*$mergedProps*/
        e[2].elem_classes,
        "ms-gr-antd-color-picker"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[2].elem_id
      )
    },
    /*$mergedProps*/
    e[2].restProps,
    /*$mergedProps*/
    e[2].props,
    bt(
      /*$mergedProps*/
      e[2]
    ),
    {
      value: (
        /*$mergedProps*/
        e[2].props.value ?? /*$mergedProps*/
        e[2].value
      )
    },
    {
      slots: (
        /*$slots*/
        e[3]
      )
    },
    {
      presetItems: (
        /*$presets*/
        e[4]
      )
    },
    {
      value_format: (
        /*value_format*/
        e[1]
      )
    },
    {
      onValueChange: (
        /*func*/
        e[21]
      )
    },
    {
      setSlotParams: (
        /*setSlotParams*/
        e[9]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [ks]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let o = 0; o < r.length; o += 1)
    i = Pe(i, r[o]);
  return t = new /*ColorPicker*/
  e[25]({
    props: i
  }), {
    c() {
      Ns(t.$$.fragment);
    },
    l(o) {
      Ls(t.$$.fragment, o);
    },
    m(o, a) {
      Xs(t, o, a), n = !0;
    },
    p(o, a) {
      const s = a & /*$mergedProps, $slots, $presets, value_format, value, setSlotParams*/
      543 ? zs(r, [a & /*$mergedProps*/
      4 && {
        style: (
          /*$mergedProps*/
          o[2].elem_style
        )
      }, a & /*$mergedProps*/
      4 && {
        className: mt(
          /*$mergedProps*/
          o[2].elem_classes,
          "ms-gr-antd-color-picker"
        )
      }, a & /*$mergedProps*/
      4 && {
        id: (
          /*$mergedProps*/
          o[2].elem_id
        )
      }, a & /*$mergedProps*/
      4 && he(
        /*$mergedProps*/
        o[2].restProps
      ), a & /*$mergedProps*/
      4 && he(
        /*$mergedProps*/
        o[2].props
      ), a & /*$mergedProps*/
      4 && he(bt(
        /*$mergedProps*/
        o[2]
      )), a & /*$mergedProps*/
      4 && {
        value: (
          /*$mergedProps*/
          o[2].props.value ?? /*$mergedProps*/
          o[2].value
        )
      }, a & /*$slots*/
      8 && {
        slots: (
          /*$slots*/
          o[3]
        )
      }, a & /*$presets*/
      16 && {
        presetItems: (
          /*$presets*/
          o[4]
        )
      }, a & /*value_format*/
      2 && {
        value_format: (
          /*value_format*/
          o[1]
        )
      }, a & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          o[21]
        )
      }, a & /*setSlotParams*/
      512 && {
        setSlotParams: (
          /*setSlotParams*/
          o[9]
        )
      }]) : {};
      a & /*$$scope*/
      4194304 && (s.$$scope = {
        dirty: a,
        ctx: o
      }), t.$set(s);
    },
    i(o) {
      n || (z(t.$$.fragment, o), n = !0);
    },
    o(o) {
      J(t.$$.fragment, o), n = !1;
    },
    d(o) {
      Us(t, o);
    }
  };
}
function ks(e) {
  let t;
  const n = (
    /*#slots*/
    e[20].default
  ), r = Ds(
    n,
    e,
    /*$$scope*/
    e[22],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(i) {
      r && r.l(i);
    },
    m(i, o) {
      r && r.m(i, o), t = !0;
    },
    p(i, o) {
      r && r.p && (!t || o & /*$$scope*/
      4194304) && Js(
        r,
        n,
        i,
        /*$$scope*/
        i[22],
        t ? Bs(
          n,
          /*$$scope*/
          i[22],
          o,
          null
        ) : Ks(
          /*$$scope*/
          i[22]
        ),
        null
      );
    },
    i(i) {
      t || (z(r, i), t = !0);
    },
    o(i) {
      J(r, i), t = !1;
    },
    d(i) {
      r && r.d(i);
    }
  };
}
function eu(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function tu(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[2].visible && vt(e)
  );
  return {
    c() {
      r && r.c(), t = ue();
    },
    l(i) {
      r && r.l(i), t = ue();
    },
    m(i, o) {
      r && r.m(i, o), tn(i, t, o), n = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[2].visible ? r ? (r.p(i, o), o & /*$mergedProps*/
      4 && z(r, 1)) : (r = vt(i), r.c(), z(r, 1), r.m(t.parentNode, t)) : r && (Hs(), J(r, 1, 1, () => {
        r = null;
      }), Rs());
    },
    i(i) {
      n || (z(r), n = !0);
    },
    o(i) {
      J(r), n = !1;
    },
    d(i) {
      i && en(t), r && r.d(i);
    }
  };
}
function nu(e, t, n) {
  const r = ["gradio", "props", "_internal", "value", "value_format", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let i = yt(t, r), o, a, s, l, {
    $$slots: u = {},
    $$scope: p
  } = t;
  const f = cs(() => import("./color-picker-DsxDDxFg.js"));
  let {
    gradio: g
  } = t, {
    props: _ = {}
  } = t;
  const h = C(_);
  ne(e, h, (d) => n(19, o = d));
  let {
    _internal: c = {}
  } = t, {
    value: b
  } = t, {
    value_format: v = "hex"
  } = t, {
    as_item: P
  } = t, {
    visible: R = !0
  } = t, {
    elem_id: j = ""
  } = t, {
    elem_classes: I = []
  } = t, {
    elem_style: ee = {}
  } = t;
  const [Ge, nn] = Os({
    gradio: g,
    props: o,
    _internal: c,
    visible: R,
    elem_id: j,
    elem_classes: I,
    elem_style: ee,
    as_item: P,
    value: b,
    restProps: i
  });
  ne(e, Ge, (d) => n(2, a = d));
  const Ke = vs();
  ne(e, Ke, (d) => n(3, s = d));
  const rn = Ps(), {
    presets: Be
  } = Ms(["presets"]);
  ne(e, Be, (d) => n(4, l = d));
  const on = (d) => {
    n(0, b = d);
  };
  return e.$$set = (d) => {
    t = Pe(Pe({}, t), Gs(d)), n(24, i = yt(t, r)), "gradio" in d && n(11, g = d.gradio), "props" in d && n(12, _ = d.props), "_internal" in d && n(13, c = d._internal), "value" in d && n(0, b = d.value), "value_format" in d && n(1, v = d.value_format), "as_item" in d && n(14, P = d.as_item), "visible" in d && n(15, R = d.visible), "elem_id" in d && n(16, j = d.elem_id), "elem_classes" in d && n(17, I = d.elem_classes), "elem_style" in d && n(18, ee = d.elem_style), "$$scope" in d && n(22, p = d.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    4096 && h.update((d) => ({
      ...d,
      ..._
    })), nn({
      gradio: g,
      props: o,
      _internal: c,
      visible: R,
      elem_id: j,
      elem_classes: I,
      elem_style: ee,
      as_item: P,
      value: b,
      restProps: i
    });
  }, [b, v, a, s, l, f, h, Ge, Ke, rn, Be, g, _, c, P, R, j, I, ee, o, u, on, p];
}
class au extends Fs {
  constructor(t) {
    super(), Ys(this, t, nu, tu, Zs, {
      gradio: 11,
      props: 12,
      _internal: 13,
      value: 0,
      value_format: 1,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
    });
  }
  get gradio() {
    return this.$$.ctx[11];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), $();
  }
  get props() {
    return this.$$.ctx[12];
  }
  set props(t) {
    this.$$set({
      props: t
    }), $();
  }
  get _internal() {
    return this.$$.ctx[13];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), $();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), $();
  }
  get value_format() {
    return this.$$.ctx[1];
  }
  set value_format(t) {
    this.$$set({
      value_format: t
    }), $();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), $();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), $();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), $();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), $();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), $();
  }
}
export {
  au as I,
  G as a,
  ru as d,
  ou as g,
  C as w
};
