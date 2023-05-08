"use strict";
// js辅助函数
// 直接叫node跑
// 所有计算sign逻辑都复制于Partme前端的JS代码

function magic1GenCons() {
    function i(e, t) {
        var n = (65535 & e) + (65535 & t);
        return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
    }
    function o(e, t, n, r, a, o) {
        return i((s = i(i(t, e), i(r, o))) << (l = a) | s >>> 32 - l, n);
        var s, l
    }
    function s(e, t, n, r, a, i, s) {
        return o(t & n | ~t & r, e, t, a, i, s)
    }
    function l(e, t, n, r, a, i, s) {
        return o(t & r | n & ~r, e, t, a, i, s)
    }
    function c(e, t, n, r, a, i, s) {
        return o(t ^ n ^ r, e, t, a, i, s)
    }
    function u(e, t, n, r, a, i, s) {
        return o(n ^ (t | ~r), e, t, a, i, s)
    }
    function p(e, t) {
        var n, r, a, o, p;
        e[t >> 5] |= 128 << t % 32,
        e[14 + (t + 64 >>> 9 << 4)] = t;
        var d = 1732584193
          , f = -271733879
          , h = -1732584194
          , m = 271733878;
        for (n = 0; n < e.length; n += 16)
            r = d,
            a = f,
            o = h,
            p = m,
            d = s(d, f, h, m, e[n], 7, -680876936),
            m = s(m, d, f, h, e[n + 1], 12, -389564586),
            h = s(h, m, d, f, e[n + 2], 17, 606105819),
            f = s(f, h, m, d, e[n + 3], 22, -1044525330),
            d = s(d, f, h, m, e[n + 4], 7, -176418897),
            m = s(m, d, f, h, e[n + 5], 12, 1200080426),
            h = s(h, m, d, f, e[n + 6], 17, -1473231341),
            f = s(f, h, m, d, e[n + 7], 22, -45705983),
            d = s(d, f, h, m, e[n + 8], 7, 1770035416),
            m = s(m, d, f, h, e[n + 9], 12, -1958414417),
            h = s(h, m, d, f, e[n + 10], 17, -42063),
            f = s(f, h, m, d, e[n + 11], 22, -1990404162),
            d = s(d, f, h, m, e[n + 12], 7, 1804603682),
            m = s(m, d, f, h, e[n + 13], 12, -40341101),
            h = s(h, m, d, f, e[n + 14], 17, -1502002290),
            d = l(d, f = s(f, h, m, d, e[n + 15], 22, 1236535329), h, m, e[n + 1], 5, -165796510),
            m = l(m, d, f, h, e[n + 6], 9, -1069501632),
            h = l(h, m, d, f, e[n + 11], 14, 643717713),
            f = l(f, h, m, d, e[n], 20, -373897302),
            d = l(d, f, h, m, e[n + 5], 5, -701558691),
            m = l(m, d, f, h, e[n + 10], 9, 38016083),
            h = l(h, m, d, f, e[n + 15], 14, -660478335),
            f = l(f, h, m, d, e[n + 4], 20, -405537848),
            d = l(d, f, h, m, e[n + 9], 5, 568446438),
            m = l(m, d, f, h, e[n + 14], 9, -1019803690),
            h = l(h, m, d, f, e[n + 3], 14, -187363961),
            f = l(f, h, m, d, e[n + 8], 20, 1163531501),
            d = l(d, f, h, m, e[n + 13], 5, -1444681467),
            m = l(m, d, f, h, e[n + 2], 9, -51403784),
            h = l(h, m, d, f, e[n + 7], 14, 1735328473),
            d = c(d, f = l(f, h, m, d, e[n + 12], 20, -1926607734), h, m, e[n + 5], 4, -378558),
            m = c(m, d, f, h, e[n + 8], 11, -2022574463),
            h = c(h, m, d, f, e[n + 11], 16, 1839030562),
            f = c(f, h, m, d, e[n + 14], 23, -35309556),
            d = c(d, f, h, m, e[n + 1], 4, -1530992060),
            m = c(m, d, f, h, e[n + 4], 11, 1272893353),
            h = c(h, m, d, f, e[n + 7], 16, -155497632),
            f = c(f, h, m, d, e[n + 10], 23, -1094730640),
            d = c(d, f, h, m, e[n + 13], 4, 681279174),
            m = c(m, d, f, h, e[n], 11, -358537222),
            h = c(h, m, d, f, e[n + 3], 16, -722521979),
            f = c(f, h, m, d, e[n + 6], 23, 76029189),
            d = c(d, f, h, m, e[n + 9], 4, -640364487),
            m = c(m, d, f, h, e[n + 12], 11, -421815835),
            h = c(h, m, d, f, e[n + 15], 16, 530742520),
            d = u(d, f = c(f, h, m, d, e[n + 2], 23, -995338651), h, m, e[n], 6, -198630844),
            m = u(m, d, f, h, e[n + 7], 10, 1126891415),
            h = u(h, m, d, f, e[n + 14], 15, -1416354905),
            f = u(f, h, m, d, e[n + 5], 21, -57434055),
            d = u(d, f, h, m, e[n + 12], 6, 1700485571),
            m = u(m, d, f, h, e[n + 3], 10, -1894986606),
            h = u(h, m, d, f, e[n + 10], 15, -1051523),
            f = u(f, h, m, d, e[n + 1], 21, -2054922799),
            d = u(d, f, h, m, e[n + 8], 6, 1873313359),
            m = u(m, d, f, h, e[n + 15], 10, -30611744),
            h = u(h, m, d, f, e[n + 6], 15, -1560198380),
            f = u(f, h, m, d, e[n + 13], 21, 1309151649),
            d = u(d, f, h, m, e[n + 4], 6, -145523070),
            m = u(m, d, f, h, e[n + 11], 10, -1120210379),
            h = u(h, m, d, f, e[n + 2], 15, 718787259),
            f = u(f, h, m, d, e[n + 9], 21, -343485551),
            d = i(d, r),
            f = i(f, a),
            h = i(h, o),
            m = i(m, p);
        return [d, f, h, m]
    }
    function d(e) {
        var t, n = "", r = 32 * e.length;
        for (t = 0; t < r; t += 8)
            n += String.fromCharCode(e[t >> 5] >>> t % 32 & 255);
        return n
    }
    function f(e) {
        var t, n = [];
        for (n[(e.length >> 2) - 1] = void 0,
        t = 0; t < n.length; t += 1)
            n[t] = 0;
        var r = 8 * e.length;
        for (t = 0; t < r; t += 8)
            n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
        return n
    }
    function h(e) {
        var t, n, r = "0123456789abcdef", a = "";
        for (n = 0; n < e.length; n += 1)
            t = e.charCodeAt(n),
            a += r.charAt(t >>> 4 & 15) + r.charAt(15 & t);
        return a
    }
    function m(e) {
        return unescape(encodeURIComponent(e))
    }
    function g(e) {
        return function(e) {
            return d(p(f(e), 8 * e.length))
        }(m(e))
    }
    function v(e, t) {
        return function(e, t) {
            var n, r, a = f(e), i = [], o = [];
            for (i[15] = o[15] = void 0,
            a.length > 16 && (a = p(a, 8 * e.length)),
            n = 0; n < 16; n += 1)
                i[n] = 909522486 ^ a[n],
                o[n] = 1549556828 ^ a[n];
            return r = p(i.concat(f(t)), 512 + 8 * t.length),
            d(p(o.concat(r), 640))
        }(m(e), m(t))
    }
    function b(e, t, n) {
        return t ? n ? v(t, e) : h(v(t, e)) : n ? g(e) : h(g(e))
    }

    return b;
}

function magic2GenCons() {

    function r(e, r) {
        return e + Math.floor(Math.random() * (r - e + 1))
    }

    function i(e) {
        return e ? Infinity === (e = e) || e === -1 / 0 ? 17976931348623157e292 * (e < 0 ? -1 : 1) : e == e ? e : 0 : 0 === e ? e : 0
    }

    return function (e, t, n) {
        if (n && "boolean" != typeof n && a(e, t, n) && (t = n = void 0),
                    void 0 === n && ("boolean" == typeof t ? (n = t,
                    t = void 0) : "boolean" == typeof e && (n = e,
                    e = void 0)),
                    void 0 === e && void 0 === t ? (e = 0,
                    t = 1) : (e = i(e),
                    void 0 === t ? (t = e,
                    e = 0) : t = i(t)),
                    e > t) {
                        var c = e;
                        e = t,
                        t = c
                    }
                    if (n || e % 1 || t % 1) {
                        var u = l();
                        return s(e + u * (t - e + o("1e-" + ((u + "").length - 1))), t)
                    }
                    return r(e, t)
    }
}

const URL_PATH = process.argv[2]

const pathName = new URL(URL_PATH).pathname.toLowerCase()
const time = ((new Date).getTime() / 1e3).toFixed(0)
const magic2 = magic2GenCons()(1e8, 999999999, !1)
const final = magic1GenCons()("".concat(pathName, "-").concat(time, "-").concat(magic2, "-").concat(0, "-").concat("DyGDE2SSamhZtGyi"));

console.log(URL_PATH.concat("?sign=").concat(time, "-").concat(magic2, "-").concat(0, "-").concat(final))
